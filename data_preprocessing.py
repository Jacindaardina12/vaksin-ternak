import pandas as pd
import re
from sqlalchemy import create_engine, text

# ===============================
# KONFIGURASI DATABASE
# ===============================
DB_USER = "root"
DB_PASS = "72741516"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "db_vaksin"
TABLE_NAME = "vaksin"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True
)

# ===============================
# HELPER FUNCTIONS
# ===============================
def parse_umur_to_bulan(text):
    """
    Contoh:
    '3 tahun 1 bulan' -> 37
    '2 tahun' -> 24
    '5 bulan' -> 5
    """
    if not isinstance(text, str):
        return None

    tahun = re.search(r'(\d+)\s*tahun', text)
    bulan = re.search(r'(\d+)\s*bulan', text)

    total_bulan = 0
    if tahun:
        total_bulan += int(tahun.group(1)) * 12
    if bulan:
        total_bulan += int(bulan.group(1))

    return total_bulan if total_bulan > 0 else None


def clean_scientific_notation(value):
    """
    Mengubah 6.28E+12 -> '6280000000000'
    """
    try:
        if isinstance(value, float):
            return str(int(value))
        return value
    except:
        return value


# ===============================
# MAIN PREPROCESSING FUNCTION
# ===============================
def load_and_preprocess():
    # ---------------------------
    # Ambil data dari MySQL
    # ---------------------------
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, engine)

    # ---------------------------
    # Bersihkan id_penyakit: {64} -> 64
    # ---------------------------
    if "id_penyakit" in df.columns:
        df["id_penyakit"] = (
            df["id_penyakit"]
            .astype(str)
            .str.replace("{", "", regex=False)
            .str.replace("}", "", regex=False)
        )

    # ---------------------------
    # Konversi tanggal
    # ---------------------------
    if "tanggal_vaksinasi" in df.columns:
        df["tanggal"] = pd.to_datetime(
            df["tanggal_vaksinasi"],
            errors="coerce",
            dayfirst=True
        )

    # ---------------------------
    # Pastikan numerik
    # ---------------------------
    numeric_cols = ["bulan_numerik", "tahun", "urutan_vaksinasi"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------
    # Latitude & Longitude
    # ---------------------------
    for col in ["latitude", "longitude"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---------------------------
    # Umur -> bulan (numeric)
    # ---------------------------
    if "umur" in df.columns:
        df["umur_bulan"] = df["umur"].apply(parse_umur_to_bulan)

    # ---------------------------
    # Nomor ilmiah (E+)
    # ---------------------------
    sci_cols = ["nomorpetugas", "telppemilik", "nikpemilik"]
    for col in sci_cols:
        if col in df.columns:
            df[col] = df[col].apply(clean_scientific_notation)

    # ---------------------------
    # Normalisasi kategori
    # ---------------------------
    cat_cols = ["hewan", "jenis_kelamin", "kecamatan", "desa"]
    for col in cat_cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    return df


# ===============================
# TEST (optional)
# ===============================
if __name__ == "__main__":
    df_clean = load_and_preprocess()
    print("✅ Preprocessing selesai")
    print(df_clean.head())
    print("\nKolom akhir:")
    print(df_clean.columns.tolist())
