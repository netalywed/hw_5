import requests
from pprint import pprint
from datetime import datetime
from candidate import search_photos



class TheClient:
    def __init__(self, vk_token, vk_group):
        self.url = 'https://api.vk.com/method/'
        self.vk_token = vk_token
        self.vk_group = vk_group
        self.params = {
            'access_token': vk_token,
            'v': '5.131'
        }

    def bot_tells(self, id, text):
        self.vk_group.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

    # Метод для поиска необходимой информации о клиенте
    def UsersInfo(self, id_client):
        UsersInfo_url = self.url + 'users.get'
        UsersInfo_params = {
            'user_ids': id_client,
            'fields': 'sex, city, status, relation, bdate'
        }
        req = requests.get(UsersInfo_url, params={**self.params, **UsersInfo_params}).json()
        pprint(req)
        not_full = ''
        if 'sex' in req['response'][0]:
            client_sex = req['response'][0]['sex']
        else:
            not_full = 'заполнить поля'
            client_sex = ''
        try:
            if 'title' in req['response'][0]['city']:
                client_city = req['response'][0]['city']['title']
        except KeyError:
            not_full = 'заполнить поля'
            client_city = ''

        try:
            if 'bdate' in req['response'][0]:
                client_bdate = req['response'][0]['bdate']
                client_bdate = str(client_bdate)
                bdate = client_bdate[-4:]
                bdate = int(bdate)
        except KeyError:
            not_full = 'заполнить поля'
            bdate = ''

        try:
            if 'relation' in req['response'][0]:
                client_relation = req['response'][0]['relation']
        except KeyError:
            not_full = 'заполнить поля'
            client_relation = ''

        client_info = {}
        client_info['sex'] = client_sex
        client_info['city'] = client_city
        client_info['bdate'] = bdate
        client_info['status'] = client_relation
        client_info['not_full'] = not_full
        print(client_info)

        return client_info

    # если на странице неполные данные, спрашиваем пользователя
    def ask_user(self, client_info, client_id):
        if client_info['bdate'] == '':
            text = 'Напишите год вашего рождения'
        elif client_info['sex'] == '':
            text = 'Я уточню ваш пол: если вы женщина, напишите "женщина", если мужчина - "мужчина"'
        elif client_info['status'] == '' or client_info['status'] == 0:
            text = 'Какое у вас семейное положение? Выберите один из вариантов про себя: не женат, не замужем, есть друг, есть подруга, помолвлен, помолвлена, женат, замужем, всё сложно, в активном поиске, влюблён, влюблена, в гражданском браке;'
        elif client_info['city'] == '':
            text = 'В каком городе вы живете? Напишите название'
        else:
            text = 'Ура, все поля заполнены! Идем дальше)'
        self.bot_tells(client_id, text)

        return text

    # Подбираем параметры для пары клиента и ищем 3 подходящих кандидатов
    def search_pair(self, client_info):
        current_year = int(datetime.now().year)
        pair_info = {}
        pair_info['status'] = client_info['status']
        pair_info['city'] = client_info['city']
        if client_info['sex'] == 1:
            pair_info['sex'] = '2'
        elif client_info['sex'] == 2:
            pair_info['sex'] = '1'
        if client_info['sex'] == 1:
            pair_info['age_from'] = current_year - int(client_info['bdate'])
            pair_info['age_to'] = current_year - int(client_info['bdate']) + 10
        elif client_info['sex'] == 2:
            pair_info['age_from'] = current_year - int(client_info['bdate']) - 10
            pair_info['age_to'] = current_year - int(client_info['bdate'])

        search_id_url = self.url + 'users.search'
        search_id_params = {
            'count': 10,
            'sex': pair_info['sex'],
            'hometown': pair_info['city'],
            'status': pair_info['status'],
            'age_from': pair_info['age_from'],
            'age_to': pair_info['age_to']
        }
        req = requests.get(search_id_url, params={**self.params, **search_id_params}).json()
        amount_of_pairs = len(req['response']['items'])
        pair_main_info = req['response']['items']
        pairs_ids = []
        for i in range(0, amount_of_pairs):
            pair_id = pair_main_info[i]['id']
            pairs_ids.append(pair_id)
        return pairs_ids


# функция проверки в бд
# цикл фор с pairs_ids, внутри объект класса с id, проверка)
