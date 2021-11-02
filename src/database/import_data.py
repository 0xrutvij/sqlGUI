import json
import pandas as pd

from src.config import IMPORT_SOURCE


def csv_to_json(csv_loc):
    df = pd.read_csv(csv_loc)
    name_cols = df.columns[pd.Series(df.columns).str.endswith("name")]
    work_address_cols = df.columns[(pd.Series(df.columns).str.startswith("work")) & ~(pd.Series(df.columns).str.endswith("phone"))]
    home_address_cols = df.columns[(pd.Series(df.columns).str.startswith("home")) & ~(pd.Series(df.columns).str.endswith("phone"))]
    phone_cols = df.columns[pd.Series(df.columns).str.endswith("phone")]
    date_cols = df.columns[pd.Series(df.columns).str.endswith("date")]
    entries = {}
    for i, row in df.iterrows():
        entries[i] = {
            "name": row[name_cols].to_dict(),
            "addresses": {
                "home": row[home_address_cols].to_dict(),
                "work": row[work_address_cols].to_dict()
            },
            "phones": {c: v for c, v in zip(phone_cols, row[phone_cols].to_list()) if pd.notna(v)},
            "dates": {"birth_date": row[date_cols][0]} if pd.notna(row[date_cols][0]) else None
        }
        if i == -1:
            print(json.dumps(entries[i], indent="\t"))

    return entries


if __name__ == '__main__':
    table_vals = csv_to_json(IMPORT_SOURCE)

