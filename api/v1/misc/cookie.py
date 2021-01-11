from fastapi import HTTPException
from fastapi.security import OAuth2
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from starlette.requests import Request
from typing import Optional

import logging

logger = logging.getLogger()

class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):

        if not scopes:
            scopes: {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)


    async def __call__(self, request: Request) -> Optional[str]:
        
        cookie_auth: str = request.cookies.get("Authorization")
        logger.info(f"cookie_auth {cookie_auth}")
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_auth
        )

        if cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param
        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=403,
                detail="Not authenticated"
            )
        
        return param