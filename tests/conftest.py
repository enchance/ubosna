import pytest, random
from fastapi.testclient import TestClient
from tortoise import Tortoise

from main import get_app
from app.settings.db import DATABASE_MODELS



TEMP_PASSWD = 'pass123'


@pytest.fixture
def passwd():
    return TEMP_PASSWD


@pytest.fixture
def random_word():
    """For linux only"""
    with open('/usr/share/dict/cracklib-small', 'r') as w:
        words = w.read().splitlines()
    return random.choice(words)


@pytest.fixture
def random_int(minimum: int = 0, maximum: int = 120):
    return random.randint(minimum, maximum)


@pytest.fixture
def random_email(random_word):
    host = random.choice(['gmail', 'yahoo', 'amazon', 'yahoo', 'microsoft', 'google'])
    tld = random.choice(['org', 'com', 'net', 'io', 'com.ph', 'co.uk'])
    return f'{random_word}@{host}.{tld}'


@pytest.fixture
def client():
    with TestClient(get_app()) as tc:
        yield tc


# @pytest.fixture
# def fixtures():
#     async def ab():
#         await init()
#         await create_options()
#         user = await create_users()
#         await create_taxo()
#         return user
#
#     yield ab

# @pytest.fixture
# def trades_fx():
#     async def ab():
#         await trades_init()
#
#     yield ab

# @pytest.fixture
# def tempdb(fixtures):
#     async def tempdb():
#         await Tortoise.init(db_url="sqlite://:memory:", modules={"models": DATABASE_MODELS})
#         await Tortoise.generate_schemas()
#         return await fixtures()
#     yield tempdb

# @pytest.fixture
# def loop(client):
#     yield client.task.get_loop()

# @pytest.fixture
# def auth_headers_tempdb(tempdb, loop):
#     """Headers for the VERIFIED_USER_EMAIL user. Same user all the time just diff id."""
#
#     async def ab():
#         return await tempdb()
#
#     user = loop.run_until_complete(ab())
#     # ic(type(user), user)
#
#     token_data = {
#         "user_id": str(user.id),
#         "email": user.email,
#         "aud": jwtauth.token_audience,
#     }
#     access_token = generate_jwt(
#         data=token_data,
#         secret=s.SECRET_KEY,
#         lifetime_seconds=s.ACCESS_TOKEN_EXPIRE,
#     )
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#     yield headers, user, access_token

# @pytest.fixture
# def loop(client):
#     yield client.task.get_loop()


# def generate_verification_token(usermod: UserDB):
#     token_data = {
#         "user_id": str(usermod.id),
#         "email": usermod.email,
#         "aud": VERIFY_USER_TOKEN_AUDIENCE,
#     }
#     return generate_jwt(
#         data=token_data,
#         secret=s.SECRET_KEY_EMAIL,
#         lifetime_seconds=s.VERIFY_EMAIL_TTL,
#     )