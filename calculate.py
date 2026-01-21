import numpy as np


class CalculationValidationError(Exception):
    """Исключение для критичных расхождений в исходных данных."""
    pass
# ===============================================================
# -------------------- СУЗУН -----------------------------------
# ===============================================================
def suzun(
    G_buy_month, G_out_udt_month, N, Q_vankor, Q_suzun, Q_vslu, Q_tng, Q_vo, G_payaha,
    G_suzun_tng, V_suzun_tng_prev, Q_vslu_day, V_upn_suzun_prev, V_suzun_vslu_prev, Q_suzun_day,
    V_upn_suzun_0, V_suzun_vslu_0, V_suzun_tng_0, K_g_suzun, V_suzun_slu_prev, manual_V_upn_suzun, manual_V_suzun_vslu
):
    G_buy_month = np.array(G_buy_month, dtype=float)
    G_out_udt_month = np.array(G_out_udt_month, dtype=float)
    Q_vankor = np.array(Q_vankor, dtype=float)
    Q_suzun = np.array(Q_suzun, dtype=float)
    Q_vslu = np.array(Q_vslu, dtype=float)
    Q_tng = np.array(Q_tng, dtype=float)
    Q_vo = np.array(Q_vo, dtype=float)
    # Массивы для расчета месячных значений
    G_per_data = []
    G_suzun_vslu_data = []
    G_suzun_slu_data = []
    G_suzun_data = []
    N = int(N) if N else 1.0

    # --- 1. Суточное значение покупки нефти
    G_buy_day = G_buy_month / N
    # --- 2. Суточный выход с УПДТ
    G_out_udt_day = G_out_udt_month / N

    # --- 3. Расход на переработку (Gпер)
    G_per = G_buy_day - G_out_udt_day
    G_per_data.append(G_per)
    G_per_month = sum(G_per_data) # сумма на текущий день месяца

    # --- 4–8. Суммарные месячные значения
    Q_vankor_month = Q_vankor.sum()
    Q_suzun_month = Q_suzun.sum()
    Q_vslu_month = Q_vslu.sum()
    Q_tng_month = Q_tng.sum()
    Q_vo_month = Q_vo.sum()

    # --- 9. Наличие нефти Таймыр в РП УПН Сузун
    V_suzun_tng = G_payaha + V_suzun_tng_prev - G_suzun_tng

    # --- 10. Откачка нефти Сузун (ВСЛУ)
    G_suzun_vslu = Q_vslu_day
    G_suzun_vslu_data.append(G_suzun_vslu)
    G_suzun_vslu_month = sum(G_suzun_vslu_data) # сумма на текущий день месяца

    # --- 11–12. Наличие нефти
    if manual_V_upn_suzun is not None:
        V_upn_suzun = manual_V_upn_suzun
    else:
        pass
        pass
        V_upn_suzun = V_upn_suzun_prev
    if manual_V_suzun_vslu is not None:
        V_suzun_vslu = manual_V_suzun_vslu
    else:
        V_suzun_vslu = V_suzun_vslu_prev + Q_vslu_day - G_suzun_vslu

    # --- 13. Расчёт наличия нефти (СЛУ)
    V_suzun_slu_0 = V_upn_suzun_0 - V_suzun_vslu_0 - V_suzun_tng_0
    V_suzun_slu = V_upn_suzun - V_suzun_vslu - V_suzun_tng

    # --- 14. Откачка нефти Сузун (СЛУ)
    G_suzun_slu = Q_suzun_day - Q_vslu_day - (V_suzun_slu - V_suzun_slu_prev) - (Q_suzun - Q_vslu) - K_g_suzun
    G_suzun_slu_data.append(G_suzun_slu)
    G_suzun_slu_month = sum(G_suzun_slu_data) # сумма на текущий день месяца

    # --- 15. Общая откачка нефти Сузун
    G_suzun = G_suzun_vslu + G_suzun_tng + G_suzun_slu
    G_suzun_data.append(G_suzun)
    G_suzun_month = sum(G_suzun_data) # сумма на текущий день месяца

    # --- 16. Потери при откачке нефти
    G_suzun_delta = Q_suzun_day - G_suzun_slu - G_suzun_vslu - (V_upn_suzun - V_upn_suzun_prev) + G_payaha

    return {
        "G_buy_day": G_buy_day, "G_out_updt_day": G_out_udt_day, "G_per": G_per, "G_per_month": G_per_month, "Q_vankor_month": Q_vankor_month,
        "Q_suzun_month": Q_suzun_month, "Q_vslu_month": Q_vslu_month, "Q_tng_month": Q_tng_month, "Q_vo_month": Q_vo_month,
        "V_suzun_tng": V_suzun_tng, "G_suzun_vslu": G_suzun_vslu, "G_suzun_vslu_month": G_suzun_vslu_month, "V_upn_suzun": V_upn_suzun,
        "V_suzun_vslu": V_suzun_vslu, "V_suzun_slu_0": V_suzun_slu_0, "V_suzun_slu": V_suzun_slu, "G_suzun_slu": G_suzun_slu,
        "G_suzun_slu_month": G_suzun_slu_month, "G_suzun": G_suzun,"G_suzun_month": G_suzun_month, "delta_G_suzun": G_suzun_delta,
    }

# ===============================================================
# -------------------- ВОСТОК ОЙЛ -------------------------------
# ===============================================================
def VO(Q_vo_day):
    G_upn_lodochny_ichem_data = []
    G_upn_lodochny_ichem = Q_vo_day
    G_upn_lodochny_ichem_month = sum(G_upn_lodochny_ichem_data) # сумма на текущий день месяца

    return {
        "G_upn_lodochny_ichem": G_upn_lodochny_ichem,
        "G_upn_lodochny_ichem_month": G_upn_lodochny_ichem_month,
    }

# ===============================================================
# -------------------- КЧНГ -------------------------------------
# ===============================================================
def kchng(Q_kchng_day, Q_kchng):
    Q_kchng = np.array(Q_kchng, dtype=float)
    G_kchng_data = []

    Q_kchng_month = Q_kchng.sum()

    G_kchng = Q_kchng_day
    G_kchng_data.append(G_kchng)
    G_kchng_month = sum(G_kchng_data) # сумма на текущий день месяца

    return {
        "Q_kchng_month": Q_kchng_month,
        "G_kchng": G_kchng,
        "G_kchng_month": G_kchng_month,
    }

# ===============================================================
# -------------------- ЛОДОЧНЫЙ ---------------------------------
# ===============================================================
def lodochny(
    Q_tagul, Q_lodochny, V_upn_lodochny_prev, G_ichem, V_ichem_prev, G_lodochny_ichem,
    Q_tagul_prev_month, G_lodochni_upsv_yu_prev_month, K_otkachki, K_gupn_lodochny, N, Q_vo_day,
    Q_lodochny_day, Q_tagul_day, V_tagul_prev, K_g_tagul, G_kchng, day, manual_V_upn_lodochny, manual_G_sikn_tagul,
    manual_V_tagul
):
    # Преобразование входных данных
    Q_tagul = np.array(Q_tagul, dtype=float)
    Q_lodochny = np.array(Q_lodochny, dtype=float)
    K_otkachki = float(K_otkachki)
    K_gupn_lodochny = float(K_gupn_lodochny)
    K_g_tagul = float(K_g_tagul)
    # Массивы для расчета месячных значений
    G_lodochny_uspv_yu_data = []
    G_sikn_tagul_data = []
    G_tagul_data = []
    delte_G_tagul_data = []
    G_lodochny_data = []
    delte_G_upn_lodochny_data = []
    G_tagul_lodochny_data = []

    N = int(N) if N else 1.0
    # --- 20–21. Месячные значения добычи ---
    Q_tagul_month = Q_tagul.sum()
    Q_lodochny_month = Q_lodochny.sum()

    # --- 22–24. Наличие нефти ---
    if manual_V_upn_lodochny is not None:
        V_upn_lodochny = manual_V_upn_lodochny
    else:
        V_upn_lodochny = V_upn_lodochny_prev
    V_ichem = V_ichem_prev + G_lodochny_ichem - G_ichem
    V_lodochny = V_upn_lodochny - V_ichem

    # --- 25. Коэффициент откачки ---
    K_otkachki_month = (G_lodochni_upsv_yu_prev_month / Q_tagul_prev_month)
    alarm_k_otkachki = False
    if abs(K_otkachki - K_otkachki_month) >= 0.01:
        alarm_k_otkachki = {
            "value": K_otkachki,
            "status": 1,
            "message": (
                f"коэффициент откачки K_otkachki={K_otkachki:.4f} "
                f"не совпадает с расчетным {K_otkachki_month:.4f} (расхождение > 0.01)"
            ),
        }
    # --- 26. Откачка нефти Лодочного месторождения на УПСВ-Юг ---
    G_lodochny_uspv_yu = Q_lodochny_day * (1 - K_otkachki) - (K_gupn_lodochny / 2)
    G_lodochny_uspv_yu_data.append(G_lodochny_uspv_yu)
    G_lodochny_uspv_yu_month = sum(G_lodochny_uspv_yu_data) # сумма на текущий день месяца
    alarm_g_sikn_tagul = False
    if manual_G_sikn_tagul is not None:
        G_sikn_tagul = manual_G_sikn_tagul
    else:
        if day <= N-2:
            G_sikn_tagul = round(G_lodochny_uspv_yu_month / N / 10) * 10
        else:
            value = round(G_lodochny_uspv_yu_month / N / 10) * 10
            G_sikn_tagul_N = [value for _ in range(N - 2)]
            G_sikn_tagul = (G_lodochny_uspv_yu_month - sum(G_sikn_tagul_N))/2
        if not (900 <= G_sikn_tagul <= 1500):
            alarm_g_sikn_tagul = {
                "value": G_sikn_tagul,
                "status": 1,
                "message": (
                    f"откачка нефти на СИКН-1208 вне допустимой вилки (900 … 1500) т "
                    f"(текущее {G_sikn_tagul:.2f})"
                ),
            }
        else:
            alarm_g_sikn_tagul = False
    G_sikn_tagul_data.append(G_sikn_tagul)
    G_sikn_tagul_month = sum(G_sikn_tagul_data) # сумма на текущий день месяца
    # --- 28–29. Откачка в МН Тагульского месторождения ---
    if manual_V_tagul is not None:
        V_tagul = manual_V_tagul
    else:
        V_tagul = V_tagul_prev
    G_tagul = Q_tagul_day - (V_tagul - V_tagul_prev) - K_g_tagul
    G_tagul_data.append(G_tagul)
    G_tagul_month = sum(G_tagul_data) # сумма на текущий день месяца

    # --- 30. Потери ---
    delte_G_tagul = Q_tagul_day - G_tagul - (V_tagul - V_tagul_prev)
    delte_G_tagul_data.append(delte_G_tagul)
    delte_G_tagul_month = sum(delte_G_tagul_data) # сумма на текущий день месяца

    # --- 31–32. Откачка нефти в МН ---
    G_upn_lodochny = Q_lodochny_day * K_otkachki - (V_upn_lodochny-V_upn_lodochny_prev) - (K_gupn_lodochny / 2) + Q_vo_day
    G_lodochny = G_upn_lodochny - G_ichem
    G_lodochny_data.append(G_lodochny)
    G_lodochny_month = sum(G_lodochny_data) # сумма на текущий день месяца

    # --- 33–34. Сводные потери и суммарная откачка ---
    delte_G_upn_lodochny = Q_lodochny_day + Q_vo_day - G_lodochny_uspv_yu - G_lodochny - (V_upn_lodochny - V_upn_lodochny_prev)
    delte_G_upn_lodochny_data.append(delte_G_upn_lodochny)
    G_upn_lodochny_month = sum(delte_G_upn_lodochny_data)  # сумма на текущий день месяца
    
    G_tagul_lodochny = G_tagul + G_upn_lodochny + G_kchng
    G_tagul_lodochny_data.append(G_tagul_lodochny)
    G_tagul_lodochny_month = sum(G_tagul_lodochny_data)  # сумма на текущий день месяца

    return {
        "Q_tagul_month": Q_tagul_month, "Q_lodochny_month": Q_lodochny_month, "V_upn_lodochny": V_upn_lodochny,
        "V_ichem": V_ichem, "V_lodochny": V_lodochny, "K_otkachki_month": K_otkachki_month, "G_lodochny_uspv_yu": G_lodochny_uspv_yu,
        "G_lodochny_uspv_yu_month": G_lodochny_uspv_yu_month, "G_sikn_tagul": G_sikn_tagul, "G_sikn_tagul_month": G_sikn_tagul_month,
        "delta_G_tagul": delte_G_tagul, "delta_G_tagul_month": delte_G_tagul_month, "G_upn_lodochny": G_upn_lodochny,
        "G_lodochny": G_lodochny, "G_lodochny_month": G_lodochny_month, "delta_G_upn_lodochny": delte_G_upn_lodochny,
        "G_upn_lodochny_month": G_upn_lodochny_month, "G_tagul_lodochny": G_tagul_lodochny, "G_tagul_lodochny_month": G_tagul_lodochny_month,
        "G_tagul_month":G_tagul_month,"G_tagul":G_tagul,
        "alarm_k_otkachki": alarm_k_otkachki, "alarm_g_sikn_tagul": alarm_g_sikn_tagul
    }

# ===============================================================
# -------------------- Блок «ЦППН-1»: ---------------------------
# ===============================================================
def CPPN_1 (
    V_upsv_yu_prev, V_upsv_s_prev, V_cps_prev, V_upsv_yu_0, V_upsv_s_0, V_upsv_cps_0,
    V_upsv_yu, V_upsv_s, V_upsv_cps,  V_lodochny_cps_upsv_yu_prev, V_lodochny_upsv_yu,
    G_sikn_tagul, flag_list, manual_V_upsv_yu, manual_V_upsv_s, manual_V_cps,
):
# 35. Расчет наличия нефти в РВС УПСВ-Юг, т:
    if manual_V_upsv_yu is not None:
        V_upsv_yu = manual_V_upsv_yu
    else:
        V_upsv_yu = V_upsv_yu_prev
    alarm_upsv_yu = False
    if not flag_list[0]:
        if not (V_upsv_yu_prev-1500 <= V_upsv_yu <= V_upsv_yu_prev+1500):
            alarm_upsv_yu = {
                "value": V_upsv_yu,
                "status": 1,
                "message": (
                    f"УПСВ-Юг: уровень вне допустимой вилки ±1500 т "
                    f"(текущее {V_upsv_yu:.2f}, вчера {V_upsv_yu_prev:.2f})"
                ),
            }
    else:
        if V_upsv_yu_prev-2000 <= V_upsv_yu <= V_upsv_yu_prev+4000:
            alarm_upsv_yu = {
                "value": V_upsv_yu,
                "status": 1,
                "message": (
                    f"УПСВ-Юг: уровень вне допустимой вилки (-2000 … +4000) т "
                    f"(текущее {V_upsv_yu:.2f}, вчера {V_upsv_yu_prev:.2f})"
                ),
            }
    # 36. Расчет наличия нефти в РВС УПСВ-Север, т:
    if manual_V_upsv_s is not None:
        V_upsv_s = manual_V_upsv_s
    else:
        V_upsv_s = V_upsv_s_prev
    alarm_upsv_s = False
    if not flag_list[1]:
        if not(V_upsv_s_prev-1500 <= V_upsv_s <= V_upsv_s_prev+1500):
            alarm_upsv_s = {
                "value": V_upsv_s,
                "status": 1,
                "message": (
                    f"УПСВ-С: уровень вне допустимой вилки ±1500 т "
                    f"(текущее {V_upsv_s:.2f}, вчера {V_upsv_s_prev:.2f})"
                ),
            }
    else:
        if not(V_upsv_s_prev-1500 <= V_upsv_s <= V_upsv_s_prev+2000):
            alarm_upsv_s = {
                "value": V_upsv_s,
                "status": 1,
                "message": (
                    f"УПСВ-С: уровень вне допустимой вилки -1500 … +2000т "
                    f"(текущее {V_upsv_s:.2f}, вчера {V_upsv_s_prev:.2f})"
                ),
            }
    # 37. Расчет наличия нефти в РВС ЦПС, т:
    if manual_V_cps is not None:
        V_cps = manual_V_cps
    else:
        V_cps = V_cps_prev
    alarm_cps = False
    if not flag_list[2]:
        if not (V_cps_prev - 1500 <= V_upsv_cps <= V_cps_prev + 1500):
            alarm_cps = {
                "value": V_cps,
                "status": 1,
                "message": (
                    f"УПСВ-ЦПС: уровень вне допустимой вилки ±1500 т "
                    f"(текущее {V_cps:.2f}, вчера {V_cps_prev:.2f})"
                ),
            }
    else:
        if not (V_cps_prev - 2000 <= V_cps <= V_cps_prev + 3300):
            alarm_cps = {
                "value": V_cps,
                "status": 1,
                "message": (
                    f"УПСВ-ЦПС: уровень вне допустимой вилки -2000 … +3300т "
                    f"(текущее {V_cps:.2f}, вчера {V_cps_prev:.2f})"
                ),
            }
# 38. Расчет суммарного наличия нефти в РП ЦППН-1, т:
    V_cppn_1_0 = V_upsv_yu_0+V_upsv_s_0+V_upsv_cps_0
    V_cppn_1 = V_upsv_yu + V_upsv_s + V_upsv_cps

#39. Расчет наличия нефти Лодочного ЛУ в РП на ЦПС и УПСВ - Юг, т:
    V_lodochny_cps_upsv_yu = V_lodochny_cps_upsv_yu_prev + V_lodochny_upsv_yu - G_sikn_tagul
    return {
        "V_upsv_yu":V_upsv_yu, "V_upsv_s": V_upsv_s, "V_cps": V_cps, "V_cppn_1_0": V_cppn_1_0,
        "V_cppn_1": V_cppn_1, "V_lodochny_cps_upsv_yu": V_lodochny_cps_upsv_yu,
        "alarm_upsv_yu": alarm_upsv_yu, "alarm_upsv_s": alarm_upsv_s, "alarm_cps": alarm_cps,
    }
