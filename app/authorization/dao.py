import re
from flask import flash
from werkzeug.security import check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1


class User:

    def __init__(self, id, name, email, password, account_type, second_name=None, avatar=None, person_data=None, role=False):
        self.id = id
        self.name = name
        self.second_name = second_name
        self.email = email
        self.password = password
        self.account_type = account_type
        self.avatar = avatar
        self.person_data = person_data
        self.role = role

    def login_check_password_hash(self, password_user):
        print(self.password, '-', password_user)
        if check_password_hash(self.password, password_user):
            return True
        flash('Email is incorrect. ',
              category='login_error_password')
        return False

    def registration_check_user_params(self, rpt_psw:str):
        #bool_check_name = self.registration_check_user_name()
        bool_check_email = self.registration_check_user_email()
        bool_check_pass = self.registration_check_user_pass()
        bool_check_pass_repeat = self.registration_check_user_pass_repeat(rpt_psw)
        if  bool_check_email and bool_check_pass and bool_check_pass_repeat:
            return True
        return False


    def registration_check_user_name(self):
        check_name = re.search(r'([a-zA-Z]+)', self.name)
        if len(self.name) < 3 or check_name.group(1) != self.name:
            flash('Name is incorrect. The name must consist of at least three characters and consist of Latin letters',
                  category='error_name')
            return False
        return True


    def registration_check_user_email(self):
        check_email = re.search(r'([a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+)', self.email)
        if check_email is None or check_email.group(1) != self.email:
            flash('Email is incorrect.',
                  category='error_email')
            return False
        return True


    def registration_check_user_pass(self):
        if len(self.password) < 6:
            flash('Password is incorrect. Paasword must consist of at least six characters',
                  category='error_password')
            return False
        return True


    def registration_check_user_pass_repeat(self, rpt_psw:str):
        if self.password != rpt_psw:
            flash('Passwords do not match',
                  category='error_password_rpt')
            return False
        return True


    def __repr__(self):
        return f'<User %r {self.id}>'


