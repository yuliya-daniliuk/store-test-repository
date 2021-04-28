from werkzeug.security import safe_str_cmp #safe string compare
from models.user import UserModel
def authenticate(username, password):
    #gets called when a user calls /auth endpoint
    #with their username and pass
    #param username: username in str format
    #param password: un-encrypted pass in str format
    # return: a usermodel object if authenticated , or None
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user
def identity(payload):
    #gets called when user has already authenticated, and flask-JWT (token)
    #verified their authentication header is correct
    #param: payload: a dict with identity key which is the user id
    #return: a usermodel object
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)