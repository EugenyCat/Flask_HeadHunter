def_avatar = '../../static/avatars_jpeg/default_avatar.jpg'
def_type_account = 0  #Looking for work = 0 # Employer = 1


CREATE_GENDER_DOMAIN = (
    "CREATE DOMAIN gender_type AS CHAR"
    "CHECK (value IN ('f' , 'm' ) );"
)

CREATE_USERS_TABLE = (
        "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, "
        f"password TEXT NOT NULL, role BOOLEAN default False, account_type INTEGER NOT NULL DEFAULT {def_type_account},"
        f"avatar TEXT NOT NULL DEFAULT {def_avatar}, second_name TEXT, country TEXT, city TEXT, birthday DATE, "
        "gender gender_type, phone_number TEXT)"
    )


CREATE_JOBOFFERS_TABLE = (
    "CREATE TABLE joboffers("
        "author    			    INT references users(id),"
        "id 		  			SERIAL PRIMARY KEY NOT NULL,"
        "offer_description	    CHAR(256) NOT NULL,"
        "slill_list 			DATE NOT NULL DEFAULT CURRENT_DATE ),"
        "title                  CHAR(64) NOT NULL;"
    )

CREATE_FAVORITES_TABLE = (
    "CREATE TABLE favorites("
        "id    			    SERIAL PRIMARY KEY NOT NULL,"
        "id_author 		  	INT references users(id), "
        "id_offer	        INT references joboffers(id) "
    )


GET_USER_FAVORITES = (
    "SELECT * FROM favorites where id_author = %s;"
)


GET_USER_FAVORITES_DETAIL = (
    "SELECT jo.author, u.name, u.second_name, u.account_type, u.country, u.city, u.phone_number, "
    "jo.id, jo.offer_description, jo.slill_list, jo.title "
    "FROM favorites f "
    "LEFT JOIN joboffers jo on jo.id = f.id_offer "
    "LEFT JOIN users u on u.id = f.id_author "
    "where f.id_author = %s "
)




INSERT_IN_USER_FAVORITE = (
    "INSERT INTO favorites (id_author, id_offer) VALUES (%s, %s);"
)

DELETE_FROM_USER_FAVORITE = (
    "DELETE FROM favorites WHERE id_author = %s and id_offer = %s;"
)

INSERT_USER_RETURN_ID = (
        "INSERT INTO users (name, email, password, account_type, role) VALUES (%s, %s, %s, %s, %s) RETURNING id"
    )


INSERT_OFFERJOB = (
        "INSERT INTO joboffers (author, offer_description, slill_list, title) VALUES (%s, %s, %s, %s)"
    )


UPDATE_OFFERJOB = (
    "UPDATE joboffers "
    "SET author = %s,"
    "offer_description = %s,"
    "slill_list = %s,"
    "title = %s "
    "WHERE id = %s;"
)


DELETE_OFFERJOB = (
    "DELETE FROM joboffers WHERE id = %s;"
)


GET_USER_BY_EMAIL = (
        "SELECT * FROM users WHERE email = %s"
    )


GET_USER_BY_ID = (
        "SELECT * FROM users u WHERE id = %s"
    )

GET_USER_LINK_OFFERS = (
    "SELECT jo.id, jo.title "
    "FROM joboffers jo "
    "where jo.author = %s "
)


GET_USER_OFFERS_INFO = (
    "SELECT jo.author, u.name, u.second_name, u.account_type, u.country, u.city, u.phone_number, "
    "jo.id, jo.offer_description, jo.slill_list, jo.title "
    "FROM joboffers jo "
    "LEFT JOIN users u on u.id = jo.author "
    "where jo.id = %s"
)


GET_ALL_OFFERS = (
    "SELECT u.country, u.city, "
    "jo.author, jo.id, jo.offer_description, jo.slill_list, jo.title "
    "FROM joboffers jo "
    "LEFT JOIN users u on u.id = jo.author "
    "where u.account_type = %s"
)


PUT_USER_AVATAR = (
    "UPDATE users SET avatar = %s where id = %s"
)

UPDATE_USERS_PERSONAL = (
    "UPDATE users "
    "SET name = %s,"
    "second_name = %s,"
    "country = %s,"
    "city = %s,"
    "birthday = %s,"
    "gender = %s,"
    "phone_number = %s"
    " WHERE id = %s;"
)





ADD_TYPE_ACC = (
    "INSERT INTO personal_data (id_personaldata) SELECT id FROM users WHERE id < 5;"
)



MY_QUERY = (
    "ALTER TABLE users "\
    "ALTER COLUMN gender TYPE BOOLEAN;"
)



