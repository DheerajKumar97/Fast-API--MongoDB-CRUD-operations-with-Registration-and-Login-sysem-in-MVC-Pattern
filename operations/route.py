import uvicorn
import json
from fastapi import FastAPI, Request, Body, Depends, Header
from starlette.responses import JSONResponse
from fastapi import APIRouter
from . import operations
import validator
import logging
import sys
import traceback

operation_rt = APIRouter()


@operation_rt.post("/create-product")
# @token_auth.login_required
async def create_product(json_data: Request):

    try:
        if 'token' in json_data.headers:
            header_token = json_data.headers['token']
        else:
            header_token = 'None'
        print("header_token",header_token)
        if operations.login_required(header_token) is True:
            json_dict = await json_data.body()
            json_dict = json.loads(json_dict.decode('utf-8'))
            function_response = await operations.create_products(json_dict)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=function_response, headers=headers)
            logging.info(response)
            return response
    except:

        error_class = validator.get_ErrorClass(sys.exc_info())
        error_code = validator.get_ErrorCode(error_class)
        response = {"response":{},"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.info(response)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=response, headers=headers)
            return response
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response = {'response': {"message": error_class + str(" has been occurred"),
                                     "error": json.loads(json.dumps(str(sys.exc_info()[0:2]))) + " error line = " + str(
                                         exc_tb.tb_lineno),
                                     'error_code': 'ER_UNK025'}, "status": "error"}
            logging.exception(str(traceback.TracebackException(exc_type, exc_obj, exc_tb)))
            logging.info(response)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=response, headers=headers)
            return response


@operation_rt.get("/get-product")
async def get_product(json_data: Request,Uid: str = None):

    try:

        if 'token' in json_data.headers:
            header_token = json_data.headers['token']
        else:
            header_token = 'None'
        print("header_token",header_token)
        if operations.login_required(header_token) is True:

            Uid = Uid
            print("Uid",Uid)
            function_response = await operations.get_products(Uid)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=function_response, headers=headers)
            logging.info(response)
            return response
    except:

        error_class = validator.get_ErrorClass(sys.exc_info())
        error_code = validator.get_ErrorCode(error_class)
        response = {"response":{},"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.info(response)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=response, headers=headers)
            return response
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response = {'response': {"message": error_class + str(" has been occurred"),
                                     "error": json.loads(json.dumps(str(sys.exc_info()[0:2]))) + " error line = " + str(
                                         exc_tb.tb_lineno),
                                     'error_code': 'ER_UNK025'}, "status": "error"}
            logging.exception(str(traceback.TracebackException(exc_type, exc_obj, exc_tb)))
            logging.info(response)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=response, headers=headers)
            return response


@operation_rt.post("/update-product")
async def update_product(json_data: Request,Uid: str = None):

    try:

        if 'token' in json_data.headers:
            header_token = json_data.headers['token']
        else:
            header_token = 'None'
        print("header_token",header_token)
        if operations.login_required(header_token) is True:

            json_dict = await json_data.body()
            json_dict = json.loads(json_dict.decode('utf-8'))
            Uid = Uid
            print("Uid", Uid)
            function_response = await operations.product_update(json_dict,Uid)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=function_response, headers=headers)
            logging.info(response)
            return response
    except:

        error_class = validator.get_ErrorClass(sys.exc_info())
        error_code = validator.get_ErrorCode(error_class)
        response = {"response":{},"status": "error", "message": error_class}
        if error_code is not None:
            response['error_code'] = error_code
            logging.info(response)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=response, headers=headers)
            return response
        else:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            response = {'response': {"message": error_class + str(" has been occurred"),
                                     "error": json.loads(json.dumps(str(sys.exc_info()[0:2]))) + " error line = " + str(
                                         exc_tb.tb_lineno),
                                     'error_code': 'ER_UNK025'}, "status": "error"}
            logging.exception(str(traceback.TracebackException(exc_type, exc_obj, exc_tb)))
            logging.info(response)
            headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
            response = JSONResponse(content=response, headers=headers)
            return response


# @operation_bp.route('/delete_product',methods=['POST'])
# async def delete_product():
#
#     try:
#
#         if operations.login_required() is True:
#
#             Uid = request.args.get('Uid', None)
#             response_value = await operations.product_delete(Uid)
#             response = Response(json.dumps(response_value))
#             response.mimetype = 'application/json'
#             logging.info(response_value)
#             return response
#     except:
#
#         error_class = validator.get_ErrorClass(sys.exc_info())
#         error_code = validator.get_ErrorCode(error_class)
#         response = {"response": {"status": "error", "message": error_class}}
#         if error_code is not None:
#             response["response"]['error_code'] = error_code
#             logging.info(response)
#             response = Response(json.dumps(response))
#             response.mimetype = 'application/json'
#             return response
#         else:
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             response = {'response': {"message": error_class + str(" has been occurred"),
#                                      "error": json.loads(json.dumps(str(sys.exc_info()[0:2]))) + " error line = " + str(
#                                          exc_tb.tb_lineno),
#                                      'error_code': 'ER_UNK025'}, "status": "error"}
#             logging.exception(str(traceback.TracebackException(exc_type, exc_obj, exc_tb)))
#             logging.info(response)
#             response = Response(json.dumps(response))
#             response.mimetype = 'application/json'
#             return response
