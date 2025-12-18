import pandas as pd

def collectes_per_dag_naar_scipio_csv(input: pd.DataFrame, output_path: str):
    input.to_csv(output_path, index=False)

if __name__ == "__main__":
    print ("todo")