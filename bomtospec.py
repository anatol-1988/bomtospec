# -*- coding: utf-8 -*-
"""
    bomtospec
    ~~~~~~~~~

    Утилита для получения файла спецификации из BOM-перечня.

    :author: Anatol Karalkou
    :contact: anatol1988@gmail.com
    :license: Apache License Version 2.0, see LICENSE for details.
"""

import csv
import re
import argparse
import sys
from element_types import element_types


def find_type(ref_des):
    """
    Возвращает группу видов элементов

    Параметры
    _________

    ref_des : Позиционное обозначение элемента
    """
    # Выделяем позиционное обозначение
    comp_type = ref_des[ref_des.find('-') + 1:] if (
        '-' in ref_des) else ref_des
    # Выделяем код элемента
    code = re.match('[A-Z]*', comp_type).group(0)
    # Возвращаем группу видов элементов
    return element_types[code] if code in element_types else ''


if __name__ == '__main__':
    sys.stdout = open('log.txt', 'w')

    # Настройка аргументов утилиты
    parser = argparse.ArgumentParser(
        description='Выдает список спецификации на основании BOM')
    parser.add_argument('input', help='файл BOM')
    parser.add_argument('output', help='файл спецификации')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='cp1251') as csv_input:
        bom = csv.DictReader(csv_input, delimiter=',')

        # Перечень компонентов с относящимся к ним списком
        # позиционных обозначений
        component_map = {}

        for position in bom:
            comp_name = position['Value']
            ref_des = position['RefDes']

            if comp_name not in component_map:
                component_map[comp_name] = [ref_des]
            else:
                component_map[comp_name].append(ref_des)

    # Список спецификации
    specification = []

    for component in component_map:
        specification.append({'Раздел': find_type(component_map[component][0]),
                              'Наименование': component,
                              'Количество': len(component_map[component]),
                              'Примечание': ', '.join(component_map[component])
                              })

    # Записываем спецификацию в файл
    with open(args.output, 'w', newline='', encoding='cp1251') as csv_output:
        spec_writer = csv.DictWriter(
            csv_output,
            ['Раздел', 'Наименование', 'Количество', 'Примечание'],
            delimiter=';',
            quoting=csv.QUOTE_MINIMAL,
            extrasaction='ignore')

        spec_writer.writeheader()

        for component in specification:
            spec_writer.writerow(component)
