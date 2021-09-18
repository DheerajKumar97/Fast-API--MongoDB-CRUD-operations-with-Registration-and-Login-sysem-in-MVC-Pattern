import uvicorn
import json
from fastapi import FastAPI, Request, Body, Depends, Header
from starlette.responses import JSONResponse
from fastapi import APIRouter
from . import auth
import validator
import logging
import sys
import traceback

login_rt = APIRouter()


@login_rt.post("/login_json")
async def login_data(json_data: Request):
    try:

        json_dict = await json_data.body()
        json_dict = json.loads(json_dict.decode('utf-8'))
        function_response = await auth.login_func(json_dict['emailId'], json_dict['password'],
                                                  json_data.headers['user-agent'])
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
