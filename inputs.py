import json
from functools import lru_cache
from typing import Any, Dict

from config import INPUT_JSON_PATH


@lru_cache(maxsize=1)
def _load_json() -> Dict[str, Any]:
    with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _section(name: str) -> Dict[str, Any]:
    return _load_json().get(name, {}) or {}


def get_suzun_inputs():
    """Загрузка параметров SUZUN из JSON."""
    data = _section("suzun")
    return {
        "G_payaha": float(data.get("G_payaha", 0)),
        "G_suzun_tng": float(data.get("G_suzun_tng", 0)),
        "K_g_suzun": float(data.get("K_g_suzun", 0)),
        "manual_V_upn_suzun": data.get("manual_V_upn_suzun"),
        "manual_V_suzun_vslu": data.get("manual_V_suzun_vslu"),
    }


def get_lodochny_inputs():
    """Загрузка параметров LODOCHNY из JSON."""
    data = _section("lodochny")
    return {
        "G_ichem": float(data.get("G_ichem", 0)),
        "K_otkachki": float(data.get("K_otkachki", 0)),
        "K_gupn_lodochny": float(data.get("K_gupn_lodochny", 0)),
        "K_g_tagul": float(data.get("K_g_tagul", 0)),
        "manual_V_upn_lodochny": data.get("manual_V_upn_lodochny"),
        "manual_G_sikn_tagul": data.get("manual_G_sikn_tagul"),
        "manual_V_tagul": data.get("manual_V_tagul"),
    }


def get_cppn_1_inputs():
    """Загрузка параметров CPPN_1 из JSON."""
    data = _section("cppn_1")
    return {
        "manual_V_upsv_yu": data.get("manual_V_upsv_yu"),
        "manual_V_upsv_s": data.get("manual_V_upsv_s"),
        "manual_V_cps": data.get("manual_V_cps"),
    }


def get_rn_vankor_inputs():
    """Загрузка параметров rn_vankor из JSON."""
    data = _section("rn_vankor")
    return {
        "manual_F_bp_vn": data.get("manual_F_bp_vn"),
        "manual_F_bp_suzun": data.get("manual_F_bp_suzun"),
        "manual_F_bp_suzun_vankor": data.get("manual_F_bp_suzun_vankor"),
        "manual_F_bp_tagul_tpu": data.get("manual_F_bp_tagul_tpu"),
        "manual_F_bp_tagul_lpu": data.get("manual_F_bp_tagul_lpu"),
        "manual_F_bp_skn": data.get("manual_F_bp_skn"),
        "manual_F_bp_vo": data.get("manual_F_bp_vo"),
        "manual_F_bp_suzun_vslu": data.get("manual_F_bp_suzun_vslu"),
        "manual_F_tng": data.get("manual_F_tng"),
        "manual_F_kchng": data.get("manual_F_kchng"),
    }


def get_sikn_1208_inputs():
    data = _section("sikn_1208")
    return {
        "K_delte_g_sikn": float(data.get("K_delte_g_sikn", 0)),
        "G_skn": float(data.get("G_skn", 0)),
    }


def get_TSTN_inputs():
    data = _section("tstn")
    return {
        "K_suzun": float(data.get("K_suzun", 0)),
        "K_vankor": float(data.get("K_vankor", 0)),
        "G_skn": float(data.get("G_skn", 0)),
        "K_skn": float(data.get("K_skn", 0)),
        "K_ichem": float(data.get("K_ichem", 0)),
        "K_payaha": float(data.get("K_payaha", 0)),
        "K_tagul": float(data.get("K_tagul", 0)),
        "K_lodochny": float(data.get("K_lodochny", 0)),
        "manual_G_gnps_i": data.get("manual_G_gnps_i"),
    }


