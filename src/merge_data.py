import os
import re
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent / "merged"

PRODUCTION_TYPES = ["Mar", "Presal", "Terra"]
FILE_PATTERN = re.compile(r"^(\d{4})_(\d{2})_producao_(Mar|Presal|Terra)\.csv$")


def merge_csvs():
    OUTPUT_DIR.mkdir(exist_ok=True)

    groups: dict[str, list[pd.DataFrame]] = {t: [] for t in PRODUCTION_TYPES}

    for filename in sorted(os.listdir(DATA_DIR)):
        match = FILE_PATTERN.match(filename)
        if not match:
            continue

        year, month, prod_type = match.group(1), match.group(2), match.group(3)
        timestamp = f"{month}/{year}"

        df = pd.read_csv(DATA_DIR / filename, encoding="latin-1")
        df["timestamp"] = timestamp
        groups[prod_type].append(df)

    for prod_type, frames in groups.items():
        if not frames:
            print(f"No files found for type: {prod_type}")
            continue

        merged = pd.concat(frames, ignore_index=True)
        output_path = OUTPUT_DIR / f"producao_{prod_type}.parquet"
        merged.to_parquet(output_path, index=False)
        print(f"Saved {len(merged)} rows -> {output_path}")


if __name__ == "__main__":
    merge_csvs()
