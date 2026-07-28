# Portfolio Change Log

## 2026-07-28

- Reorganized three supplied project packages into one public, recruiter-oriented repository.
- Preserved authored RTL, testbenches, vectors, Quartus projects, and ModelSim flows while removing submission-only wording and private source packages.
- Updated Project 1 ModelSim and Quartus paths to match the public directory layout.
- Set Project 1's public Quartus target to `A5ED065BB32AE6SR0`, matching Projects 2 and 3; RTL behavior is unchanged.
- Moved the Project 2 PPA launcher under `scripts/` and corrected its working directory.
- Added an explicit ModelSim availability check to the Project 3 batch launcher.
- Added documentation, validation automation, CI, architectural SVGs, and a GitHub Pages portfolio.

No architectural output policy was normalized across projects: Projects 1 and 2 force invalid data to zero, while Project 3 holds the last valid data value when `oDataEn=0`.

