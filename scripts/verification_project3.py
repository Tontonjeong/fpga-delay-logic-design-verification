"""Project 3 file-driven regression definition."""

from pathlib import Path

from verification_lib import compile_design, run_logged


def project3(repo: Path, iverilog: str, vvp: str) -> dict[str, object]:
    project = repo / "03_memory_based_dv"
    output = compile_design(
        iverilog,
        project,
        "tb_memory_delay_logic",
        [
            "rtl/memory_delay_logic.sv",
            "tb/input_driver.sv",
            "tb/output_checker.sv",
            "tb/tb_memory_delay_logic.sv",
        ],
        "project3_regression.vvp",
        "project3_compile.log",
    )
    scenarios: list[dict[str, object]] = []
    for scenario in (1, 2, 3):
        console_log = project / f"results/scenario{scenario}_console.log"
        run_logged(
            [
                vvp,
                str(output.relative_to(project)),
                f"+SCENARIO={scenario}",
                "+DUMP_VCD",
            ],
            project,
            console_log,
            ("[CHECKER][PASS]", "[TEST PASS]"),
        )
        generated_vcd = project / "results/memory_delay_logic.vcd"
        scenario_vcd = project / f"results/scenario{scenario}_waveform.vcd"
        generated_vcd.replace(scenario_vcd)
        scenarios.append(
            {
                "scenario": scenario,
                "status": "PASS",
                "console_log": str(console_log.relative_to(repo)).replace("\\", "/"),
                "checker_log": (
                    f"03_memory_based_dv/results/scenario{scenario}_simulation.log"
                ),
                "vcd": str(scenario_vcd.relative_to(repo)).replace("\\", "/"),
            }
        )
    return {
        "status": "PASS",
        "scope": "file-driven DUT/checker scenarios 1-3",
        "scenarios": scenarios,
    }
