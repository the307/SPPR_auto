import numpy as np
import pandas as pd



# модуль собирает все значения из master_df и формирует словари,
# которые соответствуют аргументам оригинального main.py → calculate.*

# -------------------------
# Вспомогательные функции для получения данных
# -------------------------

def _get_month_values(master_df, column_name, month):
    """Получает значения колонки за указанный месяц."""
    if column_name not in master_df.columns:
        return np.array([], dtype=float)
    return master_df.loc[master_df["date"].dt.month == month, column_name].values

def _get_const(master_df, column_name, default=0.0):
    """Возвращает константу из master_df (первое валидное значение столбца)."""
    if column_name not in master_df.columns:
        return default
    series = master_df[column_name].dropna()
    if series.empty:
        return default
    return _to_scalar(series.values)


def _to_scalar(val):
    """Безопасно извлекает скаляр из массива/списка/скаляра."""
    if isinstance(val, (list, np.ndarray)):
        if len(val) == 0:
            return 0.0
        return float(val[0])
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _get_day_value(master_df, column_name, date, *, scalar: bool = True):
    """Получает значение колонки за указанный день. По умолчанию возвращает скаляр."""
    if column_name not in master_df.columns:
        return 0.0 if scalar else np.array([], dtype=float)
    target_date = pd.to_datetime(date, errors="coerce").normalize()
    values = master_df.loc[master_df["date"] == target_date, column_name].values
    return _to_scalar(values) if scalar else values


def prepare_suzun_data(master_df, n, m, prev_days, prev_month, N):
    """Собирает все аргументы, которые в оригинале передавались в calculate.suzun."""
    # --- Покупка и отгрузка ---
    G_buy_month = float(np.nansum(_get_month_values(master_df, "G_buy_day", m)))
    G_out_udt_month = float(np.nansum(_get_month_values(master_df, "G_out_updt_day", m)))
    # --- GTM данные ---
    Q_vankor = float(np.nansum(_get_month_values(master_df, "Q_vankor", m)))
    Q_suzun = float(np.nansum(_get_month_values(master_df, "Q_suzun", m)))
    Q_vslu = float(np.nansum(_get_month_values(master_df, "Q_vslu", m)))
    Q_tng = float(np.nansum(_get_month_values(master_df, "Q_tng", m)))
    Q_vo = float(np.nansum(_get_month_values(master_df, "Q_vo", m)))
    # --- Данные за текущий день ---
    Q_vslu_day = _get_day_value(master_df, "Q_vslu", n, scalar=True)
    Q_suzun_day = _get_day_value(master_df, "Q_suzun", n, scalar=True)
    # --- Предыдущий день ---
    V_suzun_tng_prev = _get_day_value(master_df, "V_suzun_tng", prev_days, scalar=True)
    V_upn_suzun_prev = _get_day_value(master_df, "V_upn_suzun", prev_days, scalar=True)
    V_suzun_vslu_prev = _get_day_value(master_df, "V_suzun_vslu", prev_days, scalar=True)
    V_suzun_slu_prev = _get_day_value(master_df, "V_suzun_slu", prev_days, scalar=True)
    G_per_month_prev = _get_day_value(master_df, "G_per_month", prev_days, scalar=True)
    G_suzun_vslu_month_prev = _get_day_value(master_df, "G_suzun_vslu_month", prev_days, scalar=True)
    G_suzun_slu_month_prev = _get_day_value(master_df, "G_suzun_slu_month", prev_days, scalar=True)
    G_suzun_month_prev = _get_day_value(master_df, "G_suzun_month", prev_days, scalar=True)
    # --- Конец прошлого месяца ---
    V_suzun_tng_0 = _get_const(master_df, "V_suzun_tng_0")
    V_upn_suzun_0 = _get_const(master_df, "V_upn_suzun_0")
    V_suzun_vslu_0 = _get_const(master_df, "V_suzun_vslu_0")
    

    return {
        "G_buy_month":G_buy_month,
        "G_out_udt_month":G_out_udt_month,
        "N":N,
        "Q_vankor":Q_vankor,
        "Q_suzun":Q_suzun,
        "Q_vslu":Q_vslu,
        "Q_tng":Q_tng,
        "Q_vo":Q_vo,
        "V_suzun_tng_prev":V_suzun_tng_prev,
        "Q_vslu_day":Q_vslu_day,
        "V_upn_suzun_prev":V_upn_suzun_prev,
        "V_suzun_vslu_prev":V_suzun_vslu_prev,
        "Q_suzun_day":Q_suzun_day,
        "V_upn_suzun_0":V_upn_suzun_0,
        "V_suzun_vslu_0":V_suzun_vslu_0,
        "V_suzun_tng_0":V_suzun_tng_0,
        "V_suzun_slu_prev":V_suzun_slu_prev,
        "G_per_month_prev": G_per_month_prev,
        "G_suzun_vslu_month_prev": G_suzun_vslu_month_prev,
        "G_suzun_slu_month_prev": G_suzun_slu_month_prev,
        "G_suzun_month_prev": G_suzun_month_prev,

    }


def prepare_vo_data(master_df, n, prev_day):
    Q_vo_day = _get_day_value(master_df, "Q_vo", n, scalar=True)
    G_upn_lodochny_ichem_month_prev = _get_day_value(
        master_df, "G_upn_lodochny_ichem_month", prev_day, scalar=True
    )

    return {
        "Q_vo_day": Q_vo_day,
        "G_upn_lodochny_ichem_month_prev": G_upn_lodochny_ichem_month_prev,
    }


def prepare_kchng_data(master_df, n, m, prev_day):
    Q_kchng = _get_month_values(master_df, "Q_kchng", m)
    Q_kchng_day = _get_day_value(master_df, "Q_kchng", n, scalar=True)
    G_kchng_month_prev = _get_day_value(master_df, "G_kchng_month", prev_day, scalar=True)

    return {
        "Q_kchng_day": Q_kchng_day,
        "Q_kchng": Q_kchng,
        "G_kchng_month_prev": G_kchng_month_prev,
    }


def prepare_lodochny_data(master_df, n, m, prev_days, prev_month, N, day, kchng_results):
    Q_tagulsk = _get_month_values(master_df, "Q_tagul", m)
    Q_lodochny = _get_month_values(master_df, "Q_lodochny", m)
    Q_lodochny_day = _get_day_value(master_df, "Q_lodochny", n, scalar=True)
    Q_tagulsk_day = _get_day_value(master_df, "Q_tagul", n, scalar=True)
    V_upn_lodochny_prev = _get_day_value(master_df, "V_upn_lodochny", prev_days, scalar=True)
    V_ichem_prev = _get_day_value(master_df, "V_ichem", prev_days, scalar=True)
    G_lodochny_ichem = _get_day_value(master_df, "G_upn_lodochny_ichem", n, scalar=True)
    V_tagul_prev = _get_day_value(master_df, "V_tagul", prev_days, scalar=True)
    G_lodochny_uspv_yu_month_prev = _get_day_value(master_df, "G_lodochny_uspv_yu_month", prev_days, scalar=True)
    G_sikn_tagul_month_prev = _get_day_value(master_df, "G_sikn_tagul_month", prev_days, scalar=True)
    G_tagul_month_prev = _get_day_value(master_df, "G_tagul_month", prev_days, scalar=True)
    delta_G_tagul_month_prev = _get_day_value(master_df, "delta_G_tagul_month", prev_days, scalar=True)
    G_lodochny_month_prev = _get_day_value(master_df, "G_lodochny_month", prev_days, scalar=True)
    delte_G_upn_lodochny_month_prev = _get_day_value(master_df, "delte_G_upn_lodochny_month", prev_days, scalar=True)
    G_tagul_lodochny_month_prev = _get_day_value(master_df, "G_tagul_lodochny_month", prev_days, scalar=True)


    return {
        "Q_tagul": Q_tagulsk,
        "Q_lodochny": Q_lodochny,
        "V_upn_lodochny_prev": V_upn_lodochny_prev,
        "V_ichem_prev": V_ichem_prev,
        "G_lodochny_ichem": G_lodochny_ichem,
        "N": N,
        "Q_vo_day": _get_day_value(master_df, "Q_vo", n, scalar=True),
        "Q_lodochny_day": Q_lodochny_day,
        "Q_tagul_day": Q_tagulsk_day,
        "V_tagul_prev": V_tagul_prev,
        "G_kchng": kchng_results.get("G_kchng", 0),
        "day": day,
        "G_lodochny_uspv_yu_month_prev": G_lodochny_uspv_yu_month_prev,
        "G_sikn_tagul_month_prev": G_sikn_tagul_month_prev,
        "G_tagul_month_prev": G_tagul_month_prev,
        "delta_G_tagul_month_prev": delta_G_tagul_month_prev,
        "G_lodochny_month_prev": G_lodochny_month_prev,
        "delte_G_upn_lodochny_month_prev": delte_G_upn_lodochny_month_prev,
        "G_tagul_lodochny_month_prev": G_tagul_lodochny_month_prev,
    }


def prepare_cppn1_data(master_df, n, prev_days,  lodochny_results):
    flag_list = [0, 0, 0]  # Для отслеживания остановки
    V_upsv_yu_0 = _get_const(master_df, "V_upsv_yu_0")
    V_upsv_s_0 = _get_const(master_df, "V_upsv_s_0")
    V_upsv_cps_0 = _get_const(master_df, "V_cps_0")
    V_upsv_yu_prev = _get_day_value(master_df, "V_upsv_yu", prev_days, scalar = True)
    V_upsv_s_prev = _get_day_value(master_df, "V_upsv_s", prev_days, scalar = True)
    V_cps_prev = _get_day_value(master_df, "V_cps", prev_days, scalar = True)
    V_lodochny_cps_upsv_yu_prev = _get_day_value(master_df, "V_lodochny_cps_upsv_yu", prev_days, scalar=True)
    return {
        "V_upsv_yu_prev":V_upsv_yu_prev,
        "V_upsv_s_prev":V_upsv_s_prev,
        "V_cps_prev":V_cps_prev,
        "V_upsv_yu_0":V_upsv_yu_0,
        "V_upsv_s_0":V_upsv_s_0,
        "V_upsv_cps_0":V_upsv_cps_0,
        "V_lodochny_cps_upsv_yu_prev":V_lodochny_cps_upsv_yu_prev,
        "G_sikn_tagul":lodochny_results.get("G_sikn_tagul"),
        "G_lodochny_uspv_yu":lodochny_results.get("G_lodochny_uspv_yu"),
        "flag_list":flag_list
    }


