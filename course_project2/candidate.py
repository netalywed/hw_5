import json
import requests
from pprint import pprint
from bd_script import is_mentioned
import time


def filter_pairs(pairs_ids, id_client_in_bd):
    pairs = []
    print("pairs_ids", len(pairs_ids))
    print(pairs_ids)
    # for candidate in pairs:
    for i in range(0, len(pairs_ids)):
        candidate = pairs_ids[i]
        print(candidate)
        if not is_mentioned(id_client_in_bd, candidate):
            pairs.append(candidate)
    print("pairs_ids", len(pairs))
    print(pairs)
    return pairs


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


# распознает речь клиента: находит нужную тематику и значение
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


def send_pair_into_to_user(client_obj, a_client_pair, client_id, vk_token):
    for pair in a_client_pair:
        pair_id_full = 'https://vk.com/id' + str(pair)
        client_obj.bot_tells(client_id, pair_id_full)
        # ищем фотографии
        all_pair_photos = search_photos(pair, vk_token)
        print(all_pair_photos)
        if all_pair_photos[0] == "профиль закрыт":
            text = 'У этого пользователя закрытый аккаунт, поэтому я не смогу прислать фото. Но вы можете добавиться к этому человеку в друзья:)'
            client_obj.bot_tells(client_id, text)
        else:
            for i in all_pair_photos:
                text = str(i)
                client_obj.bot_tells(client_id, text)
        time.sleep(2)


def check_status_and_search_pair(info_user, client_obj, client_id, user_id_in_bd, vk_token):
    # проверяем статус пользователя (не женат ли он и т.д.)
    status = info_user["status"]
    if status == '2' or status == '3' or status == '4' or status == '7' or status == '8':
        client_obj.bot_tells(client_id,
                             'Упс, ваш статус показывает, что у вас уже есть любимый человек. К сожалению, по этическим соображениям, не мог у искать вам пару:(')
    else:
        client_pairs = client_obj.search_pair(info_user)
        # добавляем пары в бд
        filtered_pairs = filter_pairs(client_pairs, user_id_in_bd)
        print(filtered_pairs)
        if not filtered_pairs:
            client_obj.bot_tells(client_id,
                                 'По вашему запросу больше ничего не найдено. К вашему рассмотрению предлагаем уже выданные страницы')
        else:
            send_pair_into_to_user(client_obj, filtered_pairs, client_id, vk_token)
