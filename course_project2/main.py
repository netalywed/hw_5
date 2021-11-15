from pprint import pprint
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import time


class TheClient:
    url = 'https://api.vk.com/method/'

    def __init__(self, token):
        self.params = {
            'access_token': token,
            'v': '5.131'
        }

    def bot_tells(self, id, text):
        vk_group.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

    # Метод для поиска необходимой информации о клиенте
    def UsersInfo(self, id_client):
        self.UsersInfo_url = self.url + 'users.get'
        self.UsersInfo_params = {
            'user_ids': id_client,
            'fields': 'sex, city, status, relation, bdate'
        }
        req = requests.get(self.UsersInfo_url, params={**self.params, **self.UsersInfo_params}).json()
        # pprint(req)
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
                client_info = {}
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

    def check_marrage_search_pair(self, client_info, client_id):
        status = client_info['status']
        pairs_ids = {}
        if status == 2 or status == 3 or status == 4 or status == 7 or status == 8:
            text = 'Упс, ваш статус показывает, что у вас уже есть любимый человек. К сожалению, по этическим соображениям, не могу искать вам пару:('
            self.bot_tells(client_id, text)
        else:
            pairs_ids = self.search_pair(client_info)
        return pairs_ids
    # Подбираем параметры для пары клиента и ищем 3 подходящих кандидатов
    def search_pair(self, client_info):   #(self, client_info_all):
        pair_info = {}
        pair_info['status'] = '1'
        pair_info['city'] = client_info['city']
        if client_info['sex'] == 1:
            pair_info['sex'] = '2'
        elif client_info['sex'] == 2:
            pair_info['sex'] = '1'
        if client_info['sex'] == 1:
            pair_info['age_from'] = 2021 - int(client_info['bdate'])
            pair_info['age_to'] = 2021 - int(client_info['bdate']) + 10
        elif client_info['sex'] == 2:
            pair_info['age_from'] = 2021 - int(client_info['bdate']) - 10
            pair_info['age_to'] = 2021 - int(client_info['bdate'])

        self.search_id_url = self.url + 'users.search'
        self.search_id_params = {
            'count': 10,
            'sex': pair_info['sex'],
            'hometown': pair_info['city'],
            'status': pair_info['status'],
            'age_from': pair_info['age_from'],
            'age_to': pair_info['age_to']
        }
        req = requests.get(self.search_id_url, params={**self.params, **self.search_id_params}).json()
        amount_of_pairs = len(req['response']['items'])
        pair_main_info = req['response']['items']
        pairs_ids = []
        for i in range(0, amount_of_pairs):
            pair_id = pair_main_info[i]['id']
            pairs_ids.append(pair_id)
        if len(pairs_ids) > 3:           # такое маленькое количество поставлено для тестирования. Иначе вк выдает ошибку о большом кол-ве сообщений
            pairs_ids = pairs_ids[-3:]
        return pairs_ids


def search_photos(pair_id, token):
    # берем id пары и ищем фотографии.
    # берем 3 фото с наибольшем количеством лайков
    chosen_photos = []
    photos_search_url = 'https://api.vk.com/method/photos.get'
    params = {'v': '5.131',
              'access_token': token}
    photos_search_params = {
        'album_id': 'profile',
        'owner_id': pair_id,
        'extended': 1
    }
    req = requests.get(photos_search_url, params={**params, **photos_search_params}).json()
    chosen_photos_raw = []
    try:
        photos_amount = len(req['response']['items'])
        photos_info = req['response']['items']
        for i in range(0, photos_amount):
            photos_list_raw = []
            likes = photos_info[i]['likes']['count']
            comments = photos_info[i]['comments']['count']
            weight = likes + comments
            photos_list_raw.append(weight)
            bigger_photo = photos_info[i]['sizes'][-1]
            url = bigger_photo['url']
            photos_list_raw.append(url)
            chosen_photos_raw.append(photos_list_raw)
        chosen_photos_raw = sorted(chosen_photos_raw, key=lambda photo: photo[0])
        if len(chosen_photos_raw) > 3:
            chosen_photos_raw = chosen_photos_raw[-3:]
        chosen_photos = list(map(lambda photo: photo[1], chosen_photos_raw))
        pprint(chosen_photos)
    except KeyError:
        chosen_photos.append("профиль закрыт")
        pass

    return chosen_photos

