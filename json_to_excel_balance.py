#Функция превода данных из JSON в таблцу Excel

import json
from datetime import datetime
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Чтение json
json_path = Path("output.json")
with json_path.open("r", encoding="utf-8") as f:
    dist_json = json.load(f)

error = dist_json.get("error")
if error:
    raise SystemExit(f'Ошибка расчета: {error.get("message")}')

days = dist_json.get("days") or []
calc_date = None
if days:
    last_day = days[-1].get("date")
    if last_day:
        try:
            calc_date = datetime.strptime(last_day, "%Y-%m-%d")
        except ValueError:
            calc_date = None
if calc_date is None:
    calc_date = datetime.today()
date_str = calc_date.strftime("%d.%m.%Y")


# Чтение excel шаблона
excel_file = load_workbook('balance_sample.xlsx')
excel_sheet = excel_file.active


# Создаем стили заливки
# Вычисляемые значения
pale_green_fill = PatternFill(start_color='DAEEAD', end_color='DAEEAD', fill_type='solid')
# Вводимые значения
pale_blue_fill = PatternFill(start_color='BDE8F5', end_color='BDE8F5', fill_type='solid')
# Проверка не пройдена
red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
# Проверка пройдена
green_fill = PatternFill(start_color='00FF00', end_color='00FF00', fill_type='solid')


# Записываем в Excel значения на начало месяца
row = 4

# excel_sheet['A'+ str(row)] = '0'
# excel_sheet['A'+ str(row)].fill = pale_blue_fill

# excel_sheet['F'+ str(row)] = dist_json["V_upsv_yu_0"]
# excel_sheet['F'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['G'+ str(row)] = dist_json["V_upsv_s_0"]
# excel_sheet['G'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['H'+ str(row)] = dist_json["V_cps_0"]
# excel_sheet['H'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['I'+ str(row)] = dist_json["V_cppn_1_0"]
# excel_sheet['I'+ str(row)].fill = pale_green_fill
#
# excel_sheet['J'+ str(row)] = dist_json["V_lodochny_cps_upsv_0"]
# excel_sheet['J'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['V'+ str(row)] = dist_json["V_upn_suzun_0"]
# excel_sheet['V'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['W'+ str(row)] = dist_json["V_suzun_slu_0"]
# excel_sheet['W'+ str(row)].fill = pale_green_fill
#
# excel_sheet['X'+ str(row)] = dist_json["V_suzun_vslu_0"]
# excel_sheet['X'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['Y'+ str(row)] = dist_json["V_suzun_tng_0"]
# excel_sheet['Y'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['AL'+ str(row)] = dist_json.get("V_tagul_tp_0")
# excel_sheet['AL'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['AR'+ str(row)] = dist_json["V_upn_lodochny_0"]
# excel_sheet['AR'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['AS'+ str(row)] = dist_json["V_lodochny_0"]
# excel_sheet['AS'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['AT'+ str(row)] = dist_json["V_ichem_0"]
# excel_sheet['AT'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BF'+ str(row)] = dist_json.get("V_gnps_0")
# excel_sheet['BF'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BG'+ str(row)] = dist_json["V_nps_1_0"]
# excel_sheet['BG'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BH'+ str(row)] = dist_json["V_nps_2_0"]
# excel_sheet['BH'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BI'+ str(row)] = dist_json.get("V_knps_0")
# excel_sheet['BI'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BJ'+ str(row)] = dist_json["V_tstn_0"]
# excel_sheet['BJ'+ str(row)].fill = pale_green_fill
#
# excel_sheet['BK'+ str(row)] = dist_json["V_tstn_rn_vn_0"]
# excel_sheet['BK'+ str(row)].number_format = "0.000"
# excel_sheet['BK'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BL'+ str(row)] = dist_json["V_tstn_vn_0"]
# excel_sheet['BL'+ str(row)].fill = pale_green_fill
#
# excel_sheet['BM'+ str(row)] = dist_json["V_tstn_suzun_0"]
# excel_sheet['BM'+ str(row)].number_format = "0.000"
# excel_sheet['BM'+ str(row)].fill = pale_green_fill
#
# excel_sheet['BN'+ str(row)] = dist_json["V_tstn_suzun_vankor_0"]
# excel_sheet['BN'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BO'+ str(row)] = dist_json["V_tstn_suzun_vslu_0"]
# excel_sheet['BO'+ str(row)].number_format = "0.000"
# excel_sheet['BO'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BP'+ str(row)] = dist_json.get("V_tstn_tagul_obch_0")
# excel_sheet['BP'+ str(row)].number_format = "0.000"
# excel_sheet['BP'+ str(row)].fill = pale_green_fill
#
# excel_sheet['BQ'+ str(row)] = dist_json["V_tstn_lodochny_0"]
# excel_sheet['BQ'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BR'+ str(row)] = dist_json["V_tstn_tagul_0"]
# excel_sheet['BR'+ str(row)].number_format = "0.000"
# excel_sheet['BR'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BS'+ str(row)] = dist_json["V_tstn_skn_0"]
# excel_sheet['BS'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BT'+ str(row)] = dist_json["V_tstn_vo_0"]
# excel_sheet['BT'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BU'+ str(row)] = dist_json["V_tstn_tng_0"]
# excel_sheet['BU'+ str(row)].fill = pale_blue_fill
#
# excel_sheet['BV'+ str(row)] = dist_json["V_tstn_kchng_0"]
# excel_sheet['BV'+ str(row)].fill = pale_blue_fill

