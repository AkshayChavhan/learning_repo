from pydantic import BaseModel, ValidationError
from typing import Optional ,List ,Union

# ===============================================================
# NOTE — three nesting patterns in one file
# ===============================================================
#
# 1) OPTIONAL NESTED MODELS      Employee -> Company? -> Address?
#    Each level may be None, so the CHAIN may break at any point:
#
#        emp.company.address.city      <-- AttributeError if company is None
#
#    None has no `.address`. Guard before you drill:
#        if emp.company and emp.company.address: ...
#    Optional means "may be absent", NOT "safe to dot through".
#
# 2) MIXED TYPES with Union       sections: List[Union[Text, Image]]
#    A list whose items can be EITHER model. Pydantic tries each type
#    and keeps the one that validates.
#
#      {"type":"text","content":"hi"}  -> TextContent  (ImageContent
#                                         fails: no url/alt_text)
#      {"type":"Image","url":..., "alt_text":...} -> ImageContent
#
#    PITFALL: this works only because the two shapes cannot both match.
#    If a dict could satisfy BOTH, pydantic picks by its own heuristics
#    and you may silently get the wrong class. The robust fix is a
#    DISCRIMINATED UNION — mark the tag field with Literal and tell
#    pydantic which field decides:
#
#        type: Literal['text']                     # in TextContent
#        type: Literal['image']                    # in ImageContent
#        sections: List[Union[TextContent, ImageContent]] = Field(
#            ..., discriminator='type')
#
#    That reads the tag ONCE instead of trying every option, and the
#    error message names the real problem instead of dumping every
#    failed attempt. (`type: str` cannot be a discriminator — it must
#    be a Literal.)
#
# 3) DEEP NESTING     Organization -> Addreess -> City -> State -> Country
#    Validation and serialization recurse the whole way down. One
#    model_dump() flattens all five levels into nested dicts.
#
# MUTABLE DEFAULT — `branch: List[Addreess] = []`
#    In ordinary Python `def f(x=[])` is the classic bug: every call
#    SHARES one list. Pydantic does NOT have this bug — it deep-copies
#    the default for each instance, so two Organizations never share a
#    branch list. (Example 6 proves it.)
#    Still, `Field(default_factory=list)` is the conventional spelling
#    and makes the intent obvious to readers.
# ===============================================================


# Optional Nested Models
class Address(BaseModel):
    street: str
    city: str
    postal_code: int

class Company(BaseModel):
    name: str
    address: Optional[Address] = None

class Employee(BaseModel):
    name: str
    company: Optional[Company] = None


# -----------------------------------------------

# Mixed data types
class TextContent(BaseModel):
    type: str = 'text'
    content: str

class ImageContent(BaseModel):
    type: str = 'Image'
    url: str
    alt_text: str

class Article(BaseModel):
    title: str
    sections: List[Union[TextContent,ImageContent]]

# DEEPLY NESTED STRUCTURE
class Country(BaseModel):
    code: str
    name: str

class State(BaseModel):
    state_id: str
    name: str
    country: Country

class City(BaseModel):
    city_id: str
    name: str
    state: State

class Addreess(BaseModel):
    street: str
    city: City
    postal_code: int

class Organization(BaseModel):
    name: str
    headquaters: Addreess
    branch: List[Addreess]=[]


# ===============================================================
# EXAMPLES — 1. Optional nested models
# ===============================================================

# Example 1 — every optional level omitted
e1 = Employee(name="Akshay")
print(e1)
print(e1.company)                      # None

# Example 2 — company present, but its address is not
e2 = Employee(name="Riya", company={"name": "RT Ledgers"})
print(e2)
print(e2.company.name)
print(e2.company.address)              # None

# Example 3 — the full chain filled in
e3 = Employee(
    name="Sam",
    company={
        "name": "RT Ledgers",
        "address": {"street": "MG Road 42", "city": "Pune", "postal_code": 411001},
    },
)
print(e3.company.address.city)

# the trap: dotting through a None blows up
try:
    print(e1.company.address.city)     # e1.company is None
except AttributeError as e:
    print("AttributeError ->", e)

# the safe way
for emp in (e1, e2, e3):
    if emp.company and emp.company.address:
        print(emp.name, "->", emp.company.address.city)
    else:
        print(emp.name, "-> no address on file")


# ===============================================================
# EXAMPLES — 2. Mixed types with Union
# ===============================================================

# Example 4 — pydantic picks the matching class per list item
article = Article(
    title="Trip to Jaipur",
    sections=[
        {"type": "text", "content": "We left early in the morning."},
        {"type": "Image", "url": "https://img.io/fort.png", "alt_text": "Amber Fort"},
        {"type": "text", "content": "The fort was the highlight."},
    ],
)

for s in article.sections:
    print(type(s).__name__, "->", s)

# a section matching NEITHER shape is rejected;
# the error lists what each Union option complained about
try:
    Article(title="Broken", sections=[{"type": "video", "src": "clip.mp4"}])
except ValidationError as e:
    print(e)


# ===============================================================
# EXAMPLES — 3. Deeply nested structure
# ===============================================================

# Example 5 — five levels, built from one nested dict
org = Organization(**{
    "name": "RT Ledgers",
    "headquaters": {
        "street": "MG Road 42",
        "postal_code": 411001,
        "city": {
            "city_id": "C-01",
            "name": "Pune",
            "state": {
                "state_id": "S-27",
                "name": "Maharashtra",
                "country": {"code": "IN", "name": "India"},
            },
        },
    },
})

# drill all the way down
print(org.headquaters.city.state.country.name)
print(org.branch)                      # [] -> no branches yet

# one call serializes all five levels
print(org.model_dump())

# Example 6 — the mutable default is NOT shared between instances
org2 = Organization(name="Second Co", headquaters=org.headquaters)
org.branch.append(org.headquaters)
print(len(org.branch), len(org2.branch))   # 1 and 0 -> separate lists

# Example 7 — a bad value deep in the tree names its full path
# error path: headquaters -> city -> state -> country -> code
try:
    Organization(**{
        "name": "Broken Co",
        "headquaters": {
            "street": "X",
            "postal_code": 1,
            "city": {
                "city_id": "C-02",
                "name": "Delhi",
                "state": {
                    "state_id": "S-07",
                    "name": "Delhi",
                    "country": {"name": "India"},    # 'code' is missing
                },
            },
        },
    })
except ValidationError as e:
    print(e)
