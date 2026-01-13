import numpy as np



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
    values = master_df.loc[master_df["date"] == date, column_name].values
    return _to_scalar(values) if scalar else values


def prepare_suzun_data(master_df, n, m, prev_days, prev_month, N):
    """Собирает все аргументы, которые в оригинале передавались в calculate.suzun."""
    # --- Покупка и отгрузка ---
    G_buy_month = _get_month_values(master_df, "buying_oil", m)
    G_out_udt_month = _get_month_values(master_df, "out_udt", m)
    # --- GTM данные ---
    Q_vankor = _get_month_values(master_df, "gtm_vn", m)
    Q_suzun = _get_month_values(master_df, "gtm_suzun", m)
    Q_vslu = _get_month_values(master_df, "gtm_vslu", m)
    Q_tng = _get_month_values(master_df, "gtm_taymyr", m)
    Q_vo = _get_month_values(master_df, "gtm_vostok", m)
    G_per_data = _get_month_values(master_df, "per_data", m)
    G_suzun_vslu_data = _get_month_values(master_df, "suzun_vslu_data", m)
    G_suzun_slu_data = _get_month_values(master_df, "suzun_slu_data", m)
    G_suzun_data = _get_month_values(master_df, "suzun_data", m)

    # --- Данные за текущий день ---
    Q_vslu_day = _get_day_value(master_df, "gtm_vslu", n, scalar=True)
    Q_suzun_day = _get_day_value(master_df, "gtm_suzun", n, scalar=True)
    # --- Предыдущий день ---
    V_suzun_tng_prev = _get_day_value(master_df, "suzun_tng", prev_days, scalar=True)
    V_upn_suzun_prev = _get_day_value(master_df, "upn_suzun", prev_days, scalar=True)
    V_suzun_vslu_prev = _get_day_value(master_df, "suzun_vslu", prev_days, scalar=True)
    # --- Конец прошлого месяца ---
    V_suzun_tng_0 = _get_day_value(master_df, "suzun_tng", prev_month, scalar=True)
    V_upn_suzun_0 = _get_day_value(master_df, "upn_suzun", prev_month, scalar=True)
    V_suzun_vslu_0 = _get_day_value(master_df, "suzun_vslu", prev_month, scalar=True)
    V_suzun_slu_prev = _get_day_value(master_df, "suzun_slu", prev_days, scalar=True)

    return {
        "G_buy_month":G_buy_month,
        "G_out_udt_month":G_out_udt_month,
        "N":N,
        "Q_vankor":Q_vankor,
        "Q_suzun":Q_suzun,
        "Q_vslu":Q_vslu,
        "Q_tng":Q_tng,
        "Q_vo":Q_vo,
        "G_per_data":G_per_data,
        "G_suzun_vslu_data":G_suzun_vslu_data,
        "G_suzun_data":G_suzun_data,
        "G_suzun_slu_data":G_suzun_slu_data,
        "V_suzun_tng_prev":V_suzun_tng_prev,
        "Q_vslu_day":Q_vslu_day,
        "V_upn_suzun_prev":V_upn_suzun_prev,
        "V_suzun_vslu_prev":V_suzun_vslu_prev,
        "Q_suzun_day":Q_suzun_day,
        "V_upn_suzun_0":V_upn_suzun_0,
        "V_suzun_vslu_0":V_suzun_vslu_0,
        "V_suzun_tng_0":V_suzun_tng_0,
        "V_suzun_slu_prev":V_suzun_slu_prev,

    }


def prepare_vo_data(master_df, n, m):
    Q_vo_day = _get_day_value(master_df, "gtm_vostok", n, scalar=True)
    G_upn_lodochny_ichem_data = _get_month_values(master_df, "upn_lodochny_ichem_data", m)

    return {"Q_vo_day": Q_vo_day, "G_upn_lodochny_ichem_data": G_upn_lodochny_ichem_data, "m": m}


def prepare_kchng_data(master_df, n, m):
    Q_kchng = _get_month_values(master_df, "kchng", m)
    Q_kchng_day = _get_day_value(master_df, "kchng", n, scalar=True)
    G_kchng_data = _get_month_values(master_df, "kchng_data", m)

    return {"Q_kchng_day": Q_kchng_day, "Q_kchng": Q_kchng, "G_kchng_data": G_kchng_data}


