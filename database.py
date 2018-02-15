from datetime import datetime
from pony import orm

from config import Config

db = orm.Database()


class User(db.Entity):
    """Information on user"""
    tg_id = orm.Required(str, unique=True)
    tg_first_name = orm.Required(str)
    tg_last_name = orm.Required(str)
    tg_nick_name = orm.Required(str)
    phone = orm.Optional(str)
    email = orm.Optional(str)
    real_first_name = orm.Optional(str)
    real_middle_name = orm.Optional(str)
    real_last_name = orm.Optional(str)
    real_country = orm.Optional(str)
    real_city = orm.Optional(str)
    actions = orm.Set('UserAction')


class UserAction(db.Entity):
    user = orm.Required(User)
    channel = orm.Optional(str)
    date = orm.Required(datetime)
    action = orm.Required(str)


class Database:
    def __init__(self, config: Config):
        host = config.get_db_host()
        user = config.get_db_user()
        password = config.get_db_password()
        name = config.get_db_name()
        db.bind('mysql', host=host, user=user, password=password, db=name)

        try:
            db.generate_mapping(create_tables=True)
        except:
            db.drop_all_tables(with_all_data=True)
            db.create_tables()

    @orm.db_session
    def user_exists(self, tg_id: str):
        return User.exists(tg_id=tg_id)

    @orm.db_session
    def save_user(self, tg_id: str, nick: str, name: str, last_name: str, channel: str):
        user = User(tg_id=tg_id, tg_first_name=name, tg_last_name=last_name, tg_nick_name=nick)
        UserAction(user=user, action="added", channel=channel, date=datetime.now())


