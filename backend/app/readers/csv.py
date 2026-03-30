import pandas as pd


def read_csv(path: str) -> list[dict]:
    df = pd.read_csv(path)
    text = df.to_string(index=False)
    return [{"text": text}] if text.strip() else []
