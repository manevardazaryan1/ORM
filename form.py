"""File is for form creation."""


from base import BaseModel, Field


class User(BaseModel):
    id = Field('INTEGER PRIMARY KEY AUTOINCREMENT')
    first_name = Field('VARCHAR(30)', default="")
    last_name = Field('VARCHAR(30)', default="")
    age = Field('INTEGER')
