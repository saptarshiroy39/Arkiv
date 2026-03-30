import pandas as pd


def read_excel(path: str) -> list[dict]:
    sheets = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    pages = []
    for name, df in sheets.items():
        if df.empty:
            continue
        text = f"Sheet: {name}\n{df.to_string(index=False)}"
        pages.append({"text": text})
    return pages
