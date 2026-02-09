import pandas as pd
from pathlib import Path
import warnings

from loader import build_all_data, get_day,load_input_json, has_missing_input_values
from update_df import update_df
from calculate import (
    prev_day_calc,
    month_calc,
    precalc_value,
    value_recalculation,
    rn_vankor_calc,
    CalculationValidationError,
    lodochny_upsv_yu_calc,
    day_zero_calc,
    availability_and_pumping_calc,
    auto_balance_volumes_calc,
    rn_vankor_balance_calc,
    availability_oil_calc,
    bp_month_calc,
    rn_vankor_check_calc,
    deviations_from_bp_calc,
    planned_balance_for_bp_vn_calc,
    planned_balance_for_bp_suzun_calc,
)

from data_prep import (
    get_prev_day_data,
    get_month_data,
    precalc_value_data,
    recalculation_data,
    vankor_data,
    lodochny_upsv_yu_data,
    get_day_zero_data,
    get_availability_and_pumping_data,
    get_auto_balance_volumes,
    get_balance_data,
    get_availability_oil_data,
    get_bp_month_data,
    get_rn_vankor_check_data,
    get_deviations_from_bp_data,
    get_planned_balance_for_bp_vn_data,
    get_planned_balance_for_bp_suzun_data
)
from export import export_to_json, export_to_excel, export_input_template
from error_handler import handle_error
from datetime import timedelta
from pandas.errors import PerformanceWarning