def prepare_rn_vankor_data(master_df, n, prev_days, N, day, m):
    F_vn = _get_day_value(master_df, "F_vn", n, scalar=True)
    F_suzun_obsh = _get_day_value(master_df, "F_suzun", n, scalar=True)
    F_suzun_vankor = _get_day_value(master_df, "F_suzun_vankor", n, scalar=True)
    F_bp_data = _get_month_values(master_df, "F_bp", m).tolist()
    V_tstn_suzun_vslu_norm = _get_const(master_df, "V_tstn_suzun_vslu_norm")
    V_tstn_suzun_vslu = _get_day_value(master_df, "V_tstn_suzun_vslu", n, scalar=True)
    F_tagul_lpu = _get_day_value(master_df, "F_tagul_lpu", n, scalar=True)
    F_tagul_tpu = _get_day_value(master_df, "F_tagul_tpu", n, scalar=True)
    F_skn = _get_day_value(master_df, "F_skn", n, scalar=True)
    F_vo = _get_day_value(master_df, "F_vo", n, scalar=True)
    F_kchng = _get_day_value(master_df, "F_kchng", n, scalar=True)
    e_suzun_vankor = _get_day_value(master_df, "e_suzun_vankor", n, scalar=True)
    e_vo = _get_day_value(master_df, "e_vo", n, scalar=True)     
    e_tng = _get_day_value(master_df, "e_tng", n, scalar=True)         
    e_kchng = _get_day_value(master_df, "e_kchng", n, scalar=True)         
    F_tng = _get_day_value(master_df, "F_tng", n, scalar=True)        
    F_bp_vn_month_prev = _get_day_value(master_df, "F_bp_vn_month", prev_days, scalar=True)
    F_bp_suzun_month_prev = _get_day_value(master_df, "F_bp_suzun_month", prev_days, scalar=True)
    F_bp_suzun_vankor_month_prev = _get_day_value(master_df, "F_bp_suzun_vankor_month", prev_days, scalar=True)
    F_bp_suzun_vslu_month_prev = _get_day_value(master_df, "F_bp_suzun_vslu_month", prev_days, scalar=True)
    F_bp_tagul_lpu_month_prev = _get_day_value(master_df, "F_bp_tagul_lpu_month", prev_days, scalar=True)
    F_bp_tagul_tpu_month_prev = _get_day_value(master_df, "F_bp_tagul_tpu_month", prev_days, scalar=True)
    F_bp_tagul_month_prev = _get_day_value(master_df, "F_bp_tagul_month", prev_days, scalar=True)
    F_bp_skn_month_prev = _get_day_value(master_df, "F_bp_skn_month", prev_days, scalar=True)
    F_bp_vo_month_prev = _get_day_value(master_df, "F_bp_vo_month", prev_days, scalar=True)
    F_bp_tng_month_prev = _get_day_value(master_df, "F_bp_tng_month", prev_days, scalar=True)
    F_bp_kchng_month_prev = _get_day_value(master_df, "F_bp_kchng_month", prev_days, scalar=True)
    F_bp_month_prev = _get_day_value(master_df, "F_bp_month", prev_days, scalar=True)


    return {
        "F_vn": F_vn,
        "F_suzun_obsh": F_suzun_obsh,
        "F_suzun_vankor": F_suzun_vankor,
        "N": N,
        "day": day,
        "F_bp_data": F_bp_data,
        "V_tstn_suzun_vslu_norm": V_tstn_suzun_vslu_norm,
        "V_tstn_suzun_vslu": V_tstn_suzun_vslu,
        "F_tagul_lpu": F_tagul_lpu,
        "F_tagul_tpu": F_tagul_tpu,
        "F_skn": F_skn,
        "F_vo": F_vo,
        "F_kchng": F_kchng,
        "e_suzun_vankor": e_suzun_vankor,
        "e_vo": e_vo,
        "e_tng": e_tng,
        "e_kchng": e_kchng,
        "F_tng": F_tng,
        "F_bp_vn_month_prev": F_bp_vn_month_prev,
        "F_bp_suzun_month_prev": F_bp_suzun_month_prev,
        "F_bp_suzun_vankor_month_prev": F_bp_suzun_vankor_month_prev,
        "F_bp_suzun_vslu_month_prev": F_bp_suzun_vslu_month_prev,
        "F_bp_tagul_lpu_month_prev": F_bp_tagul_lpu_month_prev,
        "F_bp_tagul_tpu_month_prev": F_bp_tagul_tpu_month_prev,
        "F_bp_tagul_month_prev": F_bp_tagul_month_prev,
        "F_bp_skn_month_prev": F_bp_skn_month_prev,
        "F_bp_vo_month_prev": F_bp_vo_month_prev,
        "F_bp_tng_month_prev": F_bp_tng_month_prev,
        "F_bp_kchng_month_prev": F_bp_kchng_month_prev,
        "F_bp_month_prev": F_bp_month_prev,

    }
def prepare_sikn_1208_data(master_df, n, prev_day, suzun_results, lodochny_results, G_suzun_tng, cppn1_results):


    Q_vankor = _get_day_value(master_df, "Q_vankor", n, scalar=True)
    V_upsv_yu_prev = _get_day_value(master_df, "V_upsv_yu", prev_day, scalar=True)
    V_upsv_s_prev = _get_day_value(master_df, "V_upsv_s", prev_day, scalar=True)
    V_upsv_cps_prev = _get_day_value(master_df, "V_cps", prev_day, scalar=True)
    V_cppn_1_prev = _get_day_value(master_df,"V_cppn_1", prev_day, scalar=True)
    G_sikn_vslu_month_prev = _get_day_value(master_df, "G_sikn_vslu_month", prev_day, scalar=True)
    G_sikn_tagul_month_prev = _get_day_value(master_df, "G_sikn_tagul_month", prev_day, scalar=True)
    G_sikn_suzun_month_prev = _get_day_value(master_df, "G_sikn_suzun_month", prev_day, scalar=True)
    G_sikn_tng_month_prev = _get_day_value(master_df, "G_sikn_tng_month", prev_day, scalar=True)
    G_sikn_month_prev = _get_day_value(master_df, "G_sikn_month", prev_day, scalar=True)
    G_sikn_vankor_month_prev = _get_day_value(master_df, "G_sikn_vankor_month", prev_day, scalar=True)
    G_skn_month_prev = _get_day_value(master_df, "G_skn_month", prev_day, scalar=True)
    delta_G_sikn_month_prev = _get_day_value(master_df, "delta_G_sikn_month", prev_day, scalar=True)
    return {
        "G_suzun_vslu": _to_scalar(suzun_results.get("G_suzun_vslu")),
        "G_buy_day": _to_scalar(suzun_results.get("G_buy_day")),
        "G_per": _to_scalar(suzun_results.get("G_per")),
        "G_suzun": _to_scalar(suzun_results.get("G_suzun")),
        "G_suzun_tng": G_suzun_tng,
        "Q_vankor": Q_vankor,
        "V_upsv_yu": _to_scalar(cppn1_results.get("V_upsv_yu")),
        "V_upsv_s": _to_scalar(cppn1_results.get("V_upsv_s")),
        "V_upsv_cps": _to_scalar(cppn1_results.get("V_cps")),
        "V_upsv_yu_prev": V_upsv_yu_prev,
        "V_upsv_s_prev": V_upsv_s_prev,
        "V_upsv_cps_prev": V_upsv_cps_prev,
        "G_lodochny_uspv_yu": lodochny_results.get("G_lodochny_uspv_yu"),
        "V_cppn_1": cppn1_results.get("V_cppn_1"),
        "G_sikn_tagul": lodochny_results.get("G_sikn_tagul"),
        "V_cppn_1_prev":V_cppn_1_prev
        ,
        "G_sikn_vslu_month_prev": G_sikn_vslu_month_prev,
        "G_sikn_tagul_month_prev": G_sikn_tagul_month_prev,
        "G_sikn_suzun_month_prev": G_sikn_suzun_month_prev,
        "G_sikn_tng_month_prev": G_sikn_tng_month_prev,
        "G_sikn_month_prev": G_sikn_month_prev,
        "G_sikn_vankor_month_prev": G_sikn_vankor_month_prev,
        "G_skn_month_prev": G_skn_month_prev,
        "delta_G_sikn_month_prev": delta_G_sikn_month_prev
    }