# ===============================================================
# ------------------ Блок «Сдача ООО «РН-Ванкор»: ---------------
# ===============================================================
def rn_vankor(
    F_vn, F_suzun_obsh, F_suzun_vankor, N, day,V_tstn_suzun_vslu_norm, V_tstn_suzun_vslu,
    F_tagul_lpu, F_tagul_tpu, F_skn, F_vo,manual_F_bp_vn, manual_F_bp_suzun, manual_F_bp_suzun_vankor,
    manual_F_bp_tagul_lpu, manual_F_bp_tagul_tpu, manual_F_bp_skn, manual_F_bp_vo, manual_F_bp_suzun_vslu,
    F_kchng, F_bp_data, manual_F_kchng, e_suzun_vankor, e_vo, e_kchng, e_tng, F_tng, manual_F_tng
    ):

    # ---------- Инициализация  ----------
    F_bp_suzun_vankor = 0 # для расчета с e если дата не попадет в диапозон где дата должна быть кратной e выведет число 0
    F_bp_suzun_vslu = 0 # для расчета с e если дата не попадет в диапозон где дата должна быть кратной e выведет число 0
    F_bp_vo = 0 # для расчета с e если дата не попадет в диапозон где дата должна быть кратной e выведет число 0
    F_bp_kchng = 0# для расчета с e если дата не попадет в диапозон где дата должна быть кратной e выведет число 0
    F_bp_tng = 0
    # Массивы для расчета месячных значений
    F_bp_vn = 0.0
    F_bp_vn_data = []
    F_bp_suzun_data = []
    F_bp_suzun_vankor_data = []
    F_bp_suzun_vslu_data = []
    F_bp_tagul_lpu_data = []
    F_bp_tagul_tpu_data = []
    F_bp_tagul_data = []
    F_bp_skn_data = []
    F_bp_vo_data = []
    F_bp_tng_data = []
    F_bp_kchng_data = []
    alarm_first_10_days = False
    # =========================================================
    # 40. Ванкорнефть
    if manual_F_bp_vn is not None:
        F_bp_vn = manual_F_bp_vn
    else:
        base = round((F_vn / N) / 50) * 50
        if day < (N-2):
            F_bp_vn = base
        else:
            F_bp_vn = (F_vn - base * (N - 2))/2
    F_bp_vn_data.append(F_bp_vn)
    F_bp_vn_month = sum(F_bp_vn_data) # сумма на текущий день месяца

    # =========================================================
    # 41. Сузун (общий)
    F_suzun = F_suzun_obsh - F_suzun_vankor
    if manual_F_bp_suzun is not None:
        F_bp_suzun = manual_F_bp_suzun
    else:
        base = round((F_suzun / N) / 50) * 50
        if day < (N-2):
            F_bp_suzun = base
        else:
            F_bp_suzun = F_suzun - (base * (N - 2))/2
    F_bp_suzun_data.append(F_bp_suzun)
    F_bp_suzun_month = sum(F_bp_suzun_data) # сумма на текущий день месяца

    # =========================================================
    # 42. Сузун → Ванкор (через e)
    if manual_F_bp_suzun_vankor is not None:
        F_bp_suzun_vankor = manual_F_bp_suzun_vankor
    elif F_suzun_vankor < 20000:
        if e_suzun_vankor is None:
            raise CalculationValidationError(
                f"Сузун → Ванкор: e не установлен"
            )
        elif not (e_suzun_vankor > 0):
            raise CalculationValidationError(
                f"Сузун → Ванкор: e должно быть больше 0"
            )
        delivery_days = [d for d in range(1, N + 1) if d % e_suzun_vankor == 0]
        if delivery_days:
            delivery_count = len(delivery_days)
            last_day = delivery_days[-1]
            base = round((F_suzun_vankor / delivery_count) / 50) * 50
            if day in delivery_days:
                if day != last_day:
                    F_bp_suzun_vankor = base
                else:
                    F_bp_suzun_vankor = F_suzun_vankor - base * (delivery_count - 1)
    elif F_suzun_vankor >= 20000:
        base = round((F_suzun_vankor / N) / 50) * 50
        if day < N-2:
            F_bp_suzun_vankor = base
        else:
            F_bp_suzun_vankor = (F_suzun_vankor - base * (N - 2))/2
    F_bp_suzun_vankor_data.append(F_bp_suzun_vankor)
    F_bp_suzun_vankor_month = sum(F_bp_suzun_vankor_data) # сумма на текущий день месяца

    # =========================================================
    # 43. Сузун → ВСЛУ
    if manual_F_bp_suzun_vslu is not None:
        F_bp_suzun_vslu = manual_F_bp_suzun_vslu
    elif V_tstn_suzun_vslu > V_tstn_suzun_vslu_norm + 1000:
        F_bp_suzun_vslu = 1000
    F_bp_suzun_vslu_data.append(F_bp_suzun_vslu)
    F_bp_suzun_vslu_month = sum(F_bp_suzun_vslu_data) # сумма на текущий день месяца

    # =========================================================
    # 44. Тагульское — ЛПУ
    if manual_F_bp_tagul_lpu is not None:
        F_bp_tagul_lpu = manual_F_bp_tagul_lpu
    else:
        base = round((F_tagul_lpu / N) / 50) * 50
        if day < N-2:
            F_bp_tagul_lpu = base
        else:
            F_bp_tagul_lpu = (F_tagul_lpu - base * (N - 2))/2
    F_bp_tagul_lpu_data.append(F_bp_tagul_lpu)
    F_bp_tagul_lpu_month = sum(F_bp_tagul_lpu_data) # сумма на текущий день месяца

    # =========================================================
    # 45. Тагульское — ТПУ
    if manual_F_bp_tagul_tpu is not None:
        F_bp_tagul_tpu = manual_F_bp_tagul_tpu
    else:
        base = round((F_tagul_tpu / N) / 50) * 50
        if day < N-2:
            F_bp_tagul_tpu = base
        else:
            F_bp_tagul_tpu = (F_tagul_tpu - base * (N - 2))/2
    F_bp_tagul_tpu_data.append(F_bp_tagul_tpu)
    F_bp_tagul_tpu_month = sum(F_bp_tagul_tpu_data) # сумма на текущий день месяца
    # =========================================================
    # 47. Расчет суммарной сдачи ООО "Тагульское" через СИКН №1209
    F_bp_tagul = F_bp_tagul_lpu + F_bp_tagul_tpu
    F_bp_tagul_data.append(F_bp_tagul)
    F_bp_tagul_month = sum(F_bp_tagul_data)
    # =========================================================
    # 47. СКН
    if manual_F_bp_skn is not None:
        F_bp_skn = manual_F_bp_skn
    else:
        base = round((F_skn / N) / 50) * 50
        F_bp_skn = base if day < (N-2) else (F_skn - base * (N - 1))/2
    F_bp_skn_data.append(F_bp_skn)
    F_bp_skn_month = sum(F_bp_skn_data) # сумма на текущий день месяца

    # =========================================================
    # 48. Восток Ойл (через e)
    if manual_F_bp_vo is not None:
        F_bp_vo = manual_F_bp_vo
    elif F_vo < 20000:
        if e_vo is None:
            raise CalculationValidationError(
                f"Восток Ойл: e не установлен"
            )
        elif not (e_vo > 0):
            raise CalculationValidationError(
                f"Восток Ойл: e должно быть больше 0"
            )
        delivery_days = [d for d in range(1, N - 1) if d % e_vo == 0]
        if delivery_days:
            delivery_count = len(delivery_days)
            last_day = delivery_days[-1]
            base = round((F_vo / delivery_count) / 50) * 50

            if day in delivery_days:
                if day != last_day:
                    F_bp_vo = base
                else:
                    F_bp_vo = F_vo - base * (delivery_count - 1)
    else:
        base = round((F_vo / N) / 50) * 50
        F_bp_vo = base if day < N else F_vo - base * (N - 1)
    F_bp_vo_data.append(F_bp_vo)
    F_bp_vo_month = sum(F_bp_vo_data) # сумма на текущий день месяца
    
    # =========================================================
    # 49. Определение посуточной сдачи нефти АО "Таймырнефтегаз" через СИКН №1209
    if manual_F_tng is not None:
        F_bp_tng = manual_F_tng
    elif F_tng < 20000:
        if e_tng is None:
            raise CalculationValidationError(
                f"Таймырнефтегаз: e не установлен"
            )
        elif not (e_tng > 0):
            raise CalculationValidationError(
                f"Таймырнефтегаз: e должно быть больше 0"
            )
        delivery_days = [d for d in range(1, N - 1) if d % e_tng == 0]
        if delivery_days:
            delivery_count = len(delivery_days)
            last_day = delivery_days[-1]
            base = round((F_tng / delivery_count) / 50) * 50
            if day in delivery_days:
                if day != last_day:
                    F_bp_tng = base
                else:
                    F_bp_tng = F_tng - base * (delivery_count - 1)
    else:
        base = round((F_tng / N) / 50) * 50
        F_bp_tng = base if day < N else F_tng - base * (N - 1)
    F_bp_tng_data.append(F_bp_tng)
    F_bp_tng_month = sum(F_bp_tng_data) # сумма на текущий день месяца

    F_bp_tng = 0 # в дальнейшим заменить расчетной формулой
    # =========================================================
    #  50.	Определение посуточной сдачи нефти ООО «КЧНГ» через СИКН № 1209, т/сут:
    if manual_F_kchng is not None:
        F_kchng = manual_F_kchng
    elif F_kchng < 20000:
        if e_kchng is None:
            raise CalculationValidationError(
                f"КЧНГ: e не установлен"
            )
        elif not (e_kchng > 0):
            raise CalculationValidationError(
                f"КЧНГ: e должно быть больше 0"
            )
        delivery_days = [d for d in range(1, N + 1) if d % e_kchng == 0]
        if delivery_days:
            delivery_count = len(delivery_days)
            last_day = delivery_days[-1]
            base = round((F_kchng / delivery_count) / 50) * 50

            if day in delivery_days:
                if day != last_day:
                    F_bp_kchng = base
                else:
                    F_bp_kchng = (F_kchng - base * (delivery_count - 2))/2
    else:
        base = round((F_vo / N) / 50) * 50
        F_bp_kchng = base if day < N else F_kchng - base * (N - 1)
    F_bp_kchng_data.append(F_bp_kchng)
    F_bp_kchng_month = sum(F_bp_kchng_data) # сумма на текущий день месяца
    F_bp = F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun
    F_bp_data.append(F_bp)
    F_bp_month = sum(F_bp_data) # сумма на текущий день месяца
    F_bp_sr = F_bp_month/N
    first_10_sum = sum(F_bp_data[:10])
    if first_10_sum < F_bp_sr:
        alarm_first_10_days = {
            "value": first_10_sum,
            "status": 1,
            "message": (
                "Сдача нефти за первые 10 суток меньше "
                "среднесуточного значения за месяц"
            ),
        }
    return {
        "F_bp_vn": F_bp_vn, "F_bp_vn_month": F_bp_vn_month, "F_bp_suzun": F_bp_suzun, "F_bp_suzun_month": F_bp_suzun_month,
        "F_bp_suzun_vankor": F_bp_suzun_vankor, "F_bp_suzun_vankor_month": F_bp_suzun_vankor_month, "F_bp_suzun_vslu": F_bp_suzun_vslu,
        "F_bp_suzun_vslu_month": F_bp_suzun_vslu_month, "F_bp_tagul_lpu": F_bp_tagul_lpu, "F_bp_tagul_lpu_month": F_bp_tagul_lpu_month,
        "F_bp_tagul_tpu": F_bp_tagul_tpu, "F_bp_tagul_tpu_month": F_bp_tagul_tpu_month, "F_bp_skn": F_bp_skn, "F_bp_skn_month": F_bp_skn_month,
        "F_bp_vo": F_bp_vo, "F_bp_vo_month": F_bp_vo_month, "F_bp_kchng":F_bp_kchng, "F_bp_kchng_month":F_bp_kchng_month,"F_bp_tng_month":F_bp_tng_month, "F_bp_tng":F_bp_tng , "F_bp": F_bp,
        "F_bp_month":F_bp_month, "F_bp_sr":F_bp_sr, "alarm_first_10_days":alarm_first_10_days, "F_bp_tagul":F_bp_tagul, "F_bp_tagul_month":F_bp_tagul_month
    }

# ===============================================================
# ---------------------- Блок «СИКН-1208»: ----------------------
# ===============================================================
def sikn_1208 (
    G_suzun_vslu, G_buy_day, G_per, G_suzun, G_sikn_tagul, G_suzun_tng, Q_vankor, V_upsv_yu, 
    V_upsv_s, V_upsv_cps, V_upsv_yu_prev, V_upsv_s_prev, V_upsv_cps_prev,G_lodochny_uspv_yu, K_delte_g_sikn, 
    V_cppn_1, G_skn, V_cppn_1_prev
):
    # Массивы для расчета месячных значений
    G_sikn_vslu_data = []
    g_sikn_tagul_data = []
    G_sikn_suzun_data = []
    G_suzun_tng_data = []
    G_sikn_data = []
    G_sikn_vankor_data = []
    G_skn_data = []
    G_delta_sikn_data = []
# 52.	Определение откачки нефти АО «Сузун» (ВСЛУ) через СИКН № 1208, т/сут:
    G_sikn_vslu = G_suzun_vslu
    G_sikn_vslu_data.append(G_sikn_vslu)
    G_sikn_vslu_month = sum(G_sikn_vslu_data) # сумма на текущий день месяца

# 53.	Определение суммарного месячного значения откачки нефти ООО «Тагульское» через СИКН № 1208, т/сут:
    g_sikn_tagul_data.append(G_sikn_tagul)
    G_sikn_tagul_month = sum(g_sikn_tagul_data)

# 54.	Расчет суммарной откачки нефти АО «Сузун» (СЛУ+ВСЛУ) через СИКН № 1208, т/сут:
    G_sikn_suzun = G_suzun + G_buy_day - G_per
    G_sikn_suzun_data.append(G_sikn_suzun)
    G_sikn_suzun_month = sum(G_sikn_suzun_data) # сумма на текущий день месяца
# 55.
    G_sikn_tng = G_suzun_tng
    G_suzun_tng_data.append(G_sikn_tng)
    G_sikn_tng_month = sum(G_suzun_tng_data) # сумма на текущий день месяца

# 57.	Расчет суммарной откачки нефти через СИКН № 1208, т/сут:
    G_sikn = Q_vankor + G_suzun - (V_upsv_yu - V_upsv_yu_prev) - (V_upsv_s - V_upsv_s_prev) - (V_upsv_cps - V_upsv_cps_prev) + G_lodochny_uspv_yu + K_delte_g_sikn + G_buy_day - G_per
    G_sikn_data.append(G_sikn)
    G_sikn_month = sum(G_sikn_data) # сумма на текущий день месяца

# 58.	Расчет откачки нефти АО «Ванкорнефть» через СИКН № 1208, т/сут:
    G_sikn_vankor = G_sikn - G_sikn_tagul - G_sikn_suzun - G_sikn_tng
    G_sikn_vankor_data.append(G_sikn_vankor)
    G_sikn_vankor_month = sum(G_sikn_vankor_data) # сумма на текущий день месяца

# 59.	Определение суммарного месячного значения передачи нефти ООО «СКН» на транспортировку КНПС, т/сут:
    G_skn_data.append(G_skn)
    G_skn_month = sum(G_skn_data) # сумма на текущий день месяца

# 60.	Расчет потерь при откачке через СИКН № 1208 (потери+отпуск+прочее), т/сут:
    G_delta_sikn = Q_vankor + G_suzun + G_lodochny_uspv_yu - G_sikn - (V_cppn_1 - V_cppn_1_prev) + G_buy_day - G_per
    G_delta_sikn_data.append(G_delta_sikn)
    G_delta_sikn_month = sum(G_delta_sikn_data) # сумма на текущий день месяца

    return {
        "G_sikn_vslu":G_sikn_vslu, "G_sikn_vslu_month":G_sikn_vslu_month, "G_sikn_tagul":G_sikn_tagul, "G_sikn_suzun":G_sikn_suzun,
        "G_sikn_suzun_month":G_sikn_suzun_month, "G_sikn_tng":G_sikn_tng, "G_sikn_tng_month":G_sikn_tng_month, "G_sikn":G_sikn, "G_sikn_month":G_sikn_month,
        "G_sikn_vankor":G_sikn_vankor, "G_sikn_vankor_month":G_sikn_vankor_month, "G_skn_month":G_skn_month, "delta_G_sikn":G_delta_sikn,"delta_G_sikn_month": G_delta_sikn_month,
    }

def tstn_precalc(
        V_gnps_0, VN_min_gnsp, N, G_sikn, manual_G_gnps_i,
        V_gnps_prev, V_nps_1_prev, V_nps_2_prev,
        V_tstn_suzun_vslu_prev, F_suzun_vslu, G_suzun_vslu, K_suzun,
        V_tstn_suzun_vankor_prev, F_suzun_vankor, G_buy_day, G_per, K_vankor,
        V_tstn_tagul_prev, G_tagul, F_tagul, K_tagul,
        V_tstn_lodochny_prev, G_sikn_tagul, G_lodochny, F_tagul_lpu, K_lodochny,
        V_tstn_rn_vn_prev
):
    if manual_G_gnps_i is not None:
        G_gnps_i = manual_G_gnps_i
    else:
        G_gnps_i = G_sikn + (V_gnps_0 - VN_min_gnsp) / N
    # В TSTN рассчитывается G_gnps_month, затем делится на N
    G_gnps = G_gnps_i / N

    V_gnps = V_gnps_prev + G_sikn - G_gnps
    V_nps_1 = V_nps_1_prev
    V_nps_2 = V_nps_2_prev

    V_tstn_suzun_vslu = V_tstn_suzun_vslu_prev - F_suzun_vslu + G_suzun_vslu - F_suzun_vslu * (K_suzun / 100)
    V_tstn_suzun_vankor = V_tstn_suzun_vankor_prev - F_suzun_vankor + (G_buy_day - G_per) - F_suzun_vankor * (K_vankor / 100)

    V_tstn_tagul = V_tstn_tagul_prev + G_tagul - F_tagul - F_tagul * (K_tagul / 100)
    V_tstn_lodochny = V_tstn_lodochny_prev + G_sikn_tagul + G_lodochny - F_tagul_lpu - F_tagul_lpu * (K_lodochny / 100)
    V_tstn_tagul_obch = V_tstn_tagul + V_tstn_lodochny

    V_tstn_rn_vn = V_tstn_rn_vn_prev

    return {
        "G_gnps_i": G_gnps_i,
        "G_gnps": G_gnps,
        "V_gnps": V_gnps,
        "V_nps_1": V_nps_1,
        "V_nps_2": V_nps_2,
        "V_tstn_rn_vn": V_tstn_rn_vn,
        "V_tstn_tagul_obch": V_tstn_tagul_obch,
        "V_tstn_tagul": V_tstn_tagul,
        "V_tstn_lodochny": V_tstn_lodochny,
        "V_tstn_suzun_vslu": V_tstn_suzun_vslu,
        "V_tstn_suzun_vankor": V_tstn_suzun_vankor,
    }


def TSTN (
        V_gnps_0,V_gnps_prev, N, VN_min_gnps
        , G_sikn, flag_list, V_nps_1_prev, V_nps_2_prev, G_tagul, G_upn_lodochny, G_skn, G_kchng,
        V_knps_prev, V_nps_1_0, V_nps_2_0, V_knps_0, G_suzun_vslu, K_suzun,  V_tstn_suzun_vslu_prev, F_suzun_vankor, V_tstn_suzun_vankor_prev, K_vankor,
        G_buy_day, G_per, F_suzun_vslu, V_suzun_slu_0, V_tstn_suzun_prev, G_suzun_slu, V_tstn_skn_prev, F_skn, K_skn, G_ichem, F_vo, V_tstn_vo_prev,
        K_ichem, F_tng, G_suzun_tng, V_tstn_tng_prev,K_payaha, V_tstn_tagul_prev, F_kchng, K_tagul,V_tstn_kchng_prev, V_tstn_lodochny_prev,
        G_sikn_tagul, F_tagul_lpu, K_lodochny, V_tstn_rn_vn_prev, manual_G_gnps_i, G_lodochny,
        V_tstn_suzun_vankor_0, V_tstn_suzun_vslu_0, V_tstn_tagul_0, V_tstn_lodochny_0, V_tstn_rn_vn_0,
        V_tstn_kchng_0, V_tstn_skn_0, V_tstn_vo_0, V_tstn_tng_0, F_suzun, F, F_tagul,
        G_gnps_i, G_gnps, V_gnps, V_nps_1, V_nps_2, V_tstn_suzun_vslu, V_tstn_suzun_vankor,
        V_tstn_tagul, V_tstn_lodochny, V_tstn_tagul_obch, V_tstn_rn_vn
          ):
    # Массивы для расчета месячных значений
    # Значения G_gnps / V_gnps / V_nps_* и V_tstn_* передаются из tstn_precalc
    G_gnps_month = G_gnps_i
    V_gnps_out = V_gnps
    if not flag_list[0]:
        if not (V_gnps_prev-1500 <= V_gnps <= V_gnps_prev+1500):
            V_gnps_out = {
                "value": V_gnps,
                "status": 1,
                "message": (
                    f"РП ГНПС: уровень вне допустимой вилки ±1500 т "
                    f"(текущее {V_gnps:.2f}, вчера {V_gnps_prev:.2f})"
                ),
            }
    else:
        if not (V_gnps_prev - 2000 <= V_gnps <= V_gnps_prev + 3000):
            V_gnps_out = {
                "value": V_gnps,
                "status": 1,
                "message": (
                    f"РП ГНПС: уровень вне допустимой вилки -2000 … +3000т "
                    f"(текущее {V_gnps:.2f}, вчера {V_gnps_prev:.2f})"
                ),
            }

    # 63. Расчет наличия нефти в РП НПС-1, т:
    V_nps_1_out = V_nps_1
    if not flag_list[1]:
        if not (V_nps_1_prev - 700 <= V_nps_1 <= V_nps_1_prev + 700):
            V_nps_1_out = {
                "value": V_nps_1,
                "status": 1,
                "message": (
                    f"РП НПС-1: уровень вне допустимой вилки ±700 т "
                    f"(текущее {V_nps_1:.2f}, вчера {V_nps_1_prev:.2f})"
                ),
            }
    else:
        if not (V_nps_1_prev - 2000 <= V_nps_1 <= V_nps_1_prev + 4000):
            V_nps_1_out = {
                "value": V_nps_1,
                "status": 1,
                "message": (
                    f"РП НПС-1: уровень вне допустимой вилки -2000 … +4000т "
                    f"(текущее {V_nps_1:.2f}, вчера {V_nps_1_prev:.2f})"
                ),
            }

    # 64. Расчет наличия нефти в РП НПС-2, т:
    V_nps_2_out = V_nps_2
    if not flag_list[1]:
        if not (V_nps_2_prev - 700 <= V_nps_2 <= V_nps_2_prev + 700):
            V_nps_2_out = {
                "value": V_nps_2,
                "status": 1,
                "message": (
                    f"РП НПС-1: уровень вне допустимой вилки ±700 т "
                    f"(текущее {V_nps_1:.2f}, вчера {V_nps_1_prev:.2f})"),
            }
    else:
        if not (V_nps_2_prev - 2000 <= V_nps_2 <= V_nps_2_prev + 4000):
            V_nps_2_out = {
                "value": V_nps_2,
                "status": 1,
                "message": (
                    f"РП НПС-1: уровень вне допустимой вилки -2000 … +4000 т "
                    f"(текущее {V_nps_1:.2f}, вчера {V_nps_1_prev:.2f})"),
            }

