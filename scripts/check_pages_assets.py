#!/usr/bin/env python3
"""Fail on missing local Pages assets or non-200 deployed asset URLs."""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


ROOT = Path(__file__).parents[1]
DOCS = ROOT / "docs"


class AssetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.assets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag in {"img", "script"} and values.get("src"):
            self.assets.append(values["src"])
        if tag in {"source", "link"} and values.get("srcset"):
            self.assets.append(values["srcset"].split()[0])
        if tag == "link" and values.get("rel") == "stylesheet" and values.get("href"):
            self.assets.append(values["href"])


def local_assets(html: Path) -> list[Path]:
    parser = AssetParser()
    text = html.read_text(encoding="utf-8")
    parser.feed(text)
    if re.search(r"\b(Not rerun|ModelSim not run)\b", text, re.IGNORECASE):
        raise AssertionError(f"stale validation wording remains in {html}")
    resolved: list[Path] = []
    for asset in parser.assets:
        parsed = urlparse(asset)
        if parsed.scheme or asset.startswith("/"):
            continue
        resolved.append((html.parent / parsed.path).resolve())
    return resolved


def check_local() -> list[str]:
    errors: list[str] = []
    pages = [DOCS / "index.html", DOCS / "en/index.html", DOCS / "404.html"]
    seen: set[Path] = set()
    for page in pages:
        if not page.is_file():
            errors.append(f"MISSING PAGE {page}")
            continue
        for asset in local_assets(page):
            seen.add(asset)
            if not asset.is_file():
                errors.append(f"MISSING ASSET {asset} referenced by {page}")
            elif asset.stat().st_size == 0:
                errors.append(f"EMPTY ASSET {asset}")
    print(f"LOCAL pages={len(pages)} unique_assets={len(seen)}")
    return errors


def check_deployed(base_url: str) -> list[str]:
    errors: list[str] = []
    urls = [urljoin(base_url, ""), urljoin(base_url, "en/")]
    discovered: set[str] = set()
    for page_url in urls:
        try:
            with urllib.request.urlopen(page_url, timeout=20) as response:
                html = response.read().decode("utf-8")
                print(f"HTTP {response.status} {page_url}")
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"HTTP ERROR {page_url}: {exc}")
            continue
        parser = AssetParser()
        parser.feed(html)
        discovered.update(urljoin(page_url, asset) for asset in parser.assets)
    for asset_url in sorted(discovered):
        request = urllib.request.Request(asset_url, method="HEAD")
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                print(f"HTTP {response.status} {asset_url}")
                if response.status != 200:
                    errors.append(f"NON-200 {response.status} {asset_url}")
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"HTTP ERROR {asset_url}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="deployed Pages base URL")
    args = parser.parse_args()
    errors = check_local()
    if args.url:
        errors.extend(check_deployed(args.url.rstrip("/") + "/"))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PAGES_ASSET_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
