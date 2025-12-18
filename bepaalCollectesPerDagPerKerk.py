from pathlib import Path
from dataclasses import dataclass
import pandas as pd
import numpy as np
from typing import List

@dataclass
class CollectionItem:
    index: int | None
    charity: str

    def ToString(self) -> str:
        if (self.index is not None):
            return f"Col-{self.index}: {self.charity}"
        else:
            return self.charity

@dataclass
class CollectionPerDay:
    date: pd.Timestamp
    special: str
    collections: list[CollectionItem]


def collection_per_day_to_df(data: list[CollectionPerDay]) -> pd.DataFrame:
    # Determine max number of collections
    max_collections = max(len(d.collections) for d in data)

    rows = []
    for d in data:
        row = {
            "Datum": d.date,
            "Bijzonderheden": d.special,
        }

        # Convert collections using ToString()
        collection_strings = [c.ToString() for c in d.collections]

        # Fill dynamic collection columns
        for i in range(max_collections):
            row[f"Collecte_{i+1}"] = (
                collection_strings[i] if i < len(collection_strings) else None
            )

        rows.append(row)

    return pd.DataFrame(rows)

def bepaalCollectes2025() -> List[tuple[str, pd.DataFrame]]:
    churches = ["BK", "OH", "WK"]
    churchesHeaders = [f"{church}_{i}" for church in churches for i in range(1, 4)]
    xls = pd.ExcelFile(r"input/Collecterooster_PGK_2026___Definitief_12-11-2025.xlsx")
    df = xls.parse(sheet_name="Collectes 2026 A4 per kerk", index_col=0, skiprows=2, nrows=82, names=["Datum", "Bijzonderheden"] + churchesHeaders)
    df.index  = df.index.to_series().ffill()
    df.replace("K&E", "Kerk en Eredienst", inplace=True)
    df.replace("Wel samenkomst, geen collecte", np.nan, inplace=True)
    df.dropna(inplace=True, how="all", subset=churchesHeaders)

    results: List[tuple[str, pd.DataFrame]] = []

    for church in churches:
        churchHeaders = [f"{church}_{i}" for i in range(1, 4)]
        church_df = df[["Bijzonderheden"] + churchHeaders]
        church_df.dropna(inplace=True, how="all", subset=churchHeaders)
        church_df.rename(columns={churchHeaders[0]: "1", churchHeaders[1]: "2", churchHeaders[2]: "3"}, inplace=True)
        dates = church_df.index.unique()

        collections: List[CollectionPerDay] = []
        for data in dates:
            church_data_df = church_df.loc[data]

            collectionPerDay: CollectionPerDay = CollectionPerDay(data, "", [])
            def AddCollectionForItem(object):
                for i in range(1, 4):
                    item = object[str(i)]
                    if (item == item):  # not NaN
                        collectionPerDay.collections.append(CollectionItem(i, item))

            if (isinstance(church_data_df, pd.Series)): # only one row for this data
                specialItem = church_data_df["Bijzonderheden"]
                if (specialItem == specialItem):  # not NaN
                    collectionPerDay.special = specialItem
                AddCollectionForItem(church_data_df)
            else: # multiple rows for this date
                specialItems = church_data_df["Bijzonderheden"].dropna().values
                if (len(specialItems) > 0):
                    collectionPerDay.special = "| ".join(specialItems)
                
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
                                if item not in [collection.charity for collection in collectionPerDay.collections]:
                                    newItems.append(CollectionItem(i, item))
                        if (len(newItems) == 1):
                            collectionPerDay.collections.append(CollectionItem(None, newItems[0].charity))
                        else:
                            for newItem in newItems:
                                collectionPerDay.collections.append(newItem)
            collections.append(collectionPerDay)
        results.append((church, collection_per_day_to_df(collections)))
    return results


if __name__ == "__main__":
    results = bepaalCollectes2025()

    for church, df in results:
        df.to_excel(Path(f"output/2025_{church}_collectes_per_dag.xlsx"), index=False)

    