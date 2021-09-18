import json
import hashlib
import os
import validator
import string
import random
from bson import ObjectId
from dotenv import load_dotenv
from db import user,user_session,products
from random import randint
from fastapi import Request

env_path = 'config1.env'
load_dotenv(dotenv_path=env_path)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


async def create_products(json_dict):
    update_values = {'productUid': str(int(await random_Card_uid(8), 16))}

    if 'productType' in json_dict['body']:
        update_values['productType'] = str(json_dict['body']['productType'])

    if 'productName' in json_dict['body']:
        update_values['productName'] = str(json_dict['body']['productName'])

    if 'productStatus' in json_dict['body']:
        update_values['productStatus'] = str(json_dict['body']['productStatus'])

    print("update_values", update_values)

    products.insert_one(update_values)

    fetched_records = products.find({"productUid": update_values['productUid']})
    records = [record for record in fetched_records]
    print(records)

    # print("Login Required", login_required())
    if not records == []:
        if records[0]['productUid'] == update_values['productUid']:
            response = {"resopnse": {"template_name": json_dict['template_name'], "subject": json_dict['subject'],
                                     "product": eval(str(JSONEncoder().encode(update_values)))}, "status": "success",
                        "message": "product created successfully"}
            return response
        else:
            response = {"resopnse": {}, "status": "failed",
                        "message": "product creation failed"}
            return response


async def get_products(Uid):
    if Uid is None:
        print("if block")
        fetched_records = products.find({})
    else:
        print("Uid", Uid)
        fetched_records = products.find({"productUid": Uid})
    records = []
    for record in fetched_records:
        records.append(record)
    print("records", records)
    response = {"resopnse": {"product": eval(str(JSONEncoder().encode(records)))}, "status": "success",
                "message": "product retrived successfully",
                "total_products": len(eval(str(JSONEncoder().encode(records))))}
    return response


async def product_update(json_dict, Uid):
    update_values = {'productUid': Uid}

    if 'productType' in json_dict['body']:
        update_values['productType'] = str(json_dict['body']['productType'])

    if 'productName' in json_dict['body']:
        update_values['productName'] = str(json_dict['body']['productName'])

    if 'productStatus' in json_dict['body']:
        update_values['productStatus'] = str(json_dict['body']['productStatus'])

    print("update_values", update_values)

    products.update({"productUid": str(update_values['productUid'])}, {"$set": update_values})
    response = {"response": {"template_name": json_dict['template_name'], "subject": json_dict['subject'],
                             "product": eval(str(JSONEncoder().encode(update_values)))}, "status": "success",
                "message": "record successfully updated"}
    return response


async def product_delete(Uid):
    update_values = {'productUid': Uid}

    print("update_values", update_values)

    products.remove({"productUid": update_values['productUid']})
    response = {"response": {"product": eval(str(JSONEncoder().encode(update_values)))}, "status": "success",
                "message": "record successfully deleted"}
    return response


async def random_Card_uid(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    dec_val = randint(range_start, range_end)
    if len(hex(dec_val)) > 8:
        return hex(dec_val)[2:8]


def login_required(header_token):
    # header_token = json_token.headers['token']
    print("header_token",header_token)
    token_record = user_session.find({})
    records = [record for record in token_record]
    print(records)

    token_list = []
    for token in records:
        token_list.append(token['token'])
    if header_token in token_list:
        return True
    else:
        raise validator.InvalidToken()