def rn_vankor_auto_balance_data(master_df, n,prev_day, N, rn_results, suzun_results, tstn_inputs, tstn_results,lodochny_results,kchng_results,G_ichem,G_suzun_tng):
    V_upn_suzun_prev = _get_day_value(master_df, "V_upn_suzun", prev_day, scalar = True)
    V_upn_suzun_0 = _get_const(master_df,"V_upn_suzun_0")
    VN_upn_suzun_min = _get_const(master_df,"VN_upn_suzun_min")
    V_upn_lodochny_prev = _get_day_value(master_df, "V_upn_lodochny", prev_day, scalar = True)
    V_upn_lodochny_0 = _get_const(master_df,"V_upn_lodochny_0")
    VN_upn_lodochny_min = _get_const(master_df,"VN_upn_lodochny_min")
    V_upsv_yu_0 = _get_const(master_df, "V_upsv_yu_0")
    VN_upsv_yu_min = _get_const(master_df, "VN_upsv_yu_min")
    V_upsv_yu_prev = _get_day_value(master_df, "V_upsv_yu", prev_day, scalar = True)
    V_upsv_s_0 = _get_const(master_df, "V_upsv_s_0")
    VN_upsv_s_min = _get_const(master_df, "V_upsv_min")
    V_upsv_s_prev = _get_day_value(master_df, "V_upsv_s", prev_day, scalar = True)
    V_cps_0 = _get_const(master_df, "V_cps_0")
    V_cps_prev = _get_day_value(master_df, "V_cps", prev_day, scalar = True)
    VN_cps_min = _get_const(master_df,"VN_cps_min")
    V_tstn_suzun_prev = _get_day_value(master_df,"V_tstn_suzun",prev_day,scalar = True)
    V_knps_prev = _get_day_value(master_df,"V_knps",prev_day,scalar=True)
    V_nps_1_prev = _get_day_value(master_df,"V_nps_1",prev_day,scalar=True)
    V_nps_2_prev = _get_day_value(master_df, "V_nps_2",prev_day,scalar=True)
    VN_knps_min = _get_const(master_df,"VN_knps_min")
    V_tstn_norm_suzun = _get_const(master_df,"V_tstn_norm_suzun")
    flag_sost = _get_const(master_df,"flag_sost")
    F_suzun_vankor = _get_day_value(master_df,"F_suzun_vankor",n,scalar=True)
    V_tstn_suzun_vankor_prev = _get_day_value(master_df,"V_tstn_suzun_vankor",prev_day,scalar=True)
    V_tstn_norm_suzun_vankor = _get_const(master_df,"V_tstn_norm_suzun_vankor")
    V_tstn_norm_lodochny = _get_const(master_df,"V_tstn_norm_lodochny")
    V_tstn_lodochny_prev = _get_day_value(master_df,"V_tstn_lodochny",prev_day,scalar=True)
    V_tstn_norm_tagul = _get_const(master_df,"V_tstn_norm_tagul")
    V_tstn_tagul_prev = _get_day_value(master_df,"V_tstn_tagul",prev_day,scalar=True)
    V_tstn_norm_skn = _get_const(master_df,"V_tstn_norm_skn")
    V_tstn_skn_prev = _get_day_value(master_df,"V_tstn_skn",prev_day,scalar=True)
    V_tstn_norm_vo = _get_const(master_df,"V_tstn_norm_vo")
    V_tstn_vo_prev = _get_day_value(master_df,"V_tstn_vo",prev_day,scalar=True)
    V_tstn_norm_tng = _get_const(master_df,"V_tstn_norm_tng")
    V_tstn_tng_prev = _get_day_value(master_df, "V_tstn_tng",prev_day,scalar=True)
    V_tstn_norm_kchng = _get_const(master_df,"V_tstn_norm_kchng")
    V_tstn_kchng_prev = _get_day_value(master_df,"V_tstn_kchng",prev_day,scalar=True)
    V_tstn_norm_vn = _get_const(master_df,"V_tstn_norm_vn")
    G_buy_month = float(np.nansum(_get_month_values(master_df, "G_buy_day", n.month)))
    return{
        "N":N, "F_bp_tagul_lpu":rn_results.get("F_bp_tagul_lpu"),
        "F_bp_tagul_tpu":rn_results.get("F_bp_tagul_tpu"), "F_bp_suzun_vankor":rn_results.get("F_bp_suzun_vankor"), "F_bp_suzun_vslu":rn_results.get("F_bp_suzun_vslu"),
        "F_bp_skn":rn_results.get("F_bp_skn"), "F_bp_vo":rn_results.get("F_bp_vo"), "F_bp_tng":rn_results.get("F_bp_tng"),
        "F_bp_kchng":rn_results.get("F_bp_kchng"), "F_bp_suzun":rn_results.get("F_bp_suzun"), "F_bp_vn":rn_results.get("F_bp_vn"), "G_suzun_slu":_to_scalar(suzun_results.get("G_suzun_slu")),
        "K_suzun":tstn_inputs.get("K_suzun"), "K_vankor":tstn_inputs.get("K_vankor"), "G_gnps":tstn_results.get("G_gnps"), "G_tagul":lodochny_results.get("G_tagul"),
        "G_upn_lodochny":lodochny_results.get("G_upn_lodochny"), "G_skn":tstn_inputs.get("G_skn"), "G_kchng":kchng_results.get("G_kchng"), "V_nps_1":tstn_results.get("V_nps_1"),
        "V_nps_2":tstn_results.get("V_nps_2"), "G_buy_day":_to_scalar(suzun_results.get("G_buy_day")), "G_per":_to_scalar(suzun_results.get("G_per")), "G_sikn_tagul":lodochny_results.get("G_sikn_tagul"),
        "G_lodochny":lodochny_results.get("G_lodochny"),"K_lodochny":tstn_inputs.get("K_lodochny"), "K_tagul":tstn_inputs.get("K_tagul"), "K_skn":tstn_inputs.get("K_skn"),
        "K_ichem":tstn_inputs.get("K_ichem"), "G_ichem":G_ichem,"G_suzun_tng":G_suzun_tng,"K_payaha":tstn_inputs.get("K_payaha"), "V_gnps":tstn_results.get("V_gnps"),"V_tstn_rn_vn":tstn_results.get("V_tstn_rn_vn"),
        "V_tstn_tagul_obch":tstn_results.get("V_tstn_tagul_obch"),"V_tstn_suzun_vslu":tstn_results.get("V_tstn_suzun_vslu"),"V_upn_suzun_prev":V_upn_suzun_prev,
        "V_upn_suzun_0":V_upn_suzun_0,"VN_upn_suzun_min":VN_upn_suzun_min,"V_upn_lodochny_prev":V_upn_lodochny_prev,"V_upn_lodochny_0":V_upn_lodochny_0,
        "VN_upn_lodochny_min":VN_upn_lodochny_min,"V_upsv_yu_prev":V_upsv_yu_prev,"V_upsv_yu_0":V_upsv_yu_0,"VN_upsv_yu_min":VN_upsv_yu_min,"V_upsv_s_prev":V_upsv_s_prev,
        "V_upsv_s_0":V_upsv_s_0, "VN_upsv_s_min":VN_upsv_s_min,"V_cps_prev":V_cps_prev,"V_cps_0":V_cps_0,"VN_cps_min":VN_cps_min,"V_tstn_suzun_prev":V_tstn_suzun_prev,
        "V_knps_prev":V_knps_prev, "V_nps_1_prev":V_nps_1_prev, "V_nps_2_prev":V_nps_2_prev,"VN_knps_min":VN_knps_min,"V_tstn_norm_suzun":V_tstn_norm_suzun,
        "flag_sost":flag_sost,"V_tstn_suzun_vankor_prev":V_tstn_suzun_vankor_prev,"V_tstn_norm_suzun_vankor":V_tstn_norm_suzun_vankor,
        "V_tstn_norm_lodochny":V_tstn_norm_lodochny,"V_tstn_lodochny_prev":V_tstn_lodochny_prev,"V_tstn_norm_tagul":V_tstn_norm_tagul,"V_tstn_tagul_prev":V_tstn_tagul_prev,
        "V_tstn_norm_skn":V_tstn_norm_skn,"V_tstn_skn_prev":V_tstn_skn_prev, "V_tstn_norm_vo":V_tstn_norm_vo, "V_tstn_vo_prev":V_tstn_vo_prev,"V_tstn_norm_tng":V_tstn_norm_tng,
        "V_tstn_tng_prev":V_tstn_tng_prev, "V_tstn_norm_kchng":V_tstn_norm_kchng, "V_tstn_kchng_prev":V_tstn_kchng_prev, "V_tstn_norm_vn":V_tstn_norm_vn,"V_tstn_suzun_vankor":tstn_results.get("V_tstn_suzun_vankor")
    }

