from pydantic import BaseModel, field_validator, model_validator, ValidationError

# ===============================================================
# NOTE — You NEVER call a validator yourself.
# ===============================================================
# @field_validator / @model_validator REGISTER the function onto the
# model when the class is created. Pydantic then calls it for you every
# time you build an instance. There is no manual call anywhere below.
#
#   User(username="ak")
#         |
#         +--> type check          -> str OK
#         +--> calls username_length("ak")     <-- automatic
#         |        +--> len < 4 -> raise ValueError
#         +--> ValueError wrapped -> ValidationError
#
#   SignUpModel(password="secret123", confirm_password="secret999")
#         |
#         +--> all fields type-checked first
#         +--> calls match_password(instance)  <-- automatic, mode='after'
#         |        +--> mismatch -> raise ValueError
#         +--> ValidationError
#
# field_validator  -> sees ONE field's value, runs per field.
#                     use for: length, format, allowed values.
# model_validator  -> sees the WHOLE model, runs once after fields pass.
#                     use for: cross-field checks (password == confirm).
#
# mode='after'  -> the arg is the MODEL INSTANCE  -> values.password
# mode='before' -> the arg is a RAW DICT          -> values["password"]
#
# Why it works this way: bad data can never get inside the object,
# because validation happens during construction, not after.
# ===============================================================


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

# triggers username_length("akshay") → 6 chars → passes
u1 = User(username="akshay")
print(u1)

# triggers username_length("ak") → 2 chars → raises
try:
    User(username="ak")
except ValidationError as e:
    print(e)


# ---------------------------------------------------------------
# Example 2 — SignUpModel  (model_validator: compares TWO fields)
# ---------------------------------------------------------------

# triggers match_password(instance) → both match → passes
s1 = SignUpModel(password="secret123", confirm_password="secret123")
print(s1)

# triggers match_password(instance) → they differ → raises
try:
    SignUpModel(password="secret123", confirm_password="secret999")
except ValidationError as e:
    print(e)