import json
import hashlib
import os
from dotenv import load_dotenv
from db import user


env_path = 'config1.env'
load_dotenv(dotenv_path=env_path)



async def get_headers(json_dict):

    update_values = {}

    if 'firstName' in json_dict:
        update_values['firstName'] = str(json_dict['firstName'])
    if 'lastName' in json_dict:
        update_values['lastName'] = str(json_dict['lastName'])

    hashed_json_password = hashlib.pbkdf2_hmac('sha512', bytes(json_dict['password'], 'utf-8'),
                                               bytes(os.environ.get("salt"), 'utf-8'),
                                               int(os.environ.get("iterations"))).hex()

    if 'password' in json_dict:
        update_values['password'] = str(hashed_json_password)

    if 'emailId' in json_dict:
        update_values['emailId'] = str(json_dict['emailId'])

    print("update_values ",update_values)
    user.insert_one(update_values)

    response = {"response": {"customer": json_dict}, "status": "success","message":"details inserted successfully"}
    return response