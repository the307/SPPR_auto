from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from openpyxl.comments import Comment


def export_to_excel(
    master_df,
    output_path,
    calc_date,
    alarm_flag=False,
    alarm_msg=None,
    month_column_name="F_bp_month"
):
    """
    Сохраняет DataFrame в Excel и при необходимости:
    - красит ячейку месячного значения
    - добавляет комментарий

    alarm_flag / alarm_msg — служебные сигналы из calculate
    """

    # --- 1. Сохраняем DataFrame ---
    master_df.to_excel(output_path, index=False)

    # --- 2. Если нет тревоги — выходим ---
    if not alarm_flag:
        print(f"Результат сохранён в {output_path}")
        return

    # --- 3. Открываем Excel для форматирования ---
    wb = load_workbook(output_path)
    ws = wb.active

    # --- 4. Находим колонку месячного значения ---
    headers = [cell.value for cell in ws[1]]
    if month_column_name not in headers:
        wb.save(output_path)
        print(f"Колонка {month_column_name} не найдена — файл сохранён без подсветки")
        return

    col_idx = headers.index(month_column_name) + 1

    # --- 5. Ищем строку расчётной даты ---
    target_row = None
    for row in range(2, ws.max_row + 1):
        if ws.cell(row=row, column=1).value == calc_date:
            target_row = row
            break

    if target_row is None:
        wb.save(output_path)
        print("Дата расчёта не найдена — файл сохранён без подсветки")
        return

    # --- 6. Красим и комментируем ---
    cell = ws.cell(row=target_row, column=col_idx)
    cell.fill = PatternFill("solid", fgColor="FF9999")
    cell.comment = Comment(alarm_msg, "СППР")

    wb.save(output_path)
    print(f"Результат сохранён в {output_path} (с предупреждением)")