#65.	Расчет наличия нефти в РП КНПС
    V_knps = (G_gnps - F + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng) - (V_nps_2 - V_nps_2_prev) - (V_nps_1-V_nps_1_prev)
    V_knps_out = V_knps
    if not flag_list[2]:
        if not (V_knps_prev - 1500 <= V_knps <= V_knps_prev + 1500):
            V_knps_out = {
                "value":V_knps,
                "status":1,
                "message":(
                f"РП КНПС: уровень вне допустимой вилки ±1500 т "
                f"(текущее {V_knps:.2f}, вчера {V_knps_prev:.2f})"),
            }
    else:
        if not (V_knps_prev - 2000 <= V_knps <= V_knps_prev + 3000):
            V_knps_out = {
                "value":V_knps,
                "status":1,
                "message":(
                f"РП КНПС: уровень вне допустимой вилки -2000 … +3000т "
                f"(текущее {V_knps:.2f}, вчера {V_knps_prev:.2f})"),
            }
# 66.	Расчет суммарного наличия нефти в резервуарах ЦТН, т:
    V_tstn_0 = V_gnps_0 + V_nps_1_0 + V_nps_2_0 + V_knps_0
    V_tstn = V_gnps + V_nps_1 + V_nps_2 + V_knps

    # 67. Расчет наличия нефти АО «Сузун» (ВСЛУ) в резервуарах ЦТН, т:
    V_tstn_suzun_vslu_out = V_tstn_suzun_vslu
    if not (900 <=  V_tstn_suzun_vslu <= 4000):
        V_tstn_suzun_vslu_out = {
            "value": V_tstn_suzun_vslu,
            "status": 1,
            "message": (
                f"ЦТН-ВСЛУ: уровень вне допустимой вилки 900 … 4000т "
                f"(текущее {V_tstn_suzun_vslu:.2f})"
            ),
        }


    # 68. Расчет наличия нефти АО «Сузун» (Ванкор) в резервуарах ЦТН, т:
    V_tstn_suzun_vankor_out = V_tstn_suzun_vankor
    if not (900 <= V_tstn_suzun_vankor <= 5000):
        V_tstn_suzun_vankor_out = {
            "value": V_tstn_suzun_vankor,
            "status": 1,
            "message": (
                f"ЦТН-Ванкор: уровень вне допустимой вилки 900 … 5000т "
                f"(текущее {V_tstn_suzun_vankor:.2f})"
            ),
        }

# 69.	Расчет наличия нефти АО «Сузун» (Сузун) в резервуарах ЦТН, т:
    V_tstn_suzun_0 = V_suzun_slu_0 - V_tstn_suzun_vslu_0 -  V_tstn_suzun_vankor_0
    V_tstn_suzun_0_out = V_tstn_suzun_0
    if not (2000 <= V_tstn_suzun_0 <= 6000):
        V_tstn_suzun_0_out = {
            "value": V_tstn_suzun_0,
            "status": 1,
            "message": (
                f"ЦТН-Сузун: уровень вне допустимой вилки 2000 … 6000т "
                f"(текущее {V_tstn_suzun_0:.2f})"
            ),
        }

    V_tstn_suzun = V_tstn_suzun_prev - F_suzun + G_suzun_slu - F_suzun * (K_suzun/100)
    V_tstn_suzun_out = V_tstn_suzun
    if not (2000 <= V_tstn_suzun <= 6000):
        V_tstn_suzun_out = {
            "value": V_tstn_suzun,
            "status": 1,
            "message": (
                f"ЦТН-Сузун: уровень вне допустимой вилки 2000 … 6000т "
                f"(текущее {V_tstn_suzun:.2f})"
            ),
        }

# 70.	Расчет наличия нефти ООО «СевКомНефтегаз» в резервуарах ЦТН, т:
    V_tstn_skn = V_tstn_skn_prev - F_skn + G_skn - F_skn * (K_skn/100)
    V_tstn_skn_out = V_tstn_skn
    if not (3000 <= V_tstn_skn <= 8000):
        V_tstn_skn_out = {
            "value": V_tstn_skn,
            "status": 1,
            "message": (
                f"ЦТН-СКН: уровень вне допустимой вилки 3000 … 8000т "
                f"(текущее {V_tstn_skn:.2f})"
            ),
        }

 # 71. Расчет наличия нефти ООО «Восток Оил» в резервуарах ЦТН, т:
    V_tstn_vo = V_tstn_vo_prev + G_ichem - F_vo - F_vo * (K_ichem/100)
    if not (1000 <= V_tstn_vo <= 6000):
        V_tstn_vo_out = {
            "value": V_tstn_vo,
            "status": 1,
            "message": (
                f"ЦТН-Восток Ойл: уровень вне допустимой вилки 1000 … 6000т "
                f"(текущее {V_tstn_vo:.2f})"
            ),
        }

# 72.	Расчет наличия нефти АО «Таймырнефтегаз» в резервуарах ЦТН, т:
    V_tstn_tng = V_tstn_tng_prev + G_suzun_tng - F_tng - F_tng * (K_payaha/100)
    V_tstn_tng_out = V_tstn_tng
    if not (300 <= V_tstn_tng <= 6000):
        V_tstn_tng_out = {
            "value": V_tstn_tng,
            "status": 1,
            "message": (
                f"ЦТН-Таймырнефтегаз: уровень вне допустимой вилки 300 … 6000т "
                f"(текущее {V_tstn_tng:.2f}, вчера {V_tstn_tng_prev:.2f})"
            ),
        }

# 73.	Расчет наличия нефти ООО «КЧНГ» (Русско-Реченское месторождение) в резервуарах ЦТН, т:
    V_tstn_kchng = V_tstn_kchng_prev + G_kchng - F_kchng - F_kchng * (K_tagul/100)
    V_tstn_kchng_out = V_tstn_kchng
    if not (1000 <= V_tstn_kchng <= 6000):
        V_tstn_kchng_out = {
            "value": V_tstn_kchng,
            "status": 1,
            "message": (
                f"ЦТН-КЧНГ: уровень вне допустимой вилки 1000 … 6000т "
                f"(текущее {V_tstn_kchng:.2f})"
            ),
        }
    # 74. Расчет наличия нефти ООО «Тагульское» (Тагульский ЛУ) в резервуарах ЦТН, т:
    V_tstn_tagul_out = V_tstn_tagul
    if not (4000 <= V_tstn_tagul <= 12000):
        V_tstn_tagul_out = {
            "value": V_tstn_tagul,
            "status": 1,
            "message": (
                f"ЦТН-Тагульское: уровень вне допустимой вилки 4000 … 12000т "
                f"(текущее {V_tstn_tagul:.2f})"
            ),
        }

    # 75. Расчет наличия нефти ООО «Тагульское» (Лодочный ЛУ) в резервуарах ЦТН, т:
    V_tstn_lodochny_out = V_tstn_lodochny
    if not (3000 <= V_tstn_lodochny <= 11000):
        V_tstn_lodochny_out = {
            "value": V_tstn_lodochny,
            "status": 1,
            "message": (
                f"ЦТН-Лодочный: уровень вне допустимой вилки 3000 … 11000т "
                f"(текущее {V_tstn_lodochny:.2f})"
            ),
        }

    # 76. Расчет наличия нефти ООО «Тагульское» (Всего) в резервуарах ЦТН, т:
    V_tstn_tagul_obch_0 = V_tstn_tagul_0 + V_tstn_lodochny_0
    if not (3000 <= V_tstn_tagul <= 11000):
        V_tstn_tagul_out = {
            "value": V_tstn_tagul,
            "status": 1,
            "message": (
                f"ЦТН-Тагульское: уровень вне допустимой вилки 3000 … 11000т "
                f"(текущее {V_tstn_tagul:.2f})"
            ),
        }

    # 77. Расчет наличия нефти ООО «РН-Ванкор» в резервуарах ЦТН (мертвые остатки в резервуарах), т:

# 78.	Расчет наличия нефти АО «Ванкорнефть» в резервуарах ЦТН, т:
    V_tstn_vn_0 = V_tstn_0 - V_tstn_rn_vn_0 - V_tstn_suzun_0 - V_tstn_tagul_obch_0 - V_tstn_suzun_vankor_0 - V_tstn_suzun_vslu_0 - V_tstn_skn_0 - V_tstn_vo_0 - V_tstn_tng_0 - V_tstn_kchng_0
    V_tstn_vn_0_out = V_tstn_vn_0
    if not (4000 <= V_tstn_vn_0 <= 11000):
        V_tstn_vn_0_out = {
            "value": V_tstn_vn_0,
            "status": 1,
            "message": (
                f"ЦТН-Ванкор: уровень вне допустимой вилки 4000 … 11000т "
                f"(текущее {V_tstn_vn_0:.2f})"
            ),
        }
    V_tstn_vn = V_tstn - V_tstn_rn_vn - V_tstn_suzun - V_tstn_tagul_obch - V_tstn_suzun_vankor -  V_tstn_suzun_vslu - V_tstn_skn - V_tstn_vo - V_tstn_tng - V_tstn_kchng
    V_tstn_vn_out = V_tstn_vn
    if not (4000 <= V_tstn_vn <= 11000):
        V_tstn_vn_out = {
            "value": V_tstn_vn,
            "status": 1,
            "message": (
                f"ЦТН-Ванкор: уровень вне допустимой вилки 4000 … 11000т "
                f"(текущее {V_tstn_vn:.2f})"
            ),
        }
        
    return {
        "G_gnps_i":G_gnps_i, "G_gnps_month":G_gnps_month, "G_gnps":G_gnps, "V_gnps":V_gnps_out, "V_nps_1":V_nps_1_out, "V_nps_2":V_nps_2,"V_nps_2_out":V_nps_2_out, "V_knps":V_knps,
        "V_tstn_0":V_tstn_0, "V_tstn":V_tstn, "V_tstn_suzun_vslu": V_tstn_suzun_vslu_out, "V_tstn_suzun_vankor":V_tstn_suzun_vankor_out, "V_tstn_suzun_0":V_tstn_suzun_0_out,
        "V_tstn_suzun":V_tstn_suzun_out, "V_tstn_skn":V_tstn_skn_out,"V_tstn_vo":V_tstn_vo, "V_tstn_tng":V_tstn_tng_out, "V_tstn_kchng":V_tstn_kchng_out, "V_knps_out":V_knps_out,
        "V_tstn_tagul":V_tstn_tagul_out, "V_tstn_lodochny":V_tstn_lodochny_out, "V_tstn_tagul_obch":V_tstn_tagul_obch, "V_tstn_tagul_obch_0":V_tstn_tagul_obch_0,
        "V_tstn_rn_vn":V_tstn_rn_vn, "V_tstn_vn":V_tstn_vn_out, "V_tstn_vn_0":V_tstn_vn_0_out,"V_tstn_vo_out":V_tstn_vo_out
    }
# ===============================================================
# ---------------------- Блок «РН Ванкор» автобаланс: ----------------------
# ===============================================================
def rn_vankor_balance (
        V_upn_suzun_prev, V_upn_suzun_0, VN_upn_suzun_min, N, V_upn_lodochny_prev, V_upn_lodochny_0, VN_upn_lodochny_min, V_upsv_yu_prev,
        V_upsv_yu_0, VN_upsv_yu_min, V_upsv_s_prev, V_upsv_s_0, VN_upsv_s_min, V_cps_prev, V_cps_0, VN_cps_min, flag_sost,
        V_tstn_norm_suzun, VN_knps_min, V_tstn_suzun_prev, G_suzun_slu, K_suzun, F_bp_tagul_lpu, F_bp_tagul_tpu, F_bp_suzun_vankor,
        F_bp_suzun_vslu, F_bp_skn, F_bp_vo, F_bp_tng, F_bp_kchng, F_bp_vn, G_gnps, V_knps_prev, G_tagul, G_upn_lodochny, G_skn, G_kchng,
        V_nps_2, V_nps_2_prev, V_nps_1, V_nps_1_prev,  V_tstn_norm_suzun_vankor,V_tstn_suzun_vankor_prev,G_buy_day,V_tstn_suzun_vankor,
        G_per, K_vankor,V_tstn_lodochny_prev, G_sikn_tagul, G_lodochny, K_lodochny, V_tstn_norm_lodochny, V_tstn_tagul_prev, 
        K_tagul, V_tstn_skn_prev, K_skn,V_tstn_vo_prev, G_ichem, K_ichem, V_tstn_tng_prev, G_suzun_tng, K_payaha, V_tstn_kchng_prev,
        V_tstn_norm_tagul,V_tstn_norm_skn, V_tstn_norm_vo, V_tstn_norm_tng, V_tstn_norm_kchng, V_gnps, V_tstn_rn_vn, V_tstn_tagul_obch,
        V_tstn_suzun_vslu, V_tstn_norm_vn, F_bp_suzun, ):
    F_bp_vn = 0.0 if F_bp_vn is None else F_bp_vn
    F_suzun_vankor = F_bp_suzun_vankor
    F_suzun = F_bp_suzun
    F_suzun_vslu = F_bp_suzun_vslu
    F_bp = (
        (F_bp_vn or 0)
        + (F_bp_tagul_lpu or 0)
        + (F_bp_tagul_tpu or 0)
        + (F_bp_suzun_vankor or 0)
        + (F_bp_suzun_vslu or 0)
        + (F_bp_skn or 0)
        + (F_bp_vo or 0)
        + (F_bp_tng or 0)
        + (F_bp_kchng or 0)
        + (F_bp_suzun or 0)
    )
    V_upn_suzun = V_upn_suzun_prev - (V_upn_suzun_0 - VN_upn_suzun_min)/N
    V_upn_lodochny = V_upn_lodochny_prev - (V_upn_lodochny_0 - VN_upn_lodochny_min)/N
    V_upsv_yu = V_upsv_yu_prev - (V_upsv_yu_0 - VN_upsv_yu_min)/N
    V_upsv_s = V_upsv_s_prev - (V_upsv_s_0 - VN_upsv_s_min)/N
    V_cps = V_cps_prev - (V_cps_0 - VN_cps_min)/N
    if flag_sost:
#82. Корректировка сдачи нефти АО «Сузун» Сузунское месторождение (столбец BY):
        knps_lower = VN_knps_min * 0.9
        knps_upper = VN_knps_min * 1.1
        max_iter = 1000
        suzun_lower = V_tstn_norm_suzun * 0.9
        suzun_upper = V_tstn_norm_suzun * 1.1
        iter_count = 0
        V_tstn_suzun_out = None

        while True:
            iter_count += 1
            # --- ЦТН Сузун ---
            V_tstn_suzun = (V_tstn_suzun_prev - F_bp_suzun + G_suzun_slu - F_bp_suzun * (K_suzun / 100))
            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)
            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))
            suzun_ok = suzun_lower <= V_tstn_suzun <= suzun_upper
            knps_ok = knps_lower <= V_knps <= knps_upper
            if suzun_ok and knps_ok:
                break
            # --- корректировка ЦТН Сузун ---
            if not suzun_ok:
                if V_tstn_suzun > suzun_upper:
                    F_bp_suzun += 50
                elif V_tstn_suzun < suzun_lower:
                    F_bp_suzun = max(0, F_bp_suzun - 50)
                # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_suzun_out = {
                    "value": V_tstn_suzun,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_suzun не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_suzun_out is None:
            V_tstn_suzun_out = {"value": V_tstn_suzun, "status": 0, "message": ""}
# Корректировка сдачи нефти АО «Сузун» (Ванкор) (столбец BZ):
        if F_suzun_vankor < 20000:
            if V_tstn_suzun_vankor <= V_tstn_norm_suzun_vankor:
                F_suzun_vankor = 0
            else:
                if V_tstn_suzun_vankor >= (V_tstn_norm_suzun_vankor + F_bp_suzun_vankor):
                    F_suzun_vankor = F_bp_suzun_vankor
                else:
                    F_suzun_vankor = 0
        else:
            suzun_vankor_lower = V_tstn_norm_suzun_vankor * 0.9
            suzun_vankor_upper = V_tstn_norm_suzun_vankor * 1.1

            iter_count = 0
            V_tstn_suzun_vankor_out = None

            while True:
                iter_count += 1
                # --- ЦТН Сузун Ванкор---
                V_tstn_suzun_vankor = V_tstn_suzun_vankor_prev - F_bp_suzun_vankor + (G_buy_day - G_per) - F_bp_suzun_vankor * (K_vankor/100)

                # --- суммарный F_bp ---
                F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

                # --- КНПС ---
                V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))

                # --- защита от отрицательных значений ---
                if V_tstn_suzun_vankor < 0 or V_knps < 0:
                    break

                suzun_vankor_ok = suzun_vankor_lower <= V_tstn_suzun_vankor <= suzun_vankor_upper
                knps_ok = knps_lower <= V_knps <= knps_upper

                if suzun_vankor_ok and knps_ok:
                    break

                # --- корректировка ЦТН Сузун Ванкор ---
                if not suzun_vankor_ok:
                    if V_tstn_suzun_vankor > suzun_vankor_upper:
                        F_bp_suzun_vankor += 50
                    elif V_tstn_suzun_vankor < suzun_vankor_lower:
                        F_bp_suzun_vankor = max(0, F_bp_suzun_vankor - 50)

                if not knps_ok:
                    if V_knps > knps_upper:
                        F_bp_vn += 50
                    elif V_knps < knps_lower:
                        F_bp_vn = max(0, F_bp_vn - 50)

                if iter_count > max_iter:
                    V_tstn_suzun_vankor_out = {
                        "value": V_tstn_suzun_vankor,
                        "status": 1,
                        "message": (
                            "Значение, V_tstn_suzun не удалось скорректировать "
                            f"за отведенное число итераций {iter_count}"
                            ),
                    }
                    break

            if V_tstn_suzun_vankor_out is None:
                V_tstn_suzun_vankor_out = {"value": V_tstn_suzun_vankor, "status": 0, "message": ""}
# Корректировка сдачи нефти АО «Сузун» (ВСЛУ)
        F_suzun_vslu = F_bp_suzun_vslu
