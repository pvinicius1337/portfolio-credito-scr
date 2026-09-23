import requests
from pathlib import Path
import zipfile
import pandas as pd

def build_download_url (year: int) -> str:
    return f"https://www.bcb.gov.br/pda/desig/scrdata_{year}.zip"

def download_zip(year: int, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / f'scrdata_{year}.zip'
    url = build_download_url(year)

    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()
        total = int(response.headers.get('Content-Length', 0))
        downloaded = 0 
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
                downloaded += len(chunk)
                print(f"\r{downloaded / 1024 / 1024:.1f} MB / {total / 1024 /1024:.1f} MB", end="")
    print()
    return zip_path

#Download da base 
#download_zip(2025, Path("dados/raw/scr_data"))

zip_path = Path("dados/raw/scr_data/scrdata_2025.zip")

with zipfile.ZipFile(zip_path) as zf:
    with zf.open("scrdata_202501.csv") as f:
        df = pd.read_csv(f, sep=";", decimal=',', encoding='utf-8-sig')

print(df.shape)
print(df.dtypes)
print(df.head())

SUPRESSAO_OPERACOES = -1  # sentinela: contagem suprimida (indício, não documentado na Metodologia V2 — ver README)

qtd_suprimidas = (df["numero_de_operacoes"] == SUPRESSAO_OPERACOES).sum()
print("linhas suprimidas:", qtd_suprimidas, "de", len(df))

df["numero_de_operacoes"] = (
    df["numero_de_operacoes"]
    .replace(SUPRESSAO_OPERACOES, pd.NA)
    .astype("Int64")
)

print(df["numero_de_operacoes"].dtype)
print(df["numero_de_operacoes"].isna().sum())