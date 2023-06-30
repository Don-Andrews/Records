from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Recc:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.aors = data['aors']
        self.pop = data['pop']
        self.heard_on = data['heard_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None 
    
    def __repr__(self) -> str:
        return f"REC  Repr Method {self.id}, {self.title}, {self.artist}, {self.user}"

    @classmethod
    def create_recc(cls, data):
        query = "INSERT INTO reccs (title, artist, aors, pop, heard_on, created_at, updated_at, user_id) \
            VALUES (%(title)s, %(aname)s, %(aors)s, %(pop)s, %(hon)s, NOW(), NOW(), %(uid)s);"
        result = connectToMySQL('project_schema').query_db(query, data)
        return result
    
    @classmethod
    def delete_recc(cls, data):
        query = "DELETE FROM reccs WHERE id=%(id)s;"
        result = connectToMySQL('project_schema').query_db(query, data)
        return result

    @classmethod
    def update_recc(cls, data):
        query = "UPDATE reccs \
                Set title=%(title)s, artist=%(aname)s, aors=%(aors)s, pop=%(pop)s, heard_on=%(hon)s, updated_at=NOW() \
                WHERE id=%(u_id)s;"
        result = connectToMySQL('project_schema').query_db(query, data)
        return result
    
    @classmethod
    def select_one(cls, recc_id):
        query = "SELECT * FROM reccs \
            WHERE id=%(id)s;"
        data = {"id": recc_id}
        result = connectToMySQL('project_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def select_allReccs_Users(cls):
        query = "SELECT * FROM reccs \
        JOIN users ON reccs.user_id = users.id"
        results = connectToMySQL('project_schema').query_db(query)
        reccsNusers = []
        for row in results:
            recc_obj = cls(row)
            user_dict = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "user_name": row["user_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            user_obj = User(user_dict)
            recc_obj.user = user_obj
            reccsNusers.append(recc_obj)
            print(reccsNusers)
        return reccsNusers
    
    @classmethod
    def select_allReccs_userid(cls, data):
        print("DATA DICtionary  in REC---> ", data)
        query = "SELECT * FROM reccs \
        JOIN users ON reccs.user_id = users.id \
            WHERE users.id = %(id)s;"
        results = connectToMySQL('project_schema').query_db(query, data)
        print(results)
        reccsNusers = []
        for row in results:
            recc_obj = cls(row)
            user_dict = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "user_name": row["user_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            user_obj = User(user_dict)
            recc_obj.user = user_obj
            reccsNusers.append(recc_obj)
            print('REC USERS ************', reccsNusers)
        return reccsNusers

    @staticmethod
    def validate_recc(data):
        is_valid = True
        if len(data['title']) == 0:
            flash("Title cannot be blank!", "recc1")
            is_valid = False
        if len(data['artist']) == 0:
            flash("Artist cannot be blank!", "recc2")
            is_valid = False
        if "aors" not in data:
            flash("Please Pick Either Album or Song!", "recc3")
            is_valid = False
        if "pop" not in data:
            flash("Please Pick Either Public or Private!", "recc4")
            is_valid = False
        if data["heard_on"] == "x":
            flash("Please Make A Selection!", "recc5")
            is_valid = False
        return is_valid