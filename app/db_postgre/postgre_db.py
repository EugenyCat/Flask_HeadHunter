import psycopg2
from config import DATABASE_URL
from app.db_postgre.user_queries import *
from app.authorization.dao import User
from psycopg2.extras import RealDictCursor
import json
from flask import flash
from werkzeug.security import generate_password_hash
from datetime import date

def execute_my():
    a = PSQL()
    a.create_connection()
    a.hand_quary()


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return str(o)

        return super().encode(self.default(o))



class PSQL:

    def __init__(self):
        self.connection=None

    global personal_data_keys
    personal_data_keys = ['country', 'city', 'birthday', 'gender', 'phone_number']

    def create_connection(self):
        self.connection = psycopg2.connect(DATABASE_URL)

    def close_connection(self):
        self.connection.close()

    def get_by_email(self, value_email):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                a = cursor.execute(GET_USER_BY_EMAIL, (value_email, ))
                res = json.loads(json.dumps(cursor.fetchone(), cls=DateTimeEncoder))
                #res['gender'] = 'female' if res['gender']=='f' else 'male'
                if res:
                    personal_data = {x: res[x] for x in personal_data_keys}
                    user = User(res['id'], res['name'], res['email'], res['password'], res['account_type']
                                          , res['second_name'], res['avatar'], personal_data, res['role'])
                    flash('Email has already existed.',
                          category='error_email')
                    return user
        flash('Email hasn\'t existed.',
              category='login_error_email')
        return None


    def get_by_id(self, user_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(GET_USER_BY_ID, (user_id, ))
                res = json.loads(json.dumps(cursor.fetchone(), cls=DateTimeEncoder))
                if res:
                    res['gender'] = 'male' if res['gender'] == 'm' else 'female' if res['gender'] == 'f' else None
                    personal_data = {x: res[x] for x in personal_data_keys}
                    user = User(res['id'], res['name'], res['email'], res['password']
                                ,res['account_type'], res['second_name'], res['avatar'], personal_data, res['role'])
                    return user
        return None


    def create_table_user(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_USERS_TABLE)


    def insert_user_in_db(self, user:object):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(INSERT_USER_RETURN_ID
                               , (user.name, user.email, generate_password_hash(user.password), user.acc_type, user.role))


    def update_avatar(self, user_id, new_path:str):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(PUT_USER_AVATAR, (new_path, user_id, ))


    def update_user_personal(self, user_id, user_name, user_second_name, user_country, user_city, user_birthday, user_gender, user_phone_number):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(UPDATE_USERS_PERSONAL, (user_name,
                                                       user_second_name,
                                                       user_country,
                                                       user_city,
                                                       user_birthday,
                                                       user_gender,
                                                       user_phone_number,
                                                       user_id,
                                                       ))


    def insert_joboffer_rec(self, user_id, description, skills, title):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(INSERT_OFFERJOB, (user_id, description, skills, title, ))


    def update_joboffer_rec(self, offer_id, user_id, description, skills, title):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(UPDATE_OFFERJOB, (offer_id, user_id, description, skills, title, ))


    def delete_joboffer_rec(self, offer_id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(DELETE_OFFERJOB, (offer_id, ))


    def get_user_offers_links(self, user_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(GET_USER_LINK_OFFERS, (user_id, ))
                res = json.loads(json.dumps(cursor.fetchall()))
                return res


    def get_user_offers_info(self, offer_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(GET_USER_OFFERS_INFO, (offer_id, ))
                res = json.loads(json.dumps(cursor.fetchall()))
                return res


    def get_all_offers_info(self, acc_type=0):   #0 for resumes, 1 for jobs
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(GET_ALL_OFFERS, (acc_type,))
                res = json.loads(json.dumps(cursor.fetchall()))
                return res


    def get_user_favorites(self, user_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(GET_USER_FAVORITES, (user_id,))
                res = json.loads(json.dumps(cursor.fetchall()))
                return res


    def get_user_favorites_datail(self, user_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(GET_USER_FAVORITES_DETAIL, (user_id,))
                res = json.loads(json.dumps(cursor.fetchall()))
                return res


    def add_user_favorites(self, user_id, offer_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(INSERT_IN_USER_FAVORITE, (user_id, offer_id, ))
                res = self.get_user_favorites
                return res


    def del_user_favorites(self, user_id, offer_id):
        with self.connection:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(DELETE_FROM_USER_FAVORITE, (user_id, offer_id, ))
                res = res = self.get_user_favorites
                return res


    def hand_quary(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute(MY_QUERY)
