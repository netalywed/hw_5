documents = [
  {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
  {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
  {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
  '1': ['2207 876234', '11-2'],
  '2': ['10006'],
  '3': []
}

def find_name (docs):
  user_input = input("Назовите номер документа ")
  name = 'Такого документа не существует'
  for doc in documents:
    if doc["number"] == user_input:
      name = doc["name"]
  return name



def find_shelf (shelves):
  user_input = input("Назовите номер документа ")
  shelf_number = 'Такого документа не существует'
  for shelf in list(shelves.items()):
    if user_input in shelf[1]:
      shelf_number = shelf[0]
  return shelf_number


def find_all_info (docs):
  all_docs_info = []
  for doc in docs:
    values = list(doc.values())
    print(values[0] + ' "' + values[1] + '" ', '"' + values[2] + '"')
    all_docs_info.append(values)
  return all_docs_info

def add_new_person (docs, direct, doc, shelf_number):
  if shelf_number in list(direct.keys()):
    list_of_numbers = direct[shelf_number]
    doc_number = doc["number"]
    list_of_numbers.append(doc_number)
    docs.append(doc)
    result = direct
  else:
    result = "Такой полки нет, документ не был сохранен."
  return result

def remove_doc_from_shelf(doc_number):
  for directory_number, directory_docs_list in directories.items():
    if doc_number in directory_docs_list:
      directory_docs_list.remove(doc_number)
      removed = 'yes'
      break
    else:
      removed = 'no such document'
  return removed

if __name__ == '__main__':
  while True:
    user_input = input("Введите команду ")
    if user_input == "p":
      print(find_name(documents))
    if user_input == "s":
      print(find_shelf(directories))
    if user_input == "l":
      find_all_info(documents)
    if user_input == "a":
      doc = {}
      doc_type = input("Пожалуйста, введите тип документа ")
      doc["type"] = doc_type
      doc_number = input("Пожалуйста, введите номер документа ")
      doc["number"] = doc_number
      name = input("Пожалуйста, введите имя ")
      doc["name"] = name
      shelf_number = input("Введите номер полки ")
      print(add_new_person(documents, directories, doc_number, shelf_number))