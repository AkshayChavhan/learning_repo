from pydantic import BaseModel, ValidationError
from typing import List,Dict,Optional


class Cart(BaseModel):
    userId: str
    quantity: Dict[str,int]
    item: List[str]


class BookShelve(BaseModel):
    shelveId: str
    genre: str
    is_available: bool
    bookDetails: Dict[str,int]
    imageUrl: Optional[str] = None


# ---------------------------------------------------------------
# Example 1 — Cart
# ---------------------------------------------------------------
cart_items = { "userId" : "123d" , "quantity": { "Laptop": 12 , "charger": 21} , "item" : ["Laptop","Mobile","Charger"]}
cart = Cart(**cart_items)
print(cart)


# ---------------------------------------------------------------
# Example 2 — BookShelve   (imageUrl is Optional → can be skipped)
# ---------------------------------------------------------------
shelve_data = { "shelveId" : "SH-07" , "genre" : "sci-fi" , "is_available" : True ,
                "bookDetails" : { "Dune": 1965 , "Neuromancer": 1984 } }
shelve = BookShelve(**shelve_data)
print(shelve)
print(shelve.imageUrl)          # not passed → falls back to None

# same model, this time WITH the optional field
shelve2 = BookShelve(**shelve_data, imageUrl="https://img.io/dune.png")
print(shelve2.imageUrl)


# ---------------------------------------------------------------
# What pydantic does with wrong data
# ---------------------------------------------------------------

# a) Coercion — "12" is a str, but Dict[str,int] wants int → converted
loose = Cart(userId="U-2", quantity={"Pen": "12"}, item=["Pen"])
print(loose.quantity)

# b) Rejection — "twelve" can't become an int → raises
try:
    Cart(userId="U-3", quantity={"Pen": "twelve"}, item=["Pen"])
except ValidationError as e:
    print(e)