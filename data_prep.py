import numpy as np
import pandas as pd


def _to_scalar(val):
    """Безопасно извлекает скаляр из массива/списка/скаляра."""
    if isinstance(val, dict):
        if "value" in val:
            return _to_scalar(val["value"])
        return 0.0
    if isinstance(val, (list, np.ndarray)):
        if len(val) == 0:
            return 0.0
        return _to_scalar(val[0])
    if pd.isna(val):
        return 0.0
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def _get_day_value(master_df, name, day, default=0.0):
    """Безопасно получает значение колонки name на дату day.

    - Если колонки нет или строка по дате отсутствует — возвращает default.
    - Если в ячейке лежит dict {value,status,message} — берём только value.
    """
    if name not in master_df.columns:
        return default
    value = master_df.loc[master_df["date"] == day, name].values
    if len(value) == 0:
        return default
    return _to_scalar(value)

def _get_month_values(master_df, column_name, month):
    """Получает значения колонки за указанный месяц."""
    if column_name not in master_df.columns:
        return np.array([], dtype=float)
    return master_df.loc[master_df["date"].dt.month == month, column_name].values


def _get_month_scalar_values(master_df, column_name, month):
    """
    Получает значения колонки за месяц и приводит каждое значение к числу.
    Если в ячейке лежит словарь вида {value,status,message}, берём только value.
    """
    raw = _get_month_values(master_df, column_name, month)
    return np.array([_to_scalar(v) for v in raw], dtype=float)

def _get_const(master_df, column_name, default=0.0):
    """Возвращает константу из master_df (первое валидное значение столбца)."""
    if column_name not in master_df.columns:
        return default
    series = master_df[column_name].dropna()
    if series.empty:
        return default
    return _to_scalar(series.values)


def _get_last_const(master_df, column_name, default=0.0):
    """Возвращает последнее валидное (не NaN) значение столбца."""
    if column_name not in master_df.columns:
        return default
    series = master_df[column_name].dropna()
    if series.empty:
        return default
    return _to_scalar(series.iloc[-1])
    
def get_day_zero_data(master_df,prev_month):
    V_upn_suzun_0 = _get_day_value(master_df,"V_upn_suzun", prev_month)
    V_suzun_vslu_0 = _get_day_value(master_df,"V_suzun_vslu", prev_month)
    V_suzun_tng_0 = _get_day_value(master_df,"V_suzun_tng", prev_month)
    V_upsv_yu_0 = _get_day_value(master_df,"V_upsv_yu", prev_month)
    V_upsv_s_0 = _get_day_value(master_df,"V_upsv_s", prev_month)
    V_cps_0 = _get_day_value(master_df,"V_cps", prev_month)
    V_gnps_0 = _get_day_value(master_df,"V_gnps", prev_month)
    V_nps_1_0 = _get_day_value(master_df,"V_nps_1", prev_month)
    V_nps_2_0 = _get_day_value(master_df,"V_nps_2", prev_month)
    V_knps_0 = _get_day_value(master_df,"V_knps", prev_month)
    V_suzun_0 = _get_day_value(master_df,"V_suzun", prev_month)
    V_tstn_suzun_vankor_0 = _get_day_value(master_df,"V_tstn_suzun_vankor", prev_month)
    V_tstn_suzun_vslu_0 = _get_day_value(master_df,"V_tstn_suzun_vslu", prev_month)
    V_tstn_tagul_0 = _get_day_value(master_df,"V_tstn_tagul", prev_month)
    V_tstn_lodochny_0 = _get_day_value(master_df,"V_tstn_lodochny", prev_month)
    V_tstn_rn_vn_0 = _get_day_value(master_df,"V_tstn_rn_vn", prev_month)
    V_tstn_skn_0 = _get_day_value(master_df,"V_tstn_skn", prev_month)
    V_tstn_vo_0 = _get_day_value(master_df,"V_tstn_vo", prev_month) 
    V_tstn_tng_0 = _get_day_value(master_df,"V_tstn_tng", prev_month)
    V_tstn_kchng_0 = _get_day_value(master_df,"V_tstn_kchng", prev_month)
    return{
        "V_upsv_yu_0":V_upsv_yu_0,
        "V_upsv_s_0":V_upsv_s_0,
        "V_cps_0":V_cps_0,
        "V_upn_suzun_0":V_upn_suzun_0,
        "V_suzun_vslu_0":V_suzun_vslu_0,
        "V_suzun_tng_0":V_suzun_tng_0,
        "V_gnps_0":V_gnps_0,
        "V_nps_1_0":V_nps_1_0,
        "V_nps_2_0":V_nps_2_0,
        "V_knps_0":V_knps_0,
        "V_suzun_0":V_suzun_0,
        "V_tstn_suzun_vankor_0":V_tstn_suzun_vankor_0,
        "V_tstn_suzun_vslu_0":V_tstn_suzun_vslu_0,
        "V_tstn_tagul_0":V_tstn_tagul_0,
        "V_tstn_lodochny_0":V_tstn_lodochny_0,
        "V_tstn_rn_vn_0":V_tstn_rn_vn_0,
        "V_tstn_skn_0":V_tstn_skn_0,
        "V_tstn_vo_0":V_tstn_vo_0,
        "V_tstn_tng_0":V_tstn_tng_0,
        "V_tstn_kchng_0":V_tstn_kchng_0,
    }
    
def get_prev_day_data(master_df, prev_day):
    V_upn_suzun_prev = _get_day_value(master_df,"V_upn_suzun", prev_day)
    V_upn_lodochny_prev = _get_day_value(master_df,"V_upn_lodochny", prev_day)
    V_tagul_tr_prev = _get_day_value(master_df,"V_tagul_tr", prev_day)
    V_upsv_yu_prev = _get_day_value(master_df,"V_upsv_yu", prev_day)
    V_upsv_s_prev = _get_day_value(master_df,"V_upsv_s", prev_day)
    V_cps_prev = _get_day_value(master_df,"V_cps", prev_day)
    V_nps_1_prev = _get_day_value(master_df,"V_nps_1", prev_day)
    V_nps_2_prev = _get_day_value(master_df,"V_nps_2", prev_day)
    V_tstn_rn_vn_prev  = _get_day_value(master_df,"V_tstn_rn_vn", prev_day)

    return{
        "V_upn_suzun_prev": V_upn_suzun_prev,
        "V_upn_lodochny_prev":V_upn_lodochny_prev,
        "V_tagul_tr_prev":V_tagul_tr_prev,
        "V_upsv_yu_prev":V_upsv_yu_prev,
        "V_upsv_s_prev":V_upsv_s_prev,
        "V_cps_prev":V_cps_prev,
        "V_nps_1_prev":V_nps_1_prev,
        "V_nps_2_prev":V_nps_2_prev,
        "V_tstn_rn_vn_prev":V_tstn_rn_vn_prev,
    }

