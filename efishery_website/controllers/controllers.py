# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import base64


class Main(http.Controller):
    @http.route('/importusers', type='http', auth="user",
        methods=['GET'], website=True)
    def show(self, **post):
        import_ids = request.env['website.import'].search(
            [('create_uid', '=', request.uid )])
        return request.render('efishery_website.importusers',
            {'import_ids': import_ids})

    @http.route('/importusers/submit', type='http', auth="user",
        methods=['POST'], website=True)
    def submit(self, **post):
        if post.get('attachment',False):
            Attachment = request.env['ir.attachment']
            WebsiteImport = request.env['website.import']
            Users = request.env['res.users']
            file = post.get('attachment')
            name = file.filename
            attachment_id = Attachment.sudo().create({
                'name':name,
                'res_name': name,
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
            })
            import_id = WebsiteImport.create({
                'model': 'res.users',
                'attachment_id': attachment_id.id,
                'state': 'draft'
                })
            request.env.cr.commit()
            import_id._do_import()
        return request.redirect('/importusers')