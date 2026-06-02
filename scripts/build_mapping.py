import re
import pandas as pd
from pathlib import Path






def _parse_phenotype(pheno: str) -> dict[str, str]:
    """Return {marker: '+'/'-'} for a phenotype string like 'CD15-CK+CD3-'."""
    return dict(re.findall(r"([A-Za-z0-9]+)([+\-])", pheno))  # dict() zamiast comprehension


def canonical(pheno: str) -> str:
    """Canonical phenotype: markers sorted alphabetically, signs attached."""
    return "".join(
        f"{m}{s}" for m, s in sorted(re.findall(r"([A-Za-z0-9]+)([+\-])", pheno))
    )  # pomiń parse_phenotype — sortowanie par (m, s) daje ten sam efekt co sortowanie dict


def build_mapping(mapping_file: Path) -> dict[str, str]:
    df = pd.read_csv(mapping_file, usecols=["phenotype", "celltype"])  # wczytaj tylko potrzebne kolumny
    return dict(zip(df["phenotype"].map(canonical), df["celltype"]))   # iterrows() → zip (10-100x szybciej)