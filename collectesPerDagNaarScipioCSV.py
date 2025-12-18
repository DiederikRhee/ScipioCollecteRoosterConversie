import pandas as pd
from dataclasses import dataclass
from pathlib import Path
import datetime
from typing import List

@dataclass
class CollecteLoopTijd:
    Dag: datetime.date
    Van: datetime.datetime
    Tot: datetime.datetime

def collectes_per_dag_naar_scipio_csv(inputBestand: Path, outputBestand: Path):
    input_df = pd.read_excel(inputBestand)

    looptijden : List[CollecteLoopTijd] = []
    for _, data_row in input_df.iterrows():
        dag = data_row["Datum"].to_pydatetime().date()
        looptijden.append(CollecteLoopTijd(
            dag,
            datetime.datetime.combine(dag, datetime.time(0,0)) - datetime.timedelta(days=2), #bij voorkeur 2 dagen van tevoren
            datetime.datetime.combine(dag, datetime.time(23,59)) + datetime.timedelta(days=4) #bij voorkeur tot 4 dagen erna
            ))

    for i in range(1, len(looptijden)):
        vorige = looptijden[i - 1]
        huidig = looptijden[i]

        if (huidig.Van <= vorige.Tot):
            huidig.Van = datetime.datetime.combine(huidig.Dag, datetime.time(0,0))
            vorige.Tot = huidig.Van - datetime.timedelta(minutes=1)

    collectes : List[dict] = []
    for i in range(len(looptijden)):
        collecte = input_df.iloc[i]
        looptijd = looptijden[i]

        collecteItems = [index for index in collecte.index if "Collecte" in index and not pd.isna(collecte[index])]
        for collecteItem in collecteItems:
            doel = collecte[collecteItem]

            tot = looptijd.Tot - datetime.timedelta(minutes= (len(collecteItems) - collecteItems.index(collecteItem) - 1))


            collectes.append({
                "Naam doel": doel,
                "Begindatum + tijd": looptijd.Van.strftime("%d-%m-%Y %H:%M"),
                "Einddatum + tijd": tot.strftime("%d-%m-%Y %H:%M"),
                "Omschrijving": f"Collecte van {looptijd.Dag.strftime('%d-%m-%Y')}",
                "URL video": "",
                "URL website": "",
                "Opbrengst weergeven": "HIDE",
                "Is er een doelbedrag?": None
            })

    output_df = pd.DataFrame(collectes)
    output_df.to_csv(outputBestand, index=False, sep=';', encoding="utf-8-sig")

if __name__ == "__main__":
    from helpers import BepaalOutputBestandCollectPerDag, BepaalOutputBestandScipioBestand, kerken

    for kerk in kerken:
        collectes_per_dag_naar_scipio_csv(BepaalOutputBestandCollectPerDag(kerk), BepaalOutputBestandScipioBestand(kerk))

