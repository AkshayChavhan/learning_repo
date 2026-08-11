from pydantic import BaseModel, ValidationError

# ===============================================================
# NOTE — nested models: a model used as another model's field type
# ===============================================================
# address: Address  -> User now CONTAINS a fully validated Address.
# Pydantic validates the inner model too, all the way down.
#
#   User(id=1, name="Akshay", address={...})
#         |
#         +--> id, name checked
#         +--> address dict handed to Address
#                  +--> street, city, postal_code checked
#                  +--> becomes a real Address object
#
# TWO WAYS TO PASS THE INNER MODEL (both give the same result):
#   1. a dict     -> address={"street": "...", ...}   pydantic converts it
#   2. an object  -> address=some_address_instance
#
# KEYWORD ARGS vs DICT KEYS — do not mix them:
#   Address(street="x")          OK   bare name, no quotes
#   Address(**{"street": "x"})   OK   quotes live inside the dict
#   Address("street" = "x")      SyntaxError — a quoted string can
#                                never be a keyword argument name
#
# Errors report the FULL PATH to the bad field, e.g. "address.postal_code",
# so you can see which level failed.
#
# model_dump() flattens the whole tree into plain nested dicts.
# ===============================================================


class Address(BaseModel):
    street: str
    city: str
    postal_code: int


class User(BaseModel):
    id: int
    name: str
    address: Address

# ---------------------------------------------------------------
# Example 1 — build the inner model on its own
# ---------------------------------------------------------------

address = Address(
    street="Street address 1",
    city="Jaipur",
    postal_code=2344234
)
print(address)
print(address.city)


# ---------------------------------------------------------------
# Example 2 — nest it by passing the OBJECT
# ---------------------------------------------------------------

u1 = User(id=1, name="Akshay", address=address)
print(u1)
print(u1.address.city)           # drill down with dots


# ---------------------------------------------------------------
# Example 3 — nest it by passing a DICT (pydantic converts it)
# ---------------------------------------------------------------

u2 = User(
    id=2,
    name="Riya",
    address={
        "street": "MG Road 42",
        "city": "Pune",
        "postal_code": 411001,
    },
)
print(u2)
print(type(u2.address).__name__)   # it really is an Address, not a dict


# ---------------------------------------------------------------
# Example 4 — the whole tree serializes together
# ---------------------------------------------------------------

print(u2.model_dump())
print(u2.model_dump_json())


# ---------------------------------------------------------------
# Example 5 — errors point at the exact nested field
# ---------------------------------------------------------------

# postal_code is not a number -> error path is "address.postal_code"
try:
    User(
        id=3,
        name="Sam",
        address={"street": "X", "city": "Delhi", "postal_code": "not-a-number"},
    )
except ValidationError as e:
    print(e)

# missing a required inner field -> error path is "address.city"
try:
    User(id=4, name="Sam", address={"street": "X", "postal_code": 111})
except ValidationError as e:
    print(e)