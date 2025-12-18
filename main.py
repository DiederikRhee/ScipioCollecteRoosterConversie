if __name__ == "__main__":
    from bepaalCollectesPerDagPerKerk import bepaalCollectes2025
    from collectesPerDagNaarScipioCSV import collectes_per_dag_naar_scipio_csv
    from helpers import BepaalOutputBestandCollectPerDag, BepaalOutputBestandScipioBestand

    results = bepaalCollectes2025()

    for church, df in results:
        df.to_excel(BepaalOutputBestandCollectPerDag(church), index=False)

        collectes_per_dag_naar_scipio_csv(df, BepaalOutputBestandScipioBestand(church)) 

    