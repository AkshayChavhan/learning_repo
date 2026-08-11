from typing import List, Optional
from pydantic import BaseModel, ValidationError

# ===============================================================
# NOTE — self-referencing model: a model that contains ITSELF
# ===============================================================
# This is how you model a TREE: comment -> replies -> replies -> ...
# with no fixed depth.
#
#   Comment(id=1)
#     +-- Comment(id=2)
#     |     +-- Comment(id=4)      <-- same class, nested in itself
#     +-- Comment(id=3)
#
# WHY THE QUOTES around 'Comment'?
#   replies: Optional[List['Comment']] = None
#                          ^^^^^^^^^
#   At the moment this line runs, the class Comment does NOT exist yet
#   — Python is still busy building it. Writing the name bare would be
#   a NameError. Quoting it makes a FORWARD REFERENCE: "resolve this
#   name later, once the class is finished."
#
# WHY `= None` IS ESSENTIAL:
#   It gives the recursion a STOPPING POINT. A leaf comment has no
#   replies. Without a default, every comment would require replies,
#   which would require replies... forever.
#
# model_rebuild():
#   Finalises the forward reference. In pydantic v2 a plain self-reference
#   like this usually resolves on its own, so the call is often optional —
#   but it is REQUIRED when the name cannot be resolved yet, e.g. the model
#   is defined inside a function, or it points at a class defined further
#   down the file. Calling it anyway is harmless and a safe habit.
# ===============================================================


class Comment(BaseModel):
    id : int
    content: str
    replies: Optional[List['Comment']] = None


# we need to rebuild whenever we do self reference
Comment.model_rebuild()


# ---------------------------------------------------------------
# Example 1 — a leaf comment (recursion stops here)
# ---------------------------------------------------------------

leaf = Comment(id=10, content="Totally agree!")
print(leaf)
print(leaf.replies)              # None -> nothing nested below


# ---------------------------------------------------------------
# Example 2 — one level of nesting, built from OBJECTS
# ---------------------------------------------------------------

thread = Comment(
    id=1,
    content="What did you think of the movie?",
    replies=[
        Comment(id=2, content="Loved it."),
        Comment(id=3, content="Too long for me."),
    ],
)
print(thread)
print(len(thread.replies))
print(thread.replies[0].content)


# ---------------------------------------------------------------
# Example 3 — deep nesting, built from plain DICTS
# ---------------------------------------------------------------
# This is what real API/JSON input looks like. Pydantic turns every
# level into a Comment object, however deep it goes.

deep = Comment(**{
    "id": 1,
    "content": "Root comment",
    "replies": [
        {
            "id": 2,
            "content": "First reply",
            "replies": [
                {"id": 4, "content": "Reply to the reply"},
            ],
        },
        {"id": 3, "content": "Second reply"},
    ],
})

print(type(deep.replies[0].replies[0]).__name__)   # Comment, not dict
print(deep.replies[0].replies[0].content)


# ---------------------------------------------------------------
# Example 4 — walking the tree with recursion
# ---------------------------------------------------------------

def show(comment, depth=0):
    print("   " * depth + "- #{} {}".format(comment.id, comment.content))
    for reply in comment.replies or []:      # `or []` handles None leaves
        show(reply, depth + 1)

show(deep)


# ---------------------------------------------------------------
# Example 5 — the whole tree serializes in one call
# ---------------------------------------------------------------

print(deep.model_dump())


# ---------------------------------------------------------------
# Example 6 — validation reaches every level
# ---------------------------------------------------------------
# The deepest id is a bad value; the error path shows the exact route:
# replies -> 0 -> replies -> 0 -> id
try:
    Comment(**{
        "id": 1,
        "content": "Root",
        "replies": [
            {
                "id": 2,
                "content": "Child",
                "replies": [
                    {"id": "not-an-int", "content": "Grandchild"},
                ],
            },
        ],
    })
except ValidationError as e:
    print(e)

