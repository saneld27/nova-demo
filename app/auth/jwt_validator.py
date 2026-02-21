from __future__ import annotations

import logging
from typing import Any

import httpx
from jose import JWTError, jwt

from app.config import Settings

logger = logging.getLogger(__name__)


class Auth0JWTValidator:
    """Validates Auth0-issued JWTs and enforces Revit provider claim."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._jwks: dict[str, Any] | None = None

    # ── JWKS fetching ────────────────────────────────────────────────────────

    async def _get_jwks(self) -> dict[str, Any]:
        """Fetch and lazily cache the JWKS from Auth0."""
        if self._jwks is None:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self._settings.auth0_jwks_uri, timeout=10)
                resp.raise_for_status()
                self._jwks = resp.json()
        return self._jwks

    async def _get_signing_key(self, token: str) -> str:
        """Extract the RSA public key matching the JWT's 'kid' header."""
        try:
            unverified_header = jwt.get_unverified_header(token)
        except JWTError as exc:
            raise ValueError(f"Invalid JWT header: {exc}") from exc

        kid = unverified_header.get("kid")
        jwks = await self._get_jwks()

        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return key  # python-jose accepts the JWK dict directly

        # Force-refresh once in case keys rotated
        self._jwks = None
        jwks = await self._get_jwks()
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return key

        raise ValueError(f"Unable to find signing key for kid={kid!r}")

    # ── Token validation ─────────────────────────────────────────────────────

    async def validate(self, token: str) -> dict[str, Any]:
        """
        Validate token signature, expiry, audience, issuer **and** Revit
        provider claim.  Returns the decoded claims dict on success.
        """
        signing_key = await self._get_signing_key(token)

        try:
            claims: dict[str, Any] = jwt.decode(
                token,
                signing_key,
                algorithms=self._settings.auth0_algorithms,
                audience=self._settings.auth0_audience,
                issuer=f"https://{self._settings.auth0_domain}/",
            )
        except JWTError as exc:
            raise ValueError(f"JWT validation failed: {exc}") from exc

        self._enforce_provider_claim(claims)
        logger.debug("JWT validated for sub=%s", claims.get("sub"))
        return claims

    def _enforce_provider_claim(self, claims: dict[str, Any]) -> None:
        """Reject tokens that don't carry the expected Revit provider claim."""
        if self._settings.app_env == "development":
            logger.warning(
                "Skipping provider claim check in development mode. "
                "Ensure the Auth0 Action is configured for production."
            )
            return
        key = self._settings.revit_provider_claim_key
        expected = self._settings.revit_provider_claim_value
        actual = claims.get(key)
        if actual != expected:
            raise ValueError(
                f"Provider claim mismatch: expected {expected!r}, got {actual!r}"
            )
