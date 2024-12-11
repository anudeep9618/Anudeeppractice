import json
import time
import sys, os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from fastapi import Body, FastAPI, Header, Path, Response, Request, status, Query, HTTPException
from fastapi.responses import JSONResponse
from models.GetKirkeResponsePayload import GetKirkeResponsePayload
from models.GetLocationResponsePayload import GetLocationResponsePayload
from pydantic.v1 import validate_model
from models.FailureResponse import FailureResponse
from services.RequestHandlers import RequestHandlers
from vzLog import vzLog
import uvicorn
from models.AccessTokenResponsePayload import AccessTokenResponsePayload
from models.AccessTokenRequestPayload import AccessTokenRequestPayload
from models.CreateKirkeRequestPayload import CreateKirkeRequestPayload
from models.CreateKirkeResponsePayload import CreateKirkeResponsePayload

# from pydantic import BaseModel

# app = FastAPI(root_path="/mediation")
app = FastAPI()
vzLog.set_level("DEBUG")
vzLog.log_info("Kirke-wrapper Starting...")


"""
    Middleware to add custom header to each reponse. Adds server side request process time.
"""


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time * 1000.0) + " ms"
    return response


@app.get("/kirke-wrapper/")
def read_root():
    return JSONResponse(
        content={"msg": "Request Received"}, status_code=status.HTTP_200_OK
    )


"""
    TODO: move env active/passive validation to the  so all middleware reqs to passive env are rejected (need to exclude k8s liveness/readiness)
"""


@app.post("/kirke-wrapper/createKirke", response_model=CreateKirkeResponsePayload,
          responses = {
              500: {"model": FailureResponse, "description": "Internal Server Error"},
              403: {"model": FailureResponse, "description": "Forbidden Error"},
          }
          )
async def create_kirke(create_kirke_request_payload: CreateKirkeRequestPayload, authorization: str = Header(..., description="Authorization token")):
    vzLog.log_info(
        f"Received create_kirke request. payload={create_kirke_request_payload}"
    )
    try:
        # validate token
        validated = await request_handlers.handle_validate_token(authorization)
        if validated:
            # request handler
            return await request_handlers.handle_create_kirke(create_kirke_request_payload)
        else:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Access is denied" 
            )
    except HTTPException as e:
        vzLog.log_error(e.detail)
        return JSONResponse(
            content=FailureResponse(message = e.detail, status_code = e.status_code).model_dump(),
            media_type="application/json",
            status_code=e.status_code,
        )
    except Exception as e:
        vzLog.log_error("Internal Server Error")
        return JSONResponse(
            content=FailureResponse(message = "create_kirke method failed", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR).model_dump(),
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
		
		@app.get("/kirke-wrapper/getkirke/{request_id}", response_model=GetKirkeResponsePayload,
          responses = {
              500: {"model": FailureResponse, "description": "Internal Server Error"},
              403: {"model": FailureResponse, "description": "Forbidden Error"},
          }
          )
async def get_kirke(request_id: int = Path(..., description="request_id to get kirke"), authorization: str = Header(..., description="Authorization token")):
    vzLog.log_info(
        f"Received get_kirke request id for {request_id}"
    )
    try:
        # validate token
        validated = await request_handlers.handle_validate_token(authorization)
        if validated:
            # request handler
            return await request_handlers.handle_get_kirke(request_id)
        else:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Access is denied" 
            )
    except HTTPException as e:
        vzLog.log_error(e.detail)
        return JSONResponse(
            content=FailureResponse(message = e.detail, status_code = e.status_code).model_dump(),
            media_type="application/json",
            status_code=e.status_code,
        )
    except Exception as e:
        vzLog.log_error("Internal Server Error")
        return JSONResponse(
            content=FailureResponse("get_kirke method failed").model_dump(),
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@app.get("/kirke-wrapper/getlocation/", response_model=GetLocationResponsePayload,
          responses = {
              500: {"model": FailureResponse, "description": "Internal Server Error"},
              403: {"model": FailureResponse, "description": "Forbidden Error"},
          }
          )
async def get_location(    
        state: str = Query(..., description="State code (e.g., AR)"),
        city: str = Query(..., description="City name (e.g., BISCOE)"),
        country: str = Query(..., description="Country code (e.g., USA)"),
        page: int = Query(0, description="Page number"),
        # apikey: str = Header(..., description="API key"),
        authorization: str = Header(..., description="token")
    ):
    vzLog.log_info(
        f"Received get_kirke Location request for the {state, city, country, page}"
    )
    try:
         # validate token
        validated = await request_handlers.handle_validate_token(authorization)
        if validated:
            # request handler
            return await request_handlers.handle_get_location(state, city, country, page)
        else:
            raise HTTPException(
                status_code=403,
                detail="Forbidden: Access is denied" 
            )
    except HTTPException as e:
        vzLog.log_error(e.detail)
        return JSONResponse(
            content=FailureResponse(message = e.detail, status_code = e.status_code).model_dump(),
            media_type="application/json",
            status_code=e.status_code,
        )
    except Exception as e:
        vzLog.log_error("Internal Server Error")
        return JSONResponse(
            content=FailureResponse("get_kirke location method failed").model_dump(),
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@app.post("/kirke-wrapper/getaccesstoken", response_model=AccessTokenResponsePayload,
          responses = {
              500: {"model": FailureResponse, "description": "Internal Server Error"},
              401: {"model": FailureResponse, "description": "Unauthorized"},
          }
          )
async def get_access_token(access_token_request_payload: AccessTokenRequestPayload):
    vzLog.log_info(
        f"Received access_token request. payload={access_token_request_payload}"
    )
    try:
        # request handler
        return await request_handlers.handle_access_token(access_token_request_payload)
    except Exception as e:
        vzLog.log_error("Internal Server Error")
        return JSONResponse(
            content=FailureResponse(message = "access_token method failed", status_code = status.HTTP_500_INTERNAL_SERVER_ERROR).model_dump(),
            media_type="application/json",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

def init():
    global request_handlers
    vzLog.log_info(f"App init...")

    # Init services
    try:
        request_handlers = RequestHandlers()

    except Exception as e:
        vzLog.log_error(f"App init failed!!!")
        vzLog.log_error(str(e))


init()

if __name__ == "__main__":
    vzLog.log_info("Starting app...")
    uvicorn.run(app, host="0.0.0.0", port=8081)