def prepare_tstn_data(master_df, N, prev_day, sikn_1208_results, lodochny_results, kchng_results, suzun_results, G_ichem, G_suzun_tng, auto_balance_results, tstn_precalc_results):
    V_gnps_0 = _get_const(master_df, "V_gnps_0")
    V_nps_1_0 = _get_const(master_df, "V_nps_1_0")
    V_nps_2_0 = _get_const(master_df, "V_nps_2_0")
    V_knps_0 = _get_const(master_df, "V_knps_0")
    V_suzun_slu_0 = _get_const(master_df, "V_suzun_slu_0")
    V_tstn_suzun_vankor_0 = _get_const(master_df, "V_tstn_suzun_vankor_0")
    V_tstn_suzun_vslu_0 = _get_const(master_df, "V_tstn_suzun_vslu_0")
    V_tstn_tagul_0 = _get_const(master_df, "V_tstn_tagul_0")
    V_tstn_lodochny_0 = _get_const(master_df, "V_tstn_lodochny_0")
    V_tstn_rn_vn_0 = _get_const(master_df, "V_tstn_rn_vn_0")
    V_tstn_skn_0 = _get_const(master_df, "V_tstn_skn_0")
    V_tstn_vo_0 = _get_const(master_df, "V_tstn_vo_0")
    V_tstn_tng_0 = _get_const(master_df, "V_tstn_tng_0")
    V_tstn_kchng_0 = _get_const(master_df, "V_tstn_kchng_0")

    V_knps_prev = _get_day_value(master_df, "V_knps", prev_day, scalar=True)
    V_gnps_prev = _get_day_value(master_df, "V_gnps", prev_day, scalar=True)
    V_nps_1_prev = _get_day_value(master_df, "V_nps_1", prev_day, scalar=True)
    V_nps_2_prev = _get_day_value(master_df, "V_nps_2", prev_day, scalar=True)
    V_tstn_suzun_vslu_prev = _get_day_value(master_df, "V_tstn_suzun_vslu", prev_day, scalar=True)
    V_tstn_suzun_vankor_prev = _get_day_value(master_df, "V_tstn_suzun_vankor", prev_day, scalar=True)
    V_tstn_suzun_prev = _get_day_value(master_df, "V_tstn_suzun", prev_day, scalar=True)
    V_tstn_skn_prev = _get_day_value(master_df, "V_tstn_skn", prev_day, scalar=True)
    V_tstn_vo_prev = _get_day_value(master_df, "V_tstn_vo", prev_day, scalar=True)
    V_tstn_tng_prev = _get_day_value(master_df, "V_tstn_tng", prev_day, scalar=True)
    V_tstn_tagul_prev = _get_day_value(master_df, "V_tstn_tagul", prev_day, scalar=True)
    V_tstn_kchng_prev = _get_day_value(master_df, "V_tstn_kchng", prev_day, scalar=True)
    V_tstn_lodochny_prev = _get_day_value(master_df, "V_tstn_lodochny", prev_day, scalar=True)
    V_tstn_rn_vn_prev = _get_day_value(master_df, "V_tstn_rn_vn", prev_day, scalar=True)



    VN_min_gnps = _get_const(master_df, "VN_min_gnps")
    flag_list = [0,1,0]
    return {
        "V_gnps_0": V_gnps_0, "N": N, "VN_min_gnps": VN_min_gnps, "G_sikn": _to_scalar(sikn_1208_results.get("G_sikn")),
        "V_gnps_prev": V_gnps_prev, "flag_list": flag_list, "V_nps_1_prev": V_nps_1_prev,
        "V_nps_2_prev": V_nps_2_prev, "G_tagul": _to_scalar(lodochny_results.get("G_tagul")), "G_upn_lodochny": _to_scalar(lodochny_results.get("G_upn_lodochny")),
        "G_kchng": _to_scalar(kchng_results.get("G_kchng")), "V_knps_prev": V_knps_prev, "V_nps_1_0": V_nps_1_0, "V_nps_2_0": V_nps_2_0,
        "V_knps_0": V_knps_0, "G_suzun_vslu": _to_scalar(suzun_results.get("G_suzun_vslu")), "V_tstn_suzun_vslu_prev": V_tstn_suzun_vslu_prev,
        "V_tstn_suzun_vankor_prev": V_tstn_suzun_vankor_prev,"G_buy_day": _to_scalar(suzun_results.get("G_buy_day")), "G_per": _to_scalar(suzun_results.get("G_per")),
        "V_suzun_slu_0": V_suzun_slu_0,"V_tstn_suzun_prev": V_tstn_suzun_prev, "G_suzun_slu": _to_scalar(suzun_results.get("G_suzun_slu")),
        "V_tstn_skn_prev": V_tstn_skn_prev, "V_tstn_vo_prev": V_tstn_vo_prev, "G_ichem": G_ichem,
        "G_suzun_tng": G_suzun_tng, "V_tstn_tng_prev": V_tstn_tng_prev, "V_tstn_tagul_prev": V_tstn_tagul_prev,
        "V_tstn_kchng_prev": V_tstn_kchng_prev, "V_tstn_lodochny_prev": V_tstn_lodochny_prev,
        "G_sikn_tagul": _to_scalar(sikn_1208_results.get("G_sikn_tagul")), "V_tstn_rn_vn_prev": V_tstn_rn_vn_prev,
        "G_lodochny": lodochny_results.get("G_lodochny"), "V_tstn_suzun_vankor_0":V_tstn_suzun_vankor_0, "V_tstn_suzun_vslu_0":V_tstn_suzun_vslu_0,
        "V_tstn_tagul_0":V_tstn_tagul_0, "V_tstn_lodochny_0":V_tstn_lodochny_0, "V_tstn_rn_vn_0":V_tstn_rn_vn_0, "V_tstn_suzun_vankor_0":V_tstn_suzun_vankor_0,
        "V_tstn_suzun_vslu_0":V_tstn_suzun_vslu_0, "V_tstn_skn_0":V_tstn_skn_0, "V_tstn_vo_0":V_tstn_vo_0, "V_tstn_tng_0":V_tstn_tng_0,
        "V_tstn_kchng_0":V_tstn_kchng_0,"F":auto_balance_results.get("F"),"F_suzun_vslu":auto_balance_results.get("F_suzun_vslu"),
        "F_suzun_vankor":auto_balance_results.get("F_suzun_vankor"), "F_suzun":auto_balance_results.get("F_suzun"), "F_skn":auto_balance_results.get("F_skn"),
        "F_vo":auto_balance_results.get("F_vo"), "F_tng":auto_balance_results.get("F_tng"), "F_kchng":auto_balance_results.get("F_kchng"),
        "F_tagul":auto_balance_results.get("F_tagul"),"F_tagul_lpu":auto_balance_results.get("F_tagul_lpu"),
        "G_gnps_i": tstn_precalc_results.get("G_gnps_i"),
        "G_gnps": tstn_precalc_results.get("G_gnps"),
        "V_gnps": tstn_precalc_results.get("V_gnps"),
        "V_nps_1": tstn_precalc_results.get("V_nps_1"),
        "V_nps_2": tstn_precalc_results.get("V_nps_2"),
        "V_tstn_suzun_vslu": tstn_precalc_results.get("V_tstn_suzun_vslu"),
        "V_tstn_suzun_vankor": tstn_precalc_results.get("V_tstn_suzun_vankor"),
        "V_tstn_tagul": tstn_precalc_results.get("V_tstn_tagul"),
        "V_tstn_lodochny": tstn_precalc_results.get("V_tstn_lodochny"),
        "V_tstn_tagul_obch": tstn_precalc_results.get("V_tstn_tagul_obch"),
        "V_tstn_rn_vn": tstn_precalc_results.get("V_tstn_rn_vn"),
    }


def prepare_tstn_precalc_data(master_df, prev_day, N, sikn_1208_results, lodochny_results, suzun_results, rn_results, tstn_inputs):
    def _num(value):
        return float(value) if value is not None else 0.0

    F_tagul_lpu = _num(rn_results.get("F_bp_tagul_lpu"))
    F_tagul_tpu = _num(rn_results.get("F_bp_tagul_tpu"))
    F_tagul = F_tagul_lpu + F_tagul_tpu

    return {
        "V_gnps_0": _get_const(master_df, "V_gnps_0"),
        "VN_min_gnps": _get_const(master_df, "VN_min_gnps"),
        "N": N,
        "G_sikn": _to_scalar(sikn_1208_results.get("G_sikn")),
        "manual_G_gnps_i": tstn_inputs.get("manual_G_gnps_i"),
        "V_gnps_prev": _get_day_value(master_df, "V_gnps", prev_day, scalar=True),
        "V_nps_1_prev": _get_day_value(master_df, "V_nps_1", prev_day, scalar=True),
        "V_nps_2_prev": _get_day_value(master_df, "V_nps_2", prev_day, scalar=True),
        "V_tstn_suzun_vslu_prev": _get_day_value(master_df, "V_tstn_suzun_vslu", prev_day, scalar=True),
        "F_suzun_vslu": _num(rn_results.get("F_bp_suzun_vslu")),
        "G_suzun_vslu": _to_scalar(suzun_results.get("G_suzun_vslu")),
        "K_suzun": tstn_inputs.get("K_suzun"),
        "V_tstn_suzun_vankor_prev": _get_day_value(master_df, "V_tstn_suzun_vankor", prev_day, scalar=True),
        "F_suzun_vankor": _num(rn_results.get("F_bp_suzun_vankor")),
        "G_buy_day": _to_scalar(suzun_results.get("G_buy_day")),
        "G_per": _to_scalar(suzun_results.get("G_per")),
        "K_vankor": tstn_inputs.get("K_vankor"),
        "V_tstn_tagul_prev": _get_day_value(master_df, "V_tstn_tagul", prev_day, scalar=True),
        "G_tagul": lodochny_results.get("G_tagul"),
        "F_tagul": F_tagul,
        "K_tagul": tstn_inputs.get("K_tagul"),
        "V_tstn_lodochny_prev": _get_day_value(master_df, "V_tstn_lodochny", prev_day, scalar=True),
        "G_sikn_tagul": lodochny_results.get("G_sikn_tagul"),
        "G_lodochny": lodochny_results.get("G_lodochny"),
        "F_tagul_lpu": F_tagul_lpu,
        "K_lodochny": tstn_inputs.get("K_lodochny"),
        "V_tstn_rn_vn_prev": _get_day_value(master_df, "V_tstn_rn_vn", prev_day, scalar=True),
    }

