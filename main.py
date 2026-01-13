import pandas as pd
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
    prepare_TSTN_data
)
from inputs import (
    get_suzun_inputs,
    get_lodochny_inputs,
    get_cppn_1_inputs,
    get_rn_vankor_inputs,
    get_sikn_1208_inputs,
    get_TSTN_inputs
)
from export import export_to_json
from datetime import timedelta
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

        dates = get_day()
        # get_day() возвращает datetime объекты, конвертируем в pandas Timestamp и нормализуем
        dates = [pd.Timestamp(d).normalize() for d in dates]

        # ------------------------------------------------------------------
        # 2. Ручные вводы (ОДИН РАЗ)
        # ------------------------------------------------------------------
        suzun_inputs = get_suzun_inputs()
        lodochny_inputs = get_lodochny_inputs()
        cppn_1_inputs = get_cppn_1_inputs()
        rn_vankor_inputs = get_rn_vankor_inputs()
        sikn_1208_inputs = get_sikn_1208_inputs()
        TSTN_inputs = get_TSTN_inputs()

        # ------------------------------------------------------------------
        # 3. Аккумулятор результатов
        # ------------------------------------------------------------------
        result_rows = []
        alarm_flag = False
        alarm_msg = None

        # ------------------------------------------------------------------
        # 4. Основной цикл по дням
        # ------------------------------------------------------------------
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
            vo_data = prepare_vo_data(master_df, n)
            vo_results = calculate.VO(**vo_data)
            day_result.update(vo_results)

            # -------------------- КЧНГ -------------------------------------
            kchng_data = prepare_kchng_data(master_df, n, m)
            kchng_results = calculate.kchng(**kchng_data)
            day_result.update(kchng_results)

            # -------------------- ЛОДОЧНЫЙ ---------------------------------
            lodochny_data = prepare_lodochny_data(master_df, n, m, prev_day, prev_month, N, n.day, kchng_results)
            lodochny_results = calculate.lodochny(**lodochny_data, **lodochny_inputs)
            day_result.update(lodochny_results)

            # -------------------- ЦППН-1 -----------------------------------
            cppn1_data = prepare_cppn1_data(master_df, n, prev_day, prev_month, lodochny_results)
            cppn1_results = calculate.CPPN_1(**cppn1_data, **cppn_1_inputs)
            day_result.update(cppn1_results)

            # -------------------- РН-ВАНКОР --------------------------------
            rn_data = prepare_rn_vankor_data(master_df, n, prev_day, N, n.day, m, lodochny_results)
            rn_results = calculate.rn_vankor(**rn_data, **rn_vankor_inputs)

            alarm_flag = rn_results.pop("__alarm_first_10_days", alarm_flag)
            alarm_msg = rn_results.pop("__alarm_first_10_days_msg", alarm_msg)
            day_result.update(rn_results)

            # -------------------- СИКН-1208 --------------------------------
            G_suzun_tng = suzun_inputs["G_suzun_tng"]
            sikn_1208_data = prepare_sikn_1208_data(master_df, n, m, prev_month, suzun_results, lodochny_results, G_suzun_tng, cppn1_results)
            sikn_1208_results = calculate.sikn_1208(**sikn_1208_data, **sikn_1208_inputs)
            day_result.update(sikn_1208_results)
            # -------------------- ТСТН -------------------------------------
            G_ichem = lodochny_inputs["G_ichem"]

            TSTN_data = prepare_TSTN_data(master_df, n, prev_day, prev_month, m, N, sikn_1208_results, lodochny_results, kchng_results, suzun_results, G_ichem, G_suzun_tng,)
            TSTN_results = calculate.TSTN(**TSTN_data, **TSTN_inputs)
            day_result.update(TSTN_results)
            # -------------------- СОХРАНЕНИЕ ДНЯ ---------------------------
            result_rows.append(day_result)

        # ------------------------------------------------------------------
        # 5. Итоговый DataFrame
        # ------------------------------------------------------------------
        result_df = pd.DataFrame(result_rows)
        result_df.sort_values("date", inplace=True)
        result_df.reset_index(drop=True, inplace=True)
    except calculate.CalculationValidationError as exc:
        error_info = {
            "code": "K_OTKACHKI_MISMATCH",
            "message": str(exc),
        }
    except Exception as exc:
        error_info = {
            "code": "UNEXPECTED_CALCULATION_ERROR",
            "message": str(exc),
        }

    if error_info:
        export_to_json(
            master_df=None,
            output_path="output.json",
            calc_date=None,
            alarm_flag=False,
            alarm_msg=None,
            error=error_info,
        )
        return

    # ------------------------------------------------------------------
    # 6. Экспорт в JSON
    # ------------------------------------------------------------------
    export_to_json(
        master_df=result_df,
        output_path="output.json",
        calc_date=dates[-1],
        alarm_flag=alarm_flag,
        alarm_msg=alarm_msg,
    )

if __name__ == "__main__":
    main()