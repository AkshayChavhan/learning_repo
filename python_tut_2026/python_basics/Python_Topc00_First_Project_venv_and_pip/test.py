import requests
import sys

response = requests.get("https://api.github.com")

print("Response :" , response.connection)
print("Response :" , response.cookies)
print("Response :" , response.encoding)
print("Response :" , response.history)
print("Status code :" , response.status_code)
print("It works!")

# pip freeze reuirements
# (.venv) l910009@l910009-Latitude-3420:~/Documents/workspace/learning_repo/python_tut_2026/python_basics/Python_Topc00_First_Project_venv_and_pip$ python test.py
# Response : <requests.adapters.HTTPAdapter object at 0x7f04069c3d90>
# Response : <RequestsCookieJar[]>
# Response : utf-8
# Response : []
# Status code : 200
# It works!



print("Hello from Python")
print("version -> ", sys.version)