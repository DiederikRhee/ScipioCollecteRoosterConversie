import pandas as pd
from dataclasses import dataclass

@dataclass
class ScipioCollecteItem:
    Naam: str
    Van: str
    Tot: str
    Omschrijving : str

def collectes_per_dag_naar_scipio_csv(input: pd.DataFrame, output_path: str):
    input.to_csv(output_path, index=False)

if __name__ == "__main__":
    from helpers import BepaalOutputBestandCollectPerDag, BepaalOutputBestandScipioBestand, kerken

    for kerk in kerken:
        df = pd.read_excel(BepaalOutputBestandCollectPerDag(kerk))

        collectes_per_dag_naar_scipio_csv(df, BepaalOutputBestandScipioBestand(kerk))

