a = 250
b = 250
# print( a is b)

x= 258
y = 258
# print( x is y )

# --------------------------
def check(item , store=None):
    if(store == None):
        store = []
    store.append(item)
    return store

# print(check(1))
# print(check(2))

# --------------------------
# Names vs values (the reference model)
item1 = [ 1, 2, 3]
item2 = item1

item1.append(4)

# print(f"item1 -> {item1}")
# print(f"item2 -> {item2}")


# --------------------------

personName = "Akshay"
personAge = 29
personHeight = 6

print(f" personName -> " , type(personName))
print(f" personAge -> " , type(personAge))
print(f" personHeight -> " , type(personHeight))

# personName ->  <class 'str'>
#  personAge ->  <class 'int'>
#  personHeight ->  <class 'int'>

# --------------------------

