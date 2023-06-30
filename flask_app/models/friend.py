from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Friend:
    STATUS_ACCEPTED = "accept"
    STATUS_PENDING = "pending"
    STATUS_REJECTED = "deny"
    
    def __init__(self, data):
        self.id = data['id']
        self.friend_id = data['friend_id']
        self.user_id = data['user_id']
        self.friend_status = data['friend_status']
        self.sender = None
        self.reciever = None

    @classmethod
    def create_friend(cls, data):
        query ="""
            INSERT INTO friends (friend_id, user_id, friend_status)
            VALUES (%(friend_id)s, %(user_id)s, %(friend_status)s); 
            """
        data['friend_status'] = Friend.STATUS_PENDING
        result = connectToMySQL('project_schema').query_db(query, data)
        return result
    
    @classmethod
    def accept_friend(cls, data):
        query = """
            UPDATE friends SET friend_status=%(fstats)s 
            WHERE user_id=%(sendid)s AND friend_id=%(recid)s;
        """
        data['fstats'] = Friend.STATUS_ACCEPTED
        result = connectToMySQL('project_schema').query_db(query, data)
        return result

    @classmethod
    def delete_as_sender(cls, data):
        query = """ 
            DELETE FROM friends WHERE friends.user_id = %(sendid)s AND friends.friend_id=%(recid)s;
        """
        result = connectToMySQL('project_schema').query_db(query, data)
        return result
    
    @classmethod
    def delete_as_reciever(cls, data):
        query = """ 
            DELETE FROM friends WHERE friends.user_id = %(recid)s AND friends.friend_id=%(sendid)s;
        """
        result = connectToMySQL('project_schema').query_db(query, data)
        return result

    @classmethod
    def selectPending_withSender(cls, data):
        query = """SELECT * FROM friends
            JOIN users ON friends.user_id = users.id
            JOIN users AS frienduser ON friends.friend_id = frienduser.id
            WHERE friend_status='pending' AND users.id=%(id)s;
        """
        results = connectToMySQL('project_schema').query_db(query ,data)
        friends = []
        for row in results:
            friend = cls(row)
            user_dict = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "user_name": row["user_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            friends_dict = {
                "id": row["frienduser.id"],
                "first_name": row["frienduser.first_name"],
                "last_name": row["frienduser.last_name"],
                "user_name": row["frienduser.user_name"],
                "email": row["frienduser.email"],
                "password": row["frienduser.password"],
                "created_at": row["frienduser.created_at"],
                "updated_at": row["frienduser.updated_at"]
            }
            user_obj = User(user_dict)
            friend_obj = User(friends_dict)
            friend.sender = user_obj
            friend.reciever = friend_obj
            friends.append(friend)
        return friends
    
    @classmethod
    def selectPending_withReciever(cls, data):
        query = """SELECT * FROM friends
            JOIN users ON friends.user_id = users.id
            JOIN users AS frienduser ON friends.friend_id = frienduser.id
            WHERE friend_status='pending' AND frienduser.id=%(id)s;
        """
        results = connectToMySQL('project_schema').query_db(query ,data)
        friends = []
        for row in results:
            friend = cls(row)
            user_dict = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "user_name": row["user_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            friends_dict = {
                "id": row["frienduser.id"],
                "first_name": row["frienduser.first_name"],
                "last_name": row["frienduser.last_name"],
                "user_name": row["frienduser.user_name"],
                "email": row["frienduser.email"],
                "password": row["frienduser.password"],
                "created_at": row["frienduser.created_at"],
                "updated_at": row["frienduser.updated_at"]
            }
            user_obj = User(user_dict)
            friend_obj = User(friends_dict)
            friend.sender = user_obj
            friend.reciever = friend_obj
            friends.append(friend)
        return friends
    
    @classmethod
    def select_if_friends(cls, data):
        query = """
            SELECT * FROM friends
            JOIN users ON friends.user_id = users.id
            JOIN users AS frienduser ON friends.friend_id = frienduser.id
            WHERE users.id=%(id)s AND frienduser.id=%(fu_id)s;
        """
        result = connectToMySQL('project_schema').query_db(query, data)
        if len(result) < 1:
            return False
        friend = cls(result[0])
        return friend

    @classmethod
    def select_if_friendr(cls, data):
        query = """
            SELECT * FROM friends
            JOIN users ON friends.user_id = users.id
            JOIN users AS frienduser ON friends.friend_id = frienduser.id
            WHERE users.id=%(fu_id)s AND frienduser.id=%(id)s;
        """
        result = connectToMySQL('project_schema').query_db(query, data)
        if len(result) < 1:
            return False
        friend = cls(result[0])
        user_dict = {
                "id": result[0]["users.id"],
                "first_name": result[0]["first_name"],
                "last_name": result[0]["last_name"],
                "user_name": result[0]["user_name"],
                "email": result[0]["email"],
                "password": result[0]["password"],
                "created_at": result[0]["created_at"],
                "updated_at": result[0]["updated_at"]
            }
        friends_dict = {
                "id": result[0]["frienduser.id"],
                "first_name": result[0]["frienduser.first_name"],
                "last_name": result[0]["frienduser.last_name"],
                "user_name": result[0]["frienduser.user_name"],
                "email": result[0]["frienduser.email"],
                "password": result[0]["frienduser.password"],
                "created_at": result[0]["frienduser.created_at"],
                "updated_at": result[0]["frienduser.updated_at"]
            }
        friend.sender = User(user_dict)
        friend.reciever = User(friends_dict)
        return friend
    
    @classmethod
    def select_UserFriends(cls, data):
        query = """SELECT * FROM friends
            JOIN users ON friends.user_id = users.id
            JOIN users AS frienduser ON friends.friend_id = frienduser.id
            WHERE friend_status='accept' AND (frienduser.id=%(id)s OR users.id=%(id)s);
        """
        results = connectToMySQL('project_schema').query_db(query ,data)
        friends = []
        for row in results:
            friend = cls(row)
            user_dict = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "user_name": row["user_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            friends_dict = {
                "id": row["frienduser.id"],
                "first_name": row["frienduser.first_name"],
                "last_name": row["frienduser.last_name"],
                "user_name": row["frienduser.user_name"],
                "email": row["frienduser.email"],
                "password": row["frienduser.password"],
                "created_at": row["frienduser.created_at"],
                "updated_at": row["frienduser.updated_at"]
            }
            user_obj = User(user_dict)
            friend_obj = User(friends_dict)
            friend.sender = user_obj
            friend.reciever = friend_obj
            friends.append(friend)
        return friends