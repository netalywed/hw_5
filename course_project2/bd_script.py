import sqlalchemy
import settings

engine = sqlalchemy.create_engine(settings.postgres_request)
connection = engine.connect()


def check_client_id_in_bd(client_id):
    id_client_bd_try = connection.execute(f'SELECT id FROM client WHERE id_vk_client = {client_id}').fetchone()
    print(id_client_bd_try)
    if id_client_bd_try is None:
        connection.execute(f'INSERT INTO client(id_vk_client) VALUES({client_id});') # insert client
        id_client_bd = connection.execute(f'SELECT id FROM client WHERE id_vk_client = {client_id}').fetchone()
        id_client_bd_int = id_client_bd[0]
    else:
        id_client_bd_int = id_client_bd_try[0]
    return id_client_bd_int


def is_mentioned(id_client_bd_int, candidate_id):

    candidate_bd_try = connection.execute(f'SELECT id FROM candidate WHERE id_vk_candidate = {candidate_id}').fetchone()
    print(candidate_bd_try)
    if candidate_bd_try is None:
        print("new candidate")
        connection.execute(f'INSERT INTO candidate(id_vk_candidate) VALUES({candidate_id});') # insert
        id_candidate_bd = connection.execute(f'SELECT id FROM candidate WHERE id_vk_candidate = {candidate_id}').fetchone()
        id_candidate_bd_int = id_candidate_bd[0]
    else:
        id_candidate_bd_int = candidate_bd_try[0]


    constraint_id = connection.execute(f'SELECT client_id, candidate_id FROM clientcandidate WHERE client_id = {id_client_bd_int} AND candidate_id = {id_candidate_bd_int};').fetchone()
    print(constraint_id)
    if constraint_id is None:
        connection.execute(f'INSERT INTO clientcandidate(client_id, candidate_id) VALUES({id_client_bd_int},{id_candidate_bd_int});')  # insert
        already_mentioned = False
        print(already_mentioned)
    else:
        already_mentioned = True

    return already_mentioned


# client = 11337793
# candidate = 22668807
# client_id = check_client_id_in_bd(client)
# print(is_mentioned(client_id, candidate))