def prepare_lodochny_data(master_df, n, m, prev_days, prev_month, N, day, kchng_results):
    Q_tagulsk_prev_month = _get_day_value(master_df, "gtm_tagulsk", prev_month, scalar=True)
    G_lodochni_upsv_yu_prev_month = _get_day_value(master_df, "lodochni_upsv_yu", prev_month, scalar=True)
    Q_tagulsk = _get_month_values(master_df, "gtm_tagulsk", m)
    Q_lodochny = _get_month_values(master_df, "gtm_lodochny", m)
    Q_lodochny_day = _get_day_value(master_df, "gtm_lodochny", n, scalar=True)
    Q_tagulsk_day = _get_day_value(master_df, "gtm_tagulsk", n, scalar=True)
    V_upn_lodochny_prev = _get_day_value(master_df, "upn_lodochny", prev_days, scalar=True)
    V_ichem_prev = _get_day_value(master_df, "ichem", prev_days, scalar=True)
    G_lodochny_ichem = _get_day_value(master_df, "lodochny_ichem", n, scalar=True)
    V_tagul = _get_day_value(master_df, "tagul", n, scalar=True)
    V_tagul_prev = _get_day_value(master_df, "tagul", prev_days, scalar=True)
    G_lodochny_uspv_yu_data = _get_month_values(master_df, "lodochny_uspv_yu_data", m)
    G_sikn_tagul_data = _get_month_values(master_df, "sikn_tagul_data", m)
    G_tagul_data = _get_month_values(master_df, "tagul_data", m)
    delte_G_tagul_data = _get_month_values(master_df, "delte_tagul_data", m)
    G_lodochny_data = _get_month_values(master_df, "lodochny_data", m)
    delte_G_upn_lodochny_data = _get_month_values(master_df, "delte_upn_lodochny_data", m)
    G_tagul_lodochny_data = _get_month_values(master_df, "tagul_lodochny_data", m)

    return {
        "Q_tagul": Q_tagulsk,
        "Q_lodochny": Q_lodochny,
        "V_upn_lodochny_prev": V_upn_lodochny_prev,
        "V_ichem_prev": V_ichem_prev,
        "G_lodochny_ichem": G_lodochny_ichem,
        "Q_tagul_prev_month": Q_tagulsk_prev_month,
        "G_lodochni_upsv_yu_prev_month": G_lodochni_upsv_yu_prev_month,
        "N": N,
        "Q_vo_day": _get_day_value(master_df, "gtm_vostok", n, scalar=True),
        "Q_lodochny_day": Q_lodochny_day,
        "Q_tagul_day": Q_tagulsk_day,
        "V_tagul": V_tagul,
        "V_tagul_prev": V_tagul_prev,
        "G_kchng": kchng_results.get("G_kchng", 0),
        "day": day,
        "G_lodochny_uspv_yu_data": G_lodochny_uspv_yu_data,
        "G_sikn_tagul_data": G_sikn_tagul_data,
        "G_tagul_data": G_tagul_data,
        "delte_G_tagul_data": delte_G_tagul_data,
        "G_lodochny_data": G_lodochny_data,
        "delte_G_upn_lodochny_data": delte_G_upn_lodochny_data,
        "G_tagul_lodochny_data": G_tagul_lodochny_data
    }


