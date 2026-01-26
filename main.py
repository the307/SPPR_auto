import os
import runpy
from pathlib import Path

import pandas as pd
import warnings
import calculate
from loader import build_all_data, get_day
from data_prep import (
    prepare_suzun_data,
    prepare_vo_data,
    prepare_kchng_data,
    prepare_lodochny_data,
    prepare_cppn1_data,
    prepare_rn_vankor_data,
    prepare_sikn_1208_data,
    prepare_tstn_data,
    prepare_tstn_precalc_data,
    prepare_auto_balance_volumes_data,
    rn_vankor_check_data,
    rn_vankor_auto_balance_data,
    plan_sdacha_data,
    balance_po_business_plan_data,
    plan_balance_gtm_data,
)   
from inputs import (
    get_suzun_inputs,
    get_lodochny_inputs,
    get_cppn_1_inputs,
    get_rn_vankor_inputs,
    get_sikn_1208_inputs,
    get_TSTN_inputs,
    get_plan_balance_gtm_inputs,
    get_balance_po_business_inputs,

)
from export import export_to_json
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


def main():
    error_info = None

    try:
        # ------------------------------------------------------------------
        # 1. Исходные данные
        # ------------------------------------------------------------------
        master_df = build_all_data()

        if "date" not in master_df.columns:
            raise ValueError("master_df не содержит колонку 'date'")

        master_df["date"] = pd.to_datetime(master_df["date"]).dt.normalize()

        # Всегда работаем с текущим месяцем
        dates = [pd.Timestamp(d).normalize() for d in get_day()]

        # ------------------------------------------------------------------
        # 2. Ручные вводы (ОДИН РАЗ)
        # ------------------------------------------------------------------
        suzun_inputs = get_suzun_inputs()
        lodochny_inputs = get_lodochny_inputs()
        cppn_1_inputs = get_cppn_1_inputs()
        rn_vankor_inputs = get_rn_vankor_inputs()
        sikn_1208_inputs = get_sikn_1208_inputs()
        TSTN_inputs = get_TSTN_inputs()
        plan_balance_gtm_inputs = get_plan_balance_gtm_inputs()
        balance_po_business_inputs = get_balance_po_business_inputs()
        # ------------------------------------------------------------------
        # 3. Аккумулятор результатов
        # ------------------------------------------------------------------
        alarm_flag = False
        alarm_msg = None

        # ------------------------------------------------------------------
        # 4. Основной цикл по дням
        # ------------------------------------------------------------------
        last_context = {}
        print(master_df)
        for n in dates:
            m = n.month
            prev_day = n - timedelta(days=1)
            prev_month = n.replace(day=1) - timedelta(days=1)
            N = calendar.monthrange(n.year, n.month)[1]

            # Словарь результатов за день
            day_result = {"date": n}

            # -------------------- СУЗУН -----------------------------------
            suzun_data = prepare_suzun_data(master_df, n, m, prev_day, prev_month, N)
            suzun_results = calculate.suzun(**suzun_data, **suzun_inputs)
            day_result.update(suzun_results)

            # -------------------- ВОСТОК ОЙЛ -------------------------------
            vo_data = prepare_vo_data(master_df, n, prev_day)
            vo_results = calculate.VO(**vo_data)
            day_result.update(vo_results)

            # -------------------- КЧНГ -------------------------------------
            kchng_data = prepare_kchng_data(master_df, n, m, prev_day)
            kchng_results = calculate.kchng(**kchng_data)
            day_result.update(kchng_results)

            # -------------------- ЛОДОЧНЫЙ ---------------------------------
            lodochny_data = prepare_lodochny_data(master_df, n, m, prev_day, prev_month, N, n.day, kchng_results)
            g_ichem = lodochny_inputs["G_ichem"]
            if isinstance(g_ichem, (list, tuple)):
                idx = n.day - 1
                g_ichem = g_ichem[idx] if idx < len(g_ichem) else g_ichem[-1]
            lodochny_results = calculate.lodochny(**lodochny_data, **{**lodochny_inputs, "G_ichem": g_ichem})
            day_result.update(lodochny_results)

            # -------------------- ЦППН-1 -----------------------------------
            cppn1_data = prepare_cppn1_data(master_df, n, prev_day, lodochny_results)
            cppn1_results = calculate.CPPN_1(**cppn1_data, **cppn_1_inputs)
            day_result.update(cppn1_results)

            # -------------------- РН-ВАНКОР --------------------------------
            rn_data = prepare_rn_vankor_data(master_df, n, prev_day, N, n.day, m, suzun_results)
            rn_results = calculate.rn_vankor(**rn_data, **rn_vankor_inputs)

            day_result.update(rn_results)

            # -------------------- СИКН-1208 --------------------------------
            g_skn = sikn_1208_inputs["G_skn"]
            if isinstance(g_skn, (list, tuple)):
                idx = n.day - 1
                g_skn = g_skn[idx] if idx < len(g_skn) else g_skn[-1]
            sikn_1208_inputs_day = {**sikn_1208_inputs, "G_skn": g_skn}
            tstn_inputs_day = {**TSTN_inputs, "G_skn": g_skn}

            G_suzun_tng = suzun_inputs["G_suzun_tng"]
            sikn_1208_data = prepare_sikn_1208_data(
                master_df,
                n,
                prev_day,
                suzun_results,
                lodochny_results,
                G_suzun_tng,
                cppn1_results,
            )
            sikn_1208_results = calculate.sikn_1208(**sikn_1208_data, **sikn_1208_inputs_day)
            day_result.update(sikn_1208_results)
            # --------------------Предрасчет параметров-------------------------------------
            G_ichem = g_ichem
            G_suzun_tng = suzun_inputs["G_suzun_tng"]
            tstn_precalc_data = prepare_tstn_precalc_data(
                master_df,
                prev_day,
                N,
                sikn_1208_results,
                lodochny_results,
                suzun_results,
                rn_results,
                tstn_inputs_day,
            )
            tstn_precalc_results = calculate.tstn_precalc(**tstn_precalc_data)
            # -------------------- Блок «Сдача ООО «РН-Ванкор» (автобаланс)-------------------------------------
            auto_balance_volumes_data = prepare_auto_balance_volumes_data(
                master_df,
                prev_day,
                N,
                suzun_results,
            )
            auto_balance_volumes_results = calculate.auto_balance_volumes(**auto_balance_volumes_data)
            day_result.update(auto_balance_volumes_results)
            updated_upn_suzun = auto_balance_volumes_results.get("V_upn_suzun")
            updated_upn_lodochny = auto_balance_volumes_results.get("V_upn_lodochny")
            updated_upn_yu = auto_balance_volumes_results.get("V_upsv_yu")
            updated_upn_s = auto_balance_volumes_results.get("V_upsv_s")
            updated_upn_cps = auto_balance_volumes_results.get("V_cps")
            if updated_upn_suzun is not None and updated_upn_suzun != suzun_results.get("V_upn_suzun"):
                suzun_inputs_adjusted = {**suzun_inputs, "V_upn_suzun_auto": updated_upn_suzun}
                suzun_results = calculate.suzun(**suzun_data, **suzun_inputs_adjusted)
                day_result.update(suzun_results)
            if updated_upn_lodochny is not None and updated_upn_lodochny != lodochny_results.get("V_upn_lodochny"):
                lodochny_inputs_adjusted = {
                    **lodochny_inputs,
                    "G_ichem": g_ichem,
                    "V_upn_lodochny_auto": updated_upn_lodochny,
                }
                lodochny_results = calculate.lodochny(**lodochny_data, **lodochny_inputs_adjusted)
                day_result.update(lodochny_results)
            if (
                (updated_upn_yu is not None and updated_upn_yu != cppn1_results.get("V_upsv_yu"))
                or (updated_upn_s is not None and updated_upn_s != cppn1_results.get("V_upsv_s"))
                or (updated_upn_cps is not None and updated_upn_cps != cppn1_results.get("V_cps"))
            ):
                cppn1_inputs_adjusted = {
                    **cppn_1_inputs,
                    "V_upsv_yu_auto": updated_upn_yu,
                    "V_upsv_s_auto": updated_upn_s,
                    "V_cps_auto": updated_upn_cps,
                }
                cppn1_results = calculate.CPPN_1(**cppn1_data, **cppn1_inputs_adjusted)
                day_result.update(cppn1_results)
            # -------------------- Блок «Сдача ООО «РН-Ванкор» (автобаланс)-------------------------------------
            auto_balance_data = rn_vankor_auto_balance_data(master_df, n, prev_day, N, rn_results, suzun_results, tstn_inputs_day, tstn_precalc_results, lodochny_results, kchng_results, G_ichem, G_suzun_tng)
            auto_balance_results = calculate.rn_vankor_balance(**auto_balance_data)
            day_result.update(auto_balance_results)
            # -------------------- ТСТН -------------------------------------
            G_ichem = g_ichem
            tstn_data = prepare_tstn_data(master_df, N, prev_day, sikn_1208_results, lodochny_results, kchng_results, suzun_results, G_ichem, G_suzun_tng, auto_balance_results, tstn_precalc_results)
            tstn_results = calculate.TSTN(**tstn_data, **tstn_inputs_day)
            day_result.update(tstn_results)

            # -------------------- Блок «Сдача ООО «РН-Ванкор» (проверка) -------------------------------------
            # check_data = rn_vankor_check_data(master_df, n, prev_day, tstn_results, lodochny_results, suzun_results, cppn1_results, auto_balance_results)
            # check_data_results = calculate.rn_vankor_check(**check_data)
            # day_result.update(check_data_results)

            # # Сохраняем контекст последнего дня для расчётов после цикла
            # last_context = {
            #     "n": n,
            #     "m": m,
            #     "prev_day": prev_day,
            #     "prev_month": prev_month,
            #     "cppn1_results": cppn1_results,
            #     "tstn_results": tstn_results,
            #     "suzun_results": suzun_results,
            #     "lodochny_results": lodochny_results,
            # }

            # -------------------- СОХРАНЕНИЕ ДНЯ ---------------------------
            # обновляем master_df
            day_mask = master_df["date"] == n
            if day_mask.any():
                for key, value in day_result.items():
                    if key == "date":
                        continue
                    if isinstance(value, dict):
                        if key in master_df.columns and master_df[key].dtype != "object":
                            master_df[key] = master_df[key].astype("object")
                    master_df.loc[day_mask, key] = value
            else:
                master_df = pd.concat([master_df, pd.DataFrame([day_result])], ignore_index=True)

        master_df.sort_values("date", inplace=True)
        master_df.reset_index(drop=True, inplace=True)

        # -------------------- Сравнение плановой сдачи нефти с бизнес планом (после расчёта всех дней) --------------------
        # if last_context:
        #     last_n = last_context["n"]
        #     last_prev_day = last_context["prev_day"]
        #     last_prev_month = last_context["prev_month"]

        #     plan_sdacha_inputs = plan_sdacha_data(master_df, last_n)
        #     plan_sdacha_result = calculate.plan_sdacha(**plan_sdacha_inputs)

        #     business_plan_data = balance_po_business_plan_data(master_df, last_n)
        #     business_plan_result = calculate.balance_po_business_plan(**business_plan_data,**balance_po_business_inputs)

        #     K_vankor = TSTN_inputs["K_vankor"]
        #     K_suzun = TSTN_inputs["K_suzun"]
        #     K_tagul = TSTN_inputs["K_tagul"]
        #     plan_gtm_data = plan_balance_gtm_data(
        #         master_df,
        #         last_n,
        #         last_context["cppn1_results"],
        #         last_context["tstn_results"],
        #         last_context["suzun_results"],
        #         last_context["lodochny_results"],
        #         K_vankor,
        #         K_suzun,
        #         K_tagul,
        #     )
        #     plan_gtm_result = calculate.plan_balance_gtm(**plan_gtm_data, **plan_balance_gtm_inputs)

        #     last_mask = master_df["date"] == last_n
        #     if last_mask.any():
        #         for key, value in {
        #             **plan_sdacha_result,
        #             **business_plan_result,
        #             **plan_gtm_result,
        #         }.items():
        #             master_df.loc[last_mask, key] = value

    except calculate.CalculationValidationError as exc:
        error_info = {
            "code": "K_OTKACHKI_MISMATCH",
            "message": str(exc),
        }
    except Exception as exc:
        import traceback
        error_info = {
            "code": "UNEXPECTED_CALCULATION_ERROR",
            "message": f"{exc}\n{traceback.format_exc()}",
        }

    if handle_error(error_info, output_path="output.json"):
        return

    # ------------------------------------------------------------------
    # 6. Экспорт в JSON
    # ------------------------------------------------------------------
    export_to_json(
        master_df=master_df,
        output_path="output.json",
        calc_date=dates[-1],
        alarm_flag=alarm_flag,
        alarm_msg=alarm_msg,
    )

    # ------------------------------------------------------------------
    # 7. Экспорт баланса в Excel из JSON
    # ------------------------------------------------------------------
    try:
        script_path = Path(__file__).with_name("json_to_excel_balance.py")
        if script_path.exists():
            current_dir = Path.cwd()
            try:
                os.chdir(script_path.parent)
                runpy.run_path(str(script_path), run_name="__main__")
            finally:
                os.chdir(current_dir)
        else:
            print("Файл json_to_excel_balance.py не найден — экспорт в Excel пропущен")
    except SystemExit as exc:
        print(f"Экспорт в Excel прерван: {exc}")
    except Exception as exc:
        print(f"Ошибка экспорта в Excel: {exc}")

if __name__ == "__main__":
    main()