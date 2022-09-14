
from ninja import Schema


class RegisterIn(Schema):
    username: str
    password: str
    confirm_password: str



class LoiginIn(Schema):
    username: str
    password: str