def precalc_value_data(master_df, n, prev_day,N,day):
    Q_vslu = _get_day_value(master_df,"Q_vslu",n)
    G_payaha = _get_day_value(master_df,"G_payaha",n)
    G_suzun_tng = _get_day_value(master_df,"G_suzun_tng",n)
    Q_vo = _get_day_value(master_df,"Q_vo",n)
    G_ichem = _get_day_value(master_df,"G_ichem",n)
    Q_tagul = _get_day_value(master_df,"Q_tagul",n)
    V_tagul_tr_prev = _get_day_value(master_df,"V_tagul_tr",prev_day)
    V_tagul_tr = _get_day_value(master_df,"V_tagul_tr",n)
    K_delta_g_tagul = _get_day_value(master_df,"K_delta_g_tagul",n)
    Q_kchng = _get_day_value(master_df,"Q_kchng",n)
    G_buying_oil_month = _get_const(master_df, "G_buying_oil_month")
    G_out_udt_month = _get_const(master_df, "G_out_udt_month")
    V_lodochny_cps_upsv_yu_prev = _get_day_value(master_df,"V_lodochny_cps_upsv_yu",prev_day)
    G_lodochny_upsv_yu = _get_day_value(master_df,"G_lodochny_upsv_yu",n)
    G_lodochny_upsv_yu_month = _get_last_const(master_df, "G_lodochny_upsv_yu_month")
    G_sikn_tagul = _get_day_value(master_df,"G_sikn_tagul",n)
    V_suzun_vslu_prev = _get_day_value(master_df,"V_suzun_vslu",prev_day)
    V_suzun_tng_prev = _get_day_value(master_df,"V_suzun_tng",prev_day)
    V_ichem_prev = _get_day_value(master_df, "V_ichem", prev_day)


    return{
        "V_lodochny_cps_upsv_yu_prev":V_lodochny_cps_upsv_yu_prev,
        "G_lodochny_upsv_yu":G_lodochny_upsv_yu,
        "Q_vslu":Q_vslu,
        "V_suzun_vslu_prev":V_suzun_vslu_prev,
        "V_suzun_tng_prev":V_suzun_tng_prev,
        "G_payaha":G_payaha,
        "G_suzun_tng":G_suzun_tng,
        "V_ichem_prev":V_ichem_prev,
        "Q_vo":Q_vo,
        "G_ichem":G_ichem,
        "G_lodochny_upsv_yu_month":G_lodochny_upsv_yu_month,
        "Q_tagul":Q_tagul,
        "V_tagul_tr_prev":V_tagul_tr_prev,
        "V_tagul_tr":V_tagul_tr,
        "K_delta_g_tagul":K_delta_g_tagul,
        "N":N,
        "Q_kchng":Q_kchng,
        "G_buying_oil_month":G_buying_oil_month,
        "G_out_udt_month":G_out_udt_month,
        "day":day,
        "G_sikn_tagul":G_sikn_tagul,

    }

def lodochny_upsv_yu_data(master_df, n, prev_day, day, N, month):
    G_lodochny_upsv_yu_month_prev = _get_day_value(master_df,"G_lodochny_upsv_yu_month",prev_day)
    Q_lodochny = _get_day_value(master_df,"Q_lodochny",n)
    K_otkachki = _get_day_value(master_df,"K_otkachki",n)
    K_delta_g_upn_lodochny = _get_day_value(master_df,"K_delta_g_upn_lodochny",n)
    Q_tagul = _get_month_values(master_df,"Q_tagul",month)
    return{
        "Q_lodochny":Q_lodochny,
        "K_otkachki":K_otkachki,
        "K_delta_g_upn_lodochny":K_delta_g_upn_lodochny,
        "G_lodochny_upsv_yu_month_prev":G_lodochny_upsv_yu_month_prev,
        "N":N,
        "day":day,
        "Q_tagul":Q_tagul
    }


def recalculation_data(master_df,n,prev_day,N,prev_month):
    V_upn_suzun = _get_day_value(master_df, "V_upn_suzun",n)
    V_upn_suzun_prev = _get_day_value(master_df, "V_upn_suzun",prev_day)
    V_suzun_vslu = _get_day_value(master_df,"V_suzun_vslu",n)
    V_suzun_tng = _get_day_value(master_df,"V_suzun_tng",n)
    Q_suzun = _get_day_value(master_df,"Q_suzun",n)
    Q_vslu = _get_day_value(master_df,"Q_vslu",n)
    K_delta_g_suzun = _get_day_value(master_df,"K_delta_g_suzun",n)
    G_suzun_vslu = _get_day_value(master_df,"G_suzun_vslu",n)
    G_suzun_tng = _get_day_value(master_df,"G_suzun_tng",n)
    G_payaha  = _get_day_value(master_df,"G_payaha",n)
    V_suzun_slu_prev = _get_day_value(master_df,"V_suzun_slu",prev_day)
    V_upn_lodochny = _get_day_value(master_df,"V_upn_lodochny",n)
    V_ichem = _get_day_value(master_df,"V_ichem",n)
    Q_lodochny = _get_day_value(master_df,"Q_lodochny",n)
    Q_vo = _get_day_value(master_df,"Q_vo",n)
    G_lodochny_upsv_yu = _get_day_value(master_df,"G_lodochny_upsv_yu",n)
    K_otkachki = _get_day_value(master_df,"K_otkachki",n)
    V_upn_lodochny_prev = _get_day_value(master_df,"V_upn_lodochny",prev_day)
    K_delta_g_upn_lodochny = _get_day_value(master_df,"K_delta_g_upn_lodochny",n)
    G_ichem = _get_day_value(master_df,"G_ichem",n)
    G_tagul = _get_day_value(master_df,"G_tagul",n)
    G_kchng = _get_day_value(master_df,"G_kchng",n)
    V_upsv_yu = _get_day_value(master_df,"V_upsv_yu",n)
    V_upsv_s = _get_day_value(master_df,"V_upsv_s",n)
    V_cps = _get_day_value(master_df,"V_cps",n)
    G_buying_oil = _get_day_value(master_df,"G_buying_oil",n)
    G_per = _get_day_value(master_df,"G_per",n)
    Q_vankor = _get_day_value(master_df,"Q_vankor",n)
    V_upsv_yu_prev = _get_day_value(master_df,"V_upsv_yu",prev_day)
    V_upsv_s_prev = _get_day_value(master_df,"V_upsv_s",prev_day)
    V_cps_prev = _get_day_value(master_df,"V_cps",prev_day)
    G_sikn_tng = _get_day_value(master_df,"G_sikn_tng",n)
    G_sikn_tagul = _get_day_value(master_df,"G_sikn_tagul",n)
    V_cppn_1_0 = _get_day_value(master_df,"V_cppn_1_0",prev_month)
    V_gnps_0 = _get_day_value(master_df,"V_gnps",prev_month)
    VN_gnps_min = _get_const(master_df,"VN_gnps_min")

    return{
        "V_upn_suzun":V_upn_suzun,
        "V_upn_suzun_prev":V_upn_suzun_prev,
        "V_suzun_vslu":V_suzun_vslu,
        "V_suzun_tng":V_suzun_tng,
        "VN_gnps_min":VN_gnps_min,
        "Q_suzun":Q_suzun,
        "Q_vslu":Q_vslu,
        "K_delta_g_suzun":K_delta_g_suzun,
        "G_suzun_vslu":G_suzun_vslu,
        "G_suzun_tng":G_suzun_tng,
        "G_payaha":G_payaha,
        "V_suzun_slu_prev":V_suzun_slu_prev,
        "V_upn_lodochny":V_upn_lodochny,
        "V_ichem":V_ichem,
        "Q_lodochny":Q_lodochny,
        "Q_vo":Q_vo,
        "G_lodochny_upsv_yu":G_lodochny_upsv_yu,
        "K_otkachki":K_otkachki,
        "V_upn_lodochny_prev":V_upn_lodochny_prev,
        "K_delta_g_upn_lodochny":K_delta_g_upn_lodochny,
        "G_ichem":G_ichem,
        "G_tagul":G_tagul,
        "G_kchng":G_kchng,
        "V_upsv_yu":V_upsv_yu,
        "V_upsv_s":V_upsv_s,
        "V_cps":V_cps,
        "G_buying_oil":G_buying_oil,
        "G_per":G_per,
        "V_upsv_yu_prev":V_upsv_yu_prev,
        "Q_vankor":Q_vankor,
        "V_upsv_s_prev":V_upsv_s_prev,
        "V_cps_prev":V_cps_prev,
        "G_sikn_tng":G_sikn_tng,
        "G_sikn_tagul":G_sikn_tagul,
        "V_gnps_0":V_gnps_0,
        "N":N,
        "V_cppn_1_0":V_cppn_1_0,
    }

