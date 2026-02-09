from typing import Any, Dict, Optional

from export import export_to_json


def handle_error(
    error_info: Optional[Dict[str, Any]],
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Возвращает dict с ошибкой (готовый для API). Файл НЕ создаётся, если output_path не задан."""
    if not error_info:
        return {}

    return export_to_json(
        master_df=None,
        output_path=output_path,
        error=error_info,
    )
