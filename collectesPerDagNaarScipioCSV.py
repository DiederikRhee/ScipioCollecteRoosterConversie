import pandas as pd
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ScipioCollecteItem:
    Naam: str
    Van: str
    Tot: str
    Omschrijving : str

def collectes_per_dag_naar_scipio_csv(inputBestand: Path, outputBestand: Path):
    input_df = pd.read_excel(inputBestand)
    otput_df = input_df.copy()
    otput_df.to_csv(outputBestand, index=False)

if __name__ == "__main__":
    from helpers import BepaalOutputBestandCollectPerDag, BepaalOutputBestandScipioBestand, kerken

    for kerk in kerken:
        collectes_per_dag_naar_scipio_csv(BepaalOutputBestandCollectPerDag(kerk), BepaalOutputBestandScipioBestand(kerk))

