import csv
import re
import argparse

type_codes = {
    'R': 'Резистор',
    'VT': 'Транзистор',
    'VD': 'Диод',
    'X': 'Разъем',
    'C': 'Конденсатор',
    'L': 'Дроссель',
    'D': 'Микросхема',
    'VT': 'Транзистор',
    'ZQ': 'Кварцевый резонатор',
    'XP': 'Вилка штыревая'
}


def find_type(ref_des):
    comp_type = ref_des[ref_des.find(
        '-') + 1:] if ('-' in ref_des) else ref_des
    return type_codes[re.match('[A-Z]*', comp_type).group(0)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Выдает список спецификации на основании BOM')
    parser.add_argument('input', help='файл BOM')
    parser.add_argument('output', help='файл спецификации')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='cp1251') as inCsv:
        bom = csv.DictReader(inCsv, delimiter=',')

        componentMap = {}

        for position in bom:
            compName = position['Value']
            refDes = position['RefDes']

            if compName not in componentMap:
                componentMap[compName] = [refDes]
            else:
                componentMap[compName].append(refDes)

    specification = []

    for component in componentMap:
        specification.append({'Раздел': find_type(
            componentMap[component][0]), 'Наименование': component,
            'Количество': len(componentMap[component]),
            'Примечание': ', '.join(componentMap[component])})

    with open(args.output, 'w', newline='', encoding='cp1251') as outFile:
        bomOut = csv.DictWriter(
            outFile, ['Раздел', 'Наименование', 'Количество', 'Примечание'],
            delimiter=';', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
        bomOut.writeheader()

        for component in specification:
            bomOut.writerow(component)
