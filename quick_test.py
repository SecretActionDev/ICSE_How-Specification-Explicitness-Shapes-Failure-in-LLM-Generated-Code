from pathlib import Path
import numpy as np
import pandas as pd

root = Path(".")

rq1 = pd.read_csv(
    root / "Analysis/RQs/RQ1/rq1_outputs/rq1_paper_main_table.csv"
)
assert np.allclose(
    rq1["Failure count, mean (SD)"].str.extract(r"([0-9.]+)")[0].astype(float),
    [21.54, 19.67, 11.38],
    atol=0.01,
)

rq2 = pd.read_csv(
    root / "Analysis/RQs/RQ2/rq2_outputs/tables/"
           "rq2_requirement_predictive_power_success_odds.csv"
)
expected_or = {
    "Functional Requirements": 2.80,
    "Invariants": 2.62,
    "Negative Requirements": 2.62,
    "Tie-Breaking Rules": 1.99,
}
for label, expected in expected_or.items():
    observed = rq2.loc[rq2["label"] == label, "odds_ratio"].iloc[0]
    assert np.isclose(observed, expected, atol=0.02)

rq3 = pd.read_csv(
    root / "Analysis/RQs/RQ3/rq3_outputs/rq3_compact_table.csv"
)
assert rq3["Any regression"].tolist() == [
    "2/24 (8.3%)", "2/24 (8.3%)", "4/24 (16.7%)"
]

rq4 = pd.read_csv(
    root / "Analysis/RQs/RQ4/rq4_outputs/tables/"
           "rq4_descriptive_calibration_by_phase_spec.csv"
)
observed = rq4["overconfidence_pp_mean"].round(2).tolist()
expected = [22.78, 5.65, -22.20, 22.73, -17.43, -18.22]
assert np.allclose(observed, expected, atol=0.02)

p1 = pd.read_csv(root / "Data/prompt_data/Phase1_prompt_type.csv")
p2 = pd.read_csv(root / "Data/prompt_data/Phase2_prompt_type.csv")
assert len(p1) == 341 and len(p2) == 377

print("Artifact verification passed.")