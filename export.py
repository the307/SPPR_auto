"""
МОДУЛЬ ЭКСПОРТА РЕЗУЛЬТАТОВ В JSON

Преобразует результаты расчётов (DataFrame) в JSON формат,
идентичный входному JSON-шаблону.
"""

import json
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from config import INPUT_JSON_PATH
from loader import load_input_json


# -------------------------
# Вспомогательные функции
# -------------------------

def _to_serializable(value: Any):
    """Преобразует значение в JSON-сериализуемый формат."""
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer, np.int64, int)):
        return int(value)
    if isinstance(value, (np.floating, np.float64, float)):
        return float(value)
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.strftime("%Y-%m-%d") if pd.notna(value) else None
    if isinstance(value, (list, tuple, np.ndarray)):
        return [_to_serializable(v) for v in value]
    return value


def _safe_print(message: str) -> None:
    """Печатает строку, заменяя неподдерживаемые символы."""
    try:
        print(message)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(message.encode("cp1251", errors="replace") + b"\n")


def export_input_template(
    output_path: str = "output.json",
    input_path: str = INPUT_JSON_PATH,
) -> None:
    template = load_input_json(input_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)
    _safe_print(f"Результат сохранён в {output_path}")


def _load_input_template(path: str = INPUT_JSON_PATH) -> Dict[str, Any]:
    return load_input_json(path)


_EXPLICIT_KEY_MAP: Dict[str, str] = {}


_RE_V_OST_NEW = re.compile(r"^V_(.+)_ost_(.+)_(nm|km)$")
_RE_V_OST_OLD = re.compile(r"^V_(.+)_(nm|km)_ost_(.+)$")
_RE_V_PATH_NEW = re.compile(r"^V_(.+)_path_(nm|km)$")
_RE_V_PATH_OLD = re.compile(r"^V_(.+)_(nm|km)_path$")
_RE_V_GTM_OST_NEW = re.compile(r"^V_(.+)_gtm_ost_(.+)_(nm|km)$")
_RE_V_GTM_OST_OLD = re.compile(r"^V_(.+)_(nm|km)_gtm_ost_(.+)$")
_RE_V_GTM_PATH_NEW = re.compile(r"^V_(.+)_gtm_path_(nm|km)$")
_RE_V_GTM_PATH_OLD = re.compile(r"^V_(.+)_(nm|km)_gtm_path$")


def _normalize_suffixes(key: str) -> str:
    key = key.replace("_gtm_ost_product", "_gtm_ost_tov")
    key = key.replace("_rvs_clear", "_rvs_clean").replace("_texn", "_tech")
    return key


def _normalize_input_key(key: str) -> str:
    key = key.strip()
    if key in _EXPLICIT_KEY_MAP:
        return _EXPLICIT_KEY_MAP[key]

    m = _RE_V_OST_OLD.match(key)
    if m:
        return _normalize_suffixes(f"V_{m.group(1)}_ost_{m.group(3)}_{m.group(2)}")
    m = _RE_V_OST_NEW.match(key)
    if m:
        return _normalize_suffixes(key)

    m = _RE_V_PATH_OLD.match(key)
    if m:
        return f"V_{m.group(1)}_path_{m.group(2)}"
    m = _RE_V_PATH_NEW.match(key)
    if m:
        return key

    m = _RE_V_GTM_OST_OLD.match(key)
    if m:
        return _normalize_suffixes(f"V_{m.group(1)}_gtm_ost_{m.group(3)}_{m.group(2)}")
    m = _RE_V_GTM_OST_NEW.match(key)
    if m:
        return _normalize_suffixes(key)

    m = _RE_V_GTM_PATH_OLD.match(key)
    if m:
        return f"V_{m.group(1)}_gtm_path_{m.group(2)}"
    m = _RE_V_GTM_PATH_NEW.match(key)
    if m:
        return key

    return _normalize_suffixes(key)


def _merge_template_value(template_value: Any, actual_value: Any) -> Any:
    if isinstance(template_value, dict) and "value" in template_value:
        base_value = template_value.get("value")
        status = template_value.get("status")
        message = template_value.get("message")
        if isinstance(actual_value, dict):
            value = actual_value.get("value")
            if value is None:
                value = base_value
            status = actual_value.get("status", status)
            message = actual_value.get("message", message)
        else:
            value = actual_value if actual_value is not None else base_value
        # На выходе: если status пустой/NaN — считаем "норм" (ставим 0),
        # чтобы в результирующем JSON не было NaN/null статусов.
        try:
            if pd.isna(status):
                status = 0
        except Exception:
            pass
        return {"value": _to_serializable(value), "status": status, "message": message}
    if isinstance(actual_value, dict):
        value = actual_value.get("value")
        if value is None:
            value = template_value
    else:
        value = actual_value if actual_value is not None else template_value
    return _to_serializable(value)


def _row_for_date(df: pd.DataFrame, date_value: Any) -> Optional[pd.Series]:
    if date_value is None:
        return None
    dt = pd.to_datetime(date_value, errors="coerce", dayfirst=True)
    if pd.isna(dt):
        return None
    target = dt.normalize()
    matches = df.loc[df["date"] == target]
    if matches.empty:
        return None
    return matches.iloc[-1]