def prepare_cppn1_data(master_df, n, prev_days, prev_month, lodochny_results):
    flag_list = [0, 0, 0]  # Для отслеживания остановки
    V_upsv_yu_0 = _get_day_value(master_df, "upsv_yu", prev_month, scalar=True)
    V_upsv_s_0 = _get_day_value(master_df, "upsv_s", prev_month, scalar=True)
    V_upsv_cps_0 = _get_day_value(master_df, "upsv_cps", prev_month, scalar=True)
    V_upsv_yu_prev = _get_day_value(master_df, "upsv_yu", prev_days, scalar=True)
    V_upsv_s_prev = _get_day_value(master_df, "upsv_s", prev_days, scalar=True)
    V_upsv_cps_prev = _get_day_value(master_df, "upsv_cps", prev_days, scalar=True)
    V_upsv_yu = _get_day_value(master_df, "upsv_yu", n, scalar=True)
    V_upsv_s = _get_day_value(master_df, "upsv_s", n, scalar=True)
    V_upsv_cps = _get_day_value(master_df, "upsv_cps", n, scalar=True)
    V_lodochny_cps_upsv_yu_prev = _get_day_value(master_df, "lodochny_cps_upsv_yu", prev_days, scalar=True)
    V_lodochny_upsv_yu = _get_day_value(master_df, "lodochny_upsv_yu", prev_days, scalar=True)
    return {
        "V_upsv_yu_prev":V_upsv_yu_prev,
        "V_upsv_s_prev":V_upsv_s_prev,
        "V_upsv_cps_prev":V_upsv_cps_prev,
        "V_upsv_yu_0":V_upsv_yu_0,
        "V_upsv_s_0":V_upsv_s_0,
        "V_upsv_cps_0":V_upsv_cps_0,
        "V_upsv_yu":V_upsv_yu,
        "V_upsv_s":V_upsv_s,
        "V_upsv_cps":V_upsv_cps,
        "V_lodochny_cps_upsv_yu_prev":V_lodochny_cps_upsv_yu_prev,
        "G_sikn_tagul":lodochny_results.get("G_sikn_tagul"),
        "V_lodochny_upsv_yu":V_lodochny_upsv_yu,
        "flag_list":flag_list
    }


def prepare_rn_vankor_data(master_df, n, prev_days, N, day, m):
    F_vn = _get_month_values(master_df, "volume_vankor", m)
    F_suzun_obsh = _get_month_values(master_df, "volume_suzun", m)
    F_suzun_vankor = _get_month_values(master_df, "suzun_vankor", m)
    V_ctn_suzun_vslu_norm = _get_day_value(master_df, "ctn_suzun_vslu_norm", prev_days, scalar=True)
    V_ctn_suzun_vslu = _get_day_value(master_df, "ctn_suzun_vslu", n, scalar=True)
    F_tagul_lpu = _get_month_values(master_df, "volume_lodochny", m)
    F_tagul_tpu = _get_month_values(master_df, "volume_tagulsk", m)
    F_skn = _get_day_value(master_df, "skn", n, scalar=True)
    F_vo = _get_month_values(master_df, "volume_vostok_oil", m)
    F_kchng = _get_month_values(master_df, "volum_kchng", m)
    F_bp_data = _get_month_values(master_df, "bp_data", m)
    F_bp_vn_data = _get_month_values(master_df, "bp_vn_data", m)
    F_bp_suzun_data = _get_month_values(master_df, "bp_suzun_data", m)
    F_bp_suzun_vankor_data = _get_month_values(master_df, "bp_suzun_vankor_data", m)
    F_bp_suzun_vslu_data = _get_month_values(master_df, "bp_suzun_vslu_data", m)
    F_bp_tagul_lpu_data = _get_month_values(master_df, "bp_tagul_lpu_data", m)
    F_bp_tagul_tpu_data = _get_month_values(master_df, "bp_tagul_tpu_data", m)
    F_bp_skn_data = _get_month_values(master_df, "bp_skn_data", m)
    F_bp_vo_data = _get_month_values(master_df, "bp_vo_data", m)
    F_bp_kchng_data = _get_month_values(master_df, "bp_kchng_data", m)

    return {
        "F_vn": F_vn,
        "F_suzun_obsh": F_suzun_obsh,
        "F_suzun_vankor": F_suzun_vankor,
        "N": N,
        "day": day,
        "V_ctn_suzun_vslu_norm": V_ctn_suzun_vslu_norm,
        "V_ctn_suzun_vslu": V_ctn_suzun_vslu,
        "F_tagul_lpu": F_tagul_lpu,
        "F_tagul_tpu": F_tagul_tpu,
        "F_skn": F_skn,
        "F_vo": F_vo,
        "F_kchng": F_kchng,
        "F_bp_data": F_bp_data,
        "F_bp_vn_data": F_bp_vn_data,
        "F_bp_suzun_data": F_bp_suzun_data,
        "F_bp_suzun_vankor_data": F_bp_suzun_vankor_data,
        "F_bp_suzun_vslu_data": F_bp_suzun_vslu_data,
        "F_bp_tagul_lpu_data": F_bp_tagul_lpu_data,
        "F_bp_tagul_tpu_data": F_bp_tagul_tpu_data,
        "F_bp_skn_data": F_bp_skn_data,
        "F_bp_vo_data": F_bp_vo_data,
        "F_bp_kchng_data": F_bp_kchng_data,
    }
