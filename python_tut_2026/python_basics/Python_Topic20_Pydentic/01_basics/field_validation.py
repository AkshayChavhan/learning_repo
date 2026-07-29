from pydantic import BaseModel, field_validator, model_validator, ValidationError


class User(BaseModel):
    username: str


    @field_validator("username")
    def username_length(cls,v):
        if len(v) < 4:
            raise ValueError("Username must be of 4 characters")
        return v


class SignUpModel(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def match_password(cls, values):
        if values.password != values.confirm_password:
            raise ValueError("Password does not match.")
        return values


# ---------------------------------------------------------------
# Example 1 — User  (field_validator: checks ONE field)
# ---------------------------------------------------------------

# passes → "akshay" is 6 chars
u1 = User(username="akshay")
print(u1)

# fails → "ak" is only 2 chars
try:
    User(username="ak")
except ValidationError as e:
    print(e)


# ---------------------------------------------------------------
# Example 2 — SignUpModel  (model_validator: compares TWO fields)
# ---------------------------------------------------------------

# passes → both match
s1 = SignUpModel(password="secret123", confirm_password="secret123")
print(s1)

# fails → they differ
try:
    SignUpModel(password="secret123", confirm_password="secret999")
except ValidationError as e:
    print(e)