def vankor_data(master_df,n,N,day,prev_day):
    F_vn_month = _get_const(master_df, "F_vn_month")
    F_suzun_month = _get_const(master_df, "F_suzun_month")
    V_tstn_suzun_vslu_norm = _get_const(master_df, "V_tstn_suzun_vslu_norm")
    F_tagul_lpu_month = _get_const(master_df, "F_tagul_lpu_month")
    F_tagul_tpu_month = _get_const(master_df, "F_tagul_tpu_month")
    F_skn_month = _get_const(master_df, "F_skn_month")
    F_vo_month = _get_const(master_df, "F_vo_month")
    F_kchng_month = _get_const(master_df,"F_kchng_month")
    e_suzun = _get_day_value(master_df,"e_suzun",n)
    e_vo = _get_day_value(master_df,"e_vo",n)
    e_kchng = _get_day_value(master_df,"e_kchng",n)
    e_tng = _get_day_value(master_df,"e_tng",n)
    F_tng_month = _get_const(master_df,"F_tng_month")
    G_suzun_vslu = _get_day_value(master_df,"G_suzun_vslu",n)
    F_suzun_vankor_month = _get_day_value(master_df,"F_suzun_vankor_month",n)
    F_bp_suzun_vankor = _get_day_value(master_df,"F_bp_suzun_vankor",n)
    V_tstn_suzun_vslu_prev = _get_day_value(master_df, "V_tstn_suzun_vslu",prev_day)
    F_bp_vn = _get_day_value(master_df, "F_bp_vn",n)
    F_bp_suzun = _get_day_value(master_df, "F_bp_suzun",n)
    F_bp_suzun_vslu = _get_day_value(master_df, "F_bp_suzun_vslu",prev_day)
    F_bp_tagul_lpu = _get_day_value(master_df, "F_bp_tagul_lpu",n)
    F_bp_tagul_tpu = _get_day_value(master_df, "F_bp_tagul_tpu",n)
    F_bp_skn = _get_day_value(master_df, "F_bp_skn",n)
    F_bp_vo = _get_day_value(master_df, "F_bp_vo",n)
    F_bp_tng = _get_day_value(master_df, "F_bp_tng",n)
    F_bp_kchng = _get_day_value(master_df, "F_bp_kchng",n)
    return{
        "F_vn_month":F_vn_month,
        "F_suzun_month":F_suzun_month,
        "V_tstn_suzun_vslu_norm":V_tstn_suzun_vslu_norm,
        "F_tagul_lpu_month":F_tagul_lpu_month,
        "F_tagul_tpu_month":F_tagul_tpu_month,
        "F_skn_month":F_skn_month,
        "F_vo_month":F_vo_month,
        "F_kchng_month":F_kchng_month,
        "e_suzun":e_suzun,
        "e_vo":e_vo,
        "e_kchng":e_kchng,
        "e_tng":e_tng,
        "F_tng_month":F_tng_month,
        "G_suzun_vslu":G_suzun_vslu,
        "F_suzun_vankor_month":F_suzun_vankor_month,
        "F_bp_suzun_vankor":F_bp_suzun_vankor,
        "V_tstn_suzun_vslu_prev":V_tstn_suzun_vslu_prev,
        "N":N,
        "day":day,
        "F_bp_vn":F_bp_vn,
        "F_bp_suzun":F_bp_suzun,
        "F_bp_suzun_vslu":F_bp_suzun_vslu,
        "F_bp_tagul_lpu":F_bp_tagul_lpu,
        "F_bp_tagul_tpu":F_bp_tagul_tpu,
        "F_bp_skn":F_bp_skn,
        "F_bp_vo":F_bp_vo,
        "F_bp_tng":F_bp_tng,
        "F_bp_kchng":F_bp_kchng,
    }
def get_availability_and_pumping_data(master_df, n, N, month, prev_day):
    G_suzun_vslu = _get_day_value(master_df, "G_suzun_vslu",n)
    G_sikn = _get_day_value(master_df, "G_sikn",n)
    V_gnps_prev = _get_day_value(master_df, "V_gnps",prev_day)
    # month здесь — номер месяца (1..12), поэтому берём ряд значений за месяц
    G_gpns_i = _get_month_values(master_df, "G_gpns_i", month)
    return {
        "N":N,
        "G_suzun_vslu":G_suzun_vslu,
        "G_sikn":G_sikn,
        "V_gnps_prev":V_gnps_prev,
        "G_gpns_i":G_gpns_i,
    }
def get_month_data(master_df,month):
    Q_vankor = _get_month_values(master_df,"Q_vankor",month)
    Q_suzun = _get_month_values(master_df,"Q_suzun",month)
    Q_vslu =  _get_month_values(master_df,"Q_vslu",month)
    Q_tng = _get_month_values(master_df,"Q_tng",month)
    Q_vo = _get_month_values(master_df,"Q_vo",month)
    Q_lodochny = _get_month_values(master_df,"Q_lodochny",month)
    G_suzun_vslu = _get_month_values(master_df,"G_suzun_vslu",month)
    G_suzun_slu = _get_month_scalar_values(master_df, "G_suzun_slu", month)
    G_suzun = _get_month_values(master_df,"G_suzun",month)
    delta_G_suzun = _get_month_values(master_df,"delta_G_suzun",month)
    G_upn_lodochny_ichem = _get_month_values(master_df,"G_upn_lodochny_ichem",month)
    Q_kchng = _get_month_values(master_df,"Q_kchng",month)
    G_kchng = _get_month_values(master_df,"G_kchng",month)
    G_sikn_tagul = _get_month_scalar_values(master_df, "G_sikn_tagul", month)
    delta_G_upn_lodochny = _get_month_values(master_df,"delta_G_upn_lodochny",month)
    G_tagul = _get_month_values(master_df,"G_tagul",month)
    delta_G_tagul = _get_month_values(master_df,"delta_G_tagul",month)
    G_tagul_lodochny = _get_month_values(master_df,"G_tagul_lodochny",month)
    G_lodochny = _get_month_values(master_df,"G_lodochny",month)
    G_sikn_vslu = _get_month_values(master_df,"G_sikn_vslu",month)
    G_sikn_suzun = _get_month_values(master_df,"G_sikn_suzun",month)
    G_sikn_tng = _get_month_values(master_df,"G_sikn_tng",month)
    G_sikn = _get_month_values(master_df,"G_sikn",month)
    G_sikn_vankor = _get_month_values(master_df,"G_sikn_vankor",month)
    G_skn = _get_month_values(master_df,"G_skn",month)
    delta_G_sikn = _get_month_values(master_df,"delta_G_sikn",month)
    # month_calc ожидает суточный ряд G_per, а не месячную сумму
    G_per = _get_month_values(master_df,"G_per",month)
    V_ichem = _get_month_values(master_df,"V_ichem",month)
    G_upn_lodochny = _get_month_values(master_df,"G_upn_lodochny",month)
    return{
        "Q_vankor":Q_vankor,
        "Q_suzun":Q_suzun,
        "Q_vslu":Q_vslu,
        "Q_tng":Q_tng,
        "Q_vo":Q_vo,
        "Q_lodochny":Q_lodochny,
        "G_suzun_vslu":G_suzun_vslu,
        "G_sikn":G_sikn,
        "G_sikn_tagul":G_sikn_tagul,
        "G_sikn_suzun":G_sikn_suzun,
        "G_sikn_tng":G_sikn_tng,
        "G_suzun_slu":G_suzun_slu,
        "G_sikn_vankor":G_sikn_vankor,
        "G_skn":G_skn,
        "delta_G_sikn":delta_G_sikn,
        "delta_G_upn_lodochny":delta_G_upn_lodochny,
        "delta_G_tagul":delta_G_tagul,
        "G_suzun":G_suzun,
        "G_sikn_vslu":G_sikn_vslu,
        "G_lodochny":G_lodochny,
        "G_tagul_lodochny":G_tagul_lodochny,
        "delta_G_suzun":delta_G_suzun,
        "G_tagul":G_tagul,
        "G_upn_lodochny_ichem":G_upn_lodochny_ichem,
        "G_kchng":G_kchng,
        "Q_kchng":Q_kchng,
        "G_per":G_per,
        "V_ichem":V_ichem,
        "G_upn_lodochny":G_upn_lodochny,
    }