def rn_vankor_check_data(master_df, n, prev_day, tstn_results, lodochny_results, suzun_results, cppn1_results, auto_balance_results):
    def _val(value):
        return value.get("value") if isinstance(value, dict) else value
    VA_upsv_yu_min = _get_const(master_df, "VA_upsv_yu_min")
    VA_upsv_yu_max = _get_const(master_df, "VA_upsv_yu_max")
    V_delta_upsv_yu_max = _get_const(master_df,"V_delta_upsv_yu_max")
    VO_delta_upsv_yu_max = _get_const(master_df,"VO_delta_upsv_yu_max")
    VA_upsv_s_min = _get_const(master_df, "VA_upsv_s_min")
    VA_upsv_s_max = _get_const(master_df, "VA_upsv_s_max")
    V_delta_upsv_s_max = _get_const(master_df,"V_delta_upsv_s_max")
    VO_delta_upsv_s_max = _get_const(master_df,"VO_delta_upsv_s_max")
    VA_cps_min = _get_const(master_df, "VA_cps_min")
    VA_cps_max = _get_const(master_df, "VA_cps_max")
    V_delta_cps_max = _get_const(master_df,"V_delta_cps_max")
    VO_delta_cps_max = _get_const(master_df,"VO_delta_cps_max")
    VA_upn_suzun_min = _get_const(master_df,"VA_upn_suzun_min")
    VA_upn_suzun_max = _get_const(master_df,"VA_upn_suzun_max")
    V_delta_upn_suzun_max = _get_const(master_df,"V_delta_upn_suzun_max")
    VO_delta_upn_suzun_max = _get_const(master_df,"VO_delta_upn_suzun_max")
    VA_upn_lodochny_min = _get_const(master_df,"VA_upn_lodochny_min")
    VA_upn_lodochny_max = _get_const(master_df,"VA_upn_lodochny_max")
    V_delta_upn_lodochny_max = _get_const(master_df,"V_delta_upn_lodochny_max")
    VO_upn_lodochny_max = _get_const(master_df,"VO_upn_lodochny_max")
    VA_tagul_min = _get_const(master_df,"VA_tagul_min")
    VA_tagul_max = _get_const(master_df,"VA_tagul_max")
    VA_gnps_min = _get_const(master_df,"VA_gnps_min")
    VA_gnps_max = _get_const(master_df,"VA_gnps_max")
    V_delta_gnps_max = _get_const(master_df,"V_delta_gnps_max")
    VO_gnps_max = _get_const(master_df,"VO_gnps_max")
    VA_nps_1_min = _get_const(master_df,"VA_nps_1_min")
    VA_nps_1_max = _get_const(master_df,"VA_nps_1_max")
    V_delta_nps_1_max = _get_const(master_df,"V_delta_nps_1_max")
    VO_nps_1_max = _get_const(master_df,"VO_nps_1_max")
    VA_nps_2_min = _get_const(master_df,"VA_nps_2_min")
    VA_nps_2_max = _get_const(master_df,"VA_nps_2_max")
    V_delta_nps_2_max = _get_const(master_df,"V_delta_nps_2_max")
    VO_nps_2_max = _get_const(master_df,"VO_nps_2_max")
    VN_knps_min = _get_const(master_df,"VA_knps_min")
    VN_knps_max = _get_const(master_df,"VA_knps_max")
    V_delta_knps_max = _get_const(master_df,"V_delta_knps_max")
    VO_knps_max = _get_const(master_df,"VO_knps_max")
    V_ichem_min = _get_const(master_df,"V_ichem_min")
    V_ichem_max = _get_const(master_df,"V_ichem_max")
    V_tstn_min = _get_const(master_df,"V_tstn_min")
    V_tstn_max = _get_const(master_df,"V_tstn_max")
    V_tstn_suzun_min = _get_const(master_df,"V_tstn_suzun_min")
    V_tstn_suzun_max = _get_const(master_df,"V_tstn_suzun_max")
    V_tstn_suzun_vankor_min = _get_const(master_df,"V_tstn_suzun_vankor_min")
    V_tstn_suzun_vankor_max =_get_const(master_df,"V_tstn_suzun_vankor_max")
    V_tstn_suzun_vslu_min = _get_const(master_df,"V_tstn_suzun_vslu_min")
    V_tstn_suzun_vslu_max = _get_const(master_df,"V_tstn_suzun_vslu_max")
    V_tstn_tagul_obch_min = _get_const(master_df,"V_tstn_tagul_obch_min")
    V_tstn_tagul_min = _get_const(master_df, "V_tstn_tagul_min")
    V_tstn_tagul_max = _get_const(master_df, "V_tstn_tagul_max")
    V_tstn_tagul_obch_max = _get_const(master_df,"V_tstn_tagul_obch_max")
    V_tstn_lodochny_min = _get_const(master_df,"V_tstn_lodochny_min")
    V_tstn_lodochny_max = _get_const(master_df,"V_tstn_lodochny_max")
    V_tstn_skn_min = _get_const(master_df,"V_tstn_skn_min")
    V_tstn_skn_max = _get_const(master_df,"V_tstn_skn_max")
    V_tstn_vo_min = _get_const(master_df,"V_tstn_vo_min")
    V_tstn_vo_max = _get_const(master_df,"V_tstn_vo_max")
    V_tstn_tng_min = _get_const(master_df,"V_tstn_tng_min")
    V_tstn_tng_max = _get_const(master_df,"V_tstn_tng_max")
    V_tstn_kchng_min = _get_const(master_df,"V_tstn_kchng_min")
    V_tstn_kchng_max = _get_const(master_df,"V_tstn_kchng_max")
    p_gnps = _get_const(master_df,"p_gnps")
    Q_gnps_min_1 = _get_const(master_df,"Q_gnps_min_1")
    Q_gnps_max_2 = _get_const(master_df, "Q_gnps_max_2")
    Q_gnps_max_1 = _get_const(master_df,"Q_gnps_max_1")
    p_nps_1_2 = _get_const(master_df,"p_nps_1_2")
    Q_nps_1_2_min_1 = _get_const(master_df,"Q_nps_1_2_min_1")
    Q_nps_1_2_max_2 = _get_const(master_df,"Q_nps_1_2_max_2")
    Q_nps_1_2_max_1 = _get_const(master_df,"Q_nps_1_2_max_1")
    p_knps = _get_const(master_df, "p_knps")
    Q_knps_min_1 = _get_const(master_df, "Q_knps_min_1")
    Q_knps_max_2 = _get_const(master_df, "Q_knps_max_2")
    Q_knps_max_1 = _get_const(master_df, "Q_knps_max_1")
    

    V_upsv_yu_prev = _get_day_value(master_df, "V_upsv_yu", prev_day, scalar=True)
    V_upsv_s_prev = _get_day_value(master_df, "V_upsv_s", prev_day, scalar=True)
    V_cps_prev = _get_day_value(master_df, "V_cps", prev_day, scalar=True)
    V_upn_suzun_prev = _get_day_value(master_df, "V_upn_suzun", prev_day, scalar=True)
    V_upn_lodochny_prev = _get_day_value(master_df, "V_upn_lodochny", prev_day, scalar=True)
    V_tagul = _get_day_value(master_df, "V_tagul", n, scalar=True)
    V_gnps_prev = _get_day_value(master_df, "V_gnps", prev_day, scalar=True)
    V_nps_1_prev = _get_day_value(master_df, "V_nps_1", prev_day, scalar=True)
    V_nps_2_prev = _get_day_value(master_df, "V_nps_2", prev_day, scalar=True)
    V_knps_prev = _get_day_value(master_df, "V_knps", prev_day, scalar=True)
    return{
        "V_upsv_yu":  cppn1_results.get("V_upsv_yu"), "VA_upsv_yu_min":VA_upsv_yu_min, "VA_upsv_yu_max":VA_upsv_yu_max, "V_upsv_yu_prev":V_upsv_yu_prev,
        "V_delta_upsv_yu_max":V_delta_upsv_yu_max, "VO_delta_upsv_yu_max":VO_delta_upsv_yu_max, "V_upsv_s": cppn1_results.get("V_upsv_s"),
        "VA_upsv_s_min":VA_upsv_s_min, "VA_upsv_s_max":VA_upsv_s_max, "V_delta_upsv_s_max":V_delta_upsv_s_max, "VO_delta_upsv_s_max":VO_delta_upsv_s_max,
        "V_cps":auto_balance_results.get("V_cps"), "VA_cps_min":VA_cps_min, "VA_cps_max":VA_cps_max, "V_delta_cps_max":V_delta_cps_max,
        "VO_delta_cps_max":VO_delta_cps_max, "V_upn_suzun":suzun_results.get("V_upn_suzun"), "VA_upn_suzun_min":VA_upn_suzun_min,
        "VA_upn_suzun_max":VA_upn_suzun_max, "V_delta_upn_suzun_max":V_delta_upn_suzun_max, "VO_delta_upn_suzun_max":VO_delta_upn_suzun_max, "V_upn_lodochny":lodochny_results.get("V_upn_lodochny"),
        "V_upsv_s_prev":V_upsv_s_prev, "V_cps_prev":V_cps_prev, "V_upn_suzun_prev":V_upn_suzun_prev, "VA_upn_lodochny_min":VA_upn_lodochny_min, 
        "VA_upn_lodochny_max":VA_upn_lodochny_max, "V_upn_lodochny_prev":V_upn_lodochny_prev, "V_delta_upn_lodochny_max":V_delta_upn_lodochny_max, "VO_upn_lodochny_max":VO_upn_lodochny_max, "V_tagul":V_tagul,
        "VA_tagul_min":VA_tagul_min, "VA_tagul_max":VA_tagul_max, "V_gnps":_val(tstn_results.get("V_gnps")), "VA_gnps_min":VA_gnps_min,"VA_gnps_max":VA_gnps_max,
        "V_delta_gnps_max":V_delta_gnps_max,"VO_gnps_max":VO_gnps_max, "V_gnps_prev":V_gnps_prev,"V_nps_1":tstn_results.get("V_nps_1"), 
        "V_nps_1_prev":V_nps_1_prev, "VA_nps_1_min":VA_nps_1_min, "VA_nps_1_max":VA_nps_1_max, "V_delta_nps_1_max":V_delta_nps_1_max,"VO_nps_1_max":VO_nps_1_max,
        "V_nps_2":_val(tstn_results.get("V_nps_2")),"V_nps_2_prev":V_nps_2_prev,"VA_nps_2_min":VA_nps_2_min,"VA_nps_2_max":VA_nps_2_max,"V_delta_nps_2_max":V_delta_nps_2_max,
        "VO_nps_2_max":VO_nps_2_max,"V_knps":_val(tstn_results.get("V_knps")), "VN_knps_min":VN_knps_min, "VN_knps_max":VN_knps_max, "V_delta_knps_max":V_delta_knps_max, "VO_knps_max":VO_knps_max,
        "V_knps_prev":V_knps_prev, "V_ichem": lodochny_results.get("V_ichem"), "V_ichem_min":V_ichem_min,"V_ichem_max":V_ichem_max,
        "V_lodochny_cps_uspv_yu":cppn1_results.get("V_lodochny_cps_upsv_yu"), "G_sikn_tagul":lodochny_results.get("G_sikn_tagul"), "V_tstn_vn":_val(tstn_results.get("V_tstn_vn")),
        "V_tstn_min":V_tstn_min, "V_tstn_max":V_tstn_max, "V_tstn_suzun":_val(tstn_results.get("V_tstn_suzun")), "V_tstn_suzun_min":V_tstn_suzun_min, "V_tstn_suzun_max":V_tstn_suzun_max,
        "V_tstn_suzun_vankor":_val(tstn_results.get("V_tstn_suzun_vankor")), "V_tstn_suzun_vankor_min":V_tstn_suzun_vankor_min,"V_tstn_suzun_vankor_max":V_tstn_suzun_vankor_max, "V_tstn_suzun_vslu":_val(tstn_results.get("V_tstn_suzun_vslu")),
        "V_tstn_suzun_vslu_min":V_tstn_suzun_vslu_min, "V_tstn_suzun_vslu_max":V_tstn_suzun_vslu_max,"V_tstn_tagul_obch":_val(tstn_results.get("V_tstn_tagul_obch")), "V_tstn_tagul_obch_min":V_tstn_tagul_obch_min,"V_tstn_tagul_obch_max":V_tstn_tagul_obch_max,
        "V_tstn_lodochny":_val(tstn_results.get("V_tstn_lodochny")), "V_tstn_lodochny_min":V_tstn_lodochny_min,"V_tstn_lodochny_max":V_tstn_lodochny_max,
        "V_tstn_tagul_min":V_tstn_tagul_min, "V_tstn_tagul":_val(tstn_results.get("V_tstn_tagul")), "V_tstn_tagul_max":V_tstn_tagul_max,
        "V_tstn_skn":_val(tstn_results.get("V_tstn_skn")), "V_tstn_skn_min":V_tstn_skn_min, "V_tstn_skn_max":V_tstn_skn_max, "V_tstn_vo":_val(tstn_results.get("V_tstn_vo")),"V_tstn_vo_min":V_tstn_vo_min,"V_tstn_vo_max":V_tstn_vo_max,
        "V_tstn_tng":_val(tstn_results.get("V_tstn_tng")), "V_tstn_tng_min":V_tstn_tng_min, "V_tstn_tng_max":V_tstn_tng_max,"V_tstn_kchng":_val(tstn_results.get("V_tstn_kchng")), "V_tstn_kchng_min":V_tstn_kchng_min,
        "V_tstn_kchng_max":V_tstn_kchng_max, "p_gnps":p_gnps, "G_gnps":tstn_results.get("G_gnps"), "Q_gnps_min_1":Q_gnps_min_1,"Q_gnps_max_2":Q_gnps_max_2,"Q_gnps_max_1":Q_gnps_max_1,
        "G_tagul_lodochny":lodochny_results.get("G_tagul_lodochny"), "p_nps_1_2":p_nps_1_2,"Q_nps_1_2_min_1":Q_nps_1_2_min_1,"Q_nps_1_2_max_2":Q_nps_1_2_max_2,"Q_nps_1_2_max_1":Q_nps_1_2_max_1,
        "p_knps":p_knps, "Q_knps_min_1":Q_knps_min_1,"Q_knps_max_2":Q_knps_max_2, "Q_knps_max_1":Q_knps_max_1,"F":auto_balance_results.get("F")
    }
