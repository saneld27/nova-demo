from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.jwt_validator import Auth0JWTValidator
from app.config import Settings, get_settings
from app.models.schemas import TokenClaims

_bearer_scheme = HTTPBearer(auto_error=True)


def get_validator(settings: Annotated[Settings, Depends(get_settings)]) -> Auth0JWTValidator:
    return Auth0JWTValidator(settings)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer_scheme)],
    validator: Annotated[Auth0JWTValidator, Depends(get_validator)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TokenClaims:
    """FastAPI dependency – validates the Bearer JWT and returns typed claims."""
    try:
        claims = await validator.validate(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return TokenClaims(
        sub=claims["sub"],
        email=claims.get("email"),
        provider=claims.get(settings.revit_provider_claim_key, ""),
        raw=claims,
    )


# Convenience alias for route signatures
CurrentUser = Annotated[TokenClaims, Depends(get_current_user)]