def get_auto_balance_volumes(master_df, n, prev_day, N, prev_month):
    V_upn_suzun_prev = _get_day_value(master_df,"V_upn_suzun",prev_day)
    Start_autobalance = _get_day_value(master_df,"Start_autobalance",n)
    V_upn_suzun_0 = _get_day_value(master_df,"V_upn_suzun",prev_month)
    VN_upn_suzun_min = _get_const(master_df,"VN_upn_suzun_min")
    V_upn_lodochny_0 = _get_day_value(master_df,"V_upn_lodochny",prev_month)
    VN_upn_lodochny_min = _get_const(master_df,"VN_upn_lodochny_min")
    V_upsv_yu_0 = _get_day_value(master_df,"V_upsv_yu",prev_month)
    VN_upsv_yu_min = _get_const(master_df,"VN_upsv_yu_min")
    V_upsv_s_0 = _get_day_value(master_df,"V_upsv_s_0",prev_month)
    VN_upsv_s_min = _get_const(master_df,"VN_upsv_s_min")
    V_cps_0 = _get_day_value(master_df,"V_cps",prev_month)
    VN_cps_min = _get_const(master_df,"VN_cps_min")
    V_upn_lodochny_prev = _get_day_value(master_df,"V_upn_lodochny",prev_day)
    V_upsv_yu_prev = _get_day_value(master_df,"V_upsv_yu",prev_day)
    V_upsv_s_prev = _get_day_value(master_df,"V_upsv_s",prev_day)
    V_cps_prev = _get_day_value(master_df,"V_cps",prev_day)
    # Текущее значение (нужно для ветки Start_autobalance=False)
    V_upn_suzun = _get_day_value(master_df,"V_upn_suzun",n)
    return {
        "V_upn_suzun_prev":V_upn_suzun_prev,
        "Start_autobalance":Start_autobalance,
        "V_upn_suzun_0":V_upn_suzun_0,
        "VN_upn_suzun_min":VN_upn_suzun_min,
        "V_upn_lodochny_0":V_upn_lodochny_0,
        "VN_upn_lodochny_min":VN_upn_lodochny_min,
        "V_upsv_yu_0":V_upsv_yu_0,
        "VN_upsv_yu_min":VN_upsv_yu_min,
        "V_upsv_s_0":V_upsv_s_0,
        "V_cps_0":V_cps_0,
        "VN_cps_min":VN_cps_min,
        "VN_upsv_s_min":VN_upsv_s_min,
        "V_upn_lodochny_prev":V_upn_lodochny_prev,
        "V_upsv_yu_prev":V_upsv_yu_prev,
        "V_upsv_s_prev":V_upsv_s_prev,
        "V_cps_prev":V_cps_prev,
        "V_upn_suzun":V_upn_suzun,
        "N":N
    }