def plan_sdacha_data(master_df, n):
    month_mask = (master_df["date"].dt.month == n.month) & (master_df["date"].dt.year == n.year)

    def _sum_month(column_name):
        if column_name not in master_df.columns:
            return 0.0
        values = master_df.loc[month_mask, column_name].values
        return float(np.nansum(values)) if values.size else 0.0

    return {
        # Месячные суммы (рассчитанные по дням)
        "F_vn": _sum_month("F_vn"),
        "F_suzun": _sum_month("F_suzun"),
        "F_suzun_vankor": _sum_month("F_suzun_vankor"),
        "F_suzun_vsly": _sum_month("F_suzun_vslu"),
        "F_tagul_lpy": _sum_month("F_tagul_lpu"),
        "F_tagul_tpy": _sum_month("F_tagul_tpu"),
        "F_skn": _sum_month("F_skn"),
        "F_vo": _sum_month("F_vo"),
        "F_tng": _sum_month("F_tng"),
        "F_kchng": _sum_month("F_kchng"),
        # Планы берём из JSON (monthly_data -> master_df)
        "F_vn_plan": _get_day_value(master_df, "F_vn_plan", n, scalar=True),
        "F_suzun_plan": _get_day_value(master_df, "F_suzun_plan", n, scalar=True),
        "F_suzun_vankor_plan": _get_day_value(master_df, "F_suzun_vankor_plan", n, scalar=True),
        "F_suzun_vsly_plan": _get_day_value(master_df, "F_suzun_vsly_plan", n, scalar=True),
        "F_tagul_lpy_plan": _get_day_value(master_df, "F_tagul_lpy_plan", n, scalar=True),
        "F_tagul_tpy_plan": _get_day_value(master_df, "F_tagul_tpy_plan", n, scalar=True),
        "F_skn_plan": _get_day_value(master_df, "F_skn_plan", n, scalar=True),
        "F_vo_plan": _get_day_value(master_df, "F_vo_plan", n, scalar=True),
        "F_tng_plan": _get_day_value(master_df, "F_tng_plan", n, scalar=True),
        "F_kchng_plan": _get_day_value(master_df, "F_kchng_plan", n, scalar=True),
    }

