"""Project 1 and 2 regression definitions."""

from pathlib import Path

from verification_lib import compile_design, run_logged


def project1(repo: Path, iverilog: str, vvp: str) -> dict[str, object]:
    project = repo / "01_shift_register_baseline"
    output = compile_design(
        iverilog,
        project,
        "tb_delay_logic_regression",
        ["rtl/delay_logic.sv", "tb/tb_delay_logic_regression.sv"],
        "project1_regression.vvp",
        "project1_compile.log",
    )
    run_logged(
        [vvp, str(output.relative_to(project))],
        project,
        project / "results/project1_simulation.log",
        ("[P1][PASS]",),
    )
    return {
        "status": "PASS",
        "scope": "self-checking functional regression",
        "log": "01_shift_register_baseline/results/project1_simulation.log",
        "vcd": "01_shift_register_baseline/results/project1_waveform.vcd",
    }


def project2(repo: Path, iverilog: str, vvp: str) -> dict[str, object]:
    project = repo / "02_circular_queue_ppa"
    output = compile_design(
        iverilog,
        project,
        "tb_architecture_equivalence_regression",
        [
            "rtl/shift_register_delay_logic_ppa.sv",
            "rtl/circular_queue_delay_logic.sv",
            "tb/tb_architecture_equivalence_regression.sv",
        ],
        "project2_regression.vvp",
        "project2_compile.log",
    )
    run_logged(
        [vvp, str(output.relative_to(project))],
        project,
        project / "results/project2_simulation.log",
        ("[P2][PASS]",),
    )
    return {
        "status": "PASS",
        "scope": "architecture equivalence against independent history model",
        "log": "02_circular_queue_ppa/results/project2_simulation.log",
        "vcd": "02_circular_queue_ppa/results/project2_waveform.vcd",
    }
