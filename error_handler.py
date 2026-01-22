from typing import Any, Dict, Optional

from export import export_to_json


def handle_error(
    error_info: Optional[Dict[str, Any]],
    output_path: str = "output.json",
) -> bool:
    """Пишет ошибку в JSON. Возвращает True, если обработка выполнена."""
    if not error_info:
        return False

    export_to_json(
        master_df=None,
        output_path=output_path,
        calc_date=None,
        alarm_flag=False,
        alarm_msg=None,
        error=error_info,
    )
    return True