def send_pair_into_to_user(a_client_pair, client_id):
    for pair in a_client_pair:
        pair_id_full = 'https://vk.com/id' + str(pair)
        vk_client.bot_tells(client_id, pair_id_full)
        # ищем фотографии
        all_pair_photos = search_photos(pair, token_VK)
        if all_pair_photos[0] == "профиль закрыт":
            text = 'У этого пользователя закрытый аккаунт, поэтому я не смогу прислать фото. Но вы можете добавиться к этому человеку в друзья:)'
            vk_client.bot_tells(client_id, text)
        else:
            for i in all_pair_photos:
                text = str(i)
                vk_client.bot_tells(client_id, text)
        time.sleep(2)
    return


def recognition(user_message):
    with open('dictionary.json', encoding="utf-8") as f:
        dict_to_search = json.load(f)
        rec_dict = {}

        rec_dict["topic"] = 'не определена'
        if user_message.isdigit() and len(user_message) == 3:
            rec_dict["topic"] = 'bdate'
            rec_dict["our_match"] = user_message

        for main_key, value in dict_to_search.items():
            for key, synonyms in value.items():
                if user_message in synonyms:
                    rec_dict["topic"] = main_key
                    rec_dict["our_match"] = key
                    print(rec_dict)
                    break

    return rec_dict



if __name__ == "__main__":

    # Получение ТОКЕНА. Если нет прикрепленного файла, используем ручной ввод.
    # with open('group_token.txt', 'r') as file_object:
    token_VK_group = 'b059649cc85100192ce4c665f56497fe57af9856523a558e36c153280382d0acf6a52c7c0add506eb5c94' #file_object.read().strip()
    # with open('token_VK.txt', 'r') as file_object:
    token_VK = 'e3f47e8c68cc83b35fc53f2e10c2610de82223cb9451f28d2197b4b5791afa6f23eeb96a488b701e027c4' #file_object.read().strip()

    vk_group = vk_api.VkApi(token=token_VK_group)
    # vk_session = vk_group.get_api()
    longpoll = VkLongPoll(vk_group)
    vk_client = TheClient(token_VK)
    info_about_user = {}


    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = event.text.lower()
            # Получаем id пользователя
            user_id = event.user_id
            # определяем по словарю, что говорит пользователь
            theme = recognition(message)
            # ниже в ifs фразы пользователя и реакция на них бота
            if 'привет' in message:
                vk_client.bot_tells(user_id, 'Привет! Начинаю подбирать для вас пару')
                # узнаем информацию о пользователе
                info_about_user = vk_client.UsersInfo(user_id)
                if info_about_user['not_full'] != 'заполнить поля':
                    client_pair = vk_client.check_marrage_search_pair(info_about_user, user_id)
                    send_pair_into_to_user(client_pair, user_id)
                else:
                    # когда поля недозаполнены
                    vk_client.ask_user(info_about_user, user_id)

            elif theme["topic"] == "cities":
                info_about_user['city'] = theme["our_match"]
                print(info_about_user)
                result = vk_client.ask_user(info_about_user, user_id)
                if result == 'Ура, все поля заполнены! Идем дальше)':
                    client_pair = vk_client.check_marrage_search_pair(info_about_user, user_id)
                    send_pair_into_to_user(client_pair, user_id)

            elif theme["topic"] == "status":
                info_about_user["status"] = int(theme["our_match"])
                result = vk_client.ask_user(info_about_user, user_id)
                if result == 'Ура, все поля заполнены! Идем дальше)':
                    client_pair = vk_client.check_marrage_search_pair(info_about_user, user_id)
                    send_pair_into_to_user(client_pair, user_id)

            elif theme["topic"] == "sex":
                info_about_user["sex"] = int(theme["our_match"])
                result = vk_client.ask_user(info_about_user, user_id)
                if result == 'Ура, все поля заполнены! Идем дальше)':
                    client_pair = vk_client.check_marrage_search_pair(info_about_user, user_id)
                    send_pair_into_to_user(client_pair, user_id)

            elif theme["topic"] == "bdate":
                info_about_user["bdate"] = int(theme["our_match"])
                result = vk_client.ask_user(info_about_user, user_id)
                if result == 'Ура, все поля заполнены! Идем дальше)':
                    client_pair = vk_client.check_marrage_search_pair(info_about_user, user_id)
                    send_pair_into_to_user(client_pair, user_id)

            else:
                print('Я не понял, переформулируйте, пожалуйста')
