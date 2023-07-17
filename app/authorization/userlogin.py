

class UserLogin():
    def fromDB(self, user_id, con_psql):
        try:
            self.__user = con_psql.get_by_id(user_id)
        except Exception as e:
            print("Error PostgreSQL " + str(e))
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.__user.id

    def get_account_type(self):
        return self.__user.account_type

    def get_name(self):
        return str(self.__user.name)

    def get_second_name(self):
        return self.__user.second_name

    def get_avatar(self):
        return str(self.__user.avatar)

    def get_person_data(self):
        return self.__user.person_data