def prepare_sikn_1208_data(master_df, n, prev_days, m, suzun_results, lodochny_results, G_suzun_tng, cppn1_results):
    G_suzun_sikn_data = _get_month_values(master_df, "suzun_sikn_data", m)
    G_sikn_suzun_data = _get_month_values(master_df, "sikn_suzun_data", m)
    G_suzun_tng_data = _get_month_values(master_df, "suzun_tng_data", m)
    G_sikn_data = _get_month_values(master_df, "sikn_data", m)
    G_sikn_vankor_data = _get_month_values(master_df, "sikn_vankor_data", m)
    G_skn_data = _get_month_values(master_df, "skn_data", m)

    Q_vankor = _get_day_value(master_df, "gtm_vn", n, scalar=True)
    V_upsv_yu = _get_day_value(master_df, "upsv_yu", n, scalar=True)
    V_upsv_s = _get_day_value(master_df, "upsv_s", n, scalar=True)
    V_upsv_cps = _get_day_value(master_df, "upsv_cps", n, scalar=True)
    V_upsv_yu_prev = _get_day_value(master_df, "upsv_yu", prev_days, scalar=True)
    V_upsv_s_prev = _get_day_value(master_df, "upsv_s", prev_days, scalar=True)
    V_upsv_cps_prev = _get_day_value(master_df, "upsv_cps", prev_days, scalar=True)
    return {
        "G_suzun_vslu": suzun_results.get("G_suzun_vslu"),
        "G_sikn_tagul_lod_data": lodochny_results.get("G_sikn_tagul_month"),
        "G_buy_day": suzun_results.get("G_buy_day"),
        "G_per": suzun_results.get("G_per"),
        "G_suzun": suzun_results.get("G_suzun"),
        "G_suzun_sikn_data": G_suzun_sikn_data,
        "G_sikn_suzun_data": G_sikn_suzun_data,
        "G_suzun_tng": G_suzun_tng,
        "G_suzun_tng_data": G_suzun_tng_data,
        "Q_vankor": Q_vankor,
        "V_upsv_yu": V_upsv_yu,
        "V_upsv_s": V_upsv_s,
        "V_upsv_cps": V_upsv_cps,
        "V_upsv_yu_prev": V_upsv_yu_prev,
        "V_upsv_s_prev": V_upsv_s_prev,
        "V_upsv_cps_prev": V_upsv_cps_prev,
        "G_lodochny_uspv_yu": lodochny_results.get("G_lodochny_uspv_yu"),
        "G_sikn_data": G_sikn_data,
        "G_sikn_vankor_data": G_sikn_vankor_data,
        "V_cppn_1": cppn1_results.get("V_cppn_1"),
        "G_skn_data": G_skn_data,
    }
