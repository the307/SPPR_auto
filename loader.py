import calendar
import json
import re
from functools import lru_cache
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

from config import INPUT_JSON_PATH

_DATE_PARSE_KW = {"errors": "coerce", "dayfirst": True}


def get_day() -> List[datetime]:
    """Возвращает список дат для расчёта (из JSON, иначе текущий месяц)."""
    data = load_input_json()
    days = data.get("days", []) or []
    if days:
        parsed = []
        for item in days:
            dt = _parse_date(item.get("date"))
            if dt is not None:
                parsed.append(dt.to_pydatetime())
        return sorted(parsed)

    control = data.get("control", {}) or {}
    year, month = _resolve_control_period(control)
    total_days = calendar.monthrange(year, month)[1]
    start = datetime(year, month, 1)
    return [start + timedelta(days=i) for i in range(total_days)]


@lru_cache(maxsize=1)
def load_input_json(path: str = INPUT_JSON_PATH) -> Dict[str, Any]:
    """Загружает JSON с исходными данными."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    _apply_input_statuses(data)
    return data


def _extract_value(val: Any) -> Any:
    if isinstance(val, dict):
        if "value" in val:
            return _extract_value(val["value"])
        return None
    return val


def _is_value_provided(value: Any) -> bool:
    if value is None:
        return False
    if pd.isna(value):
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    if isinstance(value, (list, tuple, np.ndarray)) and len(value) == 0:
        return False
    return True


def _apply_input_statuses(node: Any) -> None:
    _SKIP_INPUT_CHECK_KEYS = {
        # days: расчётные значения (не должны становиться status=2, если пустые во входном JSON)
        "V_upsv_yu",
        "V_upsv_s",
        "V_cps",
        "V_cppn_1",
        "V_lodochny_cps_upsv_yu",
        "G_sikn",
        "G_sikn_vankor",
        "G_sikn_suzun",
        "G_sikn_vslu",
        "G_sikn_tagul",
        "G_sikn_tng",
        "delta_G_sikn",
        "V_upn_suzun",
        "V_suzun_slu",
        "V_suzun_vslu",
        "V_suzun_tng",
        "G_suzun",
        "G_suzun_slu",
        "G_suzun_vslu",
        "delta_G_suzun",
        "G_buying_oil",
        "G_out_udt",
        "G_per",
        "V_tagul_tr",
        "G_tagul",
        "delta_G_tagul",
        "G_lodochny_upsv_yu",
        "V_upn_lodochny",
        "V_lodochny",
        "V_ichem",
        "G_upn_lodochny",
        "G_lodochny",
        "G_upn_lodochny_ichem",
        "G_tagul_lodochny",
        "G_kchng",
        "G_gnps",
        "V_gnps",
        "V_nps_1",
        "V_nps_2",
        "V_knps",
        "V_tstn",
        "V_tstn_rn_vn",
        "V_tstn_vn",
        "V_tstn_suzun",
        "V_tstn_suzun_vankor",
        "V_tstn_suzun_vslu",
        "V_tstn_tagul_obsh",
        "V_tstn_lodochny",
        "V_tstn_tagul",
        "V_tstn_skn",
        "V_tstn_vo",
        "V_tstn_tng",
        "V_tstn_kchng",
        "F_bp",
        "F_bp_vn",
        "F_bp_suzun",
        "F_bp_suzun_vankor",
        "F_bp_suzun_vslu",
        "F_bp_tagul",
        "F_bp_tagul_lpu",
        "F_bp_tagul_tpu",
        "F_bp_skn",
        "F_bp_vo",
        "F_bp_tng",
        "F_bp_kchng",
        "F",
        "F_vn",
        "F_suzun",
        "F_suzun_vankor",
        "F_suzun_vslu",
        "F_tagul",
        "F_tagul_lpu",
        "F_tagul_tpu",
        "F_skn",
        "F_vo",
        "F_tng",
        "F_kchng",
        "Q_gnps",
        "Q_nps_1_2",
        "Q_knps",
        # month: расчётные проверки/дельты (в шаблоне часто {value,status,message} с null)
        "G_per_month",
    }

    def _should_skip_input_check(field_key: Optional[str]) -> bool:
        if not field_key:
            return False
        if field_key in _SKIP_INPUT_CHECK_KEYS:
            return True
        # расчётные "check" поля и дельты Ф (в шаблоне это не ввод пользователя)
        if field_key.endswith("_check"):
            return True
        if field_key.startswith("delta_F"):
            return True
        return False

    def _walk(curr: Any, field_key: Optional[str] = None) -> None:
        if isinstance(curr, dict):
            # Узел "значение" вида {value,status,message}
            if "value" in curr and "status" in curr:
                if not _should_skip_input_check(field_key):
                    # Не затираем явные статусы ошибок/проверок, если они уже проставлены в файле
                    if curr.get("status") != 3:
                        if _is_value_provided(curr.get("value")):
                            curr["status"] = 1
                            curr["message"] = "Значение введено"
                        else:
                            curr["status"] = 2
                            curr["message"] = "Значение не введено"
                return

            # Обычный dict-объект: спускаемся глубже, передавая имя ключа
            for k, v in curr.items():
                _walk(v, k)
        elif isinstance(curr, list):
            for item in curr:
                _walk(item, field_key)

    _walk(node, None)


def has_missing_input_values(node: Any) -> bool:
    if isinstance(node, dict):
        if "value" in node and "status" in node:
            if node.get("status") is not None and node.get("status") == 2:
                return True
        for value in node.values():
            if has_missing_input_values(value):
                return True
    elif isinstance(node, list):
        for item in node:
            if has_missing_input_values(item):
                return True
    return False


_EXPLICIT_KEY_MAP: Dict[str, str] = {}


_RE_V_OST_NEW = re.compile(r"^V_(.+)_ost_(.+)_(nm|km)$")
_RE_V_OST_OLD = re.compile(r"^V_(.+)_(nm|km)_ost_(.+)$")
_RE_V_PATH_NEW = re.compile(r"^V_(.+)_path_(nm|km)$")
_RE_V_PATH_OLD = re.compile(r"^V_(.+)_(nm|km)_path$")
_RE_V_GTM_OST_NEW = re.compile(r"^V_(.+)_gtm_ost_(.+)_(nm|km)$")
_RE_V_GTM_OST_OLD = re.compile(r"^V_(.+)_(nm|km)_gtm_ost_(.+)$")
_RE_V_GTM_PATH_NEW = re.compile(r"^V_(.+)_gtm_path_(nm|km)$")
_RE_V_GTM_PATH_OLD = re.compile(r"^V_(.+)_(nm|km)_gtm_path$")


def _parse_date(value: Any) -> Optional[datetime]:
    dt = pd.to_datetime(value, **_DATE_PARSE_KW)
    if pd.isna(dt):
        return None
    return dt.normalize()


@lru_cache(maxsize=512)
def _normalize_key(key: str) -> str:
    key = key.strip()
    if key in _EXPLICIT_KEY_MAP:
        return _EXPLICIT_KEY_MAP[key]

    m = _RE_V_OST_OLD.match(key)
    if m:
        key = f"V_{m.group(1)}_ost_{m.group(3)}_{m.group(2)}"
        key = key.replace("_gtm_ost_product", "_gtm_ost_tov")
        key = key.replace("_rvs_clear", "_rvs_clean").replace("_texn", "_tech")
        return key
    m = _RE_V_OST_NEW.match(key)
    if m:
        key = key.replace("_gtm_ost_product", "_gtm_ost_tov")
        key = key.replace("_rvs_clear", "_rvs_clean").replace("_texn", "_tech")
        return key

    m = _RE_V_PATH_OLD.match(key)
    if m:
        return f"V_{m.group(1)}_path_{m.group(2)}"
    m = _RE_V_PATH_NEW.match(key)
    if m:
        return key

    m = _RE_V_GTM_OST_OLD.match(key)
    if m:
        key = f"V_{m.group(1)}_gtm_ost_{m.group(3)}_{m.group(2)}"
        key = key.replace("_gtm_ost_product", "_gtm_ost_tov")
        key = key.replace("_rvs_clear", "_rvs_clean").replace("_texn", "_tech")
        return key
    m = _RE_V_GTM_OST_NEW.match(key)
    if m:
        key = key.replace("_gtm_ost_product", "_gtm_ost_tov")
        key = key.replace("_rvs_clear", "_rvs_clean").replace("_texn", "_tech")
        return key

    m = _RE_V_GTM_PATH_OLD.match(key)
    if m:
        return f"V_{m.group(1)}_gtm_path_{m.group(2)}"
    m = _RE_V_GTM_PATH_NEW.match(key)
    if m:
        return key

    key = key.replace("_gtm_ost_product", "_gtm_ost_tov")
    key = key.replace("_rvs_clear", "_rvs_clean").replace("_texn", "_tech")
    return key


def _normalize_section(section: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, val in section.items():
        norm_key = _normalize_key(key)
        normalized[norm_key] = _extract_value(val)
    return normalized


def _build_df_from_days(days: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for item in days:
        row: Dict[str, Any] = {}
        for key, val in item.items():
            if key == "date":
                continue
            norm_key = _normalize_key(key)
            row[norm_key] = _extract_value(val)
        row["date"] = item.get("date")
        rows.append(row)
    df = pd.DataFrame(rows)
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], **_DATE_PARSE_KW).dt.normalize()
    return df


def _resolve_control_period(control: Dict[str, Any]) -> tuple[int, int]:
    month = control.get("Month")
    calc_date = pd.to_datetime(control.get("Date_calculation"), **_DATE_PARSE_KW)
    if month is None:
        if pd.notna(calc_date):
            target = calc_date + timedelta(days=1)
            return target.year, target.month
        now = datetime.now()
        return now.year, now.month
    month = int(month)
    year = calc_date.year if pd.notna(calc_date) else datetime.now().year
    if pd.notna(calc_date) and month < calc_date.month:
        year += 1
    return year, month


def build_all_data() -> pd.DataFrame:
    """Собирает master_df только из JSON (Excel больше не используется)."""
    data = load_input_json()
    days = data.get("days") or []
    if not days:
        raise ValueError("Секция 'days' пуста: нечего загружать для расчётов.")

    control = data.get("control", {}) or {}
    last_day = data.get("last_day", {}) or {}
    month = data.get("month", {}) or {}
    standards = data.get("standards", {}) or {}
    plan_bp = data.get("plan_BP", {}) or {}
    plan_gtm = data.get("plan_GTM", {}) or {}

    normalized_last_day = _normalize_section(last_day)
    normalized_month = _normalize_section(month)
    normalized_standards = _normalize_section(standards)
    normalized_plan_bp = _normalize_section(plan_bp)
    normalized_plan_gtm = _normalize_section(plan_gtm)

    master_df = _build_df_from_days(days)

    calc_date = pd.to_datetime(control.get("Date_calculation"), **_DATE_PARSE_KW)
    prev_row = None
    if pd.notna(calc_date):
        prev_row = {"date": calc_date.normalize()}
        for key, val in normalized_last_day.items():
            if key.endswith("_0"):
                prev_row[key[:-2]] = val
            elif key.endswith("_prev"):
                prev_row[key[:-5]] = val
            else:
                prev_row[key] = val

    if prev_row is not None and "date" in master_df.columns:
        prev_date = prev_row["date"]
        if prev_date in master_df["date"].tolist():
            mask = master_df["date"] == prev_date
            for key, val in prev_row.items():
                if key == "date":
                    continue
                if key in master_df.columns:
                    master_df.loc[mask, key] = master_df.loc[mask, key].fillna(val)
                else:
                    master_df.loc[mask, key] = val
        else:
            master_df = pd.concat([pd.DataFrame([prev_row]), master_df], ignore_index=True)

    constants = {}
    for key, val in normalized_last_day.items():
        if key.endswith("_0"):
            constants[key] = val
    constants.update(normalized_standards)
    constants.update(normalized_plan_bp)
    constants.update(normalized_plan_gtm)
    constants.update(normalized_month)
    if "Start_autobalance" in control:
        constants["Start_autobalance"] = control.get("Start_autobalance")
    if "VN_upsv_s_min" in constants and "V_upsv_min" not in constants:
        constants["V_upsv_min"] = constants["VN_upsv_s_min"]

    for key, val in constants.items():
        if key in master_df.columns:
            master_df[key] = master_df[key].fillna(val)
        else:
            master_df[key] = val

    master_df["date"] = pd.to_datetime(master_df["date"], **_DATE_PARSE_KW).dt.normalize()
    if master_df["date"].isna().any():
        raise ValueError("Обнаружены некорректные даты в исходных данных.")

    return master_df