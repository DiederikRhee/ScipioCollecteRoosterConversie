from bepaalCollectesPerDagPerKerk import bepaalCollectes2025
from collectesPerDagNaarScipioCSV import collectes_per_dag_naar_scipio_csv
from pathlib import Path

if __name__ == "__main__":
    results = bepaalCollectes2025()

    for church, df in results:
        df.to_excel(Path(f"output/2025_{church}_collectes_per_dag.xlsx"), index=False)

        collectes_per_dag_naar_scipio_csv(df, f"output/2025_{church}_scipio_input.csv") 

    