from fastapi import Header
from dataclasses import dataclass


@dataclass()
class PreLoginHeader:
    Authorization_Code: str = Header(None, title="Authorization_Code")
    Client_Id: str = Header(None, title="Client Id")

@dataclass()
class LoginHeader(PreLoginHeader):
    Access_Token: str = Header(None, title="Access_Token")
