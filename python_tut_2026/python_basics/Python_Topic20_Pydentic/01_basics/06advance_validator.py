from pydantic import BaseModel, field_validator, ValidationError

# ===============================================================
# NOTE — advanced field_validator: many fields, transforming, modes
# ===============================================================
# 1) ONE VALIDATOR, MANY FIELDS
#    @field_validator('first_name','last_name')  -> runs once per field.
#    @field_validator('*')                       -> runs on EVERY field.
#
# 2) A VALIDATOR CAN TRANSFORM, NOT JUST CHECK
#    Whatever you `return` becomes the stored value.
#      name_must_be_capitalize -> checks, returns v unchanged
#      normalized_email        -> rewrites v to lower/stripped
#      parse_price             -> converts "$4.44" into 4.44
#
# 3) ALWAYS RETURN THE VALUE  (the #1 bug here)
#    Forget `return` and the function gives back None,
#    so the field silently becomes None. No error, just wrong data.
#
# 4) mode='before' vs mode='after' (default)
#
#    Product(price="$4.44")
#          |
#          +-- mode='before' -> runs FIRST, on the RAW input "$4.44"
#          |        parse_price strips "$" -> 4.44
#          |
#          +-- then pydantic type-checks against the annotation
#          |
#          +-- mode='after'  -> runs LAST, on the already-typed value
#
#    Rule of thumb:
#      before -> input is the WRONG TYPE and you must fix it   ("$4.44")
#      after  -> input is the RIGHT TYPE and you must judge it  (len < 4)
#
#    That is why parse_price MUST be 'before'. As 'after' it would
#    never run — the value would be rejected on type before reaching it.
#
# 5) The annotation must match what the validator RETURNS.
#    parse_price returns a float, so price is annotated `float`.
#    (Annotating it `str` contradicts the parsing — you would be
#     throwing away the number you just worked to extract.)
# ===============================================================


class Person(BaseModel):
    first_name: str
    last_name: str


    @field_validator('first_name','last_name')
    def name_must_be_capitalize(cls , v):
        if not v.istitle():
            raise ValueError("Name must be capitalized.")
        return v

class User(BaseModel):
    email: str

    @field_validator('email')
    def normalized_email(cls , v):
        return v.lower().strip()


class Product(BaseModel):
    price: float  # accepts "$4.44" and stores 4.44

    @field_validator('price', mode='before')
    def parse_price(cls,v):
        if isinstance(v, str):
            return float(v.replace("$", ""))
        return v


# ---------------------------------------------------------------
# Example 1 — Person  (one validator guarding TWO fields)
# ---------------------------------------------------------------

p1 = Person(first_name="Akshay", last_name="Chavhan")
print(p1)

# fails on first_name -> "akshay" is not title-case
try:
    Person(first_name="akshay", last_name="Chavhan")
except ValidationError as e:
    print(e)

# the SAME validator also guards last_name
try:
    Person(first_name="Akshay", last_name="chavhan")
except ValidationError as e:
    print(e)


# ---------------------------------------------------------------
# Example 2 — User  (validator that TRANSFORMS instead of rejecting)
# ---------------------------------------------------------------

# messy input is cleaned, not refused
u1 = User(email="   AKSHAY@Example.COM   ")
print(u1.email)                  # stored lower-cased and stripped

u2 = User(email="already@clean.com")
print(u2.email)


# ---------------------------------------------------------------
# Example 3 — Product  (mode='before' to fix the type first)
# ---------------------------------------------------------------

# a str goes IN, a float comes OUT
prod = Product(price="$4.44")
print(prod.price, type(prod.price).__name__)

# the isinstance guard lets a plain number pass straight through
print(Product(price=10.5).price)

# junk still fails — float("abc") raises inside the validator
try:
    Product(price="$abc")
except Exception as e:
    print(type(e).__name__, "->", e)