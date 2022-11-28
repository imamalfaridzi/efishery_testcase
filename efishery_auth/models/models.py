# Copyright 2021 ACSONE SA/NV
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from functools import partial

import jwt  # pylint: disable=missing-manifest-dependency
from jwt import PyJWKClient
from werkzeug.exceptions import InternalServerError

from odoo import _, api, fields, models, tools
from odoo.exceptions import ValidationError

from ..exceptions import (
    AmbiguousJwtValidator,
    JwtValidatorNotFound,
    UnauthorizedInvalidToken,
    UnauthorizedPartnerNotFound,
)

_logger = logging.getLogger(__name__)


class AuthJwtValidator(models.Model):
    _name = "auth.jwt.validator"
    _description = "JWT Validator Configuration"

    email = fields.Char(
        required=True
    )
    secret_key = fields.Char(
        required=True
    )

    @api.model
    def _get_validator(self):
        domain = []
        validator = self.search(domain, limit=1)
        if not validator:
            _logger.error("JWT validator not found for name %r", validator_name)
            raise JwtValidatorNotFound()
        if len(validator) != 1:
            _logger.error(
                "More than one JWT validator found for name %r", validator_name
            )
            raise AmbiguousJwtValidator()
        return validator

    def _decode(self, token):
        key = self.secret_key
        algorithm = "HS256"
        try:
            payload = jwt.decode(
                token,
                key=key,
                algorithms=[algorithm],
                options=dict(
                    require=["email", "role"],
                    verify_email=True,
                    verify_user=True,
                )
            )
        except Exception as e:
            _logger.info("Invalid token: %s", e)
            raise UnauthorizedInvalidToken()
        return payload

    def _get_user_id(self, payload):
        email = payload.get("email")
        if not email:
            _logger.debug("JWT payload does not have an email claim")
            return
        user_id = self.env["res.user"].search([("login", "=", email)])
        if not user_id:
            raise UnauthorizedPartnerNotFound()
        return user_id