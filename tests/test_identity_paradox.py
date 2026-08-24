from pathlib import Path
import runpy


MODULE = runpy.run_path(
    str(Path(__file__).parents[1] / "examples" / "identity_paradox.py")
)


def test_iconic_identity_paradox():
    result = MODULE["run_experiment"](n=10_000, k=50)
    assert abs(result["spearman"] - 0.9999985) < 1e-12
    assert result["overlap"] == 0
    assert result["ridi"] == 1.0


def test_global_agreement_converges_without_identity_recovery():
    small = MODULE["run_experiment"](n=1_000, k=25)
    large = MODULE["run_experiment"](n=100_000, k=25)
    assert large["spearman"] > small["spearman"]
    assert small["ridi"] == large["ridi"] == 1.0

