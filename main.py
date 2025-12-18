if __name__ == "__main__":
    from bepaalCollectesPerDagPerKerk import bepaalCollectes2025
    from collectesPerDagNaarScipioCSV import collectes_per_dag_naar_scipio_csv
    from helpers import BepaalOutputBestandCollectPerDag, BepaalOutputBestandScipioBestand, kerken

    bepaalCollectes2025()

    for kerk in kerken:
        collectes_per_dag_naar_scipio_csv(BepaalOutputBestandCollectPerDag(kerk), BepaalOutputBestandScipioBestand(kerk)) 

    