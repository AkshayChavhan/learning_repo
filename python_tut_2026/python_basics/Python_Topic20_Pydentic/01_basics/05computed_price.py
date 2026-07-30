from pydantic import BaseModel, Field, computed_field, ValidationError

# ===============================================================
# NOTE — computed_field = a field you DERIVE, not one you pass in.
# ===============================================================
# Normal field  -> comes from the INPUT data.        price, quantity
# Computed field-> calculated FROM other fields.     total_price
#
# You never pass total_price in. Pydantic runs the property for you
# whenever you read it, so it can never go stale or disagree with
# price/quantity. One source of truth.
#
#   Product(price=100, quantity=3)
#         |
#         +--> price=100, quantity=3 stored
#         +--> read .total_price -> runs the property -> 300
#         +--> model_dump() -> includes total_price too
#
# DECORATOR ORDER MATTERS (this is the #1 mistake):
#
#       @computed_field      <-- must be on TOP
#       @property            <-- must be UNDERNEATH
#       def total_price(self) -> float:
#
#   Flip them and it breaks. Read it as: "make a computed_field
#   out of this property".
#
# Plain @property vs @computed_field:
#
#   @property        -> works in Python, but INVISIBLE to
#                       model_dump() / model_dump_json() / API output
#   @computed_field  -> shows up in the serialized output
#
#   So: use @computed_field when the value must reach your JSON/API.
#
# Read-only: computed fields have no setter. You cannot assign to them.
#
# The return type hint (-> float) is REQUIRED — pydantic uses it to
# build the output schema.
#
# Field(..., ge=1) on nights:
#   ...   -> required, no default
#   ge=1  -> "greater than or equal to 1", so nights=0 is rejected
#            (siblings: gt, le, lt, min_length, max_length)
# ===============================================================


class Product(BaseModel):
    price: int
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity


class Booking(BaseModel):
    user_id: int
    room_id: int
    nights: int = Field(... , ge=1)
    rate_per_night: float

    @computed_field
    @property
    def total_amount(self) -> float:
        return self.rate_per_night * self.nights


# ---------------------------------------------------------------
# Example 1 — Product
# ---------------------------------------------------------------

# only price + quantity are passed; total_price is NOT an input
p1 = Product(price=100, quantity=3)
print(p1)
print(p1.total_price)               # property runs on read -> 300

# this is the payoff: the computed value lands in the dict / JSON
print(p1.model_dump())
print(p1.model_dump_json())

# it stays in sync — change an input, the total follows
p1.quantity = 5
print(p1.total_price)

# read-only: there is no setter, so assigning to it fails
try:
    p1.total_price = 9999
except Exception as e:
    print(type(e).__name__, "->", e)


# ---------------------------------------------------------------
# Example 2 — Booking  (adds Field(..., ge=1) validation)
# ---------------------------------------------------------------

b1 = Booking(user_id=1, room_id=305, nights=4, rate_per_night=2500.0)
print(b1)
print(b1.total_amount)              # 4 * 2500.0
print(b1.model_dump())

# nights=0 breaks the ge=1 rule -> rejected before any computing happens
try:
    Booking(user_id=1, room_id=305, nights=0, rate_per_night=2500.0)
except ValidationError as e:
    print(e)