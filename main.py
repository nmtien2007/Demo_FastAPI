from fastapi import FastAPI, status
# from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from views import login_api, application_api, user_api
from views import test_api
import schemas
import models
from database import engines
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
import uvicorn


# models.Base.metadata.create_all(bind=engine)
for engine in ["master", "slave"]:
    models.DefaultBase.metadata.create_all(engines[engine])

origins = [
    "http://localhost:8001",
]

app = FastAPI(
    debug=True,
    title="Demo FastApi"
)

# Mount Static folder
app.mount("/Demo_FastApi/static" , StaticFiles(directory="static"), name="static")

# Add middleware for CORS Header
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:8001", "localhost:8001", "127.0.0.1:8001", "file:///home/nmtien/Desktop"],
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["Authorization-Code", "Access-Token", "Client-Id"],
)

# app.add_api_route(
#     path="/hello_world/{item}",
#     endpoint=test_api.hello_world,
#     methods=["GET"],
# )
#
# app.add_api_route(
#     path="/test_api",
#     endpoint=test_api.test_api,
#     methods=["GET"],
# )

app.add_api_route(
    path="/authorization",
    endpoint=login_api.authorization,
    methods=["GET"],
    summary="Authorization Func",
    response_class=HTMLResponse
)

app.add_api_route(
    path="/verify_auth_code",
    endpoint=login_api.verify_authorization_code,
    methods=["POST"],
    summary="Verify Authorization Code Func",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/register_application",
    endpoint=application_api.register_application,
    methods=["POST"],
    summary="Register Application Func",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/update_application",
    endpoint=application_api.update_application,
    methods=["POST"],
    summary="Update Application",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/login",
    endpoint=login_api.login,
    methods=["POST"],
    summary="Login Func",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/login_sso",
    endpoint=login_api.login_sso,
    methods=["POST"],
    summary="Login SSO",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/logout",
    endpoint=login_api.logout,
    methods=["POST"],
    summary="Logout Func",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/create_user",
    endpoint=user_api.create_user,
    methods=["POST"],
    summary="Create User Func",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/get_user_ids",
    endpoint=user_api.get_user_ids,
    methods=["POST"],
    summary="Get User Ids Func",
    response_model=schemas.ResponseSchema
)

app.add_api_route(
    path="/get_user_infos",
    endpoint=user_api.get_user_infos,
    methods=["POST"],
    summary="Get User Infos Func",
    response_model=schemas.ResponseSchema
)

# Handle validate form schema
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    from fastapi.responses import JSONResponse
    from fastapi.encoders import jsonable_encoder

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"error": "error_params", "detail": str(exc)})
    )


#
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Custom Title Demo FastApi",
#         version="1.0.0",
#         description="This is a very custom OpenAPI schema",
#         routes=app.routes,
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema
#
#
# app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8001)

    # using reload
    # uvicorn.run("main:app", host="localhost", port=8001, reload=True)
