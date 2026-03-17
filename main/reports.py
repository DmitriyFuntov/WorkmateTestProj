from collections import defaultdict
import statistics
import csv
import os
from typing import List, Tuple

REPORT_REGISTRY = {}

def register_report(name: str):
    """Декоратор для регистрации нового отчёта"""
    def decorator(func):
        REPORT_REGISTRY[name] = func
        return func
    return decorator


@register_report('median-coffee')
def generate_median_coffee_report(file_paths: List[str]) -> Tuple[List[str], List[List]]:
    """Медиана трат на кофе по каждому студенту (по всем файлам)"""
    coffee_by_student = defaultdict(list)

    for path in file_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Файл не найден: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                student = row['student']
                try:
                    spent = int(row['coffee_spent'])
                    coffee_by_student[student].append(spent)
                except (ValueError, KeyError):
                    continue 

    if not coffee_by_student:
        return ['Студент', 'Медиана трат'], [['Нет данных']]

    medians = []
    for student, spends in coffee_by_student.items():
        med = statistics.median(spends)
        medians.append([student, int(med)]) 

    medians.sort(key=lambda x: x[1], reverse=True)
    return ['Студент', 'Медиана трат на кофе (руб)'], medians