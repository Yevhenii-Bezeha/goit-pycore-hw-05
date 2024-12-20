import sys
import os
import re
from typing import List, Dict

def parse_log_line(line: str) -> dict:

    match = re.match(r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (INFO|ERROR|DEBUG|WARNING) (.+)", line)
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2),
            "level": match.group(3),
            "message": match.group(4).strip()
        }
    return {}

def load_logs(file_path: str) -> List[dict]:

    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parsed_line = parse_log_line(line)
                if parsed_line:
                    logs.append(parsed_line)
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:

    return [log for log in logs if log.get("level") == level.upper()]

def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:

    counts = {}
    for log in logs:
        level = log.get("level")
        counts[level] = counts.get(level, 0) + 1
    return counts

def display_log_counts(counts: Dict[str, int]):

    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in sorted(counts.items()):
        print(f"{level:<16} | {count}")

def display_logs(logs: List[dict]):

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу_логів> [<рівень_логування>]")
        sys.exit(1)

    log_file = sys.argv[1]
    log_level = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isfile(log_file):
        print(f"Файл {log_file} не існує.")
        sys.exit(1)

    logs = load_logs(log_file)
    counts = count_logs_by_level(logs)

    display_log_counts(counts)

    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        print(f"\nДеталі логів для рівня '{log_level.upper()}':")
        display_logs(filtered_logs)