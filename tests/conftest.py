import pytest, random
from fastapi.testclient import TestClient
from tortoise import Tortoise
from tortoise.query_utils import Prefetch
from asyncio import get_event_loop

from main import get_app
from app import ic, settings as s
from app.auth import Account, Group, Perm, Option
from app.settings.db import DATABASE_MODELS, DATABASE_URL
from trades import Broker
from fixtures import insert_groups, insert_perms, insert_taxos, insert_options, insert_accounts



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


@pytest.fixture(scope='session')
def fixtures():
    async def ab():
        await insert_groups()
        await insert_perms()
        await insert_taxos()
        await insert_options()
        _, verified_email = await insert_accounts(verified=2, unverified=2)
        verified_account = await Account.get(email=verified_email).only('id', 'email')
        return verified_account
    yield ab


@pytest.fixture(scope='session')
def loop():
    yield get_event_loop()


@pytest.fixture(scope='session')
def db(fixtures):
    async def ab():
        if s.USE_TEMPDB:
            await Tortoise.init(db_url="sqlite://:memory:", modules={"models": DATABASE_MODELS})
        else:
            await Tortoise.init(db_url=DATABASE_URL, modules={'models': DATABASE_MODELS})
        await Tortoise.generate_schemas()
        await fixtures()
    yield ab
    

@pytest.fixture(scope="class")
def accounts(request, loop, db):
    async def ab():
        await db()
        request.cls.accounts = await Account.all().prefetch_related(
            # Only supports `only()` when prefetching
            Prefetch('accountoptions', queryset=Option.all().only('account_id', 'name'),
                     to_attr='options'),
            Prefetch('groups', queryset=Group.all().only('id', 'name')),
            Prefetch('perms', queryset=Perm.all().only('id', 'code')),
            Prefetch('brokers', queryset=Broker.all().only('id', 'name')),
        )
    loop.run_until_complete(ab())


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


