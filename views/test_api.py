from fastapi import Depends
from headers import PreLoginHeader
from api_response_data import api_response_data


def hello_world(item: str, header=Depends(PreLoginHeader)):
    return api_response_data(
        "success",
        {
            "headers": {
                "Authorization": header.Authorization_Code,
                # "Access_Token": header.Access_Token
            },
            "item": item
        }
    )


def test_api():
    return {"result": "Test API"}