# Корректировка сдачи нефти ООО «Тагульское» Лодочное месторождение
        lodochny_lower = V_tstn_norm_lodochny * 0.9
        lodochny_upper = V_tstn_norm_lodochny * 1.1

        iter_count = 0
        V_tstn_lodochny_out = None

        while True:
            iter_count += 1
            # --- ЦТН Лодочный ---
            V_tstn_lodochny = V_tstn_lodochny_prev + G_sikn_tagul + G_lodochny - F_bp_tagul_lpu - F_bp_tagul_lpu * (K_lodochny/100)

            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))

            # --- защита от отрицательных значений ---
            if V_tstn_lodochny < 0 or V_knps < 0:
                break

            lodochny_ok = lodochny_lower <= V_tstn_lodochny <= lodochny_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if lodochny_ok and knps_ok:
                break

            # --- корректировка ЦТН Лодочный ---
            if not lodochny_ok:
                if V_tstn_lodochny > lodochny_upper:
                    F_bp_tagul_lpu += 50
                elif V_tstn_lodochny < lodochny_lower:
                    F_bp_tagul_lpu = max(0, F_bp_tagul_lpu - 50)

            # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_lodochny_out = {
                    "value": V_tstn_lodochny,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_lodochny не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_lodochny_out is None:
            V_tstn_lodochny_out = {"value": V_tstn_lodochny, "status": 0, "message": ""}
# Корректировка сдачи нефти ООО «Тагульское» Тагульское месторождение (столбец CD)
        tagul_lower = V_tstn_norm_tagul * 0.9
        tagul_upper = V_tstn_norm_tagul * 1.1

        iter_count = 0
        V_tstn_tagul_out = None

        while True:
            iter_count += 1
            # --- ЦТН Тагул ---
            V_tstn_tagul = V_tstn_tagul_prev + G_tagul - F_bp_tagul_tpu - F_bp_tagul_tpu * (K_tagul/100)

            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))


            tagul_ok = tagul_lower <= V_tstn_tagul <= tagul_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if tagul_ok and knps_ok:
                break

            # --- корректировка ЦТН Тагул ---
            if not tagul_ok:
                if V_tstn_tagul > tagul_upper:
                    F_bp_tagul_tpu += 50
                elif V_tstn_tagul < tagul_lower:
                    F_bp_tagul_tpu = max(0, F_bp_tagul_tpu - 50)

            # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_tagul_out = {
                    "value": V_tstn_tagul,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_tagul не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_tagul_out is None:
            V_tstn_tagul_out = {"value": V_tstn_tagul, "status": 0, "message": ""}
# Корректировка сдачи нефти ООО «СКН» (столбец CE)
        skn_lower = V_tstn_norm_skn * 0.9
        skn_upper = V_tstn_norm_skn * 1.1

        iter_count = 0
        V_tstn_skn_out = None

        while True:
            iter_count += 1
            # --- ЦТН СКН ---
            V_tstn_skn = V_tstn_skn_prev - F_bp_skn + G_skn - F_bp_skn * (K_skn/100)

            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))


            skn_ok = skn_lower <= V_tstn_skn <= skn_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if skn_ok and knps_ok:
                break

            # --- корректировка ЦТН СКН ---
            if not skn_ok:
                if V_tstn_skn > skn_upper:
                    F_bp_skn += 50
                elif V_tstn_skn < skn_lower:
                    F_bp_skn = max(0, F_bp_skn - 50)

            # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_skn_out = {
                    "value": V_tstn_skn,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_skn не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_skn_out is None:
            V_tstn_skn_out = {"value": V_tstn_skn, "status": 0, "message": ""}
# Корректировка сдачи нефти ООО «Восток Ойл»
        vo_lower = V_tstn_norm_vo * 0.9
        vo_upper = V_tstn_norm_vo * 1.1

        iter_count = 0
        V_tstn_tng_out = None

        while True:
            iter_count += 1
            # --- ЦТН ВО ---
            V_tstn_vo = V_tstn_vo_prev + G_ichem - F_bp_vo - F_bp_vo * (K_ichem/100)

            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))

            vo_ok = vo_lower <= V_tstn_vo <= vo_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if vo_ok and knps_ok:
                break

            # --- корректировка ЦТН ВО ---
            if not vo_ok:
                if V_tstn_vo > vo_upper:
                    F_bp_vo += 50
                elif V_tstn_vo < vo_lower:
                    F_bp_vo = max(0, F_bp_vo - 50)

            # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_vo_out = {
                    "value": V_tstn_vo,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_vo не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_vo_out is None:
            V_tstn_vo_out = {"value": V_tstn_vo, "status": 0, "message": ""}
# Корректировка сдачи нефти АО «Таймыр НГ»
        tng_lower = V_tstn_norm_tng * 0.9
        tng_upper = V_tstn_norm_tng * 1.1

        iter_count = 0
        V_tstn_tng_out = None

        while True:
            iter_count += 1
            # --- ЦТН ТНГ ---
            V_tstn_tng = V_tstn_tng_prev + G_suzun_tng - F_bp_tng - F_bp_tng * (K_payaha/100)

            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))

            tng_ok = tng_lower <= V_tstn_tng <= tng_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if tng_ok and knps_ok:
                break

            # --- корректировка ЦТН ТНГ ---
            if not tng_ok:
                if V_tstn_tng > tng_upper:
                    F_bp_tng += 50
                elif V_tstn_tng < tng_lower:
                    F_bp_tng = max(0, F_bp_tng - 50)

            # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_tng_out = {
                    "value": V_tstn_tng,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_tng не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_tng_out is None:
            V_tstn_tng_out = {"value": V_tstn_tng, "status": 0, "message": ""}
# Корректировка сдачи нефти ООО «КЧНГ»
        kchng_lower = V_tstn_norm_kchng * 0.9
        kchng_upper = V_tstn_norm_kchng * 1.1

        iter_count = 0
        V_tstn_kchng_out = None

        while True:
            iter_count += 1
            # --- ЦТН ТНГ ---
            V_tstn_kchng = V_tstn_kchng_prev + G_kchng - F_bp_kchng - F_bp_kchng * (K_tagul/100)

            # --- суммарный F_bp ---
            F_bp = (F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun)

            # --- КНПС ---
            V_knps = (G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev))

            kchng_ok = kchng_lower <= V_tstn_kchng <= kchng_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if kchng_ok and knps_ok:
                break

            # --- корректировка ЦТН КЧНГ ---
            if not kchng_ok:
                if V_tstn_kchng > kchng_upper:
                    F_bp_kchng += 50
                elif V_tstn_kchng < kchng_lower:
                    F_bp_kchng = max(0, F_bp_kchng - 50)

            # --- корректировка КНПС ---
            if not knps_ok:
                if V_knps > knps_upper:
                    F_bp_vn += 50
                elif V_knps < knps_lower:
                    F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_kchng_out = {
                    "value": V_tstn_kchng,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_kchng не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_kchng_out is None:
            V_tstn_kchng_out = {"value": V_tstn_kchng, "status": 0, "message": ""}
#	Корректировка сдачи нефти АО «Ванкорнефть»
        vn_lower = V_tstn_norm_vn * 0.9
        vn_upper = V_tstn_norm_vn * 1.1

        iter_count = 0
        V_tstn_vn_out = None

        while True:
            iter_count += 1
            # --- суммарный F_bp ---
            F_bp = (
                F_bp_vn + F_bp_tagul_lpu + F_bp_tagul_tpu + F_bp_suzun_vankor
                + F_bp_suzun_vslu + F_bp_skn + F_bp_vo + F_bp_tng + F_bp_kchng + F_bp_suzun
            )

            # --- КНПС ---
            V_knps = (
                G_gnps - F_bp + V_knps_prev + G_tagul + G_upn_lodochny + G_skn + G_kchng
                - (V_nps_2 - V_nps_2_prev) - (V_nps_1 - V_nps_1_prev)
            )

            # --- ЦТН ---
            V_tstn = V_gnps + V_nps_1 + V_nps_2 + V_knps

            # --- ЦТН ВН ---
            V_tstn_vn = (
                V_tstn - V_tstn_rn_vn - V_tstn_suzun - V_tstn_tagul_obch - V_tstn_suzun_vankor
                - V_tstn_suzun_vslu - V_tstn_skn - V_tstn_vo - V_tstn_tng - V_tstn_kchng
            )

            if V_tstn_vn < 0 or V_knps < 0:
                break

            vn_ok = vn_lower <= V_tstn_vn <= vn_upper
            knps_ok = knps_lower <= V_knps <= knps_upper

            if vn_ok and knps_ok:
                break

            # --- корректировка через F_bp_vn ---
            vn_dir = 1 if V_tstn_vn > vn_upper else (-1 if V_tstn_vn < vn_lower else 0)
            knps_dir = 1 if V_knps > knps_upper else (-1 if V_knps < knps_lower else 0)

            if vn_dir == 0:
                direction = knps_dir
            elif knps_dir == 0 or vn_dir == knps_dir:
                direction = vn_dir
            else:
                # При конфликте приоритет за V_tstn_vn
                direction = vn_dir

            if direction > 0:
                F_bp_vn += 50
            elif direction < 0:
                F_bp_vn = max(0, F_bp_vn - 50)

            if iter_count > max_iter:
                V_tstn_vn_out = {
                    "value": V_tstn_vn,
                    "status": 1,
                    "message": (
                        "Значение, V_tstn_vn не удалось скорректировать "
                        f"за отведенное число итераций {iter_count}"
                    ),
                }
                break

        if V_tstn_vn_out is None:
            V_tstn_vn_out = {"value": V_tstn_vn, "status": 0, "message": ""}
        F_suzun = F_bp_suzun
        F_suzun_vankor = F_bp_suzun_vankor
        F_suzun_vslu = F_bp_suzun_vslu 
        F_tagul_lpu = F_bp_tagul_lpu
        F_tagul_tpu = F_bp_tagul_tpu
        F_tagul = F_tagul_lpu+F_tagul_tpu
        F_skn = F_bp_skn
        F_vo = F_bp_vo
        F_tng = F_bp_tng
        F_kchng = F_bp_kchng
        F_vn = F_bp_vn
        F = F_bp
    else:
        F_suzun = F_bp_suzun
        F_suzun_vankor = F_bp_suzun_vankor
        F_suzun_vslu = F_bp_suzun_vslu 
        F_tagul_lpu = F_bp_tagul_lpu
        F_tagul_tpu = F_bp_tagul_tpu
        F_tagul = F_tagul_lpu+F_tagul_tpu
        F_skn = F_bp_skn
        F_vo = F_bp_vo
        F_tng = F_bp_tng
        F_kchng = F_bp_kchng
        F_vn = F_bp_vn
        F = F_bp
        
    return{
        "V_upn_suzun":V_upn_suzun, "V_upn_lodochny":V_upn_lodochny, "V_upsv_yu":V_upsv_yu, "V_upsv_s":V_upsv_s, "V_cps":V_cps,
        "F_suzun":F_suzun, "F_suzun_vankor":F_suzun_vankor, "F_suzun_vslu":F_suzun_vslu, "F_tagul_lpu":F_tagul_lpu, "F_tagul_tpu":F_tagul_tpu,
        "F_skn":F_skn, "F_vo":F_vo, "F_tng":F_tng, "F_kchng":F_kchng, "F_vn":F_vn, "F":F,"F_tagul":F_tagul
    }
# ===============================================================
# ---------------------- Блок «РН Ванкор» проверка: ----------------------
# ===============================================================
def rn_vankor_check(
        VA_upsv_yu_min, V_upsv_yu, VA_upsv_yu_max, V_upsv_yu_prev, V_delta_upsv_yu_max, VO_delta_upsv_yu_max, VA_upsv_s_min, V_upsv_s,
        VA_upsv_s_max,V_upsv_s_prev, V_delta_upsv_s_max, VO_delta_upsv_s_max, VA_cps_min, V_cps, VA_cps_max, V_cps_prev, V_delta_cps_max,
        VO_delta_cps_max, VA_upn_suzun_min, V_upn_suzun, VA_upn_suzun_max, V_upn_suzun_prev, V_delta_upn_suzun_max, VO_delta_upn_suzun_max,
        VA_upn_lodochny_min, V_upn_lodochny, VA_upn_lodochny_max, V_upn_lodochny_prev, V_delta_upn_lodochny_max, VO_upn_lodochny_max,
        VA_tagul_min, V_tagul, VA_tagul_max, VA_gnps_min, V_gnps, VA_gnps_max, V_gnps_prev, V_delta_gnps_max,
        VO_gnps_max, VA_nps_1_min, V_nps_1, VA_nps_1_max, V_nps_1_prev, V_delta_nps_1_max, VO_nps_1_max, VA_nps_2_min,
        V_nps_2, VA_nps_2_max, V_nps_2_prev, V_delta_nps_2_max, VO_nps_2_max, VN_knps_min, V_knps, VN_knps_max, V_knps_prev, V_delta_knps_max,
        VO_knps_max, V_ichem_min, V_ichem, V_ichem_max, V_lodochny_cps_uspv_yu, G_sikn_tagul, V_tstn_min, V_tstn_vn, V_tstn_max,
        V_tstn_suzun_min, V_tstn_suzun, V_tstn_suzun_max, V_tstn_suzun_vankor_min, V_tstn_suzun_vankor, V_tstn_suzun_vankor_max, V_tstn_suzun_vslu_min,
        V_tstn_suzun_vslu, V_tstn_suzun_vslu_max, V_tstn_tagul_obch_min, V_tstn_tagul_obch, V_tstn_tagul_obch_max, V_tstn_lodochny_min,
        V_tstn_lodochny, V_tstn_lodochny_max, V_tstn_tagul_min, V_tstn_tagul, V_tstn_tagul_max, V_tstn_skn_min, V_tstn_skn, V_tstn_skn_max,
        V_tstn_vo_min, V_tstn_vo, V_tstn_vo_max, V_tstn_tng_min, V_tstn_tng, V_tstn_tng_max, V_tstn_kchng_min, V_tstn_kchng, V_tstn_kchng_max,
        G_gnps, p_gnps, Q_gnps_min_1, Q_gnps_max_2, Q_gnps_max_1, G_tagul_lodochny, p_nps_1_2, Q_nps_1_2_min_1, Q_nps_1_2_max_2, Q_nps_1_2_max_1,
        p_knps, Q_knps_min_1, Q_knps_max_2, Q_knps_max_1,F
              ):

# --- 83. Проверка выполнения условий по наличию нефти на УПСВ-Юг
    V_upsv_yu_out = {"value": V_upsv_yu, "status": 0, "message": ""}
    if VA_upsv_yu_min <= V_upsv_yu <= VA_upsv_yu_max:
        V_upsv_yu_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПСВ-Юг выполнена"})
    else:
        if V_upsv_yu < VA_upsv_yu_min:
            msg = "Наличие нефти в РП УПСВ-Юг ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu_out.update({"status": 2, "message": msg})
        elif V_upsv_yu > VA_upsv_yu_max:
            msg = "Наличие нефти в РП УПСВ-Юг выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН-1208 путем уменьшения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu_out.update({"status": 3, "message": msg})
    delta_upsv_yu = V_upsv_yu - V_upsv_yu_prev
    if delta_upsv_yu >= 0:
        if abs(delta_upsv_yu) > V_delta_upsv_yu_max:
            msg = "Скорость наполнения РП УПСВ-Юг больше допустимой величины, необходимо увеличить откачку нефти на СИКН-1208 путем уменьшения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_upsv_yu) > VO_delta_upsv_yu_max:
            msg = "Скорость опорожнения РП УПСВ-Юг больше допустимой величины, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Юг (столбец F) до нужного значения"
            V_upsv_yu_out.update({"status": 5, "message": msg})

# --- 84. Проверка выполнения условий по наличию нефти на УПСВ-Север
    V_upsv_s_out = {"value": V_upsv_s, "status": 0, "message": ""}
    if VA_upsv_s_min <= V_upsv_s <= VA_upsv_s_max:
        V_upsv_s_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПСВ-Север выполнена"})
    else:
        if V_upsv_s < VA_upsv_s_min:
            msg = "Наличие нефти в РП УПСВ-Север ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Север (столбец G) до нужного значения"
            V_upsv_s_out.update({"status": 2, "message": msg})
        elif V_upsv_s > VA_upsv_s_max:
            msg = "Наличие нефти в РП УПСВ-Север выше максимально допустимого значения, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ-Север (столбец G) до нужного значения"
            V_upsv_s_out.update({"status": 3, "message": msg})
    delta_upsv_s = V_upsv_s - V_upsv_s_prev
    if delta_upsv_s >= 0:
        if abs(delta_upsv_s) > V_delta_upsv_s_max:
            msg = "Скорость наполнения РП УПСВ Север больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПСВ Север (столбец G) до нужного значения"
            V_upsv_s_out.update({"status": 4, "message": msg})
        else:
            V_upsv_s_out.update({"status": 1, "message": "Проверка выполнения условий по скорости наполнения РП на УПСВ-Север выполнена"})
    else:
        if abs(delta_upsv_s) > VO_delta_upsv_s_max:
            msg = "Скорость опорожнения РП УПСВ Север больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПСВ Север (столбец G) до нужного значения"
            V_upsv_s_out.update({"status": 5, "message": msg})
        else:
            V_upsv_s_out.update({"status": 1, "message": "Проверка выполнения условий по скорости наполнения РП на УПСВ-Север выполнена"})

# --- 85. Проверка выполнения условий по наличию нефти на ЦПС
    V_cps_out = {"value": V_cps, "status": 0, "message": ""}
    if VA_cps_min <= V_cps <= VA_cps_max:
        V_cps_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на ЦПС выполнена"})
    else:
        if V_cps < VA_cps_min:
            msg = "Наличие нефти в РП ЦПС ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps_out.update({"status": 2, "message": msg})
        elif V_cps > VA_cps_max:
            msg = "Наличие нефти в РП ЦПС выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps_out.update({"status": 3, "message": msg})
    delta_cps = V_cps - V_cps_prev
    if delta_cps >= 0:
        if abs(delta_cps) > V_delta_cps_max:
            msg = "Скорость наполнения РП ЦПС больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_cps) > VO_delta_cps_max:
            msg = "Скорость опорожнения РП ЦПС больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП ЦПС (столбец H) до нужного значения"
            V_cps_out.update({"status": 5, "message": msg})

# --- 86. Проверка выполнения условий по наличию нефти на УПН Сузун
    V_upn_suzun_out = {"value": V_upn_suzun, "status": 0, "message": ""}
    if VA_upn_suzun_min <= V_upn_suzun <= VA_upn_suzun_max:
        V_upn_suzun_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПН Сузун выполнена"})
    else:
        if V_upn_suzun < VA_upn_suzun_min:
            msg = "Наличие нефти в РП УПН Сузун ниже минимального допустимого значения, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun_out.update({"status": 2, "message": msg})
        elif V_upn_suzun > VA_upn_suzun_max:
            msg = "Наличие нефти в РП УПН Сузун выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun_out.update({"status": 3, "message": msg})
    delta_upn_suzun = V_upn_suzun - V_upn_suzun_prev
    if delta_upn_suzun >= 0:
        if abs(delta_upn_suzun) > V_delta_upn_suzun_max:
            msg = "Скорость наполнения РП УПН Сузун больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_upn_suzun) > VO_delta_upn_suzun_max:
            msg = "Скорость опорожнения РП УПН Сузун больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Сузун (столбец V) до нужного значения"
            V_upn_suzun_out.update({"status": 5, "message": msg})

# --- 87. Проверка выполнения условий по наличию нефти на УПН Лодочное
    V_upn_lodochny_out = {"value": V_upn_lodochny, "status": 0, "message": ""}
    if VA_upn_lodochny_min <= V_upn_lodochny <= VA_upn_lodochny_max:
        V_upn_lodochny_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на УПН Лодочное выполнена"})
    else:
        if V_upn_lodochny < VA_upn_lodochny_min:
            msg = "Наличие нефти в РП УПН Лодочное ниже минимально допустимого значения, необходимо уменьшить откачку нефти на СИКН-1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny_out.update({"status": 2, "message": msg})
        elif V_upn_lodochny > VA_upn_lodochny_max:
            msg = "Наличие нефти в РП УПН Лодочное выше максимально допустимого значения, необходимо увеличить откачку нефти на СИКН-1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny_out.update({"status": 3, "message": msg})
    delta_upn_lodochny = V_upn_lodochny - V_upn_lodochny_prev
    if delta_upn_lodochny >= 0:
        if abs(delta_upn_lodochny) > V_delta_upn_lodochny_max:
            msg = "Скорость наполнения РП УПН Лодочное больше допустимой величины, необходимо увеличить откачку нефти на СИКН 1208 путем уменьшения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_upn_lodochny) > VO_upn_lodochny_max:
            msg = "Скорость опорожнения РП УПН Лодочное больше допустимой величины, необходимо уменьшить откачку нефти на СИКН 1208 путем увеличения (ручным вводом) наличия нефти в РП УПН Лодочное (столбец AR) до нужного значения"
            V_upn_lodochny_out.update({"status": 5, "message": msg})
            
# --- 88. Проверка выполнения условий по наличию нефти на Тагульском месторождении
    V_tagul_out = {"value": V_tagul, "status": 0, "message": ""}
    if VA_tagul_min <= V_tagul <= VA_tagul_max:
        V_tagul_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на Тагульском месторождении"})
    else:
        if V_tagul < VA_tagul_min:
            msg = "Наличие нефти в трубопроводах и аппаратах ООО «Тагульское» ниже минимально допустимого значения, необходимо уменьшить откачку нефти в магистральный нефтепровод путем увеличения (ручным вводом) наличия нефти в трубопроводах и аппаратах ООО «Тагульское» (столбец AL) до нужного значения"
            V_tagul_out.update({"status": 2, "message": msg})
        elif V_tagul > VA_tagul_max:
            msg = "Наличие нефти в трубопроводах и аппаратах ООО «Тагульское» выше максимально допустимого значения, необходимо увеличить откачку нефти в магистральный нефтепровод путем уменьшения (ручным вводом) наличия нефти в трубопроводах и аппаратах ООО «Тагульское» (столбец AL) до нужного значения"
            V_tagul_out.update({"status": 3, "message": msg})
    # --- 89. Проверка выполнения условий по наличию нефти на ГНПС
    V_gnps_out = {"value": V_gnps, "status": 0, "message": ""}
    if VA_gnps_min <= V_gnps <= VA_gnps_max:
        V_gnps_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на ГНПС выполнена"})
    else:
        if V_gnps < VA_gnps_min:
            msg = "Наличие нефти в РП ГНПС ниже минимального допустимого значения, необходимо либо уменьшить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо увеличить поступление нефти через СИКН-1208 [путем уменьшения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps_out.update({"status": 2, "message": msg})
        elif V_gnps > VA_gnps_max:
            msg = "Наличие нефти в РП ГНПС выше максимально допустимого значения, необходимо либо увеличить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо уменьшить поступление нефти через СИКН-1208 [путем уменьшения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps_out.update({"status": 3, "message": msg})
    delta_gnps = V_gnps - V_gnps_prev
    if delta_gnps >= 0:
        if abs(delta_gnps) > V_delta_gnps_max:
            msg = "Скорость наполнения РП ГНПС больше допустимой величины, необходимо либо увеличить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо уменьшить поступление нефти через СИКН-1208 [путем увеличения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_gnps) > VO_gnps_max:
            msg = "Скорость опорожнения РП больше допустимой величины, необходимо либо уменьшить (путем ручного ввода нужного значения) откачку нефти с ГНПС (столбец BE), либо увеличить поступление нефти через СИКН-1208 [путем увеличения ручным вводом наличия нефти в РП УПСВ-Ю (столбец F), УПСВ-С (столбец G), ЦПС (столбец H) до нужных показателей]"
            V_gnps_out.update({"status": 5, "message": msg})

# --- 90. Проверка выполнения условий по наличию нефти на НПС-1
    V_nps_1_check_out = {"value": V_nps_1, "status": 0, "message": ""}
    if VA_nps_1_min <= V_nps_1 <= VA_nps_1_max:
        V_nps_1_check_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на НПС-1 выполнена"})
    else:
        if V_nps_1 < VA_nps_1_min:
            msg = "Наличие нефти в РП НПС-1 ниже минимального допустимого значения, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1_check_out.update({"status": 2, "message": msg})
        elif V_nps_1 > VA_nps_1_max:
            msg = "Наличие нефти в РП НПС-1 выше максимально допустимого значения, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1_check_out.update({"status": 3, "message": msg})
    delta_nps_1 = V_nps_1 - V_nps_1_prev
    if delta_nps_1 >= 0:
        if abs(delta_nps_1) > V_delta_nps_1_max:
            msg = "Скорость наполнения РП НПС-1 больше допустимой величины, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем уменьшения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1_check_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_nps_1) > VO_nps_1_max:
            msg = "Скорость опорожнения РП НПС-1 больше допустимой величины, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-1 (столбец BG) до требуемого значения"
            V_nps_1_check_out.update({"status": 5, "message": msg})
            
# --- 91. Проверка выполнения условий по наличию нефти на НПС-2
    V_nps_2_check_out = {"value": V_nps_2, "status": 0, "message": ""}
    if VA_nps_2_min <= V_nps_2 <= VA_nps_2_max:
        V_nps_2_check_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на НПС-2 выполнена"})
    else:
        if V_nps_2 < VA_nps_2_min:
            msg = "Наличие нефти в РП НПС-2 ниже минимального допустимого значения, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2_check_out.update({"status": 2, "message": msg})
        elif V_nps_2 > VA_nps_2_max:
            msg = "Наличие нефти в РП НПС-2 выше максимально допустимого значения, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем уменьшения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2_check_out.update({"status": 3, "message": msg})
    delta_nps_2 = V_nps_2 - V_nps_2_prev
    if delta_nps_2 >= 0:
        if abs(delta_nps_2) > V_delta_nps_2_max:
            msg = "Скорость наполнения РП НПС-2 больше допустимой величины, необходимо увеличить откачку нефти с НПС-1 на НПС-2 путем уменьшения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2_check_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_nps_2) > VO_nps_2_max:
            msg = "Скорость опорожнения РП НПС-2 больше допустимой величины, необходимо уменьшить откачку нефти с НПС-1 на НПС-2 путем увеличения (ручным вводом) наличия нефти в РП НПС-2 до требуемого значения"
            V_nps_2_check_out.update({"status": 5, "message": msg})
# --- 92. Проверка выполнения условий по наличию нефти на КНПС
    V_knps_check_out = {"value": V_knps, "status": 0, "message": ""}
    if VN_knps_min <= V_knps <= VN_knps_max:
        V_knps_check_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти на КНПС выполнена"})
    else:
        if V_knps < VN_knps_min:
            msg = "Наличие нефти в РП КНПС ниже минимального допустимого значения, необходимо уменьшить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps_check_out.update({"status": 2, "message": msg})
        elif V_knps > VN_knps_max:
            msg = "Наличие нефти в РП КНПС выше максимально допустимого значения, необходимо увеличить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps_check_out.update({"status": 3, "message": msg})
    delta_knps = V_knps - V_knps_prev
    if delta_knps >= 0:
        if abs(delta_knps) > V_delta_knps_max:
            msg = "Скорость наполнения РП КНПС больше допустимой величины, необходимо увеличить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps_check_out.update({"status": 4, "message": msg})
    else:
        if abs(delta_knps) > VO_knps_max:
            msg = "Скорость опорожнения РП КНПС больше допустимой величины, необходимо уменьшить (ручным вводом) сдачу нефти АО «ВН» (столбец BX) в магистральный нефтепровод через СИКН 1209 "
            V_knps_check_out.update({"status": 5, "message": msg})
# --- 93. Проверка наличия нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное
    V_ichem_out = {"value": V_ichem, "status": 0, "message": ""}
    if V_ichem_min <= V_ichem <= V_ichem_max:
        V_ichem_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное"})
    else:
        if V_ichem < V_ichem_min:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) откачку нефти Ичемминского ЛУ в магистральный нефтепровод (столбец AW)"
            V_ichem_out.update({"status": 2, "message": msg})
        elif V_ichem > V_ichem_max:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РВС УПН Лодочное больше максимально допустимого значения. Необходимо увеличить (ручным вводом) откачку нефти Ичемминского ЛУ в магистральный нефтепровод (столбец AW)"
            V_ichem_out.update({"status": 3, "message": msg})
