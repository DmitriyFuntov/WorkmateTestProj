import argparse
import sys
from reports import REPORT_REGISTRY


def main():
    parser = argparse.ArgumentParser(
        description='Отчет о потреблении кофе студентов',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--files', nargs='+', required=True,
                        help='Пути к одному или нескольким CSV-файлам')
    parser.add_argument('--report', required=True,
                        help='Название отчета (сейчас только median-coffee)')

    args = parser.parse_args()

    if args.report not in REPORT_REGISTRY:
        print(f"Ошибка: неизвестный отчёт '{args.report}'")
        print(f"Доступные отчёты: {list(REPORT_REGISTRY.keys())}")
        sys.exit(1)

    try:
        generator = REPORT_REGISTRY[args.report]
        headers, table_data = generator(args.files)
        from tabulate import tabulate
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()