def _build_output_dict(
    template: Dict[str, Any],
    master_df: pd.DataFrame,
    calc_date: Optional[datetime],
) -> Dict[str, Any]:
    """Собирает итоговый dict результата (в памяти, без записи на диск)."""
    df = master_df.copy()
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()

    output: Dict[str, Any] = dict(template)
    control = template.get("control", {}) or {}
    output["control"] = control

    control_date = control.get("Date_calculation")
    row_prev = _row_for_date(df, control_date)

    last_date = pd.to_datetime(calc_date) if calc_date is not None else df["date"].max()
    last_date = last_date.normalize() if pd.notna(last_date) else df["date"].max()
    row_last = _row_for_date(df, last_date)

    month_data = df[(df["date"].dt.month == last_date.month) & (df["date"].dt.year == last_date.year)].copy()
    month_sum_map = {
        "G_buying_oil_month": "G_buying_oil",
        "G_out_udt_month": "G_out_udt",
    }

    if "last_day" in template:
        last_day_out = {}
        for key, tpl_val in (template.get("last_day") or {}).items():
            norm_key = _normalize_input_key(key)
            actual = None
            if row_prev is not None:
                if norm_key in row_prev:
                    actual = row_prev.get(norm_key)
                elif norm_key.endswith("_0"):
                    alt_key = norm_key[:-2]
                    actual = row_prev.get(alt_key) if alt_key in row_prev else None
                elif norm_key.endswith("_prev"):
                    alt_key = norm_key[:-5]
                    actual = row_prev.get(alt_key) if alt_key in row_prev else None
            if actual is None and norm_key in df.columns:
                series = df[norm_key].dropna()
                if not series.empty:
                    actual = series.iloc[0]
            last_day_out[key] = _merge_template_value(tpl_val, actual)
        output["last_day"] = last_day_out

    if "month" in template:
        month_out = {}
        for key, tpl_val in (template.get("month") or {}).items():
            norm_key = _normalize_input_key(key)
            actual = None
            if row_last is not None and norm_key in row_last:
                actual = row_last.get(norm_key)
            if actual is None and not month_data.empty and norm_key in month_data.columns:
                actual = month_data[norm_key].iloc[-1]
            if actual is None and key in month_sum_map and not month_data.empty:
                source_col = month_sum_map[key]
                if source_col in month_data.columns:
                    actual = month_data[source_col].sum()
            month_out[key] = _merge_template_value(tpl_val, actual)
        output["month"] = month_out

    if "standards" in template:
        standards_out = {}
        for key, tpl_val in (template.get("standards") or {}).items():
            norm_key = _normalize_input_key(key)
            actual = row_last.get(norm_key) if row_last is not None and norm_key in row_last else None
            standards_out[key] = _merge_template_value(tpl_val, actual)
        output["standards"] = standards_out

    if "plan_BP" in template:
        plan_bp_out = {}
        for key, tpl_val in (template.get("plan_BP") or {}).items():
            norm_key = _normalize_input_key(key)
            actual = row_last.get(norm_key) if row_last is not None and norm_key in row_last else None
            plan_bp_out[key] = _merge_template_value(tpl_val, actual)
        output["plan_BP"] = plan_bp_out

    if "plan_GTM" in template:
        plan_gtm_out = {}
        for key, tpl_val in (template.get("plan_GTM") or {}).items():
            norm_key = _normalize_input_key(key)
            actual = row_last.get(norm_key) if row_last is not None and norm_key in row_last else None
            plan_gtm_out[key] = _merge_template_value(tpl_val, actual)
        output["plan_GTM"] = plan_gtm_out

    if "days" in template:
        days_out: List[Dict[str, Any]] = []
        for day_tpl in template.get("days", []) or []:
            day_out: Dict[str, Any] = {}
            date_str = day_tpl.get("date")
            day_out["date"] = date_str
            row = _row_for_date(df, date_str)
            for key, tpl_val in day_tpl.items():
                if key == "date":
                    continue
                norm_key = _normalize_input_key(key)
                actual = row.get(norm_key) if row is not None and norm_key in row else None
                day_out[key] = _merge_template_value(tpl_val, actual)
            days_out.append(day_out)
        output["days"] = days_out

    return output


# -------------------------
# Основная функция экспорта
# -------------------------

def export_to_json(
    master_df: Optional[pd.DataFrame],
    output_path: Optional[str] = None,
    calc_date: Optional[datetime] = None,
    error: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Собирает результаты расчётов в dict (структура входного JSON-шаблона)
    и **возвращает**

    Если передан *output_path* — дополнительно сохраняет dict на диск.
    Если *output_path* не задан — файл НЕ создаётся.

    В случае *error* — возвращает только объект ошибки, расчёт
    считается прерванным.
    """
    if error is not None:
        output: Dict[str, Any] = {"error": error}
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
        _safe_print(f"Расчёт прерван. Ошибка: {error.get('message')}")
        return output

    if master_df is None or master_df.empty:
        raise ValueError("DataFrame пуст, нет данных для экспорта")

    template = _load_input_template()
    if not (isinstance(template, dict) and "days" in template and "control" in template):
        raise ValueError("Входной JSON не содержит секции 'control' и 'days'.")

    result = _build_output_dict(template, master_df, calc_date)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        _safe_print(f"Результат сохранён в {output_path}")

    return result


def export_to_excel(
    *,
    script_name: str = "json_to_excel_balance.py",
) -> None:
    """Конвертирует `output.json` в Excel через `json_to_excel_balance.py`.

    Скрипт сам читает `data_output.json` (если есть) иначе `output.json`,
    и сохраняет файл вида `balance_<date>[_auto].xlsx`.
    """
    script_path = Path(__file__).resolve().parent / script_name
    if not script_path.exists():
        raise FileNotFoundError(f"Не найден скрипт для экспорта в Excel: {script_path}")
    subprocess.run([sys.executable, str(script_path)], check=True, cwd=str(script_path.parent))