# --- 94. Проверка выполнения условий наличия нефти Лодочного ЛУ в РП на ЦПС и УПСВ-Юг
    V_lodochny_cps_uspv_yu_out = {"value": V_lodochny_cps_uspv_yu, "status": 0, "message": ""}
    if V_lodochny_cps_uspv_yu >= 0:
        V_lodochny_cps_uspv_yu_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти Лодочного ЛУ в РП на ЦПС и УПСВ-ЮГ"})
    else:
        msg = "Значение наличия нефти Лодочного ЛУ на ЦПС и на УПСВ-Юг меньше нуля. Необходимо уменьшить откачку нефти ООО «Тагульское» на СИНК-1208 (столбец Р)."
        V_lodochny_cps_uspv_yu_out.update({"status": 2, "message": msg})
        G_sikn_tagul = G_sikn_tagul - abs(V_lodochny_cps_uspv_yu)
# --- 95.	Проверка наличия нефти на объектах ЦТН по недропользователям
    V_tstn_vn_out = {"value": V_tstn_vn, "status": 0, "message": ""}
    if V_tstn_min <= V_tstn_vn <= V_tstn_max:
        V_tstn_vn_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Ванкорнефть» на ЦТН"})
    else:
        if V_tstn_vn < V_tstn_min:
            msg = "Наличие нефти АО «Ванкорнефть» в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «ВН» через СИКН-1209 (столбец BX) до нужного значения"
            V_tstn_vn_out.update({"status": 2, "message": msg})
        elif V_tstn_vn > V_tstn_max:
            msg = "Наличие нефти АО «Ванкорнефть» в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «ВН» через СИКН-1209 (столбец BX) до нужного значения"
            V_tstn_vn_out.update({"status": 3, "message": msg})

    V_tstn_suzun_out = {"value": V_tstn_suzun, "status": 0, "message": ""}
    if V_tstn_suzun_min <= V_tstn_suzun <= V_tstn_suzun_max:
        V_tstn_suzun_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Сузун» на ЦТН"})
    else:
        if V_tstn_suzun < V_tstn_suzun_min:
            msg = "Наличие нефти АО «Сузун» (Сузун) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Сузун» (Сузун) через СИКН-1209 (столбец BY) до нужного значения"
            V_tstn_suzun_out.update({"status": 2, "message": msg})
        elif V_tstn_suzun > V_tstn_suzun_max:
            msg = "Наличие нефти АО «Сузун» (Сузун) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Сузун» (Сузун) через СИКН-1209 (столбец BY) до нужного значения"
            V_tstn_suzun_out.update({"status": 3, "message": msg})

    V_tstn_suzun_vankor_out = {"value": V_tstn_suzun_vankor, "status": 0, "message": ""}
    if V_tstn_suzun_vankor_min <= V_tstn_suzun_vankor <= V_tstn_suzun_vankor_max:
        V_tstn_suzun_vankor_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Сузун» (Ванкор) на ЦТН"})
    else:
        if V_tstn_suzun_vankor < V_tstn_suzun_vankor_min:
            msg = "Наличие нефти АО «Сузун» (Ванкор) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Сузун» (Ванкор) через СИКН-1209 (столбец BZ) до нужного значения"
            V_tstn_suzun_vankor_out.update({"status": 2, "message": msg})
        elif V_tstn_suzun_vankor > V_tstn_suzun_vankor_max:
            msg = "Наличие нефти АО «Сузун» (Ванкор) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Сузун» (Ванкор) через СИКН-1209 (столбец BZ) до нужного значения"
            V_tstn_suzun_vankor_out.update({"status": 3, "message": msg})

    V_tstn_suzun_vslu_out = {"value": V_tstn_suzun_vslu, "status": 0, "message": ""}
    if V_tstn_suzun_vslu_min <= V_tstn_suzun_vslu <= V_tstn_suzun_vslu_max:
        V_tstn_suzun_vslu_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Сузун» (ВСЛУ) на ЦТН"})
    else:
        if V_tstn_suzun_vslu < V_tstn_suzun_vslu_min:
            msg = "Наличие нефти АО «Сузун» (ВСЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Сузун» (ВСЛУ) через СИКН-1209 (столбец CA) до нужного значения"
            V_tstn_suzun_vslu_out.update({"status": 2, "message": msg})
        elif V_tstn_suzun_vslu > V_tstn_suzun_vslu_max:
            msg = "Наличие нефти АО «Сузун» (ВСЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Сузун» (ВСЛУ) через СИКН-1209 (столбец CA) до нужного значения"
            V_tstn_suzun_vslu_out.update({"status": 3, "message": msg})
    
    V_tstn_tagul_obch_out = {"value": V_tstn_tagul_obch, "status": 0, "message": ""}
    if V_tstn_tagul_obch_min <= V_tstn_tagul_obch <= V_tstn_tagul_obch_max:
        V_tstn_tagul_obch_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «Тагульское» (всего) на ЦТН"})
    else:
        if V_tstn_tagul_obch < V_tstn_tagul_obch_min:
            msg = "Наличие нефти ООО «Тагульское» (всего) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC), ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul_obch_out.update({"status": 2, "message": msg})
        elif V_tstn_tagul_obch > V_tstn_tagul_obch_max:
            msg = "Наличие нефти ООО «Тагульское» (всего) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC), ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul_obch_out.update({"status": 3, "message": msg})
    
    V_tstn_lodochny_out = {"value": V_tstn_lodochny, "status": 0, "message": ""}
    if V_tstn_lodochny_min <= V_tstn_lodochny <= V_tstn_lodochny_max:
        V_tstn_lodochny_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «Тагульское» (Лодочный ЛУ) на ЦТН"})
    else:
        if V_tstn_lodochny < V_tstn_lodochny_min:
            msg = "Наличие нефти ООО «Тагульское» (Лодочный ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC) через СИКН-1209 до нужного значения"
            V_tstn_lodochny_out.update({"status": 2, "message": msg})
        elif V_tstn_lodochny > V_tstn_lodochny_max:
            msg = "Наличие нефти ООО «Тагульское» (Лодочный ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Тагульское» (Лодочный ЛУ) (столбец CC)  через СИКН-1209 до нужного значения"
            V_tstn_lodochny_out.update({"status": 3, "message": msg})
    
    V_tstn_tagul_out = {"value": V_tstn_tagul, "status": 0, "message": ""}
    if V_tstn_tagul_min <= V_tstn_tagul <= V_tstn_tagul_max:
        V_tstn_tagul_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «Тагульское» (Тагульский ЛУ) на ЦТН"})
    else:
        if V_tstn_tagul < V_tstn_tagul_min:
            msg = "Наличие нефти ООО «Тагульское» (Тагульский ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul_out.update({"status": 2, "message": msg})
        elif V_tstn_tagul > V_tstn_tagul_max:
            msg = "Наличие нефти ООО «Тагульское» (Тагульский ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Тагульское» (Тагульский ЛУ) (столбец CD) через СИКН-1209 до нужного значения"
            V_tstn_tagul_out.update({"status": 3, "message": msg})
    
    V_tstn_skn_out = {"value": V_tstn_skn, "status": 0, "message": ""}
    if V_tstn_skn_min <= V_tstn_skn <= V_tstn_skn_max:
        V_tstn_skn_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «СевКомНефтегаз» на ЦТН"})
    else:
        if V_tstn_skn < V_tstn_skn_min:
            msg = "Наличие нефти ООО «СевКомНефтегаз» в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «СевКомНефтегаз» через СИКН-1209 (столбец CE) до нужного значения."
            V_tstn_skn_out.update({"status": 2, "message": msg})
        elif V_tstn_skn > V_tstn_skn_max:
            msg = "Наличие нефти ООО «СевКомНефтегаз» в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «СевКомНефтегаз» через СИКН-1209 (столбец CE) до нужного значения."
            V_tstn_skn_out.update({"status": 3, "message": msg})
    
    V_tstn_vo_out = {"value": V_tstn_vo, "status": 0, "message": ""}
    if V_tstn_vo_min <= V_tstn_vo <= V_tstn_vo_max:
        V_tstn_vo_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «Восток Ойл» (Ичемминский ЛУ) на ЦТН"})
    else:
        if V_tstn_vo < V_tstn_vo_min:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «Восток Ойл» (Ичемминский ЛУ) через СИКН-1209 (столбец CF) до нужного значения"
            V_tstn_vo_out.update({"status": 2, "message": msg})
        elif V_tstn_vo > V_tstn_vo_max:
            msg = "Наличие нефти ООО «Восток Ойл» (Ичемминский ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «Восток Ойл» (Ичемминский ЛУ) через СИКН-1209 (столбец CF) до нужного значения"
            V_tstn_vo_out.update({"status": 3, "message": msg})
    
    V_tstn_tng_out = {"value": V_tstn_tng, "status": 0, "message": ""}
    if V_tstn_tng_min <= V_tstn_tng <= V_tstn_tng_max:
        V_tstn_tng_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) на ЦТН"})
    else:
        if V_tstn_tng < V_tstn_tng_min:
            msg = "Наличие нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) через СИКН-1209 (столбец CG) до нужного значения"
            V_tstn_tng_out.update({"status": 2, "message": msg})
        elif V_tstn_tng > V_tstn_tng_max:
            msg = "Наличие нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти АО «Таймырнефтегаз» (Пайяхский ЛУ) через СИКН-1209 (столбец CG) до нужного значения"
            V_tstn_tng_out.update({"status": 3, "message": msg})
    
    V_tstn_kchng_out = {"value": V_tstn_kchng, "status": 0, "message": ""}
    if V_tstn_kchng_min <= V_tstn_kchng <= V_tstn_kchng_max:
        V_tstn_kchng_out.update({"status": 1, "message": "Проверка выполнения условий по наличию нефти ООО «КЧНГ» (Русско-Реченское месторождение) на ЦТН"})
    else:
        if V_tstn_kchng < V_tstn_kchng_min:
            msg = "Наличие нефти ООО «КЧНГ» (Русско-Реченское месторождение) в РП ЦТН ниже минимального допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти ООО «КЧНГ» (Русско-Реченское месторождение) через СИКН-1209 (столбец CH) до нужного значения."
            V_tstn_kchng_out.update({"status": 2, "message": msg})
        elif V_tstn_kchng > V_tstn_kchng_max:
            msg = "Наличие нефти ООО «КЧНГ» (Русско-Реченское месторождение)в РП ЦТН больше максимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти ООО «КЧНГ» (Русско-Реченское месторождение) через СИКН-1209 (столбец CH) до нужного значения"
            V_tstn_kchng_out.update({"status": 3, "message": msg})