def prepare_TSTN_data(master_df, n, prev_days, prev_month, m, N, sikn_1208_results, lodochny_results, kchng_results, suzun_results, G_ichem, G_suzun_tng):
    V_gnsp_0 = _get_day_value(master_df, "gnsp", prev_month, scalar=True)
    V_nps_1_0 = _get_day_value(master_df, "nps_1", prev_month, scalar=True)
    V_nps_2_0 = _get_day_value(master_df, "nps_2", prev_month, scalar=True)
    V_knps_0 = _get_day_value(master_df, "knps", prev_month, scalar=True)
    V_suzun_put_0 = _get_day_value(master_df, "suzun_put", prev_month, scalar=True)

    V_knps_prev = _get_day_value(master_df, "knps", prev_days, scalar=True)
    V_gnsp_prev = _get_day_value(master_df, "gnsp", prev_days, scalar=True)
    V_nps_1_prev = _get_day_value(master_df, "nps_1", prev_days, scalar=True)
    V_nps_2_prev = _get_day_value(master_df, "nps_2", prev_days, scalar=True)
    V_tstn_suzun_vslu_prev = _get_day_value(master_df, "tstn_vslu", prev_days, scalar=True)
    V_tstn_suzun_vankor_prev = _get_day_value(master_df, "tstn_suzun_vankor", prev_days, scalar=True)
    V_tstn_suzun_prev = _get_day_value(master_df, "tstn_suzun", prev_days, scalar=True)
    V_tstn_skn_prev = _get_day_value(master_df, "tstn_skn", prev_days, scalar=True)
    V_tstn_vo_prev = _get_day_value(master_df, "tstn_vo", prev_days, scalar=True)
    V_tstn_tng_prev = _get_day_value(master_df, "tstn_tng", prev_days, scalar=True)
    V_tstn_tagul_prev = _get_day_value(master_df, "tstn_tagul", prev_days, scalar=True)
    V_tstn_kchng_prev = _get_day_value(master_df, "tstn_kchng", prev_days, scalar=True)
    V_tstn_lodochny_prev = _get_day_value(master_df, "tstn_lodochny", prev_days, scalar=True)
    V_tstn_rn_vn_prev = _get_day_value(master_df, "tstn_rn_vn", prev_days, scalar=True)

    F_kchng = _get_month_values(master_df, "volum_kchng", m)
    G_gpns_data = _get_month_values(master_df, "gpns_data", m)
    F_suzun_vankor = _get_month_values(master_df, "suzun_vankor", m)
    F_vo = _get_month_values(master_df, "volume_vostok_oil", m)
    F_tng = _get_month_values(master_df, "volume_taymyr", m)
    F_tagul_lpu = _get_month_values(master_df, "volume_lodochny", m)

    F_skn = _get_day_value(master_df, "_F_skn", n, scalar=True)
    VN_min_gnsp = 2686.761
    flag_list = [0, 0, 0, 0]
    return {
        "V_gnsp_0": V_gnsp_0,
        "N": N,
        "VN_min_gnsp": VN_min_gnsp,
        "G_sikn": sikn_1208_results.get("G_sikn"),
        "G_gpns_data": G_gpns_data,
        "V_gnsp_prev": V_gnsp_prev,
        "flag_list": flag_list,
        "V_nps_1_prev": V_nps_1_prev,
        "V_nps_2_prev": V_nps_2_prev,
        "G_tagul": lodochny_results.get("G_tagul"),
        "G_upn_lodochny": lodochny_results.get("G_upn_lodochny"),
        "G_kchng": kchng_results.get("G_kchng"),
        "V_knps_prev": V_knps_prev,
        "V_nps_1_0": V_nps_1_0,
        "V_nps_2_0": V_nps_2_0,
        "V_knps_0": V_knps_0,
        "G_suzun_vslu": suzun_results.get("G_suzun_vslu"),
        "V_tstn_suzun_vslu_prev": V_tstn_suzun_vslu_prev,
        "F_suzun_vankor": F_suzun_vankor,
        "V_tstn_suzun_vankor_prev": V_tstn_suzun_vankor_prev,
        "G_buy_day": suzun_results.get("G_buy_day"),
        "G_per": suzun_results.get("G_per"),
        "V_suzun_put_0": V_suzun_put_0,
        "V_tstn_suzun_prev": V_tstn_suzun_prev,
        "G_suzun_slu": suzun_results.get("G_suzun_slu"),
        "V_tstn_skn_prev": V_tstn_skn_prev,
        "F_skn": F_skn,
        "V_tstn_vo_prev": V_tstn_vo_prev,
        "G_ichem": G_ichem,
        "F_vo": F_vo,
        "F_tng": F_tng,
        "G_suzun_tng": G_suzun_tng,
        "V_tstn_tng_prev": V_tstn_tng_prev,
        "V_tstn_tagul_prev": V_tstn_tagul_prev,
        "F_kchng": F_kchng,
        "V_tstn_kchng_prev": V_tstn_kchng_prev,
        "V_tstn_lodochny_prev": V_tstn_lodochny_prev,
        "G_sikn_tagul": sikn_1208_results.get("G_sikn_tagul"),
        "F_tagul_lpu": F_tagul_lpu,
        "V_tstn_rn_vn_prev": V_tstn_rn_vn_prev
    }