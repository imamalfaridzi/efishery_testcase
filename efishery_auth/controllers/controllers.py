# -*- coding: utf-8 -*-

from odoo import http
import base64

import json

from odoo.http import Controller, Response, request, route


import json

from odoo.http import Controller, Response, request, route


class EfisheryAuth(Controller):
    @route("/api/auth_jwt", type="http", auth="jwt", csrf=False, cors="*",
        save_session=False, methods=['GET'])
    def whoami(self):
        data = {}
        if request.jwt_user_id:
            user_id = request.env['res.users'].sudo().browse(request.jwt_user_id)
            role = user_id._is_system() and "Super Admin" or \
                user_id._is_admin() and "Admin" or "User"
            data.update(name=user_id.name, email=user_id.email, role=role)
        return Response(json.dumps(data), content_type="application/json", status=200)

    @route("/api/auth_jwt_json", type="json", auth="jwt", save_session=False, methods=['GET'])
    def whoami_json(self):
        data = {}
        if request.jwt_user_id:
            user_id = request.env['res.users'].sudo().browse(request.jwt_user_id)
            role = user_id._is_system() and "Super Admin" or \
                user_id._is_admin() and "Admin" or "User"
            data.update(name=user_id.name, email=user_id.email, role=role)
        return data