# --- 96. Проверка соблюдения нормативных значений насосного оборудования ГНПС
    Q_gnps = G_gnps / (p_gnps / 100 * 24)
    Q_gnps_out = {"value": Q_gnps, "status": 0, "message": ""}
    if Q_gnps < Q_gnps_min_1:
        msg = "Расход нефти на насосы ГНПС ниже минимально допустимого значения. Необходимо увеличить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_gnps_out.update({"status": 3, "message": msg})
    elif Q_gnps > Q_gnps_max_2:
        msg = "Расход нефти на насосы ГНПС больше максимально допустимого значения. Необходимо уменьшить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_gnps_out.update({"status": 4, "message": msg})
    elif Q_gnps <= Q_gnps_max_1:
        Q_gnps_out.update({"status": 1, "message": "Режим работы насосного оборудования 1-1-1"})
    else:
        Q_gnps_out.update({"status": 2, "message": "Режим работы насосного оборудования 2-2-2. Рекомендуется перераспределить объемы перекачиваемой нефти."})
    # --- 97. Проверка соблюдения нормативных значений насосного оборудования ГНПС
    Q_nps_1_2 = (G_gnps + G_tagul_lodochny + V_nps_1 - V_nps_1_prev + V_nps_2 - V_nps_2_prev) / (p_nps_1_2 / 100 * 24)
    Q_nps_1_2_out = {"value": Q_nps_1_2, "status": 0, "message": ""}
    if Q_nps_1_2 < Q_nps_1_2_min_1:
        msg = "Расход нефти на насосы НПС-1, НПС-2 ниже минимально допустимого значения. Необходимо увеличить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_nps_1_2_out.update({"status": 3, "message": msg})
    elif Q_nps_1_2 > Q_nps_1_2_max_2:
        msg = "Расход нефти на насосы НПС-1, НПС-2 больше максимально допустимого значения. Необходимо уменьшить (ручным вводом) откачку нефти с ГНПС (столбец BE) до нужного значения"
        Q_nps_1_2_out.update({"status": 4, "message": msg})
    elif Q_nps_1_2 <= Q_nps_1_2_max_1:
        Q_nps_1_2_out.update({"status": 1, "message": "Режим работы насосного оборудования 1-1-1"})
    else:
        Q_nps_1_2_out.update({"status": 2, "message": "Режим работы насосного оборудования 2-2-2. Рекомендуется перераспределить объемы перекачиваемой нефти."})
    # --- 98. Проверка соблюдения нормативных значений насосного оборудования КНПС
    Q_knps = F / (p_knps / 100 * 24)
    Q_knps_out = {"value": Q_knps, "status": 0, "message": ""}
    if Q_knps < Q_knps_min_1:
        msg = "Расход нефти на насосы КНПС ниже минимально допустимого значения. Необходимо увеличить (ручным вводом) сдачу нефти через СИКН-1209 (столбцы BX-CH) до нужного значения "
        Q_knps_out.update({"status": 3, "message": msg})
    elif Q_knps > Q_knps_max_2:
        msg = "Расход нефти на насосы КНПС больше максимально допустимого значения. Необходимо уменьшить (ручным вводом) сдачу нефти через СИКН-1209 (столбцы BX-CH) до нужного значения "
        Q_knps_out.update({"status": 4, "message": msg})
    elif Q_knps <= Q_knps_max_1:
        Q_knps_out.update({"status": 1, "message": "Режим работы насосного оборудования 1-1-1"})
    else:
        Q_knps_out.update({"status": 2, "message": "Режим работы насосного оборудования 2-2-2. Рекомендуется рассмотреть возможность перераспределения перекачиваемой нефти по дням."})
    return{
        "V_upsv_yu_out":V_upsv_yu_out, "V_upsv_s_out":V_upsv_s_out, "V_cps_out":V_cps_out, "V_upn_suzun_out":V_upn_suzun_out, "V_upn_lodochny_out":V_upn_lodochny_out,
        "V_tagul_tr_out":V_tagul_out, "V_gnps_out":V_gnps_out, "V_nps_1_check_out":V_nps_1_check_out, "V_nps_2_check_out":V_nps_2_check_out,
        "V_knps_check_out":V_knps_check_out, "V_ichem_out":V_ichem_out, "V_lodochny_cps_uspv_yu_out":V_lodochny_cps_uspv_yu_out, "V_tstn_vn_out":V_tstn_vn_out,
        "V_tstn_suzun_out":V_tstn_suzun_out, "V_tstn_suzun_vankor_out":V_tstn_suzun_vankor_out, "V_tstn_suzun_vslu_out":V_tstn_suzun_vslu_out,
        "V_tstn_tagul_obch_out":V_tstn_tagul_obch_out, "V_tstn_lodochny_out":V_tstn_lodochny_out, "V_tstn_tagul_out":V_tstn_tagul_out, "V_tstn_skn_out":V_tstn_skn_out,
        "V_tstn_vo_out":V_tstn_vo_out, "V_tstn_tng_out":V_tstn_tng_out, "V_tstn_kchng_out":V_tstn_kchng_out, "Q_gnps":Q_gnps, "Q_gnps_out":Q_gnps_out,
        "Q_nps_1_2":Q_nps_1_2, "Q_nps_1_2_out":Q_nps_1_2_out, "Q_knps":Q_knps, "F":F
    }   
# ===============================================================
# ---------------------- Блок «Сравнения плановой сдачи нефти с бизнес-планом» ----------------------
# ===============================================================
# --- 99.	Расчет суммарной плановой сдачи нефти по недропользователям и расчет отклонений от БП:
def plan_sdacha (F_vn, F_vn_plan, F_suzun, F_suzun_vankor, F_suzun_plan, F_suzun_vankor_plan,
        F_suzun_vsly, F_suzun_vsly_plan, F_tagul_lpy, F_tagul_lpy_plan, F_tagul_tpy, F_tagul_tpy_plan, F_skn, F_vo_plan, F_vo, F_tng,
        F_tng_plan, F_kchng, F_kchng_plan,F_skn_plan):
    def delta(F, F_plan):
        return F - F_plan
    F_vn_delta = delta(F_vn, F_vn_plan)
    F_suzun_delta = delta(F_suzun, F_suzun_plan)
    F_suzun_vankor_delta = delta(F_suzun_vankor, F_suzun_vankor_plan)
    F_suzun_vsly_delta = delta(F_suzun_vsly, F_suzun_vsly_plan)
    F_tagul_lpy_delta = delta(F_tagul_lpy, F_tagul_lpy_plan)
    F_tagul_tpy_delta = delta(F_tagul_tpy, F_tagul_tpy_plan)
    F_tagul_delta = F_tagul_lpy_delta + F_tagul_tpy_delta
    F_skn_delta = delta(F_skn, F_skn_plan)
    F_vo_delta = delta(F_vo, F_vo_plan)
    F_tng_delta = delta(F_tng, F_tng_plan)
    F_kchng_delta = delta(F_kchng, F_kchng_plan)
    F_delta = F_vn_delta + F_suzun_delta + F_tagul_lpy_delta + F_tagul_tpy_delta + F_suzun_vankor_delta + F_suzun_vsly_delta + F_skn_delta + F_vo_delta + F_tng_delta + F_kchng_delta
    return{
        "F_vn_delta":F_vn_delta, "F_suzun_delta":F_suzun_delta, "F_suzun_vankor_delta":F_suzun_vankor_delta, "F_suzun_vsly_delta":F_suzun_vsly_delta,
        "F_tagul_lpy_delta":F_tagul_lpy_delta, "F_tagul_tpy_delta":F_tagul_tpy_delta, "F_tagul_delta":F_tagul_delta, "F_skn_delta":F_skn_delta,
        "F_vo_delta":F_vo_delta, "F_tng_delta":F_tng_delta, "F_kchng_delta":F_kchng_delta, "F_delta":F_delta
    }
# ===============================================================
# ---------------------- Блок «Сравнения плановой сдачи нефти с бизнес-планом» ----------------------
# ===============================================================
def balance_po_business_plan (
        V_vn_nm_ost_np, V_vn_nm_ost_app, V_vn_nm_ost_texn, V_vn_nm_path, Q_vn_condensate, Q_vn_oil, V_vn_lost_oil, V_vn_lost_condensate,
        V_vn_lost_transport, G_vn_release_rn_drillig, G_vn_release_suzun, G_vn_release_well_service, V_vn_km_ost_np, V_vn_km_ost_app,
        V_vn_km_ost_texn, V_vn_km_path, F_vn_total, V_suzun_nm_ost_np, V_suzun_nm_ost_app, V_suzun_nm_ost_texn, V_suzun_ost_app,V_suzun_km_texn,V_suzun_nm_path,
        Q_suzun_oil, Q_suzun_condensate, V_suzun_lost_oil, G_suzun_buy, V_suzun_lost_transport_suzun, V_suzun_lost_transport_vankor,
        G_suzun_mupn, G_suzun_release_rn_drillig, F_suzun_vankor, F_suzun_total, V_suzun_km_ost_np,V_suzun_km_path, V_vo_nm_ost_np, V_vo_nm_ost_app,
        V_vo_nm_ost_texn, V_vo_nm_path, Q_vo_oil, Q_vo_condensate, V_vo_lost_oil, V_vo_lost_condensate, V_vo_lost_transport, G_vo_fuel, G_vo_fill,
        G_vn_fuel, G_vn_fill, V_vo_km_ost_np, V_vo_km_ost_app, V_vo_km_ost_texn, V_vo_km_path, G_vo_release, F_vo_total,
        V_lodochny_nm_ost_np, V_lodochny_nm_ost_app, V_lodochny_nm_ost_texn, V_lodochny_nm_path, Q_lodochny_oil, Q_lodochny_condensate,
        V_lodochny_lost_oil, V_lodochny_lost_transport, G_lodochny_fuel, G_lodochny_release_rn_drillig, V_lodochny_km_ost_np, V_lodochny_km_ost_app,
        V_lodochny_km_ost_texn, V_lodochny_km_path, F_lodochny_total, V_tagul_nm_ost_np, V_tagul_nm_ost_app, V_tagul_nm_ost_texn,
        V_tagul_nm_path, Q_tagul_oil, Q_tagul_condensate, V_tagul_lost_oil, V_tagul_lost_transport, G_tagul_fuel, G_tagul_release_rn_drillig,
        G_tagul_release_vpt_neftmash, V_tagul_km_ost_np, V_tagul_km_ost_app, V_tagul_km_ost_texn, V_tagul_km_path, F_tagul_total,

):

# Остатки нефти на ВПУ на начало месяца
    V_vn_nm_ost_vpy = V_vn_nm_ost_np + V_vn_nm_ost_app + V_vn_nm_ost_texn
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_vn_nm_ost = V_vn_nm_ost_vpy + V_vn_nm_path
# Добыча нефти (газового конденсата)
    Q_vn_total = Q_vn_oil + Q_vn_condensate
#  Технологические потери нефти (газового конденсата)
    V_vn_lost = V_vn_lost_oil + V_vn_lost_condensate + V_vn_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vn_own = G_vn_fuel + G_vn_fill
# Отпуск нефти (газового конденсата), всего
    G_vn_release = G_vn_release_rn_drillig + G_vn_release_suzun + G_vn_release_well_service
