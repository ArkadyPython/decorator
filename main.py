from mains import logger
from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
@logger('main.log')
def normal_name(rows):
    result = [' '.join(i[:3]).split(' ')[:3] + i[3:] for i in rows]
    return result

def delete_dublicates(correct_list):
    no_dublicates = []
    for compared in correct_list:
        for employee in correct_list:
            if compared[0:2] == employee[0:2]:
                list_employee = compared
                compared = list_employee[0:2]
                for i in range(2, 7):
                    if list_employee[i] == '':
                        compared.append(employee[i])
                    else:
                        compared.append(list_employee[i])
        if compared not in no_dublicates:
            no_dublicates.append(compared)

    return no_dublicates

def updating_phone(rows, regular, new):
    phonebook = []
    pattern = re.compile(regular)
    phonebook = [[pattern.sub(new, string) for string in strings] for strings in rows]
    return phonebook

correct_list = normal_name(contacts_list)
no_dublicates_list = delete_dublicates(correct_list)
regular = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})'
correct_list_2 = updating_phone(no_dublicates_list, regular, r'+7(\2)\3-\4-\5')
regular2 = r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*'
correct_list_3 = updating_phone(correct_list_2, regular2, r'+7(\2)\3-\4-\5 доб.\6')

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(correct_list_3)