# Заглушка от предупреждений pandas
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Parsing dates in %Y-%m-%d format when dayfirst=True was specified.*",
)
warnings.filterwarnings("ignore", category=PerformanceWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
import calendar
input_data = load_input_json()


def _scalarize(v):
    """Приводит значение (в т.ч. dict {value,..}) к float или NaN."""
    if isinstance(v, dict):
        return _scalarize(v.get("value"))
    if v is None:
        return float("nan")
    try:
        if pd.isna(v):
            return float("nan")
    except Exception:
        pass
    try:
        return float(v)
    except Exception:
        return float("nan")


def _changed(old_v, new_v, tol=1e-9):
    """True если значения отличаются (с допуском)."""
    old_s = _scalarize(old_v)
    new_s = _scalarize(new_v)
    if pd.isna(old_s) and pd.isna(new_s):
        return False
    if pd.isna(old_s) != pd.isna(new_s):
        return True
    return abs(old_s - new_s) > tol


def build_master_df() -> pd.DataFrame:
    master_df = build_all_data()
    if "date" not in master_df.columns:
        raise ValueError("master_df не содержит колонку 'date'")
    master_df["date"] = pd.to_datetime(master_df["date"]).dt.normalize()
    return master_df


def prepare_dates_and_N(data: dict) -> tuple[list[pd.Timestamp], int, pd.Timestamp]:
    days_section = data.get("days", []) or []
    if not days_section:
        raise ValueError("Секция 'days' пуста во входном JSON: нет дат для расчёта.")
    dates = sorted(
        pd.to_datetime(item.get("date"), errors="coerce", dayfirst=True).normalize()
        for item in days_section
        if item.get("date") is not None
    )
    dates = [d for d in dates if pd.notna(d)]
    if not dates:
        raise ValueError("В секции 'days' нет корректных дат (поле 'date').")

    _year = int(dates[0].year)
    _month = int(dates[0].month)
    N = calendar.monthrange(_year, _month)[1]
    prev_month = (dates[0].replace(day=1) - timedelta(days=1)).normalize()
    return dates, N, prev_month


def stage_day_zero(master_df: pd.DataFrame, prev_month: pd.Timestamp, state: dict) -> pd.DataFrame:
    """Считает нулевые значения 1 раз и записывает в строку prev_month."""
    state["current_date"] = prev_month
    day_result = {"date": prev_month}
    day_zero = get_day_zero_data(master_df, prev_month)
    day_zero_result = day_zero_calc(**day_zero)
    day_result.update(day_zero_result)
    return update_df(master_df, day_result)


def stage_prev_day(master_df: pd.DataFrame, dates: list[pd.Timestamp], state: dict) -> pd.DataFrame:
    for n in dates:
        state["current_date"] = n
        day_result = {"date": n}
        prev_day = n - timedelta(days=1)
        prev_day_data = get_prev_day_data(master_df, prev_day)
        prev_day_result = prev_day_calc(**prev_day_data)
        day_result.update(prev_day_result)
        master_df = update_df(master_df, day_result)
    return master_df


def stage_lodochny_upsv_yu(master_df: pd.DataFrame, dates: list[pd.Timestamp], N: int, state: dict) -> pd.DataFrame:
    for n in dates:
        state["current_date"] = n
        day_result = {"date": n}
        prev_day = n - timedelta(days=1)
        day = n.day
        month = n.month
        payload = lodochny_upsv_yu_data(master_df, n, prev_day, day, N, month)
        result = lodochny_upsv_yu_calc(**payload)
        day_result.update(result)
        master_df = update_df(master_df, day_result)
    return master_df


def stage_precalc(master_df: pd.DataFrame, dates: list[pd.Timestamp], N: int, state: dict) -> pd.DataFrame:
    for n in dates:
        state["current_date"] = n
        day_result = {"date": n}
        prev_day = n - timedelta(days=1)
        day = n.day
        payload = precalc_value_data(master_df, n, prev_day, N, day)
        result = precalc_value(**payload)
        day_result.update(result)
        master_df = update_df(master_df, day_result)
    return master_df


def stage_value_recalculation(
    master_df: pd.DataFrame,
    dates: list[pd.Timestamp],
    N: int,
    prev_month: pd.Timestamp,
    state: dict,
    start_from: pd.Timestamp | None = None,
) -> pd.DataFrame:
    for n in dates:
        if start_from is not None and n < start_from:
            continue
        state["current_date"] = n
        day_result = {"date": n}
        prev_day = n - timedelta(days=1)
        payload = recalculation_data(master_df, n, prev_day, N, prev_month)
        result = value_recalculation(**payload)
        day_result.update(result)
        master_df = update_df(master_df, day_result)
    return master_df


def stage_rn_vankor(master_df: pd.DataFrame, dates: list[pd.Timestamp], N: int, state: dict) -> pd.DataFrame:
    for n in dates:
        state["current_date"] = n
        day_result = {"date": n}
        day = n.day
        prev_day = n - timedelta(days=1)
        payload = vankor_data(master_df, n, N, day,prev_day)
        result = rn_vankor_calc(**payload)
        day_result.update(result)
        master_df = update_df(master_df, day_result)
    return master_df


def stage_availability_and_pumping(master_df: pd.DataFrame, dates: list[pd.Timestamp], N: int, state: dict) -> pd.DataFrame:
    for n in dates:
        state["current_date"] = n
        day_result = {"date": n}
        month = n.month
        prev_day = n - timedelta(days=1)
        payload = get_availability_and_pumping_data(master_df, n, N, month, prev_day)
        result = availability_and_pumping_calc(**payload)
        day_result.update(result)
        master_df = update_df(master_df, day_result)
    return master_df


def stage_month_calc(master_df: pd.DataFrame, dates: list[pd.Timestamp], state: dict, N: int) -> pd.DataFrame:

    last_date = max(dates)
    state["current_date"] = last_date
    month = int(last_date.month)
    day = int(last_date.day)
    state["current_day"] = day
    
    payload = get_month_data(master_df, month, N, day)
    result = month_calc(**payload)
    master_df = update_df(master_df, {"date": last_date, **result})
    return master_df


def stage_auto_balance_volumes(
    master_df: pd.DataFrame,
    dates: list[pd.Timestamp],
    N: int,
    prev_month: pd.Timestamp,
    state: dict,
) -> tuple[pd.DataFrame, pd.Timestamp | None]:
    """
    Применяет autobalance. Возвращает (master_df, earliest_change_date) —
    earliest_change_date нужна, чтобы при изменении ключевых объёмов сделать пересчёт value_recalculation.
    """
    earliest_change = None
    keys = ["V_upn_suzun", "V_upn_lodochny", "V_upsv_yu", "V_upsv_s", "V_cps"]

    for n in dates:
        state["current_date"] = n
        day_result = {"date": n}
        prev_day = n - timedelta(days=1)

        old_row = master_df.loc[master_df["date"] == n]
        old_vals = {}
        if not old_row.empty:
            for k in keys:
                old_vals[k] = old_row.iloc[0][k] if k in old_row.columns else float("nan")
        else:
            for k in keys:
                old_vals[k] = float("nan")

        payload = get_auto_balance_volumes(master_df, n, prev_day, N, prev_month)
        result = auto_balance_volumes_calc(**payload)
        day_result.update(result)
        master_df = update_df(master_df, day_result)

        for k in keys:
            if k in result and _changed(old_vals.get(k), result.get(k)):
                if earliest_change is None or n < earliest_change:
                    earliest_change = n
                break

    return master_df, earliest_change


def stage_availability_oil(master_df: pd.DataFrame, dates: list[pd.Timestamp], state: dict) -> pd.DataFrame:
    """Суточные остатки (использует уже скорректированные F_bp_* / F_* для дня n)."""
    for n in dates:
        state["current_date"] = n
        prev_day = n - timedelta(days=1)
        availability_payload = get_availability_oil_data(master_df, n, prev_day)
        availability_result = availability_oil_calc(**availability_payload)
        master_df = update_df(master_df, {"date": n, **availability_result})
    return master_df


def stage_balance_calc(master_df: pd.DataFrame, dates: list[pd.Timestamp], state: dict) -> pd.DataFrame:
    """
    1) Корректирует F_bp_* через rn_vankor_balance_calc (пишет F_* как dict + обновляет F_bp_* числами).
    2) Считает суточные остатки через availability_oil_calc (нужны для prev_day следующего дня).
    """
    for n in dates:
        state["current_date"] = n
        prev_day = n - timedelta(days=1)

        # Балансировка (обновляет F_bp_* для дня n)
        balance_payload = get_balance_data(master_df, n, prev_day)
        balance_result = rn_vankor_balance_calc(**balance_payload)
        master_df = update_df(master_df, {"date": n, **balance_result})

        # Суточные остатки (использует уже скорректированные F_bp_*)
        

    return master_df


def stage_bp_month_calc(master_df: pd.DataFrame, dates: list[pd.Timestamp], state: dict) -> pd.DataFrame:
    """Считает месячные суммы F_* и пишет их на последний день месяца."""
    if not dates:
        return master_df
    last_date = max(dates)
    state["current_date"] = last_date
    month = int(last_date.month)
    payload = get_bp_month_data(master_df, month)
    result = bp_month_calc(**payload)
    master_df = update_df(master_df, {"date": last_date, **result})
    return master_df

def stage_rn_vankor_check(master_df: pd.DataFrame, dates: list[pd.Timestamp], state: dict) -> pd.DataFrame:
    """Проверки ограничений/режимов (calculate.rn_vankor_check) по каждому дню."""
    for n in dates:
        state["current_date"] = n
        prev_day = n - timedelta(days=1)
        check_payload = get_rn_vankor_check_data(master_df, n, prev_day)
        check_result = rn_vankor_check_calc(**check_payload)
        master_df = update_df(master_df, {"date": n, **check_result})
    return master_df

def stage_deviations_from_bp(master_df: pd.DataFrame, dates: list[pd.Timestamp]) -> pd.DataFrame:
    last_date = max(dates)
    month = int(last_date.month)
    payload = get_deviations_from_bp_data(master_df, month)
    result = deviations_from_bp_calc(**payload)
    master_df = update_df(master_df, {"date": last_date, **result})
    return master_df

def stage_planned_balance_for_bp_vn(master_df: pd.DataFrame, dates: list[pd.Timestamp]) -> pd.DataFrame:
    last_date = max(dates)
    payload = get_planned_balance_for_bp_vn_data(master_df)
    result = planned_balance_for_bp_vn_calc(**payload)
    master_df = update_df(master_df, {"date": last_date, **result})
    return master_df

def stage_planned_balance_for_suzun_vn(master_df: pd.DataFrame, dates: list[pd.Timestamp]) -> pd.DataFrame:
    last_date = max(dates)
    payload = get_planned_balance_for_bp_suzun_data(master_df)
    result = planned_balance_for_bp_suzun_calc(**payload)
    master_df = update_df(master_df, {"date": last_date, **result})
    return master_df

def main():
    state = {"current_date": None}
    try:

        master_df = build_master_df()
        dates, N, prev_month = prepare_dates_and_N(input_data)

        master_df = stage_day_zero(master_df, prev_month, state)
        master_df = stage_prev_day(master_df, dates, state)
        master_df = stage_lodochny_upsv_yu(master_df, dates, N, state)
        master_df = stage_precalc(master_df, dates, N, state)
        master_df = stage_value_recalculation(master_df, dates, N, prev_month, state)
        master_df = stage_rn_vankor(master_df, dates, N, state)
        master_df = stage_availability_and_pumping(master_df, dates, N, state)
        master_df = stage_month_calc(master_df, dates, state,N)
        master_df, earliest_change = stage_auto_balance_volumes(master_df, dates, N, prev_month, state)
       
        # Если autobalance изменил ключевые объёмы — пересчитываем зависимые блоки заново
        # (value_recalculation и далее), чтобы все показатели соответствовали новым V_upn_*.
        if earliest_change is not None:
            # 1) пересчёт дневных балансов с даты первого изменения
            master_df = stage_value_recalculation(
                master_df,
                dates,
                N,
                prev_month,
                state,
                start_from=earliest_change,
            )

            # 2) availability_and_pumping зависит от месячной суммы G_gpns_i,
            # поэтому безопаснее пересчитать его для всего месяца
            master_df = stage_availability_and_pumping(master_df, dates, N, state)

            # 3) пересчёт месячных сумм и баланса/остатков
            master_df = stage_month_calc(master_df, dates, state, N)

        # Баланс + суточные остатки нужно считать последовательно по дням:
        # баланс дня n зависит от остатков prev_day, которые появляются после расчёта availability для prev_day.
        for n in dates:
            master_df = stage_balance_calc(master_df, [n], state)
            master_df = stage_availability_oil(master_df, [n], state)

        master_df = stage_bp_month_calc(master_df, dates, state)
        master_df = stage_rn_vankor_check(master_df, dates, state)
        master_df = stage_deviations_from_bp(master_df, dates)
        master_df = stage_planned_balance_for_bp_vn(master_df, dates)
        master_df = stage_planned_balance_for_suzun_vn(master_df, dates)
        # Экспорт результата
        result = export_to_json(master_df)  # dict в памяти, файл НЕ создаётся
        export_to_excel()
        return result
    except CalculationValidationError as e:
        return handle_error(
            {
                "type": "CalculationValidationError",
                "message": str(e),
                "date": str(state["current_date"]) if state.get("current_date") is not None else None,
            }
        )
    except Exception as e:
        error_result = handle_error(
            {
                "type": type(e).__name__,
                "message": str(e),
                "date": str(state["current_date"]) if state.get("current_date") is not None else None,
            }
        )
        raise

if __name__ == "__main__":
    main()