# Остатки нефти на ВПУ на конец месяца
    V_vn_km_ost_vpy = V_vn_km_ost_np + V_vn_km_ost_app + V_vn_km_ost_texn
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_vn_km_ost = V_vn_km_ost_vpy + V_vn_km_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delte_V_vn_ost = V_vn_km_ost - V_vn_nm_ost
# Выполнение процедуры проверки
    V_vn_check = (V_vn_nm_ost + Q_vn_total) - (V_vn_lost + G_vn_own + G_vn_release + F_vn_total + V_vn_km_ost)
    V_vn_check_out = V_vn_check
    if V_vn_check != 0:
        V_vn_check_out = {
            "value": V_vn_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
# _____________Формирование планового баланса добычи-сдачи нефти по АО «Сузун» (Бизнес-план)_____________
# Остатки нефти на СПУ на начало месяца
    V_suzun_nm_ost_spy = V_suzun_nm_ost_np + V_suzun_nm_ost_app + V_suzun_nm_ost_texn
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_suzun_nm_ost = V_suzun_nm_ost_spy + V_suzun_nm_path
# Добыча нефти (газового конденсата)
    Q_suzun_total = Q_suzun_oil + Q_suzun_condensate
# Технологические потери нефти (газового конденсата)
    V_suzun_lost = V_suzun_lost_oil + V_suzun_lost_transport_suzun + V_suzun_lost_transport_vankor
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_suzun_own = G_suzun_mupn
# Отпуск нефти (газового конденсата), всего
    G_suzun_release = G_suzun_release_rn_drillig
# Сдача нефти (газового конденсата) АО «Сузун» (Сузунское м/р)
    F_suzun_suzun = F_suzun_total + F_suzun_vankor
# Остатки нефти на СПУ на конец месяца
    V_suzun_km_ost_spy = V_suzun_km_ost_np + V_suzun_ost_app + V_suzun_km_texn
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_suzun_km_ost = V_suzun_km_ost_spy + V_suzun_km_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_suzun_delta_ost = V_suzun_km_ost - V_suzun_nm_ost
# Выполнение процедуры проверки
    V_suzun_check = (V_suzun_nm_ost + Q_suzun_total + G_suzun_buy) - (V_suzun_lost + G_suzun_own + G_suzun_release + F_suzun_total + V_suzun_km_ost)
    V_suzun_check_out = V_suzun_check
    if V_suzun_check != 0:
        V_suzun_check_out = {
            "value": V_suzun_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Восток Ойл» (Бизнес-план)_____________
# Остатки нефти на ВПУ на начало месяца
    V_vo_nm_ost_vpy = V_vo_nm_ost_np + V_vo_nm_ost_app + V_vo_nm_ost_texn
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_vo_nm_ost = V_vo_nm_ost_vpy + V_vo_nm_path
# Добыча нефти (газового конденсата)
    Q_vo_total = Q_vo_oil + Q_vo_condensate
# Технологические потери нефти (газового конденсата)
    V_vo_lost = V_vo_lost_oil + V_vo_lost_condensate + V_vo_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vo_own = G_vo_fuel + G_vo_fill
# Остатки нефти на ВПУ на конец месяца
    V_vo_km_ost_vpy = V_vo_km_ost_np + V_vo_km_ost_app + V_vo_km_ost_texn
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_vo_km_ost = V_vo_km_ost_vpy + V_vo_km_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delte_V_vo_ost = V_vo_km_ost - V_vo_nm_ost
# Выполнение процедуры проверки
    V_vo_check = (V_vo_nm_ost + Q_vo_total) - (V_vo_lost + G_vo_own + G_vo_release + F_vo_total + V_vo_km_ost)
    V_vo_check_out = V_vo_check
    if V_vo_check != 0:
        V_vo_check_out = {
            "value": V_vo_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
#  Формирование планового баланса добычи-сдачи нефти по ООО «Тагульское» Лодочное месторождение (Бизнес-план)
# Остатки нефти на ЛПУ на начало месяца
    V_lodochny_nm_ost_lpy = V_lodochny_nm_ost_np + V_lodochny_nm_ost_app + V_lodochny_nm_ost_texn
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_lodochny_nm_ost = V_lodochny_nm_ost_lpy + V_lodochny_nm_path
# Добыча нефти (газового конденсата)
    Q_lodochny_total = Q_lodochny_oil + Q_lodochny_condensate
# Технологические потери нефти (газового конденсата)
    V_lodochny_lost = V_lodochny_lost_oil + V_lodochny_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_lodochny_release = G_lodochny_fuel
# Отпуск нефти (газового конденсата), всего
    G_lodochny_own = G_lodochny_release_rn_drillig
# Остатки нефти на ЛПУ на конец месяца
    V_lodochny_km_ost_lpy = V_lodochny_km_ost_np + V_lodochny_km_ost_app + V_lodochny_km_ost_texn
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_lodochny_km_ost = V_lodochny_km_ost_lpy + V_lodochny_km_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_lodochny_delta_ost = V_lodochny_km_ost - V_lodochny_nm_ost
# Выполнение процедуры проверки
    V_lodochny_check = (V_lodochny_nm_ost + Q_lodochny_total) - (V_lodochny_lost + G_lodochny_release + F_lodochny_total + V_lodochny_km_ost)
    V_lodochny_check_out = V_lodochny_check
    if V_lodochny_check != 0:
        V_lodochny_check_out = {
            "value": V_lodochny_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Тагульское» Тагульское месторождение (Бизнес-план):_____________
# Остатки нефти на ТПУ на начало месяца
    V_tagul_nm_ost_tpy = V_tagul_nm_ost_np + V_tagul_nm_ost_app + V_tagul_nm_ost_texn
# Остатки нефти (газового конденсата) на начало месяца, всего
    V_tagul_nm_ost = V_tagul_nm_ost_tpy + V_tagul_nm_path
# Добыча нефти (газового конденсата)
    Q_tagul_total = Q_tagul_oil + Q_tagul_condensate
# Технологические потери нефти (газового конденсата)
    V_tagul_lost = V_tagul_lost_oil + V_tagul_lost_transport
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_tagul_own = G_tagul_fuel
# Отпуск нефти (газового конденсата), всего
    G_tagul_release = G_tagul_release_rn_drillig + G_tagul_release_vpt_neftmash
# Остатки нефти на ТПУ на конец месяца
    V_tagul_km_ost_tpy = V_tagul_km_ost_np + V_tagul_km_ost_app + V_tagul_km_ost_texn
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_tagul_km_ost = V_tagul_km_ost_tpy + V_tagul_km_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    V_tagul_delta_ost = V_tagul_km_ost - V_tagul_nm_ost
# Выполнение процедуры проверки
    V_tagul_check = (V_tagul_nm_ost + Q_tagul_total) - (V_tagul_lost + G_tagul_own + G_tagul_release + F_tagul_total + V_tagul_km_ost)
    V_tagul_check_out = V_tagul_check
    if V_tagul_check != 0:
        V_tagul_check_out = {
            "value": V_tagul_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
    return{
        "V_vn_nm_ost_vpy":V_vn_nm_ost_vpy, "V_vn_nm_ost":V_vn_nm_ost, "Q_vn_total":Q_vn_total, "V_vn_lost":V_vn_lost, "G_vn_own":G_vn_own,
        "G_vn_release":G_vn_release, "V_vn_km_ost_vpy":V_vn_km_ost_vpy, "V_vn_km_ost":V_vn_km_ost, "delte_V_vn_ost":delte_V_vn_ost,
        "V_vn_check":V_vn_check_out, "V_suzun_nm_ost_spy":V_suzun_nm_ost_spy, "V_suzun_nm_ost":V_suzun_nm_ost, "Q_suzun_total":Q_suzun_total,
        "V_suzun_lost":V_suzun_lost, "G_suzun_own":G_suzun_own, "G_suzun_release":G_suzun_release, "F_suzun_suzun":F_suzun_suzun,
        "V_suzun_km_ost_spy":V_suzun_km_ost_spy,"V_suzun_km_ost":V_suzun_km_ost, "V_suzun_delta_ost":V_suzun_delta_ost, "V_suzun_check":V_suzun_check_out,
        "V_vo_nm_ost_vpy":V_vo_nm_ost_vpy, "V_vo_nm_ost":V_vo_nm_ost, "Q_vo_total":Q_vo_total, "V_vo_lost":V_vo_lost, "G_vo_own":G_vo_own,
        "V_vo_km_ost_vpy":V_vo_km_ost_vpy, "V_vo_km_ost":V_vo_km_ost, "delte_V_vo_ost":delte_V_vo_ost, "V_vo_check":V_vo_check_out,
        "V_lodochny_nm_ost_lpy":V_lodochny_nm_ost_lpy, "V_lodochny_nm_ost":V_lodochny_nm_ost, "Q_lodochny_total":Q_lodochny_total, "V_lodochny_lost":V_lodochny_lost,
        "G_lodochny_release":G_lodochny_release, "G_lodochny_own":G_lodochny_own, "V_lodochny_km_ost_lpy":V_lodochny_km_ost_lpy,"V_lodochny_km_ost":V_lodochny_km_ost,
        "V_lodochny_delta_ost":V_lodochny_delta_ost, "V_lodochny_check":V_lodochny_check_out, "V_tagul_nm_ost_tpy":V_tagul_nm_ost_tpy, "V_tagul_nm_ost":V_tagul_nm_ost,
        "Q_tagul_total":Q_tagul_total, "V_tagul_lost":V_tagul_lost, "G_tagul_own":G_tagul_own, "G_tagul_release":G_tagul_release, "V_tagul_km_ost_tpy":V_tagul_km_ost_tpy,
        "V_tagul_km_ost":V_tagul_km_ost, "V_tagul_delta_ost":V_tagul_delta_ost, "V_tagul_check":V_tagul_check_out
    }
# ===============================================================
# ---------------------- Блок «Формирование плановых балансов по ГТМ» ----------------------
# ===============================================================
def plan_balance_gtm (
        V_cppn_1_0, V_vn_nm_gtm_ost_dead, V_tstn_vn_0, V_vn_nm_gtm_ost_np, V_vn_nm_gtm_ost_app, Q_vankor_month, Q_vn_gtm_condensate, F_vn,
        K_vankor_mining, K_vankor, V_vn_gtm_lost_condensate, G_vn_gtm_fuel, G_vn_gtm_fill, G_buy_month, G_vn_gtm_release_tbs, G_vn_gtm_release_rn_drilling,
        V_cppn_1, V_vn_nm_gtm_ost_rvs_clear, V_vn_nm_gtm_ost_product, V_vn_km_gtm_ost_app, V_tstn_vn, V_suzun_slu_0, V_suzun_vslu_0,
        V_suzun_nm_gtm_ost_cps, V_suzun_nm_gtm_ost_dead, V_suzun_nm_gtm_ost_texn, V_suzun_nm_gtm_ost_np, V_suzun_nm_tgm_ost_app, V_suzun_nm_gtm_ost_rvs,
        V_suzun_0, V_vankor_suzun_0, V_vankor_vslu_0, Q_suzun_month, Q_vslu_month, Q_suzun_gtm_condensate, K_suzun_mining, G_per_month, G_suzun_gtm_fuel,
        F_suzun_delta, F_suzun_vsly_delta, F_suzun_vankor_delta, K_suzun, V_suzun_nm_gtm_ost_app, V_suzun_nm_gtm_ost_product, V_suzun_slu,
        V_suzun_vslu, V_suzun_km_gtm_ost_cps, G_suzun_gtm_release, V_tstn_suzun, V_tstn_suzun_vslu, V_ichem_0, V_vo_nm_gtm_ost_texn,
        V_tstn_vo_0, V_vo_nm_gtm_ost_np, Q_vo_month, Q_vo_gtm_condensate, F_vo_delta, K_vo_trans, K_vo_mining, V_vo_gtm_lost_condensate,
        G_vo_gtm_fuel, G_vo_gtm_fill, V_vo_nm_gtm_ost_app, V_vo_nm_gtm_ost_dead, V_vo_nm_gtm_ost_product, V_ichem, G_vo_gtm_release, V_tstn_vo,
        V_lodochny_0, V_lodochny_nm_gtm_ost_upn_ichem, V_lodochny_nm_gtm_ost_upsv_yu, V_tstn_lodochny_0, V_lodochny_nm_gtm_ost_np, V_lodochny_nm_gtm_ost_app,
        Q_lodochny_month, Q_lodochny_gtm_condensate, F_tagul_lpy_delta, K_lodochny_mining, K_lodochny_trans, V_lodochny_nm_gtm_dead, V_lodochny_nm_gtm_ost_product,
        V_lodochny_nm_gtm_ost_rvs_clear, V_lodochny, G_lodochny_gtm_release, G_lodochny_gtm_own, V_tstn_lodochny, V_tagul_nm_gtm_ost_dead,
        V_tagul_nm_gtm_ost_texn, V_tagul_nm_gtm_ost_rvs_clear, V_tagul_nm_gtm_ost_product, V_tagul_nm_gtm_ost_np, V_tagul_nm_gtm_ost_app,
        V_tstn_tagul_0, Q_tagul_month, Q_tagul_gtm_condensate, F_tagul_tpy_delta, K_tagul_minig, K_tagul, G_tagul_gtm_fuel, G_tagul_gtm_release_russko_rechenskoe,
        G_tagul_gtm_release_rn_drilling, V_tagul_km_gtm_ost_np, V_tagul_km_gtm_ost_app, V_tstn_tagul, V_tstn_suzun_vankor
):
# Технологические остатки нефти в резервуарах ВПУ на начало месяца отчетного периода
    V_vn_nm_gtm_ost_texn = V_cppn_1_0
# Остатки нефти в резервуарах ВПУ на начало месяца отчетного периода
    V_vn_nm_gtm_ost_rvs = V_vn_nm_gtm_ost_dead + V_vn_nm_gtm_ost_texn
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_vn_nm_gtm_path = V_tstn_vn_0
# Остатки нефти (газового конденсата) на ВПУ
    V_vn_nm_gtm_ost_vpy = V_vn_nm_gtm_ost_np + V_vn_nm_gtm_ost_app + V_vn_nm_gtm_ost_rvs
# Остатки нефти (газового конденсата) АО «Ванкорнефть», всего
    V_vn_nm_gtm_ost = V_vn_nm_gtm_ost_vpy + V_vn_nm_gtm_path
# Добыча нефти (газового конденсата) АО «Ванкорнефть», всего
    Q_vn_gtm_total = Q_vankor_month
# Добыча нефти АО «Ванкорнефть»
    Q_vn_gtm_oil = Q_vn_gtm_total - Q_vn_gtm_condensate
# Сдача нефти АО «Ванкорнефть»
    F_vn_gtm_total = F_vn
# Технологические потери нефти при добыче и подготовке
    V_vn_gtm_lost_oil = Q_vn_gtm_total * (K_vankor_mining/100)
#  Технологические потери нефти (газового конденсата) при транспортировке
    V_vn_gtm_lost_path = round(F_vn_gtm_total * (K_vankor/100))
# Технологические потери нефти (газового конденсата), всего
    V_vn_gtm_lost = V_vn_gtm_lost_oil + V_vn_gtm_lost_condensate + V_vn_gtm_lost_path
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vn_gtm_own = G_vn_gtm_fuel + G_vn_gtm_fill
# Отпуск нефти АО «Сузун»
    G_vn_gtm_release_suzun = G_buy_month
# Отпуск нефти (газового конденсата) АО «Ванкорнефть», всего
    G_vn_gtm_release = G_vn_gtm_release_tbs + G_vn_gtm_release_rn_drilling + G_vn_gtm_release_suzun
# Остатки нефти на ВПУ в нефтепроводах на конец месяца
    V_vn_km_gtm_ost_np = V_vn_nm_gtm_ost_np
# Технологические остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vn_km_gtm_ost_texn = V_cppn_1
# Мертвые остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vn_km_gtm_ost_dead = V_vn_nm_gtm_ost_dead
# Остатки нефти в РВС очистных сооружений на конец месяца отчетного периода
    V_vn_km_gtm_ost_rvs_clear = V_vn_nm_gtm_ost_rvs_clear
# Товарный остатки нефти на конец месяца отчетного периода
    V_vn_km_gtm_ost_product = V_vn_nm_gtm_ost_product
# Остатки нефти на ВПУ на конец месяца, всего
    V_vn_km_gtm_ost_vpu = V_vn_km_gtm_ost_np + V_vn_km_gtm_ost_app + V_vn_km_gtm_ost_texn
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_vn_km_gtm_path = V_vn_nm_gtm_ost + Q_vn_gtm_total - V_vn_gtm_lost - V_vn_km_gtm_ost_vpu - G_vn_gtm_release - G_vn_gtm_own - F_vn_gtm_total
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_vn_km_gtm_ost = V_vn_km_gtm_ost_vpu + V_vn_km_gtm_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delte_V_vn_gtm_ost = V_vn_km_gtm_ost - V_vn_nm_gtm_ost
#
    V_vn_gtm_check = (V_vn_nm_gtm_ost + Q_vn_gtm_total) - (V_vn_gtm_lost + G_vn_gtm_own + G_vn_gtm_release + F_vn_gtm_total + V_vn_km_gtm_ost)
    V_vn_gtm_check_out = V_vn_gtm_check
    if V_vn_gtm_check != 0:
        V_vn_gtm_check_out = {
            "value": V_vn_gtm_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
    V_vn_balance_check_out = V_tstn_vn
    if abs(V_tstn_vn - V_vn_km_gtm_path) > 80:
        V_vn_balance_check_out = {
            "value": V_tstn_vn,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
# _____________Формирование планового баланса добычи-сдачи нефти по АО «Сузун»:_____________
#Технологические остатки нефти в резервуарах УПН ЦППН №2 на начало месяца отчетного периода
    V_suzun_nm_gtm_ost_upn = V_suzun_slu_0 + V_suzun_vslu_0
# Технологические остатки нефти в резервуарах СПУ на начало месяца отчетного периода
    V_suzun_nm_ost_rvs = V_suzun_nm_gtm_ost_upn + V_suzun_nm_gtm_ost_cps
# Остатки нефти в резервуарах СПУ на начало месяца отчетного периода
    V_suzun_gtm_ost_rvs = V_suzun_nm_gtm_ost_dead + V_suzun_nm_gtm_ost_texn
# Остатки нефти (газового конденсата) на СПУ
    V_suzun_nm_gtm_ost_spu = V_suzun_nm_gtm_ost_np + V_suzun_nm_tgm_ost_app + V_suzun_nm_gtm_ost_rvs
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_suzun_nm_gtm_path = V_suzun_0 + V_vankor_suzun_0 + V_vankor_vslu_0
# Остатки нефти (газового конденсата) АО «Сузун», всего
    V_suzun_nm_gtm_ost = V_suzun_nm_gtm_ost_spu + V_suzun_nm_gtm_path
# Добыча нефти Сузунского ЛУ
    Q_suzun_gtm_oil_slu = Q_suzun_month
# Добыча нефти Восточно-Сузунского ЛУ
    Q_suzun_gtm_oil_vslu = Q_vslu_month
# Добыча нефти (газового конденсата) АО «Сузун», всего
    Q_suzun_gtm_total = Q_suzun_gtm_oil_slu + Q_suzun_gtm_oil_vslu + Q_suzun_gtm_condensate
# Технологические потери нефти при добыче и подготовке
    V_suzun_gtm_lost_oil = round(Q_suzun_gtm_oil_slu * (K_suzun_mining/100))
# Расход нефти (газового конденсата) на переработку на малогабаритных установках переработки нефти (МУПН)
    G_suzun_gtm_mupn = G_per_month
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_suzun_gtm_own = G_suzun_gtm_fuel + G_suzun_gtm_mupn
# Приобретение нефти у сторонних организаций (АО «Ванкорнефть»)
    G_suzun_gtm_buy = G_buy_month
# Сдача нефти АО «Сузун» (Сузунский ЛУ)____Добавить после автобаланса
    F_suzun_gtm_slu = F_suzun_delta
# Сдача нефти АО «Сузун» (Восточно-Сузунский ЛУ)____Добавить после автобаланса
    F_suzun_gtm_vslu = F_suzun_vsly_delta
# Сдача нефти АО «Сузун» (АО «Ванкорнефть»)____Добавить после автобаланса
    F_suzun_gtm_vankor = F_suzun_vankor_delta
# Сдача нефти (газового конденсата) АО «Сузун», всего
    F_suzun_gtm_total = F_suzun_gtm_slu + F_suzun_gtm_vslu + F_suzun_gtm_vankor
# Технологические потери нефти (газового конденсата) при транспортировке (Сузунский ЛУ)
    V_suzun_gtm_lost_slu = round(F_suzun_gtm_slu * (K_suzun/100))
# Технологические потери нефти (газового конденсата) при транспортировке (Восточно-Сузунский ЛУ)
    V_suzun_gtm_lost_vslu = round(F_suzun_gtm_vslu * (K_suzun/100))
# Технологические потери нефти (газового конденсата) при транспортировке (Восточно-Сузунский ЛУ)
    V_suzun_gtm_lost_vankor = round(F_suzun_gtm_vankor * (K_vankor/100))
# Технологические потери нефти (газового конденсата), всего
    V_suzun_gtm_lost = V_suzun_gtm_lost_oil + V_suzun_gtm_lost_slu + V_suzun_gtm_lost_vslu + V_suzun_nm_gtm_ost
# Остатки нефти на СПУ в нефтепроводах на конец месяца отчетного периода
    V_suzun_km_gtm_ost_np = V_suzun_nm_gtm_ost_np
# Остатки нефти в аппаратах СПУ на конец месяца отчетного периода
    V_suzun_km_gtm_ost_app = V_suzun_nm_gtm_ost_app
# Мертвые остатки нефти в резервуарах СПУ на конец месяца отчетного
    V_suzun_gtm_ost_dead = V_suzun_nm_gtm_ost_dead
# Товарные остатки нефти на конец месяца отчетного периода
    V_suzun_km_gtm_ost_product = V_suzun_nm_gtm_ost_product
# Технологические остатки нефти в резервуарах УПН ЦППН №2 на конец месяца отчетного периода
    V_suzun_km_gtm_ost_upn = V_suzun_slu + V_suzun_vslu
# Технологические остатки нефти СПУ на конец месяца отчетного периода
    V_suzun_km_gtm_ost_texn = V_suzun_km_gtm_ost_upn + V_suzun_km_gtm_ost_cps
# Остатки нефти в резервуарах СПУ на конец месяца отчетного периода
    V_suzun_km_gtm_ost_spu = V_suzun_km_gtm_ost_np + V_suzun_km_gtm_ost_app + V_suzun_km_gtm_ost_texn
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_suzun_km_gtm_path = V_suzun_nm_gtm_ost + Q_suzun_gtm_total - V_suzun_gtm_lost - V_suzun_km_gtm_ost_spu - G_suzun_gtm_release - G_suzun_gtm_own - F_suzun_gtm_total + G_suzun_gtm_buy
# Остатки нефти (газового конденсата) на конец месяца отчетного периода, всего
    V_suzun_km_gtm_ost = V_suzun_km_gtm_ost_spu + V_suzun_km_gtm_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delete_V_suzun_gtm_ost = V_suzun_km_gtm_ost - V_suzun_nm_gtm_ost
# Проверка
    V_suzun_gtm_check = (V_suzun_nm_gtm_ost + Q_suzun_gtm_total + G_suzun_gtm_buy) - (V_suzun_gtm_lost + G_suzun_gtm_own + G_suzun_gtm_release + F_suzun_gtm_total + V_suzun_km_gtm_ost)
    V_suzun_gtm_check_out = V_suzun_gtm_check
    if V_suzun_gtm_check != 0:
        V_suzun_gtm_check_out = {
            "value": V_suzun_gtm_check,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
    V_suzun_balance_total = V_tstn_suzun_vankor + V_tstn_suzun + V_tstn_suzun_vslu
    V_suzun_balance_check_out = V_suzun_balance_total
    if abs(V_suzun_balance_total - V_suzun_km_gtm_path) > 20:
        V_suzun_balance_check_out = {
            "value": V_suzun_balance_total,
            "status": 1,
            "message": "Проверка не пройдена. Необходимо уточнить корректность введенных данных",
        }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Восток Ойл» (Бизнес-план):_____________
# Остатки нефти на УПН Лодочное на начало месяца отчетного периода
    V_vo_nm_gtm_ost_upn_lodochny = V_ichem_0
# Остатки нефти в резервуарах ВПУ на начало месяца отчетного периода
    V_vo_nm_gtm_ost_rvs = V_vo_nm_gtm_ost_dead + V_vo_nm_gtm_ost_texn + V_vo_nm_gtm_ost_upn_lodochny + V_vo_nm_gtm_ost_product
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_vo_nm_gtm_path = V_tstn_vo_0
# Остатки нефти (газового конденсата) на ВПУ
    V_vo_nm_gtm_ost_vpu = V_vo_nm_gtm_ost_np + V_vo_nm_gtm_ost_app + V_vo_nm_gtm_ost_rvs
# Остатки нефти (газового конденсата) ООО «Восток Ойл», всего
    V_vo_nm_gtm_ost = V_vo_nm_gtm_ost_vpu + V_vo_nm_gtm_path
# Добыча нефти ООО «Восток Ойл»
    Q_vo_gtm_oil = Q_vo_month
# Добыча нефти (газового конденсата) ООО «Восток Ойл», всего
    Q_vo_gtm_total = Q_vo_gtm_oil + Q_vo_gtm_condensate
# Сдача нефти (газового конденсата) ООО «Восток Ойл», всего
    F_vo_gtm_total = F_vo_delta
# Технологические потери нефти при добыче и подготовке
    V_vo_gtm_lost_oil = round(Q_vo_gtm_oil * (K_vo_mining/100))
# Технологические потери нефти (газового конденсата) при транспортировке
    V_vo_gtm_lost_trans = round(F_vo_gtm_total * (K_vo_trans/100))
# Технологические потери нефти (газового конденсата), всего
    V_vo_gtm_lost = V_vo_gtm_lost_oil + V_vo_gtm_lost_condensate + V_vo_gtm_lost_trans
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_vo_gtm_own = G_vo_gtm_fuel + G_vo_gtm_fill
# Остатки нефти на ВПУ в нефтепроводах на конец месяца отчетного периода
    V_vo_km_gtm_ost_np = V_vo_nm_gtm_ost_np
# Остатки нефти в аппаратах ВПУ на конец месяца отчетного периода
    V_vo_km_gtm_ost_app = V_vo_nm_gtm_ost_app
# Мертвые остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vo_km_gtm_ost_dead = V_vo_nm_gtm_ost_dead
# Технологические остатки нефти на ВПУ на конец месяца отчетного периода
    V_vo_km_gtm_ost_texn = V_vo_nm_gtm_ost_texn
# Товарные остатки нефти на ВПУ на конец месяца отчетного периода
    V_vo_km_gtm_ost_product = V_vo_nm_gtm_ost_product
# Остатки нефти ООО «Восток Ойл» на УПН Лодочное на конец месяца отчетного периода
    V_vo_km_gtm_ost_upn_lodochny = V_ichem
# Остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_vo_km_gtm_ost_rvs = V_vo_km_gtm_ost_dead + V_vo_km_gtm_ost_texn + V_vo_km_gtm_ost_upn_lodochny + V_vo_km_gtm_ost_product
# Остатки нефти на ВПУ на конец месяца отчетного периода
    V_vo_km_gtm_ost_vpu = V_vo_km_gtm_ost_np + V_vo_km_gtm_ost_app + V_vo_km_gtm_ost_rvs
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_vo_km_gtm_path = V_vo_nm_gtm_ost + Q_vo_gtm_total - V_vo_gtm_lost - V_vo_km_gtm_ost_vpu - G_vo_gtm_release - G_vo_gtm_own - F_vo_gtm_total
# Остатки нефти (газового конденсата) на конец месяца отчетного периода, всего
    V_vo_km_gtm_ost = V_vo_km_gtm_ost_vpu + V_vo_nm_gtm_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delte_V_vo_gtm_ost = V_vo_km_gtm_ost - V_vo_nm_gtm_ost
# Выполнение процедуры проверки
    V_vo_gtm_check = (V_vo_nm_gtm_ost + Q_vo_gtm_total) - (V_vo_gtm_lost + G_vo_gtm_own + G_vo_gtm_release + F_vo_gtm_total + V_vo_km_gtm_ost)
    V_vo_gtm_check_out = V_vo_gtm_check
    if V_vo_gtm_check != 0 or abs(V_tstn_vo - V_vo_km_gtm_path) > 40:
        V_vo_gtm_check_out = {
            "value": V_vo_gtm_check,
            "status": 1,
            "message": (
                "Проверка не пройдена. Необходимо уточнить корректность введенных данных "
                f"(значение {V_vo_gtm_check:.2f})"
            ),
        }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Тагульское» Лодочное месторождение (Бизнес-план):_____________
# Остатки нефти на УПН Лодочное на начало месяца отчетного периода
    V_lodochny_nm_gtm_ost_upn_lodochny = V_lodochny_0
# Остатки нефти в резервуарах ЛПУ на начало месяца отчетного периода
    V_lodochny_nm_gtm_ost_rvs = V_lodochny_nm_gtm_ost_upn_lodochny + V_lodochny_nm_gtm_ost_upn_ichem + V_lodochny_nm_gtm_ost_upsv_yu
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_lodochny_nm_gtm_path = V_tstn_lodochny_0
# Остатки нефти (газового конденсата) ООО «Тагульское» Лодочное месторождение, всего
    V_lodochny_nm_gtm_ost = V_lodochny_nm_gtm_ost_np + V_lodochny_nm_gtm_ost_app + V_lodochny_nm_gtm_ost_rvs + V_lodochny_nm_gtm_path
# Добыча нефти ООО «Тагульское» Лодочное месторождение
    Q_lodochny_gtm_oil = Q_lodochny_month
# Добыча нефти (газового конденсата) ООО «Тагульское» Лодочное месторождение, всего
    Q_lodochny_gtm_total = Q_lodochny_gtm_oil + Q_lodochny_gtm_condensate
# Сдача нефти (газового конденсата) ООО «Тагульское» Лодочное месторождение, всего
    F_lodochny_gtm_total = F_tagul_lpy_delta
# Технологические потери нефти при добыче и подготовке
    V_lodochny_gtm_lost_oil = round(Q_lodochny_gtm_oil * (K_lodochny_mining/100))
# Технологические потери нефти (газового конденсата) при транспортировке
    V_lodochny_gtm_lost_trans = round(F_lodochny_gtm_total * (K_lodochny_trans/100))
# Технологические потери нефти (газового конденсата), всего
    V_lodochny_gtm_lost = V_lodochny_gtm_lost_oil + V_lodochny_gtm_lost_trans
# Остатки нефти на ЛПУ в нефтепроводах на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_np = V_lodochny_nm_gtm_ost_np
# Остатки нефти в аппаратах ЛПУ на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_app = V_lodochny_nm_gtm_ost_app
# Мертвые остатки нефти на ЛПУ на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_dead = V_lodochny_nm_gtm_dead
# Технологические остатки нефти Ичемминского м/р на УПН Лодочного на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_upn_ichem = V_lodochny_nm_gtm_ost_upn_ichem
# Технологические остатки нефти на УПСВ-Юг на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_upsv_yu = V_lodochny_nm_gtm_ost_upsv_yu
# Товарные остатки нефти на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_product = V_lodochny_nm_gtm_ost_product
# Остатки нефти в РВС очистных сооружений на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_rvs_clear = V_lodochny_nm_gtm_ost_rvs_clear
# Остатки нефти ООО «Тагульское» на УПН Лодочное на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_upn_lodochny = V_lodochny
# Технологические остатки нефти ООО «Тагульское» (Лодочное месторождение) на конец месяца отчетного периода, всего
    V_lodochny_km_gtm_ost_texn = V_lodochny_km_gtm_ost_upn_lodochny + V_lodochny_km_gtm_ost_upn_ichem + V_lodochny_km_gtm_ost_upsv_yu
# Остатки нефти в резервуарах ЛПУ на конец месяца отчетного периода
    V_lodochny_km_gtm_ost_rvs = V_lodochny_km_gtm_ost_dead + V_lodochny_km_gtm_ost_texn
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_lodochny_km_gtm_path = V_lodochny_nm_gtm_ost + Q_lodochny_gtm_total - V_lodochny_gtm_lost - V_lodochny_km_gtm_ost_np - V_lodochny_km_gtm_ost_app - V_lodochny_km_gtm_ost_rvs - G_lodochny_gtm_release - G_lodochny_gtm_own - F_lodochny_gtm_total
# Остатки нефти (газового конденсата) на конец месяца отчетного периода, всего
    V_lodochny_km_gtm_ost = V_lodochny_km_gtm_ost_np + V_lodochny_km_gtm_ost_app + V_lodochny_km_gtm_ost_rvs + V_lodochny_km_gtm_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delte_V_lodoxhny_gtm_ost = V_lodochny_km_gtm_ost - V_lodochny_nm_gtm_ost
# Выполнение процедуры проверки
    V_lodochny_gtm_check = (V_lodochny_nm_gtm_ost + Q_lodochny_gtm_total) - (V_lodochny_gtm_lost + F_lodochny_gtm_total + V_lodochny_km_gtm_ost)
    V_lodochny_gtm_check_out = V_lodochny_gtm_check
    if V_lodochny_gtm_check != 0 or abs(V_tstn_lodochny - V_lodochny_km_gtm_path) > 5:
        V_lodochny_gtm_check_out = {
            "value": V_lodochny_gtm_check,
            "status": 1,
            "message": (
                "Проверка не пройдена. Необходимо уточнить корректность введенных данных "
                f"(значение {V_lodochny_gtm_check:.2f})"
            ),
        }
# _____________Формирование планового баланса добычи-сдачи нефти по ООО «Тагульское» Тагульское месторождение (ГТМ):_____________
# Остатки нефти в резервуарах ТПУ на начало месяца отчетного периода
    V_tagul_nm_gtm_ost_rvs = V_tagul_nm_gtm_ost_dead + V_tagul_nm_gtm_ost_texn + V_tagul_nm_gtm_ost_rvs_clear + V_tagul_nm_gtm_ost_product
# Остатки нефти (газового конденсата) на ТПУ
    V_tagul_nm_gtm_ost_tpu = V_tagul_nm_gtm_ost_np + V_tagul_nm_gtm_ost_app + V_tagul_nm_gtm_ost_rvs
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор») на начало месяца отчетного периода
    V_tagul_nm_gtm_path = V_tstn_tagul_0
# Остатки нефти (газового конденсата) ООО «Тагульское» Тагульское месторождение, всего
    V_tagul_nm_gtm_ost = V_tagul_nm_gtm_ost_tpu + V_tagul_nm_gtm_ost_dead + V_tagul_nm_gtm_path
# Добыча нефти (ООО «Тагульское» Тагульское месторождения
    Q_tagul_gtm_oil = Q_tagul_month
# Добыча нефти (газового конденсата) ООО «Тагульское» Тагульское месторождения, всего
    Q_tagul_gtm_total = Q_tagul_gtm_oil + Q_tagul_gtm_condensate
# Сдача нефти (газового конденсата) ООО «Тагульское» Тагульское месторождение
    F_tagul_gtm_total = F_tagul_tpy_delta
# Технологические потери нефти при добыче и подготовке
    V_tagul_gtm_lost_oil = round(Q_tagul_gtm_total * (K_tagul_minig/100))
# Технологические потери нефти (газового конденсата) при транспортировке
    V_tagul_gtm_lost_trans = round(F_tagul_gtm_total * (K_tagul/100))
# Технологические потери нефти (газового конденсата), всего
    V_tagul_gtm_lost = V_tagul_gtm_lost_oil + V_tagul_gtm_lost_trans
# Расход нефти (газового конденсата) на собственные производственно-технологические нужды и топливо
    G_tagul_gtm_own = G_tagul_gtm_fuel
# Отпуск нефти (газового конденсата) ООО «Тагульское» Тагульское месторождение, всего
    G_tagul_gtm_release = G_tagul_gtm_release_rn_drilling + G_tagul_gtm_release_russko_rechenskoe
# Технологические остатки нефти в резервуарах ТПУ на конец месяца
    V_tagul_km_gtm_ost_texn = V_tagul_nm_gtm_ost_texn
# Мертвые остатки нефти в резервуарах ТПУ на конец месяца отчетного периода
    V_tagul_km_gtm_ost_dead = V_tagul_nm_gtm_ost_dead
# Технологические остатки нефти в резервуарах ТПУ на конец месяца отчетного периода_____________________________________________________
    V_tagul_km_gtm_ost_texn = V_tagul_nm_gtm_ost_texn
# Остатки нефти в РВС очистных сооружений на конец месяца отчетного периода
    V_tagul_km_gtm_ost_rvs_clear = V_tagul_nm_gtm_ost_rvs_clear
# Товарные остатки нефти на конец месяца отчетного периода
    V_tagul_km_gtm_ost_product = V_tagul_nm_gtm_ost_product
# Остатки нефти в резервуарах ВПУ на конец месяца отчетного периода
    V_tagul_km_gtm_ost_rvs = V_tagul_km_gtm_ost_dead + V_tagul_km_gtm_ost_texn + V_tagul_km_gtm_ost_rvs_clear + V_tagul_km_gtm_ost_product
# Остатки нефти на ТПУ на конец месяца, всего
    V_tagul_km_gtm_ost_tpu = V_tagul_km_gtm_ost_np + V_tagul_km_gtm_ost_app + V_tagul_km_gtm_ost_rvs
# Нефть в пути к пунктам сдачи (ООО «РН-Ванкор»)
    V_tagul_km_gtm_path = V_tagul_nm_gtm_ost + Q_tagul_gtm_total - V_tagul_gtm_lost - V_tagul_km_gtm_ost_tpu - G_tagul_gtm_release - G_tagul_gtm_own - F_tagul_gtm_total
# Остатки нефти (газового конденсата) на конец месяца, всего
    V_tagul_km_gtm_ost = V_tagul_km_gtm_ost_tpu + V_tagul_km_gtm_path
# Изменение остатков нефти (газового конденсата) собственных, всего
    delte_V_tagul_gtm_ost = V_tagul_km_gtm_ost - V_tagul_nm_gtm_ost
# Выполнение процедуры проверки
    V_tagul_gtm_check = (V_tagul_nm_gtm_ost + Q_tagul_gtm_total) - (V_tagul_gtm_lost + G_tagul_gtm_own + G_tagul_gtm_release + F_tagul_gtm_total + V_tagul_km_gtm_ost)
    V_tagul_gtm_check_out = V_tagul_gtm_check
    if V_tagul_gtm_check != 0 or abs(V_tstn_tagul - V_tagul_km_gtm_path) > 5:
        V_tagul_gtm_check_out = {
            "value": V_tagul_gtm_check,
            "status": 1,
            "message": (
                "Проверка не пройдена. Необходимо уточнить корректность введенных данных "
                f"(значение {V_tagul_gtm_check:.2f})"
            ),
        }

    return {
        "V_vn_nm_gtm_ost_texn": V_vn_nm_gtm_ost_texn,
        "V_vn_nm_gtm_ost_rvs": V_vn_nm_gtm_ost_rvs,
        "V_vn_nm_gtm_path": V_vn_nm_gtm_path,
        "V_vn_nm_gtm_ost_vpy": V_vn_nm_gtm_ost_vpy,
        "V_vn_nm_gtm_ost": V_vn_nm_gtm_ost,
        "Q_vn_gtm_total": Q_vn_gtm_total,
        "Q_vn_gtm_oil": Q_vn_gtm_oil,
        "F_vn_gtm_total": F_vn_gtm_total,
        "V_vn_gtm_lost_oil": V_vn_gtm_lost_oil,
        "V_vn_gtm_lost_path": V_vn_gtm_lost_path,
        "V_vn_gtm_lost": V_vn_gtm_lost,
        "G_vn_gtm_own": G_vn_gtm_own,
        "G_vn_gtm_release_suzun": G_vn_gtm_release_suzun,
        "G_vn_gtm_release": G_vn_gtm_release,
        "V_vn_km_gtm_ost_np": V_vn_km_gtm_ost_np,
        "V_vn_km_gtm_ost_texn": V_vn_km_gtm_ost_texn,
        "V_vn_km_gtm_ost_dead": V_vn_km_gtm_ost_dead,
        "V_vn_km_gtm_ost_rvs_clear": V_vn_km_gtm_ost_rvs_clear,
        "V_vn_km_gtm_ost_product": V_vn_km_gtm_ost_product,
        "V_vn_km_gtm_ost_vpu": V_vn_km_gtm_ost_vpu,
        "V_vn_km_gtm_path": V_vn_km_gtm_path,
        "V_vn_km_gtm_ost": V_vn_km_gtm_ost,
        "delte_V_vn_gtm_ost": delte_V_vn_gtm_ost,
        "V_vn_gtm_check": V_vn_gtm_check_out,
        "V_vn_balance_check": V_vn_balance_check_out,
        "V_suzun_nm_gtm_ost_upn": V_suzun_nm_gtm_ost_upn,
        "V_suzun_nm_ost_rvs": V_suzun_nm_ost_rvs,
        "V_suzun_gtm_ost_rvs": V_suzun_gtm_ost_rvs,
        "V_suzun_nm_gtm_ost_spu": V_suzun_nm_gtm_ost_spu,
        "V_suzun_nm_gtm_path": V_suzun_nm_gtm_path,
        "V_suzun_nm_gtm_ost": V_suzun_nm_gtm_ost,
        "Q_suzun_gtm_oil_slu": Q_suzun_gtm_oil_slu,
        "Q_suzun_gtm_oil_vslu": Q_suzun_gtm_oil_vslu,
        "Q_suzun_gtm_total": Q_suzun_gtm_total,
        "V_suzun_gtm_lost_oil": V_suzun_gtm_lost_oil,
        "G_suzun_gtm_mupn": G_suzun_gtm_mupn,
        "G_suzun_gtm_own": G_suzun_gtm_own,
        "G_suzun_gtm_buy": G_suzun_gtm_buy,
        "F_suzun_gtm_slu": F_suzun_gtm_slu,
        "F_suzun_gtm_vslu": F_suzun_gtm_vslu,
        "F_suzun_gtm_vankor": F_suzun_gtm_vankor,
        "F_suzun_gtm_total": F_suzun_gtm_total,
        "V_suzun_gtm_lost_slu": V_suzun_gtm_lost_slu,
        "V_suzun_gtm_lost_vslu": V_suzun_gtm_lost_vslu,
        "V_suzun_gtm_lost_vankor": V_suzun_gtm_lost_vankor,
        "V_suzun_gtm_lost": V_suzun_gtm_lost,
        "V_suzun_km_gtm_ost_np": V_suzun_km_gtm_ost_np,
        "V_suzun_km_gtm_ost_app": V_suzun_km_gtm_ost_app,
        "V_suzun_gtm_ost_dead": V_suzun_gtm_ost_dead,
        "V_suzun_km_gtm_ost_product": V_suzun_km_gtm_ost_product,
        "V_suzun_km_gtm_ost_upn": V_suzun_km_gtm_ost_upn,
        "V_suzun_km_gtm_ost_texn": V_suzun_km_gtm_ost_texn,
        "V_suzun_km_gtm_ost_spu": V_suzun_km_gtm_ost_spu,
        "V_suzun_km_gtm_path": V_suzun_km_gtm_path,
        "V_suzun_km_gtm_ost": V_suzun_km_gtm_ost,
        "delete_V_suzun_gtm_ost": delete_V_suzun_gtm_ost,
        "V_suzun_gtm_check": V_suzun_gtm_check_out,
        "V_suzun_balance_check": V_suzun_balance_check_out,
        "V_suzun_balance_total": V_suzun_balance_total,
        "V_vo_nm_gtm_ost_upn_lodochny": V_vo_nm_gtm_ost_upn_lodochny,
        "V_vo_nm_gtm_ost_rvs": V_vo_nm_gtm_ost_rvs,
        "V_vo_nm_gtm_path": V_vo_nm_gtm_path,
        "V_vo_nm_gtm_ost_vpu": V_vo_nm_gtm_ost_vpu,
        "V_vo_nm_gtm_ost": V_vo_nm_gtm_ost,
        "Q_vo_gtm_oil": Q_vo_gtm_oil,
        "Q_vo_gtm_total": Q_vo_gtm_total,
        "F_vo_gtm_total": F_vo_gtm_total,
        "V_vo_gtm_lost_oil": V_vo_gtm_lost_oil,
        "V_vo_gtm_lost_trans": V_vo_gtm_lost_trans,
        "V_vo_gtm_lost": V_vo_gtm_lost,
        "G_vo_gtm_own": G_vo_gtm_own,
        "V_vo_km_gtm_ost_np": V_vo_km_gtm_ost_np,
        "V_vo_km_gtm_ost_app": V_vo_km_gtm_ost_app,
        "V_vo_km_gtm_ost_dead": V_vo_km_gtm_ost_dead,
        "V_vo_km_gtm_ost_texn": V_vo_km_gtm_ost_texn,
        "V_vo_km_gtm_ost_product": V_vo_km_gtm_ost_product,
        "V_vo_km_gtm_ost_upn_lodochny": V_vo_km_gtm_ost_upn_lodochny,
        "V_vo_km_gtm_ost_rvs": V_vo_km_gtm_ost_rvs,
        "V_vo_km_gtm_ost_vpu": V_vo_km_gtm_ost_vpu,
        "V_vo_km_gtm_path": V_vo_km_gtm_path,
        "V_vo_km_gtm_ost": V_vo_km_gtm_ost,
        "delte_V_vo_gtm_ost": delte_V_vo_gtm_ost,
        "V_vo_gtm_check": V_vo_gtm_check,
        "V_vo_gtm_check_out": V_vo_gtm_check_out,
        "V_lodochny_nm_gtm_ost_upn_lodochny": V_lodochny_nm_gtm_ost_upn_lodochny,
        "V_lodochny_nm_gtm_ost_rvs": V_lodochny_nm_gtm_ost_rvs,
        "V_lodochny_nm_gtm_path": V_lodochny_nm_gtm_path,
        "V_lodochny_nm_gtm_ost": V_lodochny_nm_gtm_ost,
        "Q_lodochny_gtm_oil": Q_lodochny_gtm_oil,
        "Q_lodochny_gtm_total": Q_lodochny_gtm_total,
        "F_lodochny_gtm_total": F_lodochny_gtm_total,
        "V_lodochny_gtm_lost_oil": V_lodochny_gtm_lost_oil,
        "V_lodochny_gtm_lost_trans": V_lodochny_gtm_lost_trans,
        "V_lodochny_gtm_lost": V_lodochny_gtm_lost,
        "V_lodochny_km_gtm_ost_np": V_lodochny_km_gtm_ost_np,
        "V_lodochny_km_gtm_ost_app": V_lodochny_km_gtm_ost_app,
        "V_lodochny_km_gtm_ost_dead": V_lodochny_km_gtm_ost_dead,
        "V_lodochny_km_gtm_ost_upn_ichem": V_lodochny_km_gtm_ost_upn_ichem,
        "V_lodochny_km_gtm_ost_upsv_yu": V_lodochny_km_gtm_ost_upsv_yu,
        "V_lodochny_km_gtm_ost_product": V_lodochny_km_gtm_ost_product,
        "V_lodochny_km_gtm_ost_rvs_clear": V_lodochny_km_gtm_ost_rvs_clear,
        "V_lodochny_km_gtm_ost_upn_lodochny": V_lodochny_km_gtm_ost_upn_lodochny,
        "V_lodochny_km_gtm_ost_texn": V_lodochny_km_gtm_ost_texn,
        "V_lodochny_km_gtm_ost_rvs": V_lodochny_km_gtm_ost_rvs,
        "V_lodochny_km_gtm_path": V_lodochny_km_gtm_path,
        "V_lodochny_km_gtm_ost": V_lodochny_km_gtm_ost,
        "delte_V_lodoxhny_gtm_ost": delte_V_lodoxhny_gtm_ost,
        "V_lodochny_gtm_check": V_lodochny_gtm_check,
        "V_lodochny_gtm_check_out": V_lodochny_gtm_check_out,
        "V_tagul_nm_gtm_ost_rvs": V_tagul_nm_gtm_ost_rvs,
        "V_tagul_nm_gtm_ost_tpu": V_tagul_nm_gtm_ost_tpu,
        "V_tagul_nm_gtm_path": V_tagul_nm_gtm_path,
        "V_tagul_nm_gtm_ost": V_tagul_nm_gtm_ost,
        "Q_tagul_gtm_oil": Q_tagul_gtm_oil,
        "Q_tagul_gtm_total": Q_tagul_gtm_total,
        "F_tagul_gtm_total": F_tagul_gtm_total,
        "V_tagul_gtm_lost_oil": V_tagul_gtm_lost_oil,
        "V_tagul_gtm_lost_trans": V_tagul_gtm_lost_trans,
        "V_tagul_gtm_lost": V_tagul_gtm_lost,
        "G_tagul_gtm_own": G_tagul_gtm_own,
        "G_tagul_gtm_release": G_tagul_gtm_release,
        "V_tagul_km_gtm_ost_texn": V_tagul_km_gtm_ost_texn,
        "V_tagul_km_gtm_ost_dead": V_tagul_km_gtm_ost_dead,
        "V_tagul_km_gtm_ost_rvs_clear": V_tagul_km_gtm_ost_rvs_clear,
        "V_tagul_km_gtm_ost_product": V_tagul_km_gtm_ost_product,
        "V_tagul_km_gtm_ost_rvs": V_tagul_km_gtm_ost_rvs,
        "V_tagul_km_gtm_ost_tpu": V_tagul_km_gtm_ost_tpu,
        "V_tagul_km_gtm_path": V_tagul_km_gtm_path,
        "V_tagul_km_gtm_ost": V_tagul_km_gtm_ost,
        "delte_V_tagul_gtm_ost": delte_V_tagul_gtm_ost,
        "V_tagul_gtm_check": V_tagul_gtm_check,
        "V_tagul_gtm_check_out": V_tagul_gtm_check_out,
    }
