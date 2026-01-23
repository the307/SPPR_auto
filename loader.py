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
    data = {"date": dates}
    for key, val in monthly_data.items():
        data[key] = _expand_value_to_days(val, days)
    return pd.DataFrame(data)


def _build_df_from_by_date(by_date: Dict[str, Any]) -> pd.DataFrame:
    """Строит DataFrame по значениям, заданным по датам."""
    if not by_date:
        return pd.DataFrame()
    dates = sorted(
        by_date.keys(),
        key=lambda d: pd.to_datetime(d, dayfirst=True, errors="coerce"),
    )
    rows = [by_date.get(d, {}) or {} for d in dates]
    df = pd.DataFrame(rows)
    df.insert(0, "date", dates)
    df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True).dt.normalize()
    return df


def _apply_manual_corrections(df: pd.DataFrame, manual_corrections: Dict[str, Any]) -> pd.DataFrame:
    """Применяет ручные корректировки из JSON (скаляры или массивы)."""
    if not manual_corrections:
        return df
    days = len(df)
    updates = {
        key: _expand_value_to_days(val, days)
        for key, val in manual_corrections.items()
        if val is not None
    }
    if not updates:
        return df
    updates_df = pd.DataFrame(updates, index=df.index)
    df = df.copy()
    df.loc[:, updates_df.columns] = updates_df
    return df


def build_all_data() -> pd.DataFrame:
    """Собирает master_df только из JSON (Excel больше не используется)."""
    data = load_input_json()
    by_date = data.get("by_date", {}) or {}
    monthly_data = data.get("monthly_data", {}) or {}
    end_of_month = data.get("end_of_month", {}) or {}
    manual_corrections = data.get("manual_corrections", {}) or {}

    dates = get_day()
    master_df = pd.DataFrame({"date": dates})

    by_date_df = pd.DataFrame()
    if by_date:
        by_date_df = _build_df_from_by_date(by_date)
        if not by_date_df.empty:
            by_date_month_df = by_date_df[by_date_df["date"].isin(master_df["date"])]
            if not by_date_month_df.empty:
                master_df = master_df.merge(by_date_month_df, on="date", how="left")

    if monthly_data:
        monthly_df = _build_df_from_monthly(monthly_data, dates).drop(columns=["date"])
        master_df = master_df.join(monthly_df)

    if end_of_month:
        master_df = master_df.copy()
        last_idx = master_df.index[-1] if len(master_df) else None
        for key, val in end_of_month.items():
            if key not in master_df.columns:
                master_df[key] = 0.0
            else:
                # ensure compatible dtype for float assignment
                master_df[key] = master_df[key].astype(float)
            if last_idx is not None:
                master_df.loc[last_idx, key] = val

    master_df = _apply_manual_corrections(master_df, manual_corrections)
    master_df["date"] = pd.to_datetime(master_df["date"], errors="coerce").dt.normalize()

    if not by_date_df.empty:
        first_day = master_df["date"].min()
        prev_day = pd.to_datetime(first_day).normalize() - timedelta(days=1)
        prev_day_row = by_date_df[by_date_df["date"] == prev_day]
        if not prev_day_row.empty:
            for col in prev_day_row.columns:
                if col == "date":
                    continue
                if col not in master_df.columns:
                    master_df[col] = 0.0
            row = {}
            first_row = master_df.iloc[0] if len(master_df) else pd.Series(dtype=float)
            for col in master_df.columns:
                if col == "date":
                    continue
                # Для предыдущего дня:
                # - списковые месячные данные (по дням) не переносим
                # - скалярные месячные параметры оставляем
                if col in monthly_data and col in first_row.index:
                    val = monthly_data[col]
                    if isinstance(val, (list, tuple, np.ndarray)):
                        row[col] = 0.0
                    else:
                        row[col] = first_row[col]
                else:
                    row[col] = 0.0
            row["date"] = prev_day
            prev_values = prev_day_row.iloc[0]
            for col in prev_day_row.columns:
                if col == "date":
                    continue
                val = prev_values[col]
                row[col] = 0.0 if pd.isna(val) else val
            master_df = pd.concat([pd.DataFrame([row]), master_df], ignore_index=True)

    # Проверяем на None/NaN: при наличии — выбрасываем ошибку с перечнем колонок/строк
    if master_df.isna().any().any():
        bad_cols = master_df.columns[master_df.isna().any()].tolist()
        bad_rows = master_df.index[master_df.isna().any(axis=1)].tolist()
        raise ValueError(
            f"Обнаружены None/NaN в исходных данных. Колонки: {bad_cols}, строки: {bad_rows}"
        )

    return master_df