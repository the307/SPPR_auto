# Путь к JSON с исходными данными
# По умолчанию используем `data_input.json` рядом с проектом (в этой же папке).
# Если файла нет — оставляем запасной путь (для старой структуры/запусков из PyCharmProjects).
from pathlib import Path

INPUT_JSON_PATH = Path(__file__).resolve().parent / "data_input.json"
