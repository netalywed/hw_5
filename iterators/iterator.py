import requests
import json
from pprint import pprint


with open('country') as f:
    file = json.load(f)
    # pprint(file)
# for country in file:
#     country_name = country['name']['common']


class Countries_list:

    def __init__(self, path):
        self.file = open(path)
        self.i = 0

    def __iter__(self):
        self.country = json.load(self.file)
        return self

    def __next__(self):
        self.i += 1
        if self.i == len(self.country):
            self.file.close()
            raise StopIteration
        country_name = self.country[self.i]['name']['common']
        country_name = country_name.replace(" ", "_")
        country_link = "https://en.wikipedia.org/wiki/" + country_name
        return country_link

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

# with Countries_list('country') as C:
#     for country_name in C:
#         print(country_name)
#
for country in Countries_list('country'):
    print(country)
# for country in file:
#     country_name = country['name']['common']
#     query_1 = 'https://en.wikipedia.org/w/api.php?action=opensearch&search='
#     query_2 = country_name
#     query_3 = '&limit=1&namespace=0&format=json'
#     response = requests.get(query_1 + query_2 + query_3)
#     raw_answer = response.text
#     answer = ''.join(raw_answer)
#     print(raw_answer.split(','))
#     link = answer[0]
#     # print(link)




# file = json.dumps(, sort_keys=True, indent=4)
# pprint(file)


# ('https://en.wikipedia.org/w/api.php?action=opensearch&search=India&limit=1&namespace=0&format=json')

