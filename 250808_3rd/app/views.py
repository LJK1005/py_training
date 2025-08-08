import os
import numpy as np
import pandas as pd

from django.shortcuts import render, HttpResponse
from django.conf import settings

def show_csv(request) -> HttpResponse:
    csv_path: str = os.path.join(settings.BASE_DIR, "app", "resources", "mn.csv")
    df: pd.DataFrame = pd.read_csv(csv_path)
    columns: pd.Index[str] = df.columns
    rows: np.ndarray = df.values

    rank_stats: pd.Series[int] = df["직급"].value_counts().sort_index()
    rank_stats: list = list(zip(rank_stats.index, rank_stats.values))

    return render(request, "app/show_csv.html", {
        "columns": columns,
        "rows": rows,
        "rank_stats": rank_stats,
    })