def get_balance_data(master_df, n, prev_day):
    Start_autobalance = _get_day_value(master_df,"Start_autobalance",n)
    V_tstn_suzun_norm = _get_const(master_df,"V_tstn_suzun_norm")
    VN_knps_min = _get_const(master_df,"VN_knps_min")
    V_tstn_kchng_norm = _get_const(master_df,"V_tstn_kchng_norm")
    V_tstn_tng_norm = _get_const(master_df,"V_tstn_tng_norm")
    V_tstn_vo_norm = _get_const(master_df,"V_tstn_vo_norm")
    V_tstn_skn_norm = _get_const(master_df,"V_tstn_skn_norm")
    V_tstn_tagul_norm = _get_const(master_df,"V_tstn_tagul_norm")
    V_tstn_suzun_vankor_norm = _get_const(master_df,"V_tstn_suzun_vankor_norm")
    V_tstn_vn_norm = _get_const(master_df,"V_tstn_vn_norm")
    V_tstn_lodochny_norm = _get_const(master_df,"V_tstn_lodochny_norm")

    V_nps_1 = _get_day_value(master_df,"V_nps_1",n)
    V_nps_2 = _get_day_value(master_df,"V_nps_2",n)
    G_suzun_slu = _get_day_value(master_df,"G_suzun_slu",n)
    K_suzun = _get_day_value(master_df,"K_suzun",n)
    G_gnps = _get_day_value(master_df,"G_gnps",n)
    G_tagul = _get_day_value(master_df,"G_tagul",n)
    G_upn_lodochny = _get_day_value(master_df,"G_upn_lodochny",n)
    G_skn = _get_day_value(master_df,"G_skn",n)
    G_kchng = _get_day_value(master_df,"G_kchng",n)
    G_buying_oil = _get_day_value(master_df,"G_buying_oil",n)
    G_suzun_tng = _get_day_value(master_df,"G_suzun_tng",n)
    K_payaha = _get_day_value(master_df,"K_payaha",n)
    K_ichem = _get_day_value(master_df,"K_ichem",n)
    G_ichem = _get_day_value(master_df,"G_ichem",n)
    K_skn = _get_day_value(master_df,"K_skn",n)
    K_tagul = _get_day_value(master_df,"K_tagul",n)
    G_per = _get_day_value(master_df,"G_per",n)
    G_sikn_tagul = _get_day_value(master_df,"G_sikn_tagul",n)
    G_lodochny = _get_day_value(master_df,"G_lodochny",n)
    V_gnps = _get_day_value(master_df,"V_gnps",n)
    V_tstn_rn_vn = _get_day_value(master_df,"V_tstn_rn_vn",n)
    K_vankor = _get_day_value(master_df,"K_vankor",n)
    K_lodochny = _get_day_value(master_df,"K_lodochny",n)
    F_bp = _get_day_value(master_df,"F_bp",n)
    G_suzun_vslu = _get_day_value(master_df,"G_suzun_vslu",n)


    V_tstn_suzun_prev = _get_day_value(master_df,"V_tstn_suzun",prev_day)
    V_tstn_suzun_vslu_prev = _get_day_value(master_df,"V_tstn_suzun_vslu",prev_day)
    V_nps_2_prev = _get_day_value(master_df,"V_nps_2",prev_day)
    V_nps_1_prev = _get_day_value(master_df,"V_nps_1",prev_day)
    V_tstn_suzun_vankor_prev = _get_day_value(master_df,"V_tstn_suzun_vankor",prev_day)
    V_tstn_tagul_prev = _get_day_value(master_df,"V_tstn_tagul",prev_day)
    V_knps_prev = _get_day_value(master_df,"V_knps",prev_day)
    V_tstn_lodochny_prev = _get_day_value(master_df,"V_tstn_lodochny",prev_day)
    V_tstn_skn_prev = _get_day_value(master_df,"V_tstn_skn",prev_day)
    V_tstn_tng_prev = _get_day_value(master_df,"V_tstn_tng",prev_day)
    V_tstn_vo_prev = _get_day_value(master_df,"V_tstn_vo",prev_day)
    V_tstn_kchng_prev = _get_day_value(master_df,"V_tstn_kchng",prev_day)

    F_bp_tagul_lpu = _get_day_value(master_df,"F_bp_tagul_lpu",n)
    F_bp_tagul_tpu = _get_day_value(master_df,"F_bp_tagul_tpu",n)
    F_bp_suzun_vankor = _get_day_value(master_df,"F_bp_suzun_vankor",n)
    F_bp_suzun_vslu = _get_day_value(master_df,"F_bp_suzun_vslu",n)
    F_bp_skn = _get_day_value(master_df,"F_bp_skn",n)
    F_bp_vo = _get_day_value(master_df,"F_bp_vo",n)
    F_bp_tng = _get_day_value(master_df,"F_bp_tng",n)
    F_bp_kchng = _get_day_value(master_df,"F_bp_kchng",n)
    F_bp_vn = _get_day_value(master_df,"F_bp_vn",n)
    F_bp_suzun = _get_day_value(master_df,"F_bp_suzun",n)


    return{
        "Start_autobalance":Start_autobalance,
        "V_tstn_suzun_norm":V_tstn_suzun_norm,
        "VN_knps_min":VN_knps_min,
        "V_tstn_kchng_norm":V_tstn_kchng_norm,
        "V_tstn_tng_norm":V_tstn_tng_norm,
        "V_tstn_vo_norm":V_tstn_vo_norm,
        "V_tstn_skn_norm":V_tstn_skn_norm,
        "V_tstn_tagul_norm":V_tstn_tagul_norm,
        "V_tstn_suzun_vankor_norm":V_tstn_suzun_vankor_norm,
        "V_tstn_vn_norm":V_tstn_vn_norm,
        "V_tstn_lodochny_norm":V_tstn_lodochny_norm,
        "V_nps_1":V_nps_1,
        "V_nps_2":V_nps_2,
        "G_suzun_slu":G_suzun_slu,
        "K_suzun":K_suzun,
        "G_gnps":G_gnps,
        "G_tagul":G_tagul,
        "G_upn_lodochny":G_upn_lodochny,
        "G_skn":G_skn,
        "G_kchng":G_kchng,
        "G_buying_oil":G_buying_oil,
        "G_suzun_tng":G_suzun_tng,
        "K_payaha":K_payaha,
        "K_ichem":K_ichem,
        "G_ichem":G_ichem,
        "K_skn":K_skn,
        "K_tagul":K_tagul,
        "G_per":G_per,
        "G_sikn_tagul":G_sikn_tagul,
        "G_lodochny":G_lodochny,
        "V_gnps":V_gnps,
        "V_tstn_rn_vn":V_tstn_rn_vn,
        "K_vankor":K_vankor,
        "K_lodochny":K_lodochny,
        "V_tstn_suzun_prev":V_tstn_suzun_prev,
        "V_tstn_suzun_vslu_prev":V_tstn_suzun_vslu_prev,
        "V_nps_2_prev":V_nps_2_prev,
        "V_nps_1_prev":V_nps_1_prev,
        "V_tstn_suzun_vankor_prev":V_tstn_suzun_vankor_prev,
        "V_tstn_tagul_prev":V_tstn_tagul_prev,
        "V_knps_prev":V_knps_prev,
        "V_tstn_lodochny_prev":V_tstn_lodochny_prev,
        "V_tstn_skn_prev":V_tstn_skn_prev,
        "V_tstn_tng_prev":V_tstn_tng_prev,
        "V_tstn_vo_prev":V_tstn_vo_prev,
        "V_tstn_kchng_prev":V_tstn_kchng_prev,
        "F_bp_tagul_lpu":F_bp_tagul_lpu,
        "F_bp_tagul_tpu":F_bp_tagul_tpu,
        "F_bp_suzun_vankor":F_bp_suzun_vankor,
        "F_bp_suzun_vslu":F_bp_suzun_vslu,
        "F_bp_skn":F_bp_skn,
        "F_bp_vo":F_bp_vo,
        "F_bp_tng":F_bp_tng,
        "F_bp_kchng":F_bp_kchng,
        "F_bp_vn":F_bp_vn,
        "F_bp_suzun":F_bp_suzun,
        "F_bp":F_bp,
        "G_suzun_vslu":G_suzun_vslu,
 }

def get_bp_month_data(master_df, month, N, day):
    F_suzun_vankor = _get_month_scalar_values(master_df,"F_suzun_vankor",month )
    F_tagul_lpu = _get_month_scalar_values(master_df,"F_tagul_lpu",month )
    F_tagul_tpu = _get_month_scalar_values(master_df,"F_tagul_tpu",month )
    F_vn = _get_month_scalar_values(master_df,"F_vn",month )
    F = _get_month_scalar_values(master_df,"F",month )
    F_skn = _get_month_scalar_values(master_df,"F_skn",month )
    F_vo = _get_month_scalar_values(master_df,"F_vo",month )
    F_tng = _get_month_scalar_values(master_df,"F_tng",month )
    F_kchng = _get_month_scalar_values(master_df,"F_kchng",month )
    F_suzun_vslu = _get_month_scalar_values(master_df,"F_suzun_vslu",month )
    F_tagul = _get_month_scalar_values(master_df,"F_tagul",month )
    return{
        "F_suzun_vankor":F_suzun_vankor,
        "F_tagul_lpu":F_tagul_lpu,
        "F_tagul_tpu":F_tagul_tpu,
        "F_vn":F_vn,
        "F":F,
        "F_skn":F_skn,
        "F_vo":F_vo,
        "F_tng":F_tng,
        "F_kchng":F_kchng,
        "F_suzun_vslu":F_suzun_vslu,
        "F_tagul":F_tagul,
        "N":N,
        "day":day
    }
