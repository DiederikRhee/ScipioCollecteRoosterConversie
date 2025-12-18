from pathlib import Path
from dataclasses import dataclass
import pandas as pd
import numpy as np
from typing import List
from helpers import kerken, BepaalOutputBestandCollectPerDag

@dataclass
class CollecteItem:
    index: int | None
    doel: str

    def MaakNaam(self) -> str:
        if (self.index is not None):
            return f"Col-{self.index}: {self.doel}"
        else:
            return self.doel

@dataclass
class CollectesPerDag:
    datum: pd.Timestamp
    bijzonderheden: str
    collectes: list[CollecteItem]


def collectesPerDagNaarDataframe(data: list[CollectesPerDag]) -> pd.DataFrame:
    # Determine max number of collections
    max_collections = max(len(d.collectes) for d in data)

    rows = []
    for d in data:
        row = {
            "Datum": d.datum,
            "Bijzonderheden": d.bijzonderheden,
        }

        # Convert collections using ToString()
        collection_strings = [c.MaakNaam() for c in d.collectes]

        # Fill dynamic collection columns
        for i in range(max_collections):
            row[f"Collecte_{i+1}"] = (
                collection_strings[i] if i < len(collection_strings) else None
            )

        rows.append(row)

    return pd.DataFrame(rows)

def bepaalCollectes2025():
    churchesHeaders = [f"{church}_{i}" for church in kerken for i in range(1, 4)]
    xls = pd.ExcelFile(r"input/Collecterooster_PGK_2026___Definitief_12-11-2025.xlsx")
    df = xls.parse(sheet_name="Collectes 2026 A4 per kerk", index_col=0, skiprows=2, nrows=82, names=["Datum", "Bijzonderheden"] + churchesHeaders)
    df.index  = df.index.to_series().ffill()
    df.replace("K&E", "Kerk en Eredienst", inplace=True)
    df.replace("Wel samenkomst, geen collecte", np.nan, inplace=True)
    df.dropna(inplace=True, how="all", subset=churchesHeaders)

    results: List[tuple[str, pd.DataFrame]] = []

    for kerk in kerken:
        churchHeaders = [f"{kerk}_{i}" for i in range(1, 4)]
        church_df = df[["Bijzonderheden"] + churchHeaders]
        church_df.dropna(inplace=True, how="all", subset=churchHeaders)
        church_df.rename(columns={churchHeaders[0]: "1", churchHeaders[1]: "2", churchHeaders[2]: "3"}, inplace=True)
        dates = church_df.index.unique()

        collections: List[CollectesPerDag] = []
        for data in dates:
            church_data_df = church_df.loc[data]

            collectionPerDay: CollectesPerDag = CollectesPerDag(data, "", [])
            def AddCollectionForItem(object):
                for i in range(1, 4):
                    item = object[str(i)]
                    if (item == item):  # not NaN
                        collectionPerDay.collectes.append(CollecteItem(i, item))

            if (isinstance(church_data_df, pd.Series)): # only one row for this data
                specialItem = church_data_df["Bijzonderheden"]
                if (specialItem == specialItem):  # not NaN
                    collectionPerDay.bijzonderheden = specialItem
                AddCollectionForItem(church_data_df)
            else: # multiple rows for this date
                specialItems = church_data_df["Bijzonderheden"].dropna().values
                if (len(specialItems) > 0):
                    collectionPerDay.bijzonderheden = "| ".join(specialItems)
                
                fistRow = True
                for row, data_row in church_data_df.iterrows():
                    if (fistRow):
                        AddCollectionForItem(data_row)
                        fistRow = False
                    else:
                        newItems = []    
                        for i in range(1, 4):
                            item = data_row[str(i)]
                            if (item == item):  # not NaN
                                if item not in [collection.doel for collection in collectionPerDay.collectes]:
                                    newItems.append(CollecteItem(i, item))
                        if (len(newItems) == 1):
                            collectionPerDay.collectes.append(CollecteItem(None, newItems[0].doel))
                        else:
                            for newItem in newItems:
                                collectionPerDay.collectes.append(newItem)
            collections.append(collectionPerDay)
        df_resultaat = collectesPerDagNaarDataframe(collections)
        df_resultaat.to_excel(BepaalOutputBestandCollectPerDag(kerk), index=False)


if __name__ == "__main__":
    bepaalCollectes2025()

    