# row += 1

# Записываем в Excel значения по дням месяца
for day_json in dist_json.get("days", []):
    excel_sheet['A'+ str(row)] = day_json["date"]
    excel_sheet['A'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['D'+ str(row)] = day_json["Q_vankor"]
    excel_sheet['D'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['F'+ str(row)] = day_json["V_upsv_yu"]["value"]
    match day_json["V_upsv_yu"]["status"]:
        case 0:
            excel_sheet['F'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['F'+ str(row)].fill = green_fill
        case _:
            excel_sheet['F'+ str(row)].fill = red_fill
    
    excel_sheet['G'+ str(row)] = day_json["V_upsv_s"]["value"]
    match day_json["V_upsv_s"]["status"]:
        case 0:
            excel_sheet['G'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['G'+ str(row)].fill = green_fill
        case _:
            excel_sheet['G'+ str(row)].fill = red_fill

    excel_sheet['H'+ str(row)] = day_json["V_cps"]["value"]
    match day_json["V_cps"]["status"]:
        case 0:
            excel_sheet['H'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['H'+ str(row)].fill = green_fill
        case _:
            excel_sheet['H'+ str(row)].fill = red_fill

    excel_sheet['I'+ str(row)] = day_json["V_cppn_1"]
    excel_sheet['I'+ str(row)].fill = pale_green_fill

    excel_sheet['J'+ str(row)] = day_json["V_lodochny_cps_upsv_yu"]["value"]
    match day_json["V_lodochny_cps_upsv_yu"]["status"]:
        case 0:
            excel_sheet['J'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['J'+ str(row)].fill = green_fill
        case _:
            excel_sheet['J'+ str(row)].fill = red_fill

    excel_sheet['K'+ str(row)] = day_json["G_payaha"]
    excel_sheet['K'+ str(row)].fill = pale_blue_fill

    excel_sheet['L'+ str(row)] = day_json["G_sikn"]
    excel_sheet['L'+ str(row)].fill = pale_green_fill
    
    excel_sheet['M'+ str(row)] = day_json["G_sikn_vankor"]
    excel_sheet['M'+ str(row)].fill = pale_green_fill
    
    excel_sheet['N'+ str(row)] = day_json["G_sikn_suzun"]
    excel_sheet['N'+ str(row)].fill = pale_green_fill
    
    excel_sheet['O'+ str(row)] = day_json["G_sikn_vslu"]
    excel_sheet['O'+ str(row)].fill = pale_green_fill
    
    excel_sheet['P'+ str(row)] = day_json["G_sikn_tagul"]["value"]
    match day_json["G_sikn_tagul"]["status"]:
        case 0:
            excel_sheet['P'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['P'+ str(row)].fill = green_fill
        case _:
            excel_sheet['P'+ str(row)].fill = red_fill
    
    excel_sheet['Q'+ str(row)] = day_json["G_sikn_tng"]
    excel_sheet['Q'+ str(row)].fill = pale_green_fill

    excel_sheet['R'+ str(row)] = day_json["delta_G_sikn"]
    excel_sheet['R'+ str(row)].fill = pale_green_fill

    excel_sheet['T'+ str(row)] = day_json["Q_suzun"]
    excel_sheet['T'+ str(row)].fill = pale_blue_fill

    excel_sheet['U'+ str(row)] = day_json["Q_vslu"]
    excel_sheet['U'+ str(row)].fill = pale_blue_fill

    excel_sheet['V'+ str(row)] = day_json["V_upn_suzun"]["value"]
    match day_json["V_upn_suzun"]["status"]:
        case 0:
            excel_sheet['V'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['V'+ str(row)].fill = green_fill
        case _:
            excel_sheet['V'+ str(row)].fill = red_fill


    excel_sheet['W'+ str(row)] = day_json["V_suzun_slu"]
    excel_sheet['W'+ str(row)].fill = pale_green_fill

    excel_sheet['X'+ str(row)] = day_json["V_suzun_vslu"]
    excel_sheet['X'+ str(row)].fill = pale_green_fill

    excel_sheet['Y'+ str(row)] = day_json["V_suzun_tng"]
    excel_sheet['Y'+ str(row)].fill = pale_green_fill

    excel_sheet['Z'+ str(row)] = day_json["G_suzun"]
    excel_sheet['Z'+ str(row)].fill = pale_green_fill

    excel_sheet['AA'+ str(row)] = day_json["G_suzun_slu"]
    excel_sheet['AA'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AB'+ str(row)] = day_json["G_suzun_vslu"]
    excel_sheet['AB'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AC'+ str(row)] = day_json["G_suzun_tng"]
    excel_sheet['AC'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['AD'+ str(row)] = day_json["delta_G_suzun"]
    excel_sheet['AD'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AE'+ str(row)] = day_json["Q_tng"]
    excel_sheet['AE'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['AF'+ str(row)] = day_json["G_payaha"]
    excel_sheet['AF'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['AG'+ str(row)] = day_json["G_buy_day"]
    excel_sheet['AG'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AH'+ str(row)] = day_json["G_out_updt_day"]
    excel_sheet['AH'+ str(row)].fill = pale_green_fill
        
    excel_sheet['AI'+ str(row)] = day_json["G_per"]
    excel_sheet['AI'+ str(row)].fill = pale_green_fill

    excel_sheet['AK'+ str(row)] = day_json["Q_tagul"]
    excel_sheet['AK'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['AL'+ str(row)] = day_json["V_tagul"]["value"]
    match day_json["V_tagul"]["status"]:
        case 0:
            excel_sheet['AL'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['AL'+ str(row)].fill = green_fill
        case _:
            excel_sheet['AL'+ str(row)].fill = red_fill
    
    excel_sheet['AM'+ str(row)] = day_json["G_tagul"]
    excel_sheet['AM'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AN'+ str(row)] = day_json["delta_G_tagul"]
    excel_sheet['AN'+ str(row)].fill = pale_green_fill

    excel_sheet['AP'+ str(row)] = day_json["Q_lodochny"]
    excel_sheet['AP'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['AQ'+ str(row)] = day_json["G_lodochny_uspv_yu"]
    excel_sheet['AQ'+ str(row)].fill = pale_green_fill
        
    excel_sheet['AR'+ str(row)] = day_json["V_upn_lodochny"]["value"]
    match day_json["V_upn_lodochny"]["status"]:
        case 0:
            excel_sheet['AR'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['AR'+ str(row)].fill = green_fill
        case _:
            excel_sheet['AR'+ str(row)].fill = red_fill

    excel_sheet['AS'+ str(row)] = day_json["V_lodochny"]
    excel_sheet['AS'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AT'+ str(row)] = day_json["V_ichem"]["value"]
    match day_json["V_ichem"]["status"]:
        case 0:
            excel_sheet['AT'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['AT'+ str(row)].fill = green_fill
        case _:
            excel_sheet['AT'+ str(row)].fill = red_fill

    
    excel_sheet['AU'+ str(row)] = day_json["G_upn_lodochny"]
    excel_sheet['AU'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AV'+ str(row)] = day_json["G_lodochny"]
    excel_sheet['AV'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AW'+ str(row)] = day_json["G_ichem"]
    excel_sheet['AW'+ str(row)].fill = pale_blue_fill

    excel_sheet['AX'+ str(row)] = day_json["delta_G_upn_lodochny"]
    excel_sheet['AX'+ str(row)].fill = pale_green_fill
    
    excel_sheet['AY'+ str(row)] = day_json["Q_vo"]
    excel_sheet['AY'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['AZ'+ str(row)] = day_json["G_upn_lodochny_ichem"]
    excel_sheet['AZ'+ str(row)].fill = pale_green_fill
    
    excel_sheet['BA'+ str(row)] = day_json["G_tagul_lodochny"]
    excel_sheet['BA'+ str(row)].fill = pale_green_fill
    
    excel_sheet['BB'+ str(row)] = day_json["Q_kchng"]
    excel_sheet['BB'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['BC'+ str(row)] = day_json["G_kchng"]
    excel_sheet['BC'+ str(row)].fill = pale_green_fill
    
    excel_sheet['BD'+ str(row)] = day_json["G_skn"]
    excel_sheet['BD'+ str(row)].fill = pale_blue_fill
    
    excel_sheet['BE'+ str(row)] = day_json["G_gnps"]
    excel_sheet['BE'+ str(row)].fill = pale_green_fill
    
    excel_sheet['BF'+ str(row)] = day_json["V_gnps"]["value"]
    match day_json["V_gnps"]["status"]:
        case 0:
            excel_sheet['BF'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BF'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BF'+ str(row)].fill = red_fill
    
    excel_sheet['BG'+ str(row)] = day_json["V_nps_1"]["value"]
    match day_json["V_nps_1"]["status"]:
        case 0:
            excel_sheet['BG'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BG'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BG'+ str(row)].fill = red_fill
    
    excel_sheet['BH'+ str(row)] = day_json["V_nps_2"]["value"]
    match day_json["V_nps_2"]["status"]:
        case 0:
            excel_sheet['BH'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BH'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BH'+ str(row)].fill = red_fill
    
    excel_sheet['BI'+ str(row)] = day_json["V_knps"]["value"]
    match day_json["V_knps"]["status"]:
        case 0:
            excel_sheet['BI'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BI'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BI'+ str(row)].fill = red_fill
    
    excel_sheet['BJ'+ str(row)] = day_json["V_tstn"]
    excel_sheet['BJ'+ str(row)].fill = pale_green_fill
    
    excel_sheet['BK'+ str(row)] = day_json["V_tstn_rn_vn"]
    excel_sheet['BK'+ str(row)].number_format = "0.000"
    excel_sheet['BK'+ str(row)].fill = pale_green_fill
    
    excel_sheet['BL'+ str(row)] = day_json["V_tstn_vn"]["value"]
    match day_json["V_tstn_vn"]["status"]:
        case 0:
            excel_sheet['BL'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BL'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BL'+ str(row)].fill = red_fill
    
    excel_sheet['BM'+ str(row)] = day_json["V_tstn_suzun"]["value"]
    excel_sheet['BM'+ str(row)].number_format = "0.000"
    match day_json["V_tstn_suzun"]["status"]:
        case 0:
            excel_sheet['BM'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BM'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BM'+ str(row)].fill = red_fill
    
    excel_sheet['BN'+ str(row)] = day_json["V_tstn_suzun_vankor"]["value"]
    match day_json["V_tstn_suzun_vankor"]["status"]:
        case 0:
            excel_sheet['BN'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BN'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BN'+ str(row)].fill = red_fill
    
    excel_sheet['BO'+ str(row)] = day_json["V_tstn_suzun_vslu"]["value"]
    excel_sheet['BO'+ str(row)].number_format = "0.000"
    match day_json["V_tstn_suzun_vslu"]["status"]:
        case 0:
            excel_sheet['BO'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BO'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BO'+ str(row)].fill = red_fill
    
    excel_sheet['BP'+ str(row)] = day_json["V_tstn_tagul_obch"]["value"]
    excel_sheet['BP'+ str(row)].number_format = "0.000"
    match day_json["V_tstn_tagul_obch"]["status"]:
        case 0:
            excel_sheet['BP'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BP'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BP'+ str(row)].fill = red_fill

    excel_sheet['BQ'+ str(row)] = day_json["V_tstn_lodochny"]["value"]
    match day_json["V_tstn_lodochny"]["status"]:
        case 0:
            excel_sheet['BQ'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BQ'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BQ'+ str(row)].fill = red_fill
    
    excel_sheet['BR'+ str(row)] = day_json["V_tstn_tagul"]["value"]
    excel_sheet['BR'+ str(row)].number_format = "0.00"
    match day_json["V_tstn_tagul"]["status"]:
        case 0:
            excel_sheet['BR'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BR'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BR'+ str(row)].fill = red_fill
    
    excel_sheet['BS'+ str(row)] = day_json["V_tstn_skn"]["value"]
    match day_json["V_tstn_skn"]["status"]:
        case 0:
            excel_sheet['BS'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BS'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BS'+ str(row)].fill = red_fill
    
    excel_sheet['BT'+ str(row)] = day_json["V_tstn_vo"]["value"]
    match day_json["V_tstn_vo"]["status"]:
        case 0:
            excel_sheet['BT'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BT'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BT'+ str(row)].fill = red_fill
    
    excel_sheet['BU'+ str(row)] = day_json["V_tstn_tng"]["value"]
    match day_json["V_tstn_tng"]["status"]:
        case 0:
            excel_sheet['BU'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BU'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BU'+ str(row)].fill = red_fill
    
    excel_sheet['BV'+ str(row)] = day_json["V_tstn_kchng"]["value"]
    match day_json["V_tstn_kchng"]["status"]:
        case 0:
            excel_sheet['BV'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BV'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BV'+ str(row)].fill = red_fill

    excel_sheet['BW'+ str(row)] = day_json["F"]["value"]
    match day_json["F"]["status"]:
        case 0:
            excel_sheet['BW'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BW'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BW'+ str(row)].fill = red_fill
    
    excel_sheet['BX'+ str(row)] = day_json["F_vn"]["value"]
    match day_json["F_vn"]["status"]:
        case 0:
            excel_sheet['BX'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BX'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BX'+ str(row)].fill = red_fill
    
    excel_sheet['BY'+ str(row)] = day_json["F_suzun"]["value"]
    match day_json["F_suzun"]["status"]:
        case 0:
            excel_sheet['BY'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BY'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BY'+ str(row)].fill = red_fill
    
    excel_sheet['BZ'+ str(row)] = day_json["F_suzun_vankor"]["value"]
    match day_json["F_suzun_vankor"]["status"]:
        case 0:
            excel_sheet['BZ'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['BZ'+ str(row)].fill = green_fill
        case _:
            excel_sheet['BZ'+ str(row)].fill = red_fill
    
    excel_sheet['CA'+ str(row)] = day_json["F_suzun_vslu"]["value"]
    match day_json["F_suzun_vslu"]["status"]:
        case 0:
            excel_sheet['CA'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CA'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CA'+ str(row)].fill = red_fill
    
    excel_sheet['CB'+ str(row)] = day_json["F_tagul"]["value"]
    match day_json["F_tagul"]["status"]:
        case 0:
            excel_sheet['CB'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CB'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CB'+ str(row)].fill = red_fill
    
    excel_sheet['CC'+ str(row)] = day_json["F_tagul_lpu"]["value"]
    match day_json["F_tagul_lpu"]["status"]:
        case 0:
            excel_sheet['CC'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CC'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CC'+ str(row)].fill = red_fill
    
    excel_sheet['CD'+ str(row)] = day_json["F_tagul_tpu"]["value"]
    match day_json["F_tagul_tpu"]["status"]:
        case 0:
            excel_sheet['CD'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CD'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CD'+ str(row)].fill = red_fill
    
    excel_sheet['CE'+ str(row)] = day_json["F_skn"]["value"]
    match day_json["F_skn"]["status"]:
        case 0:
            excel_sheet['CE'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CE'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CE'+ str(row)].fill = red_fill
    
    excel_sheet['CF'+ str(row)] = day_json["F_vo"]["value"]
    match day_json["F_vo"]["status"]:
        case 0:
            excel_sheet['CF'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CF'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CF'+ str(row)].fill = red_fill
    
    excel_sheet['CG'+ str(row)] = day_json["F_tng"]["value"]
    match day_json["F_tng"]["status"]:
        case 0:
            excel_sheet['CG'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CG'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CG'+ str(row)].fill = red_fill
    
    excel_sheet['CH'+ str(row)] = day_json["F_kchng"]["value"]
    match day_json["F_kchng"]["status"]:
        case 0:
            excel_sheet['CH'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CH'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CH'+ str(row)].fill = red_fill

    excel_sheet['CJ'+ str(row)] = day_json["Q_gnps"]["value"]
    match day_json["Q_gnps"]["status"]:
        case 0:
            excel_sheet['CJ'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CJ'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CJ'+ str(row)].fill = red_fill
    
    excel_sheet['CK'+ str(row)] = day_json["Q_nps_1_2"]["value"]
    match day_json["Q_nps_1_2"]["status"]:
        case 0:
            excel_sheet['CK'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CK'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CK'+ str(row)].fill = red_fill
    
    excel_sheet['CL'+ str(row)] = day_json["Q_knps"]["value"]
    match day_json["Q_knps"]["status"]:
        case 0:
            excel_sheet['CL'+ str(row)].fill = pale_green_fill
        case 1:
            excel_sheet['CL'+ str(row)].fill = green_fill
        case _:
            excel_sheet['CL'+ str(row)].fill = red_fill
    
    row += 1


# Записываем в Excel значения по окончании месяца
excel_sheet['A'+ str(row)] = 'накоп'
excel_sheet['A'+ str(row)].fill = pale_blue_fill

excel_sheet['AI'+ str(row)] = dist_json["G_per_month"]
excel_sheet['AI'+ str(row)].fill = pale_green_fill

excel_sheet['D'+ str(row)] = dist_json["Q_vankor_month"]
excel_sheet['D'+ str(row)].fill = pale_green_fill

excel_sheet['T'+ str(row)] = dist_json["Q_suzun_month"]
excel_sheet['T'+ str(row)].fill = pale_green_fill

excel_sheet['U'+ str(row)] = dist_json["Q_vslu_month"]
excel_sheet['U'+ str(row)].fill = pale_green_fill

excel_sheet['AE'+ str(row)] = dist_json["Q_tng_month"]
excel_sheet['AE'+ str(row)].fill = pale_green_fill

excel_sheet['AY'+ str(row)] = dist_json["Q_vo_month"]
excel_sheet['AY'+ str(row)].fill = pale_green_fill

excel_sheet['AB'+ str(row)] = dist_json["G_suzun_vslu_month"]
excel_sheet['AB'+ str(row)].fill = pale_green_fill

excel_sheet['AA'+ str(row)] = dist_json["G_suzun_slu_month"]
excel_sheet['AA'+ str(row)].fill = pale_green_fill

excel_sheet['Z'+ str(row)] = dist_json["G_suzun_month"]
excel_sheet['Z'+ str(row)].fill = pale_green_fill

excel_sheet['AD'+ str(row)] = dist_json["delta_G_suzun"]
excel_sheet['AD'+ str(row)].fill = pale_green_fill

excel_sheet['AZ'+ str(row)] = dist_json["G_upn_lodochny_ichem_month"]
excel_sheet['AZ'+ str(row)].fill = pale_green_fill

excel_sheet['BB'+ str(row)] = dist_json["Q_kchng_month"]
excel_sheet['BB'+ str(row)].fill = pale_green_fill

excel_sheet['BC'+ str(row)] = dist_json["G_kchng_month"]
excel_sheet['BC'+ str(row)].fill = pale_green_fill

excel_sheet['AK'+ str(row)] = dist_json["Q_tagul_month"]
excel_sheet['AK'+ str(row)].fill = pale_green_fill

excel_sheet['AP'+ str(row)] = dist_json["Q_lodochny_month"]
excel_sheet['AP'+ str(row)].fill = pale_green_fill

excel_sheet['AQ'+ str(row)] = dist_json["G_lodochny_uspv_yu_month"]
excel_sheet['AQ'+ str(row)].fill = pale_green_fill

excel_sheet['AX'+ str(row)] = dist_json["delte_G_upn_lodochny_month"]
excel_sheet['AX'+ str(row)].fill = pale_green_fill

excel_sheet['AM'+ str(row)] = dist_json["G_tagul_month"]
excel_sheet['AM'+ str(row)].fill = pale_green_fill

excel_sheet['AN'+ str(row)] = dist_json.get("delta_G_tagul_month", dist_json.get("delta_G_tagul"))
excel_sheet['AN'+ str(row)].fill = pale_green_fill

excel_sheet['BA'+ str(row)] = dist_json["G_tagul_lodochny_month"]
excel_sheet['BA'+ str(row)].fill = pale_green_fill

excel_sheet['AV'+ str(row)] = dist_json["G_lodochny_month"]
excel_sheet['AV'+ str(row)].fill = pale_green_fill

excel_sheet['O'+ str(row)] = dist_json["G_sikn_vslu_month"]
excel_sheet['O'+ str(row)].fill = pale_green_fill

excel_sheet['P'+ str(row)] = dist_json["G_sikn_tagul_month"]
excel_sheet['P'+ str(row)].fill = pale_green_fill

excel_sheet['N'+ str(row)] = dist_json["G_sikn_suzun_month"]
excel_sheet['N'+ str(row)].fill = pale_green_fill

excel_sheet['Q'+ str(row)] = dist_json["G_sikn_tng_month"]
excel_sheet['Q'+ str(row)].fill = pale_green_fill

excel_sheet['L'+ str(row)] = dist_json["G_sikn_month"]
excel_sheet['L'+ str(row)].fill = pale_green_fill

excel_sheet['M'+ str(row)] = dist_json["G_sikn_vankor_month"]
excel_sheet['M'+ str(row)].fill = pale_green_fill

excel_sheet['BD'+ str(row)] = dist_json["G_skn_month"]
excel_sheet['BD'+ str(row)].fill = pale_green_fill

excel_sheet['R'+ str(row)] = dist_json["delta_G_sikn_month"]
excel_sheet['R'+ str(row)].fill = pale_green_fill

excel_sheet['BZ'+ str(row)] = dist_json["F_suzun_vankor_month"]
excel_sheet['BZ'+ str(row)].fill = pale_green_fill

excel_sheet['CA'+ str(row)] = dist_json["F_suzun_vslu_month"]
excel_sheet['CA'+ str(row)].fill = pale_green_fill

excel_sheet['CC'+ str(row)] = dist_json["F_tagul_lpu_month"]
excel_sheet['CC'+ str(row)].fill = pale_green_fill

excel_sheet['CD'+ str(row)] = dist_json["F_tagul_tpu_month"]
excel_sheet['CD'+ str(row)].fill = pale_green_fill

excel_sheet['CB'+ str(row)] = dist_json["F_tagul_month"]
excel_sheet['CB'+ str(row)].fill = pale_green_fill

excel_sheet['CE'+ str(row)] = dist_json["F_skn_month"]
excel_sheet['CE'+ str(row)].fill = pale_green_fill

excel_sheet['CF'+ str(row)] = dist_json["F_vo_month"]
excel_sheet['CF'+ str(row)].fill = pale_green_fill

excel_sheet['CG'+ str(row)] = dist_json["F_tng_month"]
excel_sheet['CG'+ str(row)].fill = pale_green_fill

excel_sheet['CH'+ str(row)] = dist_json["F_kchng_month"]
excel_sheet['CH'+ str(row)].fill = pale_green_fill

excel_sheet['BW'+ str(row)] = dist_json["F_month"]
excel_sheet['BW'+ str(row)].fill = pale_green_fill

excel_sheet['BE'+ str(row)] = dist_json["G_gnps_month"]
excel_sheet['BE'+ str(row)].fill = pale_green_fill


excel_sheet['AG'+ str(row)] = dist_json["G_buying_oil"]
excel_sheet['AG'+ str(row)].fill = pale_blue_fill

excel_sheet['AH'+ str(row)] = dist_json["G_out_udt"]
excel_sheet['AH'+ str(row)].fill = pale_blue_fill

excel_sheet['BY'+ str(row)] = dist_json["F_suzun_month"]
excel_sheet['BY'+ str(row)].fill = pale_green_fill

excel_sheet['BX'+ str(row)] = dist_json["F_vn_month"]
excel_sheet['BX'+ str(row)].fill = pale_green_fill

# Сохраняем результат
excel_file.save(f"balance {date_str}.xlsx")