def balance_po_business_plan_data(master_df, n):
    V_vn_nm_ost_np = _get_day_value(master_df,"V_vn_nm_ost_np",n,scalar=True)
    V_vn_nm_ost_app = _get_day_value(master_df,"V_vn_nm_ost_app",n,scalar=True)
    V_vn_nm_ost_texn = _get_day_value(master_df,"V_vn_nm_ost_texn",n,scalar=True)
    V_vn_nm_path = _get_day_value(master_df, "V_vn_nm_path", n, scalar=True)
    Q_vn_oil = _get_day_value(master_df, "Q_vn_oil", n, scalar=True)
    Q_vn_condensate = _get_day_value(master_df, "Q_vn_condensate", n, scalar=True)
    V_vn_lost_oil = _get_day_value(master_df,"V_vn_lost_oil",n,scalar=True)
    V_vn_lost_transport = _get_day_value(master_df,"V_vn_lost_transport",n,scalar=True)
    G_vn_release_suzun = _get_day_value(master_df,"G_vn_release_suzun",n,scalar=True)
    V_vn_km_ost_np = _get_day_value(master_df,"V_vn_km_ost_np",n,scalar=True)
    V_vn_km_ost_app = _get_day_value(master_df,"V_vn_km_ost_app",n,scalar=True)
    V_vn_km_ost_texn = _get_day_value(master_df,"V_vn_km_ost_texn",n,scalar=True)
    V_vn_km_path = _get_day_value(master_df,"V_vn_km_path",n,scalar=True)
    F_vn_total = _get_day_value(master_df,"F_vn_total",n,scalar=True) 
    V_suzun_nm_ost_np = _get_day_value(master_df, "V_suzun_nm_ost_np", n, scalar=True)
    V_suzun_nm_ost_app = _get_day_value(master_df, "V_suzun_nm_ost_app", n, scalar=True)
    V_suzun_nm_ost_texn = _get_day_value(master_df,"V_suzun_nm_ost_texn",n,scalar=True)
    V_suzun_nm_path = _get_day_value(master_df,"V_suzun_nm_path",n,scalar=True)
    Q_suzun_oil = _get_day_value(master_df,"Q_suzun_oil",n,scalar=True)
    Q_suzun_condensate = _get_day_value(master_df, "Q_suzun_condensate", n, scalar=True)
    V_suzun_lost_oil = _get_day_value(master_df,"V_suzun_lost_oil",n,scalar=True)
    V_suzun_lost_transport_suzun = _get_day_value(master_df,"V_suzun_lost_transport_suzun",n,scalar=True)
    G_suzun_mupn = _get_day_value(master_df,"G_suzun_mupn",n,scalar = True)
    G_suzun_release_rn_drillig = _get_day_value(master_df,"G_suzun_release_rn_drillig",n,scalar=True)
    F_suzun_total = _get_day_value(master_df,"F_suzun_total",n,scalar=True)
    F_suzun_vankor = _get_day_value(master_df,"F_suzun_vankor",n,scalar=True)
    V_suzun_km_ost_np = _get_day_value(master_df,"V_suzun_km_ost_np",n,scalar=True)
    V_suzun_ost_app = _get_day_value(master_df,"V_suzun_ost_app",n,scalar=True)
    V_suzun_km_texn = _get_day_value(master_df,"V_suzun_km_texn",n,scalar=True)
    V_suzun_km_path = _get_day_value(master_df,"V_suzun_km_path",n,scalar=True)
    G_suzun_buy = _get_day_value(master_df,"G_suzun_buy",n,scalar=True)
    V_vo_nm_ost_np = _get_day_value(master_df, "V_vo_nm_ost_np", n, scalar=True)
    V_vo_nm_ost_app = _get_day_value(master_df,"V_vo_nm_ost_app",n,scalar=True)
    V_vo_nm_ost_texn = _get_day_value(master_df,"V_vo_nm_ost_texn",n,scalar=True)
    V_vo_nm_path = _get_day_value(master_df,"V_vo_nm_path",n,scalar=True)
    Q_vo_oil = _get_day_value(master_df,"Q_vo_oil",n,scalar=True)
    Q_vo_condensate = _get_day_value(master_df,"Q_vo_condensate",n,scalar=True)
    V_vo_lost_oil = _get_day_value(master_df,"V_vo_lost_oil",n,scalar=True)
    V_vo_lost_transport = _get_day_value(master_df,"V_vo_lost_transport",n,scalar=True)
    V_vo_km_ost_np = _get_day_value(master_df,"V_vo_km_ost_np",n,scalar=True)
    V_vo_km_ost_app = _get_day_value(master_df,"V_vo_km_ost_app",n,scalar=True)
    V_vo_km_ost_texn = _get_day_value(master_df,"V_vo_km_ost_texn",n,scalar=True)
    V_vo_km_path = _get_day_value(master_df,"V_vo_km_path",n,scalar=True)
    F_vo_total = _get_day_value(master_df,"F_vo_total",n,scalar=True)
    V_lodochny_nm_ost_np = _get_day_value(master_df,"V_lodochny_nm_ost_np",n,scalar=True)
    V_lodochny_nm_ost_app = _get_day_value(master_df,"V_lodochny_nm_ost_app",n,scalar=True)
    V_lodochny_nm_ost_texn = _get_day_value(master_df,"V_lodochny_nm_ost_texn",n,scalar=True)
    V_lodochny_nm_path = _get_day_value(master_df,"V_lodochny_nm_path",n,scalar=True)
    Q_lodochny_oil = _get_day_value(master_df,"Q_lodochny_oil",n,scalar=True)
    V_lodochny_lost_oil = _get_day_value(master_df,"V_lodochny_lost_oil",n,scalar=True)
    V_lodochny_lost_transport = _get_day_value(master_df,"V_lodochny_lost_transport",n,scalar=True)
    G_lodochny_release_rn_drillig = _get_day_value(master_df,"G_lodochny_release_rn_drillig",n,scalar=True)
    V_lodochny_km_ost_np = _get_day_value(master_df,"V_lodochny_km_ost_np",n,scalar=True)
    V_lodochny_km_ost_app = _get_day_value(master_df,"V_lodochny_km_ost_app",n,scalar=True)
    V_lodochny_km_ost_texn = _get_day_value(master_df,"V_lodochny_km_ost_texn",n,scalar=True)
    V_lodochny_km_path = _get_day_value(master_df,"V_lodochny_km_path",n,scalar=True)
    F_lodochny_total = _get_day_value(master_df,"F_lodochny_total",n,scalar=True)
    V_tagul_nm_ost_np = _get_day_value(master_df,"V_tagul_nm_ost_np",n,scalar=True)
    V_tagul_nm_ost_app = _get_day_value(master_df,"V_tagul_nm_ost_app",n,scalar=True)
    V_tagul_nm_ost_texn = _get_day_value(master_df,"V_tagul_nm_ost_texn",n,scalar=True)
    V_tagul_nm_path = _get_day_value(master_df,"V_tagul_nm_path",n,scalar=True)
    Q_tagul_oil = _get_day_value(master_df,"Q_tagul_oil",n,scalar=True)
    V_tagul_lost_oil = _get_day_value(master_df,"V_tagul_lost_oil",n,scalar=True)
    V_tagul_lost_transport = _get_day_value(master_df,"V_tagul_lost_transport",n,scalar=True)
    G_tagul_release_rn_drillig = _get_day_value(master_df,"G_tagul_release_rn_drillig",n,scalar=True)
    V_tagul_km_ost_np = _get_day_value(master_df,"V_tagul_km_ost_np",n,scalar=True)
    V_tagul_km_ost_app = _get_day_value(master_df,"V_tagul_km_ost_app",n,scalar=True)
    V_tagul_km_ost_texn = _get_day_value(master_df,"V_tagul_km_ost_texn",n,scalar=True)
    V_tagul_km_path = _get_day_value(master_df,"V_tagul_km_path",n,scalar=True)
    F_tagul_total = _get_day_value(master_df,"F_tagul_total",n,scalar=True)


    return{
        "V_vn_nm_ost_np":V_vn_nm_ost_np, "V_vn_nm_ost_app":V_vn_nm_ost_app, "V_vn_nm_ost_texn":V_vn_nm_ost_texn, "V_vn_nm_path":V_vn_nm_path,
        "Q_vn_oil":Q_vn_oil, "Q_vn_condensate":Q_vn_condensate, "V_vn_lost_oil":V_vn_lost_oil, "V_vn_lost_transport":V_vn_lost_transport,
        "G_vn_release_suzun":G_vn_release_suzun, "V_vn_km_ost_np":V_vn_km_ost_np, "V_vn_km_ost_app":V_vn_km_ost_app,"V_vn_km_ost_texn":V_vn_km_ost_texn,
        "V_vn_km_path":V_vn_km_path, "F_vn_total":F_vn_total, "V_suzun_nm_ost_np":V_suzun_nm_ost_np, "V_suzun_nm_ost_app":V_suzun_nm_ost_app,
        "V_suzun_nm_ost_texn":V_suzun_nm_ost_texn, "V_suzun_nm_path":V_suzun_nm_path, "Q_suzun_oil":Q_suzun_oil, "Q_suzun_condensate":Q_suzun_condensate,
        "V_suzun_lost_oil":V_suzun_lost_oil,"V_suzun_lost_transport_suzun":V_suzun_lost_transport_suzun,"G_suzun_mupn":G_suzun_mupn,
        "G_suzun_release_rn_drillig":G_suzun_release_rn_drillig, "F_suzun_total":F_suzun_total, "F_suzun_vankor":F_suzun_vankor, "V_suzun_km_ost_np":V_suzun_km_ost_np,
        "V_suzun_ost_app":V_suzun_ost_app, "V_suzun_km_texn":V_suzun_km_texn, "V_suzun_km_path":V_suzun_km_path, "G_suzun_buy":G_suzun_buy, "V_vo_nm_ost_np":V_vo_nm_ost_np,
        "V_vo_nm_ost_app":V_vo_nm_ost_app, "V_vo_nm_ost_texn":V_vo_nm_ost_texn, "V_vo_nm_path":V_vo_nm_path, "Q_vo_oil":Q_vo_oil, "Q_vo_condensate":Q_vo_condensate, "V_vo_lost_oil":V_vo_lost_oil,
        "V_vo_lost_transport":V_vo_lost_transport, "V_vo_km_ost_np":V_vo_km_ost_np, "V_vo_km_ost_app":V_vo_km_ost_app, "V_vo_km_ost_texn":V_vo_km_ost_texn, "V_vo_km_path":V_vo_km_path,
        "F_vo_total":F_vo_total, "F_vo_total":F_vo_total, "V_lodochny_nm_ost_np":V_lodochny_nm_ost_np, "V_lodochny_nm_ost_app":V_lodochny_nm_ost_app, "V_lodochny_nm_ost_texn":V_lodochny_nm_ost_texn,
        "V_lodochny_nm_path":V_lodochny_nm_path, "Q_lodochny_oil":Q_lodochny_oil, "V_lodochny_lost_oil":V_lodochny_lost_oil, "V_lodochny_lost_transport":V_lodochny_lost_transport,
        "G_lodochny_release_rn_drillig":G_lodochny_release_rn_drillig, "V_lodochny_km_ost_np":V_lodochny_km_ost_np, "V_lodochny_km_ost_app":V_lodochny_km_ost_app, "V_lodochny_km_ost_texn":V_lodochny_km_ost_texn,
        "V_lodochny_km_path":V_lodochny_km_path, "F_lodochny_total":F_lodochny_total, "V_tagul_nm_ost_np":V_tagul_nm_ost_np, "V_tagul_nm_ost_app":V_tagul_nm_ost_app, "V_tagul_nm_ost_texn":V_tagul_nm_ost_texn,
        "V_tagul_nm_path":V_tagul_nm_path, "Q_tagul_oil":Q_tagul_oil, "V_tagul_lost_oil":V_tagul_lost_oil, "V_tagul_lost_transport":V_tagul_lost_transport, "G_tagul_release_rn_drillig":G_tagul_release_rn_drillig,
        "V_tagul_km_ost_np":V_tagul_km_ost_np, "V_tagul_km_ost_app":V_tagul_km_ost_app, "V_tagul_km_ost_texn":V_tagul_km_ost_texn, "V_tagul_km_path":V_tagul_km_path, "F_tagul_total":F_tagul_total
    }
