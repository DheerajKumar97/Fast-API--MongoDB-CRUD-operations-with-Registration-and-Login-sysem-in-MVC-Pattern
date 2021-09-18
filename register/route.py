import uvicorn
import json
from fastapi import FastAPI, Request, Body, Depends, Header
from starlette.responses import JSONResponse
from fastapi import APIRouter
from . import register
import validator
import logging
import sys
import traceback

register_rt = APIRouter()



@register_rt.post("/user_json")
async def register_data(json_data: Request):

    try:

        json_dict = await json_data.body()
        json_dict = json.loads(json_dict.decode('utf-8'))
        function_response = await register.get_headers(json_dict)
        headers = {"Content-Type": "application/json", "Content-Language": "en-US"}
        return JSONResponse(content=function_response, headers=headers)

    except:

        error_class = validator.get_ErrorClass(sys.exc_info())
        error_code = validator.get_ErrorCode(error_class)
        response = {"status": "error", "message": error_class}
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


# @register_auth_bp.route('/register',methods=['POST'])
# async def registeration():
#
#     try:
#         json_dict = request.get_json()
#         response_value = await register.register(json_dict)
#         response = Response(json.dumps(response_value))
#         response.mimetype = 'application/json'
#         logging.info(response_value)
#         return response
#     except:
#
#         error_class = validator.get_ErrorClass(sys.exc_info())
#         error_code = validator.get_ErrorCode(error_class)
#         response = {"status": "error", "message": error_class}
#         if error_code is not None:
#             response['error_code'] = error_code
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