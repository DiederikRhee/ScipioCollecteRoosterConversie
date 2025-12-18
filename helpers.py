

from pathlib import Path

def BepaalOutputBestandCollectPerDag(kerk: str) -> Path:
    return Path(f"output/2025_{kerk}_collectes_per_dag.xlsx")

def BepaalOutputBestandScipioBestand(kerk: str) -> Path:
    return Path(f"output/2025_{kerk}_scipio.csv")

kerken = ["BK", "OH", "WK"]