def get_availability_oil_data (master_df, n, prev_day):
    V_tstn_suzun_vslu_prev = _get_day_value(master_df,"V_tstn_suzun_vslu",prev_day)
    F_suzun_vslu = _get_day_value(master_df,"F_suzun_vslu",n)
    G_suzun_vslu = _get_day_value(master_df,"G_suzun_vslu",n)
    K_suzun = _get_day_value(master_df,"K_suzun",n)
    V_tstn_tagul_prev = _get_day_value(master_df,"V_tstn_tagul",prev_day)
    G_tagul = _get_day_value(master_df,"G_tagul",n)
    F_tagul_tpu = _get_day_value(master_df,"F_tagul_tpu",n)
    K_tagul = _get_day_value(master_df,"K_tagul",n)
    V_tstn_lodochny_prev = _get_day_value(master_df,"V_tstn_lodochny",prev_day)
    G_sikn_tagul = _get_day_value(master_df,"G_sikn_tagul",n)
    G_lodochny = _get_day_value(master_df,"G_lodochny",n)
    F_tagul_lpu = _get_day_value(master_df,"F_tagul_lpu",n)
    K_lodochny = _get_day_value(master_df,"K_lodochny",n)
    V_tstn_suzun_prev = _get_day_value(master_df,"V_tstn_suzun",prev_day)
    F_suzun = _get_day_value(master_df,"F_suzun",n)
    G_suzun_slu = _get_day_value(master_df,"G_suzun_slu",n)
    V_tstn_suzun_vankor_prev = _get_day_value(master_df,"V_tstn_suzun_vankor",prev_day)
    F_suzun_vankor = _get_day_value(master_df,"F_suzun_vankor",n)
    G_buying_oil = _get_day_value(master_df,"G_buying_oil",n)
    G_per = _get_day_value(master_df,"G_per",n)
    K_vankor = _get_day_value(master_df,"K_vankor",n)
    V_tstn_skn_prev = _get_day_value(master_df,"V_tstn_skn",prev_day)
    F_skn = _get_day_value(master_df,"F_skn",n)
    G_skn = _get_day_value(master_df,"G_skn",n)
    K_skn = _get_day_value(master_df,"K_skn",n)
    V_tstn_vo_prev = _get_day_value(master_df,"V_tstn_vo",prev_day)
    G_ichem = _get_day_value(master_df,"G_ichem",n)
    F_vo = _get_day_value(master_df,"F_vo",n)
    K_ichem = _get_day_value(master_df,"K_ichem",n)
    K_payaha = _get_day_value(master_df,"K_payaha",n)
    F_tng = _get_day_value(master_df,"F_tng",n)
    V_tstn_tng_prev = _get_day_value(master_df,"V_tstn_tng",prev_day)
    G_suzun_tng = _get_day_value(master_df,"G_suzun_tng",n)
    V_tstn_kchng_prev = _get_day_value(master_df,"V_tstn_kchng",prev_day)
    G_kchng = _get_day_value(master_df,"G_kchng",n)
    F_kchng = _get_day_value(master_df,"F_kchng",n)
    G_upn_lodochny = _get_day_value(master_df,"G_upn_lodochny",n)
    V_knps_prev = _get_day_value(master_df,"V_knps",prev_day)
    F = _get_day_value(master_df,"F",n)
    G_gnps = _get_day_value(master_df,"G_gnps",n)
    V_nps_2 = _get_day_value(master_df,"V_nps_2",n)
    V_nps_1 = _get_day_value(master_df,"V_nps_1",n)
    V_nps_2_prev = _get_day_value(master_df,"V_nps_2",prev_day)
    V_nps_1_prev = _get_day_value(master_df,"V_nps_1",prev_day)
    V_gnps = _get_day_value(master_df,"V_gnps",n)
    V_tstn_rn_vn = _get_day_value(master_df,"V_tstn_rn_vn",n)
    return{
        "V_tstn_suzun_vslu_prev":V_tstn_suzun_vslu_prev,
        "F_suzun_vslu":F_suzun_vslu,
        "G_suzun_vslu":G_suzun_vslu,
        "K_suzun":K_suzun,
        "V_tstn_tagul_prev":V_tstn_tagul_prev,
        "G_tagul":G_tagul,
        "F_tagul_tpu":F_tagul_tpu,
        "K_tagul":K_tagul,
        "V_tstn_lodochny_prev":V_tstn_lodochny_prev,
        "G_sikn_tagul":G_sikn_tagul,
        "G_lodochny":G_lodochny,
        "F_tagul_lpu":F_tagul_lpu,
        "K_lodochny":K_lodochny,
        "V_tstn_suzun_prev":V_tstn_suzun_prev,
        "F_suzun":F_suzun,
        "G_suzun_slu":G_suzun_slu,
        "V_tstn_suzun_vankor_prev":V_tstn_suzun_vankor_prev,
        "F_suzun_vankor":F_suzun_vankor,
        "G_buying_oil":G_buying_oil,
        "G_per":G_per,
        "K_vankor":K_vankor,
        "V_tstn_skn_prev":V_tstn_skn_prev,
        "F_skn":F_skn,
        "G_skn":G_skn,
        "K_skn":K_skn,
        "V_tstn_vo_prev":V_tstn_vo_prev,
        "G_ichem":G_ichem,
        "F_vo":F_vo,
        "K_ichem":K_ichem,
        "K_payaha":K_payaha,
        "F_tng":F_tng,
        "V_tstn_tng_prev":V_tstn_tng_prev,
        "G_suzun_tng":G_suzun_tng,
        "V_tstn_kchng_prev":V_tstn_kchng_prev,
        "G_kchng":G_kchng,
        "F_kchng":F_kchng,
        "G_upn_lodochny":G_upn_lodochny,
        "V_knps_prev":V_knps_prev,
        "F":F,
        "G_gnps":G_gnps,
        "V_nps_2":V_nps_2,
        "V_nps_1":V_nps_1,
        "V_nps_2_prev":V_nps_2_prev,
        "V_nps_1_prev":V_nps_1_prev,
        "V_gnps":V_gnps,
        "V_tstn_rn_vn":V_tstn_rn_vn,
}

