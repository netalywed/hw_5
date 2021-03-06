from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding = "utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)



contacts_dict = {}
for line in range(1, len(contacts_list)):
    raw = ','.join(contacts_list[line])
    # for key, pattern in patterns.items():
    #     row_data = re.sub(pattern['regexp'], pattern['subst'], raw)
    # print(row_data.split(','))
    # редактируем ФИО

    name = []
    name.append(contacts_list[line][0])
    name.append(contacts_list[line][1])
    name.append(contacts_list[line][2])
    one_name = ' '.join(name)
    three_names = one_name.strip().split()

# создаем список для каждого человека
    all_info = three_names[1:3] + contacts_list[line][3:5]

    # редактируем номер телефона
#     phone_number_raw = contacts_list[line][-2]
    phone = []
    right_format_phone_ = re.search(r'((\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2}))', raw)
    if right_format_phone_ is not None:
        right_format_phone = right_format_phone_.group(0)
        right_format_phone = re.sub(r'((\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2}))', r'+7(\3)\4-\5-\6', right_format_phone)
        phone.append(right_format_phone)

    right_format_add_phone_ = re.search(r'[\(]?доб\.\s(\d+)[\)]?', raw)
    if right_format_add_phone_ is not None:
        right_format_add_phone = right_format_add_phone_.group(0)
        right_format_add_phone = re.sub(r'[\(]?доб\.\s(\d+)[\)]?', r' доп.\1', right_format_add_phone)
        phone.append(right_format_add_phone)
    phone = ''.join(phone)
    all_info.append(phone)

    # редактируем email
    email = re.search(r'([\d*]|[\w*]|[\.])*@[a-z]*\.[\w]*', raw)

    if email is not None:
        email_ = email.group(0)
        all_info.append(email_)

    # делаем проверку на повторение людей через словарь
    lastname = three_names[0]

    if lastname in contacts_dict.keys():
        new_info = []
        info_in_dict = contacts_dict[lastname]
        zipped_info = list(zip(info_in_dict, all_info))
        for double in zipped_info:
            double_rem = list(double)
            if double_rem[0] == double_rem[1]:
                double_rem.remove(double_rem[1])
                new_info.append(''.join(double_rem))
            elif double_rem[0] == '' or double_rem[1] == '':
                one_rem = double_rem[0] + double_rem[1]
                one_rem.strip()
                new_info.append(one_rem)
            else:
                new_info.append(', '.join(double_rem))
        contacts_dict.update({lastname: new_info})

    else:
        contacts_dict[lastname] = all_info
final_list = []
for key, value in list(contacts_dict.items()):
    person_list = []
    person_list.append(key)
    person_list = person_list + value
    final_list.append(person_list)
pprint(final_list)
with open("phonebook.csv", "w") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(final_list)



