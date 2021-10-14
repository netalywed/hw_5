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
    # редактируем ФИО
    name = []
    name.append(contacts_list[line][0])
    name.append(contacts_list[line][1])
    name.append(contacts_list[line][2])
    one_name = ' '.join(name)
    three_names = one_name.strip().split()

    # редактируем номер телефона
    phone_number_raw = contacts_list[line][-2]
    right_format = re.sub(r'((\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*\(?(доб\.)?\s*((\d{4}))?\)?)',
                          r'+7(\3)\4-\5-\6 \7\8', phone_number_raw)
    #создаем список для каждого человека
    all_info = three_names[1:3] + contacts_list[line][3:5]
    all_info.append(right_format)
    all_info.append(contacts_list[line][6])

    # делаем проверку на повторение людей через словарь
    lastname = three_names[0]

    if lastname in contacts_dict.keys():
        new_info = []
        info_in_dict = contacts_dict[lastname]
        zipped_info = list(zip(info_in_dict, all_info))
        pprint(zipped_info)
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

        #print(new_info)
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