def get_rn_vankor_check_data(master_df, n, prev_day):
    VA_upsv_yu_min = _get_const(master_df,"VA_upsv_yu_min")
    V_upsv_yu = _get_day_value(master_df,"V_upsv_yu",n)
    VA_upsv_yu_max = _get_const(master_df,"VA_upsv_yu_max")
    V_upsv_yu_prev = _get_day_value(master_df,"V_upsv_yu",prev_day)
    delta_V_upsv_yu_max = _get_const(master_df,"delta_V_upsv_yu_max")
    delta_VO_upsv_yu_max = _get_const(master_df,"delta_VO_upsv_yu_max")
    VA_upsv_s_min = _get_const(master_df,"VA_upsv_s_min")
    V_upsv_s = _get_day_value(master_df,"V_upsv_s",n)
    VA_upsv_s_max = _get_const(master_df,"VA_upsv_s_max")
    V_upsv_s_prev = _get_day_value(master_df,"V_upsv_s",prev_day)
    delta_V_upsv_s_max = _get_const(master_df,"delta_V_upsv_s_max")
    delta_VO_upsv_s_max = _get_const(master_df,"delta_VO_upsv_s_max")
    VA_cps_min = _get_const(master_df,"VA_cps_min")
    V_cps = _get_day_value(master_df,"V_cps",n)
    VA_cps_max = _get_const(master_df,"VA_cps_max")
    V_cps_prev = _get_day_value(master_df,"V_cps",prev_day)
    delta_V_cps_max = _get_const(master_df,"delta_V_cps_max")
    delta_VO_cps_max = _get_const(master_df,"delta_VO_cps_max")
    VA_upn_suzun_min = _get_const(master_df,"VA_upn_suzun_min")
    V_upn_suzun = _get_day_value(master_df,"V_upn_suzun",n)
    VA_upn_suzun_max = _get_const(master_df,"VA_upn_suzun_max")
    V_upn_suzun_prev = _get_day_value(master_df,"V_upn_suzun",prev_day)
    delta_V_upn_suzun_max = _get_const(master_df,"delta_V_upn_suzun_max")
    delta_VO_upn_suzun_max = _get_const(master_df,"delta_VO_upn_suzun_max")
    VA_upn_lodochny_min = _get_const(master_df,"VA_upn_lodochny_min")
    V_upn_lodochny = _get_day_value(master_df,"V_upn_lodochny",n)
    VA_upn_lodochny_max = _get_const(master_df,"VA_upn_lodochny_max")
    V_upn_lodochny_prev = _get_day_value(master_df,"V_upn_lodochny",prev_day)
    delta_V_upn_lodochny_max = _get_const(master_df,"delta_V_upn_lodochny_max")
    delta_VO_upn_lodochny_max = _get_const(master_df,"delta_VO_upn_lodochny_max")
    VA_tagul_min = _get_const(master_df,"VA_tagul_min")
    V_tagul_tr = _get_day_value(master_df,"V_tagul_tr",n)
    VA_tagul_max = _get_const(master_df,"VA_tagul_max")
    VA_gnps_min = _get_const(master_df,"VA_gnps_min")
    V_gnps = _get_day_value(master_df,"V_gnps",n)
    VA_gnps_max = _get_const(master_df,"VA_gnps_max")
    V_gnps_prev = _get_day_value(master_df,"V_gnps",prev_day)
    delta_V_gnps_max = _get_const(master_df,"delta_V_gnps_max")
    delta_VO_gnps_max = _get_const(master_df,"delta_VO_gnps_max")
    VA_nps_1_min = _get_const(master_df,"VA_nps_1_min")
    V_nps_1 = _get_day_value(master_df,"V_nps_1",n)
    VA_nps_1_max = _get_const(master_df,"VA_nps_1_max")
    V_nps_1_prev = _get_day_value(master_df,"V_nps_1",prev_day)
    delta_V_nps_1_max = _get_const(master_df,"delta_V_nps_1_max")
    delta_VO_nps_1_max = _get_const(master_df,"delta_VO_nps_1_max")
    VA_nps_2_min = _get_const(master_df,"VA_nps_2_min")
    V_nps_2 = _get_day_value(master_df,"V_nps_2",n)
    VA_nps_2_max = _get_const(master_df,"VA_nps_2_max")
    V_nps_2_prev = _get_day_value(master_df,"V_nps_2",prev_day)
    delta_V_nps_2_max = _get_const(master_df,"delta_V_nps_2_max")
    delta_VO_nps_2_max = _get_const(master_df,"delta_VO_nps_2_max")
    VN_knps_min = _get_const(master_df,"VN_knps_min")

    V_knps = _get_day_value(master_df,"V_knps",n)
    VA_knps_max = _get_const(master_df,"VA_knps_max")
    V_knps_prev = _get_day_value(master_df,"V_knps",prev_day)
    delta_V_knps_max = _get_const(master_df,"delta_V_knps_max")
    delta_VO_knps_max = _get_const(master_df,"delta_VO_knps_max")
    V_ichem_min = _get_const(master_df,"V_ichem_min")
    V_ichem = _get_day_value(master_df,"V_ichem",n)
    V_ichem_max = _get_const(master_df,"V_ichem_max")
    V_lodochny_cps_upsv_yu = _get_day_value(master_df,"V_lodochny_cps_upsv_yu",n)
    G_sikn_tagul = _get_day_value(master_df,"G_sikn_tagul",n)
    V_tstn_vn_min = _get_const(master_df,"V_tstn_vn_min")
    V_tstn_vn = _get_day_value(master_df,"V_tstn_vn",n)
    V_tstn_vn_max = _get_const(master_df,"V_tstn_vn_max")
    V_tstn_suzun_min = _get_const(master_df,"V_tstn_suzun_min")
    V_tstn_suzun = _get_day_value(master_df,"V_tstn_suzun",n)
    V_tstn_suzun_max = _get_const(master_df,"V_tstn_suzun_max")
    V_tstn_suzun_vankor_min = _get_const(master_df,"V_tstn_suzun_vankor_min")
    V_tstn_suzun_vankor = _get_day_value(master_df,"V_tstn_suzun_vankor",n)
    V_tstn_suzun_vankor_max = _get_const(master_df,"V_tstn_suzun_vankor_max")
    V_tstn_suzun_vslu_min = _get_const(master_df,"V_tstn_suzun_vslu_min")
    V_tstn_suzun_vslu = _get_day_value(master_df,"V_tstn_suzun_vslu",n)
    V_tstn_suzun_vslu_max = _get_const(master_df,"V_tstn_suzun_vslu_max")
    V_tstn_tagul_obsh_min = _get_const(master_df,"V_tstn_tagul_obsh_min")
    V_tstn_tagul_obsh = _get_day_value(master_df,"V_tstn_tagul_obsh",n)
    V_tstn_tagul_obsh_max = _get_const(master_df,"V_tstn_tagul_obsh_max")
    V_tstn_lodochny_min = _get_const(master_df,"V_tstn_lodochny_min")
    V_tstn_lodochny = _get_day_value(master_df,"V_tstn_lodochny",n)
    V_tstn_lodochny_max = _get_const(master_df,"V_tstn_lodochny_max")
    V_tstn_tagul_min = _get_const(master_df,"V_tstn_tagul_min")
    V_tstn_tagul = _get_day_value(master_df,"V_tstn_tagul",n)
    V_tstn_tagul_max = _get_const(master_df,"V_tstn_tagul_max")
    V_tstn_skn_min = _get_const(master_df,"V_tstn_skn_min")
    V_tstn_skn = _get_day_value(master_df,"V_tstn_skn",n)
    V_tstn_skn_max = _get_const(master_df,"V_tstn_skn_max")
    V_tstn_vo_min = _get_const(master_df,"V_tstn_vo_min")
    V_tstn_vo = _get_day_value(master_df,"V_tstn_vo",n)
    V_tstn_vo_max = _get_const(master_df,"V_tstn_vo_max")
    V_tstn_tng_min = _get_const(master_df,"V_tstn_tng_min")
    V_tstn_tng = _get_day_value(master_df,"V_tstn_tng",n)
    V_tstn_tng_max = _get_const(master_df,"V_tstn_tng_max")
    V_tstn_kchng_min = _get_const(master_df,"V_tstn_kchng_min")
    V_tstn_kchng = _get_day_value(master_df,"V_tstn_kchng",n)
    V_tstn_kchng_max = _get_const(master_df,"V_tstn_kchng_max")
    G_gnps = _get_day_value(master_df,"G_gnps",n)
    p_gnps = _get_day_value(master_df,"p_gnps",n)
    Q_gnps_min1 = _get_const(master_df,"Q_gnps_min1")
    Q_gnps_max2 = _get_const(master_df,"Q_gnps_max2")
    Q_gnps_max1 = _get_const(master_df,"Q_gnps_max1")
    G_tagul_lodochny = _get_day_value(master_df,"G_tagul_lodochny",n)
    p_nps_1_2 = _get_day_value(master_df,"p_nps_1_2",n)
    Q_nps_1_2_min1 = _get_const(master_df,"Q_nps_1_2_min1")
    Q_nps_1_2_max2 = _get_const(master_df,"Q_nps_1_2_max2")
    Q_nps_1_2_max1 = _get_const(master_df,"Q_nps_1_2_max1")
    p_knps = _get_day_value(master_df,"p_knps",n)
    Q_knps_min1 = _get_const(master_df,"Q_knps_min1")
    Q_knps_max2 = _get_const(master_df,"Q_knps_max2")
    Q_knps_max1 = _get_const(master_df,"Q_knps_max1")
    F = _get_day_value(master_df,"F",n)
    return{
        "VA_upsv_yu_min":VA_upsv_yu_min,
        "V_upsv_yu":V_upsv_yu,
        "VA_upsv_yu_max":VA_upsv_yu_max,
        "V_upsv_yu_prev":V_upsv_yu_prev,
        "delta_V_upsv_yu_max":delta_V_upsv_yu_max,
        "delta_VO_upsv_yu_max":delta_VO_upsv_yu_max,
        "VA_upsv_s_min":VA_upsv_s_min,
        "V_upsv_s":V_upsv_s,
        "VA_upsv_s_max":VA_upsv_s_max,
        "V_upsv_s_prev":V_upsv_s_prev,
        "delta_V_upsv_s_max":delta_V_upsv_s_max,
        "delta_VO_upsv_s_max":delta_VO_upsv_s_max,
        "VA_cps_min":VA_cps_min,
        "V_cps":V_cps,
        "VA_cps_max":VA_cps_max,
        "V_cps_prev":V_cps_prev,
        "delta_V_cps_max":delta_V_cps_max,
        "delta_VO_cps_max":delta_VO_cps_max,
        "VA_upn_suzun_min":VA_upn_suzun_min,
        "V_upn_suzun":V_upn_suzun,
        "VA_upn_suzun_max":VA_upn_suzun_max,
        "V_upn_suzun_prev":V_upn_suzun_prev,
        "delta_V_upn_suzun_max":delta_V_upn_suzun_max,
        "delta_VO_upn_suzun_max":delta_VO_upn_suzun_max,
        "VA_upn_lodochny_min":VA_upn_lodochny_min,
        "V_upn_lodochny":V_upn_lodochny,
        "VA_upn_lodochny_max":VA_upn_lodochny_max,
        "V_upn_lodochny_prev":V_upn_lodochny_prev,
        "delta_V_upn_lodochny_max":delta_V_upn_lodochny_max,
        "delta_VO_upn_lodochny_max":delta_VO_upn_lodochny_max,
        "VA_tagul_min":VA_tagul_min,
        "V_tagul_tr":V_tagul_tr,
        "VA_tagul_max":VA_tagul_max,
        "VA_gnps_min":VA_gnps_min,
        "V_gnps":V_gnps,
        "VA_gnps_max":VA_gnps_max,
        "V_gnps_prev":V_gnps_prev,
        "delta_V_gnps_max":delta_V_gnps_max,
        "delta_VO_gnps_max":delta_VO_gnps_max,
        "VA_nps_1_min":VA_nps_1_min,
        "V_nps_1":V_nps_1,
        "VA_nps_1_max":VA_nps_1_max,
        "V_nps_1_prev":V_nps_1_prev,
        "delta_V_nps_1_max":delta_V_nps_1_max,
        "delta_VO_nps_1_max":delta_VO_nps_1_max,
        "VA_nps_2_min":VA_nps_2_min,
        "V_nps_2":V_nps_2,
        "VA_nps_2_max":VA_nps_2_max,
        "V_nps_2_prev":V_nps_2_prev,
        "delta_V_nps_2_max":delta_V_nps_2_max,
        "delta_VO_nps_2_max":delta_VO_nps_2_max,
        "VN_knps_min":VN_knps_min,
        "V_knps":V_knps,
        "VA_knps_max":VA_knps_max,
        "V_knps_prev":V_knps_prev,
        "delta_V_knps_max":delta_V_knps_max,
        "delta_VO_knps_max":delta_VO_knps_max,
        "V_ichem_min":V_ichem_min,
        "V_ichem":V_ichem,
        "V_ichem_max":V_ichem_max,
        "V_lodochny_cps_upsv_yu":V_lodochny_cps_upsv_yu,
        "G_sikn_tagul":G_sikn_tagul,
        "V_tstn_vn_min":V_tstn_vn_min,
        "V_tstn_vn":V_tstn_vn,
        "V_tstn_vn_max":V_tstn_vn_max,
        "V_tstn_suzun_min":V_tstn_suzun_min,
        "V_tstn_suzun":V_tstn_suzun,
        "V_tstn_suzun_max":V_tstn_suzun_max,
        "V_tstn_suzun_vankor_min":V_tstn_suzun_vankor_min,
        "V_tstn_suzun_vankor":V_tstn_suzun_vankor,
        "V_tstn_suzun_vankor_max":V_tstn_suzun_vankor_max,
        "V_tstn_suzun_vslu_min":V_tstn_suzun_vslu_min,
        "V_tstn_suzun_vslu":V_tstn_suzun_vslu,
        "V_tstn_suzun_vslu_max":V_tstn_suzun_vslu_max,
        "V_tstn_tagul_obsh_min":V_tstn_tagul_obsh_min,
        "V_tstn_tagul_obsh":V_tstn_tagul_obsh,
        "V_tstn_tagul_obsh_max":V_tstn_tagul_obsh_max,
        "V_tstn_lodochny_min":V_tstn_lodochny_min,
        "V_tstn_lodochny":V_tstn_lodochny,
        "V_tstn_lodochny_max":V_tstn_lodochny_max,
        "V_tstn_tagul_min":V_tstn_tagul_min,
        "V_tstn_tagul":V_tstn_tagul,
        "V_tstn_tagul_max":V_tstn_tagul_max,
        "V_tstn_skn_min":V_tstn_skn_min,
        "V_tstn_skn":V_tstn_skn,
        "V_tstn_skn_max":V_tstn_skn_max,
        "V_tstn_vo_min":V_tstn_vo_min,
        "V_tstn_vo":V_tstn_vo,
        "V_tstn_vo_max":V_tstn_vo_max,
        "V_tstn_tng_min":V_tstn_tng_min,
        "V_tstn_tng":V_tstn_tng,
        "V_tstn_tng_max":V_tstn_tng_max,
        "V_tstn_kchng_min":V_tstn_kchng_min,
        "V_tstn_kchng":V_tstn_kchng,
        "V_tstn_kchng_max":V_tstn_kchng_max,
        "G_gnps":G_gnps,
        "p_gnps":p_gnps,
        "Q_gnps_min1":Q_gnps_min1,
        "Q_gnps_max2":Q_gnps_max2,
        "Q_gnps_max1":Q_gnps_max1,
        "G_tagul_lodochny":G_tagul_lodochny,
        "p_nps_1_2":p_nps_1_2,
        "Q_nps_1_2_min1":Q_nps_1_2_min1,
        "Q_nps_1_2_max2":Q_nps_1_2_max2,
        "Q_nps_1_2_max1":Q_nps_1_2_max1,
        "p_knps":p_knps,
        "Q_knps_min1":Q_knps_min1,
        "Q_knps_max2":Q_knps_max2,
        "Q_knps_max1":Q_knps_max1,
        "F":F,
    }

    