import pandas as pd

def update_df(master_df: pd.DataFrame, day_result: dict) -> pd.DataFrame:
    """
    Обновляет master_df значениями за день.

    - Если строка с date уже есть — обновляет/добавляет колонки.
    - Если строки нет — добавляет новую.
    Возвращает обновлённый master_df.
    """
    if "date" not in day_result:
        raise ValueError("day_result должен содержать ключ 'date'")

    # Общая логика: если пришли "нулевые" значения с суффиксом `_0`,
    # то дублируем их в колонки без `_0` (только если базового ключа ещё нет).
    # Пример: V_suzun_slu_0 -> V_suzun_slu
    for key, value in list(day_result.items()):
        if isinstance(key, str) and key.endswith("_0"):
            base_key = key[:-2]
            day_result.setdefault(base_key, value)

    n = pd.to_datetime(day_result["date"]).normalize()
    day_mask = master_df["date"] == n

    if day_mask.any():
        rows_idx = master_df.index[day_mask]
        for key, value in day_result.items():
            if key == "date":
                continue

            if key not in master_df.columns:
                master_df[key] = pd.NA

            is_scalar = pd.api.types.is_scalar(value)
            needs_object_write = (not is_scalar) or isinstance(value, dict)
            if needs_object_write:
                if master_df[key].dtype != "object":
                    master_df[key] = master_df[key].astype("object")
                master_df.loc[day_mask, key] = pd.Series(
                    [value] * len(rows_idx),
                    index=rows_idx,
                    dtype="object",
                )
            else:
                master_df.loc[day_mask, key] = value
    else:
        master_df = pd.concat([master_df, pd.DataFrame([day_result])], ignore_index=True)

    master_df.sort_values("date", inplace=True)
    master_df.reset_index(drop=True, inplace=True)
    return master_df