def plan_balance_gtm_data(master_df,n,cppn1_results,TSTN_results,suzun_results,lodochny_results,K_vankor,K_suzun,K_tagul):
    V_vn_nm_gtm_ost_dead = _get_day_value(master_df,"V_vn_nm_gtm_ost_dead",n,scalar=True)
    V_vn_nm_gtm_ost_np = _get_day_value(master_df,"V_vn_nm_gtm_ost_np",n,scalar=True)
    V_vn_nm_gtm_ost_app = _get_day_value(master_df,"V_vn_nm_gtm_ost_app",n,scalar=True)
    V_vn_gtm_lost_condensate = _get_day_value(master_df,"V_vn_gtm_lost_condensate",n,scalar=True)
    G_vn_gtm_release_tbs = _get_day_value(master_df,"G_vn_gtm_release_tbs",n,scalar=True)
    G_vn_gtm_release_rn_drilling = _get_day_value(master_df,"G_vn_gtm_release_rn_drilling",n,scalar=True)
    V_vn_nm_gtm_ost_rvs_clear = _get_day_value(master_df,"V_vn_nm_gtm_ost_rvs_clear",n,scalar=True)
    V_vn_nm_gtm_ost_product = _get_day_value(master_df,"V_vn_nm_gtm_ost_product",n,scalar=True)
    V_vn_km_gtm_ost_app = _get_day_value(master_df,"V_vn_km_gtm_ost_app",n,scalar=True)
    V_suzun_vslu_0 = _get_const(master_df, "V_suzun_vslu_0")
    V_suzun_nm_gtm_ost_cps = _get_day_value(master_df,"V_suzun_nm_gtm_ost_cps",n,scalar=True)
    V_suzun_nm_gtm_ost_dead = _get_day_value(master_df,"V_suzun_nm_gtm_ost_dead",n,scalar=True)
    V_suzun_nm_gtm_ost_texn = _get_day_value(master_df,"V_suzun_nm_gtm_ost_texn",n,scalar=True)
    V_suzun_nm_gtm_ost_np = _get_day_value(master_df,"V_suzun_nm_gtm_ost_np",n,scalar=True)
    V_suzun_nm_tgm_ost_app = _get_day_value(master_df,"V_suzun_nm_tgm_ost_app",n,scalar=True)
    V_suzun_nm_gtm_ost_rvs=_get_day_value(master_df,"V_suzun_nm_gtm_ost_rvs",n,scalar=True)
    V_suzun_0 = _get_const(master_df, "V_suzun_0")
    V_vankor_suzun_0 = _get_const(master_df, "V_vankor_suzun_0")
    V_vankor_vslu_0 = _get_const(master_df, "V_vankor_vslu_0")
    V_suzun_nm_gtm_ost_app = _get_day_value(master_df,"V_suzun_nm_gtm_ost_app",n,scalar = True)
    V_suzun_nm_gtm_ost_product = _get_day_value(master_df,"V_suzun_nm_gtm_ost_product",n,scalar= True)
    V_suzun_km_gtm_ost_cps=_get_day_value(master_df,"V_suzun_km_gtm_ost_cps",n,scalar=True)
    G_suzun_gtm_release = _get_day_value(master_df,"G_suzun_gtm_release",n,scalar=True)
    V_ichem_0 = _get_const(master_df, "V_ichem_0")
    V_vo_nm_gtm_ost_dead = _get_day_value(master_df,"V_vo_nm_gtm_ost_dead",n,scalar=True)
    V_tstn_vo_0 = _get_const(master_df, "V_tstn_vo_0")
    V_vo_nm_gtm_ost_np = _get_day_value(master_df,"V_vo_nm_gtm_ost_np",n,scalar=True)
    V_vo_nm_gtm_ost_app = _get_day_value(master_df,"V_vo_nm_gtm_ost_app",n,scalar=True)
    V_lodochny_0 = _get_const(master_df, "V_lodochny_0")
    V_lodochny_nm_gtm_ost_upsv_yu = _get_day_value(master_df,"V_lodochny_nm_gtm_ost_upsv_yu",n,scalar=True)
    V_tstn_lodochny_0 = _get_const(master_df, "V_tstn_lodochny_0")
    V_lodochny_nm_gtm_ost_np = _get_day_value(master_df,"V_lodochny_nm_gtm_ost_np",n,scalar=True)
    V_lodochny_nm_gtm_ost_app = _get_day_value(master_df,"V_lodochny_nm_gtm_ost_app",n,scalar=True)
    V_lodochny_nm_gtm_dead = _get_day_value(master_df,"V_lodochny_nm_gtm_dead",n,scalar=True)
    V_lodochny_nm_gtm_ost_rvs_clear = _get_day_value(master_df,"V_lodochny_nm_gtm_ost_rvs_clear",n,scalar=True)
    V_tagul_nm_gtm_ost_dead = _get_day_value(master_df,"V_tagul_nm_gtm_ost_dead",n,scalar=True)
    V_tagul_nm_gtm_ost_texn = _get_day_value(master_df,"V_tagul_nm_gtm_ost_texn",n,scalar=True)
    V_tagul_nm_gtm_ost_np = _get_day_value(master_df,"V_tagul_nm_gtm_ost_np",n,scalar=True)
    V_tagul_nm_gtm_ost_app = _get_day_value(master_df,"V_tagul_nm_gtm_ost_app",n,scalar=True)
    V_tstn_tagul_0 = _get_const(master_df,"V_tstn_tagul_0")
    G_tagul_gtm_release_rn_drilling = _get_day_value(master_df,"G_tagul_gtm_release_rn_drilling",n,scalar=True)
    V_tagul_km_gtm_ost_np = _get_day_value(master_df,"V_tagul_km_gtm_ost_np",n,scalar=True)
    V_tagul_km_gtm_ost_app = _get_day_value(master_df,"V_tagul_km_gtm_ost_app",n,scalar=True)

    F_vn = _get_day_value(master_df, "F_vn", n, scalar=True)
    V_tstn_vn = _to_scalar(TSTN_results.get("V_tstn_vn"))
    Q_vslu_month = _to_scalar(suzun_results.get("Q_vslu_month"))
    K_suzun_mining = _get_const(master_df, "K_suzun_mining")
    G_per_month = _to_scalar(suzun_results.get("G_per_month"))
    F_suzun_delta = _get_day_value(master_df, "F_suzun_delta", n, scalar=True)
    F_suzun_vsly_delta = _get_day_value(master_df, "F_suzun_vsly_delta", n, scalar=True)
    F_suzun_vankor_delta = _get_day_value(master_df, "F_suzun_vankor_delta", n, scalar=True)
    V_suzun_slu = _get_day_value(master_df, "V_suzun_slu", n, scalar=True)
    V_tstn_suzun = _to_scalar(TSTN_results.get("V_tstn_suzun"))
    V_tstn_suzun_vslu = _to_scalar(TSTN_results.get("V_tstn_suzun_vslu"))
    F_vo_delta = _get_day_value(master_df, "F_vo_delta", n, scalar=True)
    V_tstn_vo = _to_scalar(TSTN_results.get("V_tstn_vo"))
    V_tstn_lodochny = _to_scalar(TSTN_results.get("V_tstn_lodochny"))
    F_tagul_tpy_delta = _get_day_value(master_df, "F_tagul_tpy_delta", n, scalar=True)
    V_tstn_tagul = _to_scalar(TSTN_results.get("V_tstn_tagul"))
    V_tstn_suzun_vankor = _to_scalar(TSTN_results.get("V_tstn_suzun_vankor"))
    G_buy_month = float(np.nansum(_get_month_values(master_df, "G_buy_day", n.month)))
    return{
        "V_cppn_1_0":cppn1_results.get("V_cppn_1_0"), "V_tstn_vn_0":_to_scalar(TSTN_results.get("V_tstn_vn_0")),
        "Q_vankor_month": suzun_results.get("Q_vankor_month"),"K_vankor":K_vankor, "G_buy_month":G_buy_month,
        "V_cppn_1":cppn1_results.get("V_cppn_1"), "V_suzun_slu_0":suzun_results.get("V_suzun_slu_0"), "Q_suzun_month":suzun_results.get("Q_suzun_month"),
        "V_suzun_vslu":suzun_results.get("V_suzun_vslu"), "K_suzun":K_suzun, "Q_vo_month":suzun_results.get("Q_vo_month"),"V_ichem":lodochny_results.get("V_ichem"),
        "Q_lodochny_month":lodochny_results.get("Q_lodochny_month"),"V_lodochny":lodochny_results.get("V_lodochny"), "Q_tagul_month":lodochny_results.get("Q_tagul_month"),
        "K_tagul":K_tagul,"V_vn_nm_gtm_ost_dead":V_vn_nm_gtm_ost_dead, "V_vn_nm_gtm_ost_np":V_vn_nm_gtm_ost_np, "V_vn_nm_gtm_ost_app":V_vn_nm_gtm_ost_app,
        "V_vn_gtm_lost_condensate":V_vn_gtm_lost_condensate, "G_vn_gtm_release_tbs":G_vn_gtm_release_tbs, "G_vn_gtm_release_rn_drilling":G_vn_gtm_release_rn_drilling,
        "V_vn_nm_gtm_ost_rvs_clear":V_vn_nm_gtm_ost_rvs_clear, "V_vn_nm_gtm_ost_product":V_vn_nm_gtm_ost_product, "V_vn_km_gtm_ost_app":V_vn_km_gtm_ost_app,
        "V_suzun_nm_gtm_ost_cps":V_suzun_nm_gtm_ost_cps, "V_suzun_vslu_0":V_suzun_vslu_0,"V_suzun_nm_gtm_ost_dead":V_suzun_nm_gtm_ost_dead, "V_suzun_nm_gtm_ost_texn":V_suzun_nm_gtm_ost_texn,
        "V_suzun_nm_gtm_ost_np":V_suzun_nm_gtm_ost_np, "V_suzun_nm_tgm_ost_app":V_suzun_nm_tgm_ost_app,"V_suzun_nm_gtm_ost_rvs":V_suzun_nm_gtm_ost_rvs,  "V_suzun_0":V_suzun_0, 
        "V_vankor_suzun_0":V_vankor_suzun_0, "V_vankor_vslu_0":V_vankor_vslu_0, "V_suzun_nm_gtm_ost_app":V_suzun_nm_gtm_ost_app, "V_suzun_nm_gtm_ost_product":V_suzun_nm_gtm_ost_product,
        "V_suzun_km_gtm_ost_cps":V_suzun_km_gtm_ost_cps, "G_suzun_gtm_release":G_suzun_gtm_release, "V_ichem_0":V_ichem_0, "V_vo_nm_gtm_ost_dead":V_vo_nm_gtm_ost_dead,
        "V_tstn_vo_0":V_tstn_vo_0, "V_vo_nm_gtm_ost_np":V_vo_nm_gtm_ost_np, "V_vo_nm_gtm_ost_app":V_vo_nm_gtm_ost_app,"V_lodochny_0":V_lodochny_0,
        "V_lodochny_nm_gtm_ost_upsv_yu":V_lodochny_nm_gtm_ost_upsv_yu, "V_tstn_lodochny_0":V_tstn_lodochny_0, "V_lodochny_nm_gtm_ost_np":V_lodochny_nm_gtm_ost_np,
        "V_lodochny_nm_gtm_ost_app":V_lodochny_nm_gtm_ost_app, "V_lodochny_nm_gtm_dead":V_lodochny_nm_gtm_dead, "V_lodochny_nm_gtm_ost_rvs_clear":V_lodochny_nm_gtm_ost_rvs_clear,
        "V_tagul_nm_gtm_ost_dead":V_tagul_nm_gtm_ost_dead,"V_tagul_nm_gtm_ost_texn":V_tagul_nm_gtm_ost_texn,"V_tagul_nm_gtm_ost_np":V_tagul_nm_gtm_ost_np, 
        "V_tagul_nm_gtm_ost_app":V_tagul_nm_gtm_ost_app, "V_tstn_tagul_0":V_tstn_tagul_0, "G_tagul_gtm_release_rn_drilling":G_tagul_gtm_release_rn_drilling,
        "V_tagul_km_gtm_ost_np":V_tagul_km_gtm_ost_np, "V_tagul_km_gtm_ost_app":V_tagul_km_gtm_ost_app,
        "F_vn":F_vn, "V_tstn_vn":V_tstn_vn, "Q_vslu_month":Q_vslu_month, "K_suzun_mining":K_suzun_mining, "G_per_month":G_per_month,
        "F_suzun_delta":F_suzun_delta, "F_suzun_vsly_delta":F_suzun_vsly_delta, "F_suzun_vankor_delta":F_suzun_vankor_delta, "V_suzun_slu":V_suzun_slu,
        "V_tstn_suzun":V_tstn_suzun, "V_tstn_suzun_vslu":V_tstn_suzun_vslu, "F_vo_delta":F_vo_delta, "V_tstn_vo":V_tstn_vo,
        "V_tstn_lodochny":V_tstn_lodochny, "F_tagul_tpy_delta":F_tagul_tpy_delta, "V_tstn_tagul":V_tstn_tagul, "V_tstn_suzun_vankor":V_tstn_suzun_vankor,
    }    
    
