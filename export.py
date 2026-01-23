"""
МОДУЛЬ ЭКСПОРТА РЕЗУЛЬТАТОВ В JSON

Преобразует результаты расчётов (DataFrame) в JSON формат, совместимый
с example_output.json. Excel не используется.
"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd


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


def _create_status_object(value: Any, status: int = 0, message: str = "") -> Dict[str, Any]:
    """Создает объект статуса для полей с валидацией."""
    return {
        "value": _to_serializable(value),
        "status": status,
        "message": message,
    }


def _safe_print(message: str) -> None:
    """Печатает строку, заменяя неподдерживаемые символы."""
    try:
        print(message)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(message.encode("cp1251", errors="replace") + b"\n")


# -------------------------
# Основная функция экспорта
# -------------------------

def export_to_json(
    master_df: Optional[pd.DataFrame],
    output_path: str = "output.json",
    calc_date: Optional[datetime] = None,
    alarm_flag: bool = False,
    alarm_msg: Optional[str] = None,
    error: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Экспортирует результаты расчётов в JSON.

    1) Месячные итоги (monthly_totals):
       - для полей *_month берём последнее значение месяца
       - для остальных полей из списка monthly_fields — сумму
       - производные поля: F_month, F_tagul_month
    2) Объекты валидации (validation_checks):
       - статус 0/1, при alarm_flag -> 1
    3) Данные по дням (days):
       - обычные поля как есть
       - статусные поля как {"value","status","message"}
       - производное поле F_tagul = F_tagul_lpu + F_tagul_tpu
       - маппинг имён status_field_mapping
    4) В случае error — сохраняется только объект ошибки и расчёт
       считается прерванным.
    """
    if error is not None:
        output = {"error": error}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        _safe_print(f"Расчёт прерван. Ошибка: {error.get('message')}")
        return

    if master_df is None or master_df.empty:
        raise ValueError("DataFrame пуст, нет данных для экспорта")

    df = master_df.copy()
    df["date"] = pd.to_datetime(df["date"])

    # Определяем месяц (по calc_date или по последней дате)
    last_date = pd.to_datetime(calc_date) if calc_date is not None else df["date"].max()
    month = last_date.month
    year = last_date.year

    month_data = df[(df["date"].dt.month == month) & (df["date"].dt.year == year)].copy()

    # ---------------------------------------------------------
    # 1. Месячные итоги
    # ---------------------------------------------------------
    monthly_totals: Dict[str, Any] = {}
    monthly_fields: List[str] = [
        "G_per_month", "Q_vankor_month", "Q_suzun_month", "Q_vslu_month",
        "Q_tng_month", "Q_vo_month", "G_suzun_vslu_month", "G_suzun_slu_month",
        "G_suzun_month", "delta_G_suzun", "delta_G_tagul", "G_upn_lodochny_ichem_month",
        "Q_kchng_month", "G_kchng_month", "Q_tagul_month", "Q_lodochny_month",
        "K_otkachki_month", "G_lodochny_uspv_yu_month", "delte_G_upn_lodochny_month",
        "G_tagul_month", "delta_G_tagul_month", "G_tagul_lodochny_month",
        "G_lodochny_month", "G_sikn_vslu_month", "G_sikn_tagul_month",
        "G_sikn_suzun_month", "G_sikn_tng_month", "G_sikn_month",
        "G_sikn_vankor_month", "G_skn_month", "delta_G_sikn_month",
        "F_suzun_vankor_month", "F_suzun_vslu_month", "F_tagul_lpu_month",
        "F_tagul_tpu_month", "F_tagul_month", "F_skn_month", "F_vo_month",
        "F_tng_month", "F_kchng_month", "F_suzun_month", "F_vn_month",
        "F_month", "G_gnps_month",
    ]

    last_value_fields = {"delta_G_suzun", "delta_G_tagul"}

    for field in monthly_fields:
        if field in month_data.columns:
            if field.endswith("_month"):
                val = month_data[field].iloc[-1] if not month_data.empty else None
            elif field in last_value_fields:
                val = month_data[field].iloc[-1] if not month_data.empty else None
            else:
                val = month_data[field].sum() if not month_data.empty else None
            monthly_totals[field] = _to_serializable(val)
        else:
            # fallback для F_*_month -> F_bp_*_month
            if field.startswith("F_") and field.endswith("_month"):
                bp_field = field.replace("F_", "F_bp_", 1)
                if bp_field in month_data.columns:
                    val = month_data[bp_field].iloc[-1] if not month_data.empty else None
                    monthly_totals[field] = _to_serializable(val)
                else:
                    monthly_totals[field] = None
            else:
                monthly_totals[field] = None

    # F_suzun_month = F_suzun_vankor_month + F_suzun_vslu_month
    if monthly_totals.get("F_suzun_month") is None:
        f_vankor = monthly_totals.get("F_suzun_vankor_month")
        f_vslu = monthly_totals.get("F_suzun_vslu_month")
        if f_vankor is not None and f_vslu is not None:
            monthly_totals["F_suzun_month"] = _to_serializable(f_vankor + f_vslu)

    # F_vn_month из F_bp_vn_month, если есть
    if monthly_totals.get("F_vn_month") is None and "F_bp_vn_month" in month_data.columns:
        monthly_totals["F_vn_month"] = _to_serializable(
            month_data["F_bp_vn_month"].iloc[-1] if not month_data.empty else None
        )

    # F_month из F_bp_month
    if "F_bp_month" in month_data.columns:
        monthly_totals["F_month"] = _to_serializable(month_data["F_bp_month"].iloc[-1] if not month_data.empty else None)
    elif "F_month" not in monthly_totals:
        monthly_totals["F_month"] = None

    # F_tagul_month = F_bp_tagul_lpu_month + F_bp_tagul_tpu_month
    if {"F_bp_tagul_lpu_month", "F_bp_tagul_tpu_month"}.issubset(month_data.columns):
        v1 = month_data["F_bp_tagul_lpu_month"].iloc[-1] if not month_data.empty else 0
        v2 = month_data["F_bp_tagul_tpu_month"].iloc[-1] if not month_data.empty else 0
        monthly_totals["F_tagul_month"] = _to_serializable(v1 + v2)
    elif "F_tagul_month" not in monthly_totals:
        monthly_totals["F_tagul_month"] = None

    # Дополнительные месячные поля из дневных данных
    if "G_lodochny_uspv_yu" in month_data.columns:
        monthly_totals["G_lodochny_uspv_yu_month"] = _to_serializable(
            month_data["G_lodochny_uspv_yu"].sum()
        )
    if "G_buy_day" in month_data.columns:
        monthly_totals["G_buying_oil"] = _to_serializable(month_data["G_buy_day"].sum())
    if "G_out_updt_day" in month_data.columns:
        monthly_totals["G_out_udt"] = _to_serializable(month_data["G_out_updt_day"].sum())

    # ---------------------------------------------------------
    # 2. Объекты проверок (валидация)
    # ---------------------------------------------------------
    validation_checks = {
        "F_sr": _create_status_object(None, 0, ""),
        "V_vn_check": _create_status_object(None, 0, ""),
        "V_suzun_check": _create_status_object(None, 0, ""),
        "V_lodochny_check": _create_status_object(None, 0, ""),
        "V_vo_check": _create_status_object(None, 0, ""),
        "V_tagul_check": _create_status_object(None, 0, ""),
        "V_vn_gtm_check": _create_status_object(None, 0, ""),
        "V_suzun_gtm_check": _create_status_object(None, 0, ""),
        "V_vo_gtm_check": _create_status_object(None, 0, ""),
        "V_lodochny_gtm_check": _create_status_object(None, 0, ""),
        "V_tagul_gtm_check": _create_status_object(None, 0, ""),
    }
    if alarm_flag:
        validation_checks["F_sr"]["status"] = 1
        validation_checks["F_sr"]["message"] = alarm_msg or "Контрольное условие не выполнено"

    # ---------------------------------------------------------
    # 3. Данные по дням
    # ---------------------------------------------------------
    days_data: List[Dict[str, Any]] = []

    status_field_mapping = {
        "V_upsv_cps": "V_cps",
        "F_bp": "F",
        "F_bp_vn": "F_vn",
        "F_bp_suzun": "F_suzun",
        "F_bp_suzun_vankor": "F_suzun_vankor",
        "F_bp_suzun_vslu": "F_suzun_vslu",
        "F_bp_tagul": "F_tagul",
        "F_bp_tagul_lpu": "F_tagul_lpu",
        "F_bp_tagul_tpu": "F_tagul_tpu",
        "F_bp_skn": "F_skn",
        "F_bp_vo": "F_vo",
        "F_bp_kchng": "F_kchng",
    }

    status_fields = [
        "V_upsv_yu", "V_upsv_s", "V_upsv_cps", "V_lodochny_cps_upsv_yu",
        "G_sikn_tagul", "V_upn_suzun", "V_tagul", "V_upn_lodochny",
        "V_ichem", "V_gnps", "V_nps_1", "V_nps_2", "V_knps",
        "V_tstn_vn", "V_tstn_suzun", "V_tstn_suzun_vankor",
        "V_tstn_suzun_vslu", "V_tstn_tagul_obch", "V_tstn_lodochny",
        "V_tstn_tagul", "V_tstn_skn", "V_tstn_vo", "V_tstn_tng",
        "V_tstn_kchng", "F_bp", "F_bp_vn", "F_bp_suzun", "F_bp_suzun_vankor",
        "F_bp_suzun_vslu", "F_bp_tagul_lpu", "F_bp_tagul_tpu",
        "F_bp_skn", "F_bp_vo", "F_bp_kchng", "Q_gnps", "Q_nps_1_2", "Q_knps",
    ]

    regular_field_mapping = {}

    regular_fields = [
        "Q_vankor", "V_cppn_1", "G_sikn", "G_sikn_vankor", "G_sikn_suzun",
        "G_sikn_vslu", "G_sikn_tng", "delta_G_sikn", "Q_suzun", "Q_vslu",
        "V_suzun_slu", "V_suzun_vslu", "V_suzun_tng", "G_suzun",
        "G_suzun_slu", "G_suzun_vslu", "G_suzun_tng", "delta_G_suzun",
        "Q_tng", "G_payaha", "G_buy_day", "G_out_updt_day", "G_per",
        "Q_tagul", "G_tagul", "delta_G_tagul", "Q_lodochny",
        "G_lodochny_uspv_yu", "V_lodochny", "G_upn_lodochny", "G_lodochny",
        "G_ichem", "delta_G_upn_lodochny", "Q_vo", "G_upn_lodochny_ichem",
        "G_tagul_lodochny", "Q_kchng", "G_kchng", "G_skn", "G_gnps",
        "V_tstn", "V_tstn_rn_vn",
    ]

    for _, row in df.iterrows():
        day_data: Dict[str, Any] = {}
        day_data["date"] = _to_serializable(row.get("date"))

        # Обычные поля
        for field in regular_fields:
            out_field = regular_field_mapping.get(field, field)
            day_data[out_field] = _to_serializable(row[field]) if field in row else None

        # Статусные поля
        for field in status_fields:
            out_field = status_field_mapping.get(field, field)
            if out_field in day_data:
                continue
            if field in row:
                val = row[field]
            elif out_field in row:
                val = row[out_field]
            else:
                val = None
            if isinstance(val, dict):
                day_data[out_field] = _create_status_object(
                    val.get("value"),
                    val.get("status", 0),
                    val.get("message", ""),
                )
            else:
                day_data[out_field] = _create_status_object(val, 0, "")

        # F_tng / F_suzun_vslu / F_suzun_vankor — добавляем как статусные, если есть
        for f_field in ["F_tng", "F_suzun_vslu", "F_suzun_vankor"]:
            if f_field not in day_data and f_field in row:
                day_data[f_field] = _create_status_object(row[f_field], 0, "")
            elif f_field not in day_data:
                day_data[f_field] = _create_status_object(None, 0, "")

        # Производное поле F_tagul = F_tagul_lpu + F_tagul_tpu
        def _status_val(obj: Any) -> float:
            if isinstance(obj, dict):
                return obj.get("value") or 0
            return _to_serializable(obj) or 0

        f_lpu = _status_val(day_data.get("F_tagul_lpu"))
        f_tpu = _status_val(day_data.get("F_tagul_tpu"))
        day_data["F_tagul"] = _create_status_object(f_lpu + f_tpu, 0, "")

        days_data.append(day_data)

    # ---------------------------------------------------------
    # 4. Итоговая структура и сохранение
    # ---------------------------------------------------------
    # Значения на начало/конец месяца (*_0)
    init_fields = [
        "V_upsv_yu_0", "V_upsv_s_0", "V_cps_0", "V_cppn_1_0", "V_lodochny_cps_upsv_0",
        "V_upn_suzun_0", "V_suzun_slu_0", "V_suzun_vslu_0", "V_suzun_tng_0",
        "V_upn_lodochny_0", "V_lodochny_0", "V_ichem_0", "V_gnps_0", "V_nps_1_0",
        "V_nps_2_0", "V_knps_0", "V_tstn_0", "V_tstn_rn_vn_0", "V_tstn_vn_0",
        "V_tstn_suzun_0", "V_tstn_suzun_vankor_0", "V_tstn_suzun_vslu_0",
        "V_tstn_tagul_obch_0", "V_tstn_lodochny_0", "V_tstn_tagul_0",
        "V_tstn_skn_0", "V_tstn_vo_0", "V_tstn_tng_0", "V_tstn_kchng_0",
    ]
    init_values = {}
    for field in init_fields:
        if field in month_data.columns and not month_data.empty:
            init_values[field] = _to_serializable(month_data[field].iloc[-1])
        else:
            init_values[field] = None

    output = {
        **init_values,
        **monthly_totals,
        **validation_checks,
        "days": days_data,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    _safe_print(f"Результат сохранён в {output_path}")
    if alarm_flag:
        _safe_print(f"Внимание: {alarm_msg or 'Обнаружена тревога'}")

