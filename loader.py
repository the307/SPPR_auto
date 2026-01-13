import calendar
import json
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from config import INPUT_JSON_PATH


def get_day() -> List[datetime]:
    """Возвращает список дат для текущего месяца."""
    today = datetime.now().replace(day=1)  # Первый день текущего месяца
    year, month = today.year, today.month
    total_days = calendar.monthrange(year, month)[1]
    dates = [today + timedelta(days=i) for i in range(total_days)]
    return dates


@lru_cache(maxsize=1)
def load_input_json(path: str = INPUT_JSON_PATH) -> Dict[str, Any]:
    """Загружает JSON с исходными данными."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _expand_value_to_days(value: Any, days: int) -> List[Any]:
    """Приводит скаляр или список к списку длиной days."""
    if isinstance(value, (list, tuple)):
        arr = list(value)
        if len(arr) >= days:
            return arr[:days]
        last = arr[-1] if arr else 0
        arr.extend([last] * (days - len(arr)))
        return arr
    return [value for _ in range(days)]


def _build_df_from_monthly(monthly_data: Dict[str, Any], dates: List[datetime]) -> pd.DataFrame:
    """Строит DataFrame по месячным данным (массы или скаляры)."""
    days = len(dates)
    df = pd.DataFrame({"date": dates})
    for key, val in monthly_data.items():
        df[key] = _expand_value_to_days(val, days)
    return df


def _apply_manual_corrections(df: pd.DataFrame, manual_corrections: Dict[str, Any]) -> pd.DataFrame:
    """Применяет ручные корректировки из JSON (скаляры или массивы)."""
    if not manual_corrections:
        return df
    days = len(df)
    for key, val in manual_corrections.items():
        if val is None:
            continue
        df[key] = _expand_value_to_days(val, days)
    return df


def build_all_data() -> pd.DataFrame:
    """Собирает master_df только из JSON (Excel больше не используется)."""
    data = load_input_json()
    monthly_data = data.get("monthly_data", {}) or {}
    manual_corrections = data.get("manual_corrections", {}) or {}

    dates = get_day()
    master_df = _build_df_from_monthly(monthly_data, dates)
    master_df = _apply_manual_corrections(master_df, manual_corrections)

    master_df["date"] = pd.to_datetime(master_df["date"], errors="coerce").dt.normalize()
    master_df = master_df.fillna(0)
    return master_df