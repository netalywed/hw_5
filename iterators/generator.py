import json

def my_generator(path):
    file = open(path)
    i = 0
    country = json.load(file)
    while i < len(country):
        country_name = country[i]['name']['common']
        country_name = country_name.replace(" ", "_")
        country_link = "https://en.wikipedia.org/wiki/" + country_name
        i += 1
        yield country_link
    file.close()


for country in my_generator('country'):
    print(country)
