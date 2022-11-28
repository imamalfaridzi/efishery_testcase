# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, api, models, _
from odoo.http import request
from werkzeug.exceptions import Unauthorized
import logging, re, jwt

_logger = logging.getLogger(__name__)

AUTHORIZATION_RE = re.compile(r"^Bearer ([^ ]+)$")


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _decode(cls, token):
    # def _decode(self, token):
        key = "efishery" # get from odoo.conf
        algorithm = "HS256"
        try:
            payload = jwt.decode(
                token,
                key=key,
                algorithms=[algorithm],
                options=dict(
                    require=["email"],
                    verify_email=True,
                )
            )
        except Exception as e:
            _logger.info("Invalid token: %s", e)
            raise Unauthorized(_("Invalid token: %s", e))
        return payload

    # def _get_user_id(self, payload):
    #     email = payload.get("email")
    #     if not email:
    #         _logger.debug("JWT payload does not have an email claim")
    #         return
    #     user_id = self.env["res.users"].search([("login", "=", email)])
    #     if not user_id:
    #         raise Unauthorized(_("User not Found"))
    #     return user_id.id

    # @classmethod
    # def _test_get_user(cls):
    #     payload = {'email': 'admin'}
    #     env = api.Environment(request.cr, SUPERUSER_ID, {})
    #     return env['ir.http']._get_user_id(payload)

    @classmethod
    def _authenticate(cls, endpoint):
        auth_method = endpoint.routing["auth"]
        if auth_method == ("jwt"):
            if request.session.uid:
                _logger.warning(
                    'A route with auth="jwt" must not be used within a user session.'
                )
                raise Unauthorized(
                    _("'A route with auth='jwt' must not be used within a user session.'"))
            if request.uid and not hasattr(request, "jwt_payload"):
                _logger.error(
                    "A route with auth='jwt' should not have a request.uid here."
                )
                raise Unauthorized(
                    _("A route with auth='jwt' should not have a request.uid here."))
        return super()._authenticate(endpoint)

    @classmethod
    def _auth_method_jwt(cls):
        assert not request.uid
        assert not request.session.uid
        token = cls._get_bearer_token()
        assert token
        secret_key = "efishery" # get from odoo.conf
        assert secret_key

        payload = None
        exceptions = {}
        try:
            payload = cls._decode(token)
        except Exception as e:
            raise e

        email = payload.get("email")
        if not email:
            _logger.debug("JWT payload does not have an email claim")
            raise Unauthorized(_("User not Found"))

        user_id = request.env['res.users'].search([('login', '=', email)])
        if not user_id:
            raise Unauthorized(_("User not Found"))

        request.uid = user_id.id  # this resets request.env
        request.jwt_payload = payload
        request.jwt_user_id = user_id.id

    @classmethod
    def _get_bearer_token(cls):
        authorization = request.httprequest.environ.get("HTTP_AUTHORIZATION")
        if not authorization:
            _logger.info("Missing Authorization header.")
            raise Unauthorized(
                _("Missing Authorization header."))

        mo = AUTHORIZATION_RE.match(authorization)
        if not mo:
            _logger.info("Malformed Authorization header.")
            raise Unauthorized(
                _("Malformed Authorization header."))
        return mo.group(1)