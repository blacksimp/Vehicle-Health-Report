import argparse
from pathlib import Path
import pandas as pd

from src.utils.logging import get_logger

logger = get_logger(__name__)

def main(input_path: str, output_path: str) -> None:
    input_file = Path(input_path)
    output_file = Path(output_path)

    logger.info(f"Reading file: {input_file}")

    if input_file.suffix == ".csv":
        df = pd.read_csv(input_file, on_bad_lines='warn')
    elif input_file.suffix == ".parquet":
        df = pd.read_parquet(input_file)
    else:
        raise ValueError("Only CSV and Parquet are supported for now.")

    logger.info(f"Loaded shape: {df.shape}")
    
    # Convert all 'object' (mixed text/number) columns to pure strings so Parquet doesn't crash
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_file, index=False)

    logger.info(f"Saved canonical parquet to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to raw input file")
    parser.add_argument("--output", required=True, help="Path to output parquet file")
    args = parser.parse_args()

    main(args.input, args.output)