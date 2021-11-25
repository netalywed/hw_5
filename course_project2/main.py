from class_client import TheClient
from candidate import recognition, check_status_and_search_pair
from bd_script import check_client_id_in_bd
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import settings


if __name__ == "__main__":
    vk_group = vk_api.VkApi(token=settings.token_VK_group)
    vk_session = vk_group.get_api()
    longpoll = VkLongPoll(vk_group)
    # создали пользователя
    vk_client = TheClient(settings.token_VK, vk_group)
    info_about_user = {}


    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            message = event.text.lower()
            # Получаем id пользователя
            user_id = event.user_id
            # определяем по словарю, что говорит пользователь
            theme = recognition(message)
            # проверяем пользователя в бд, при отсутствии добавляем и берем его id в бд
            user_id_in_bd = check_client_id_in_bd(user_id)

            # ниже в ifs фразы пользователя и реакция на них бота
            if 'привет' in message:
                vk_client.bot_tells(user_id, 'Привет! Начинаю подбирать для вас пару')
                # узнаем информацию о пользователе
                info_about_user = vk_client.UsersInfo(user_id)
                if info_about_user['not_full'] != 'заполнить поля':
                    check_status_and_search_pair(info_about_user, vk_client, user_id, user_id_in_bd, settings.token_VK)
                else:
                    #когда поля недозаполнены
                    vk_client.ask_user(info_about_user, user_id)

            elif theme["topic"] != '':
                topic = theme["topic"]
                info_about_user[topic] = (theme["our_match"])
                q = vk_client.ask_user(info_about_user, user_id)
                print(info_about_user)
                if q == 'Ура, все поля заполнены! Идем дальше)':
                    check_status_and_search_pair(info_about_user, vk_client, user_id, user_id_in_bd, settings.token_VK)

            else:
                vk_client.bot_tells(user_id, 'Я не понял, переформулируйте, пожалуйста')