def get_balance_po_business_inputs():
    data = _section("balance_po_business")
    return{
        "V_vn_lost_condensate": float(data.get("V_vn_lost_condensate", 0)),
        "G_vn_fuel": float(data.get("G_vn_fuel", 0)),
        "G_vn_fill": float(data.get("G_vn_fill", 0)),
        "G_vn_release_rn_drillig": float(data.get("G_vn_release_rn_drillig", 0)),
        "G_vn_release_well_service": float(data.get("G_vn_release_well_service", 0)),
        "V_suzun_lost_transport_vankor": float(data.get("G_vn_release_well_service", 0)),
        "V_vo_lost_condensate": float(data.get("V_vo_lost_condensate", 0)),
        "G_vo_fuel": float(data.get("G_vo_fuel", 0)),
        "G_vo_fill": float(data.get("G_vo_fill", 0)),
        "G_vo_release": float(data.get("G_vo_release", 0)),
        "Q_lodochny_condensate": float(data.get("Q_lodochny_condensate", 0)),
        "G_lodochny_fuel": float(data.get("G_lodochny_fuel", 0)),
        "Q_tagul_condensate": float(data.get("Q_tagul_condensate", 0)),
        "G_tagul_fuel": float(data.get("G_tagul_fuel", 0)),
        "G_tagul_release_vpt_neftmash": float(data.get("G_tagul_release_vpt_neftmash", 0)),
    }

def get_plan_balance_gtm_inputs():
    data = _section("plan_balance_gtm")
    return {
        "K_vo_mining": float(data.get("K_vo_mining", 0)),
        "K_vo_trans": float(data.get("K_vo_trans", 0)),
        "V_vo_gtm_lost_condensate": float(data.get("V_vo_gtm_lost_condensate", 0)),
        "G_vo_gtm_fuel": float(data.get("G_vo_gtm_fuel", 0)),
        "G_vo_gtm_fill": float(data.get("G_vo_gtm_fill", 0)),
        "G_vo_gtm_release": float(data.get("G_vo_gtm_release", 0)),
        "V_lodochny_nm_gtm_ost_upn_ichem": float(data.get("V_lodochny_nm_gtm_ost_upn_ichem", 0)),
        "F_tagul_lpy_delta": float(data.get("F_tagul_lpy_delta", 0)),
        "Q_vn_gtm_condensate": float(data.get("Q_vn_gtm_condensate", 0)),
        "K_vankor_mining": float(data.get("K_vankor_mining", 0)),
        "G_vn_gtm_fuel": float(data.get("G_vn_gtm_fuel", 0)),
        "G_vn_gtm_fill": float(data.get("G_vn_gtm_fill", 0)),
        "Q_suzun_gtm_condensate": float(data.get("Q_suzun_gtm_condensate", 0)),
        "G_suzun_gtm_fuel": float(data.get("G_suzun_gtm_fuel", 0)),
        "V_vo_nm_gtm_ost_texn": float(data.get("V_vo_nm_gtm_ost_texn", 0)),
        "V_vo_nm_gtm_ost_product": float(data.get("V_vo_nm_gtm_ost_product", 0)),
        "Q_vo_gtm_condensate": float(data.get("Q_vo_gtm_condensate", 0)),
        "Q_lodochny_gtm_condensate": float(data.get("Q_lodochny_gtm_condensate", 0)),
        "K_lodochny_mining": float(data.get("K_lodochny_mining", 0)),
        "K_lodochny_trans": float(data.get("K_lodochny_trans", 0)),
        "V_lodochny_nm_gtm_ost_product": float(data.get("V_lodochny_nm_gtm_ost_product", 0)),
        "G_lodochny_gtm_release": float(data.get("G_lodochny_gtm_release", 0)),
        "G_lodochny_gtm_own": float(data.get("G_lodochny_gtm_own", 0)),
        "V_tagul_nm_gtm_ost_rvs_clear": float(data.get("V_tagul_nm_gtm_ost_rvs_clear", 0)),
        "V_tagul_nm_gtm_ost_product": float(data.get("V_tagul_nm_gtm_ost_product", 0)),
        "Q_tagul_gtm_condensate": float(data.get("Q_tagul_gtm_condensate", 0)),
        "G_tagul_gtm_fuel": float(data.get("G_tagul_gtm_fuel", 0)),
        "G_tagul_gtm_release_russko_rechenskoe": float(data.get("G_tagul_gtm_release_russko_rechenskoe", 0)),
        "K_tagul_minig": float(data.get("G_tagul_gtm_release_russko_rechenskoe", 0)),
    }
