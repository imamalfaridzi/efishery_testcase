# -*- coding: utf-8 -*-

from odoo import models, fields, api, registry, _
from odoo.exceptions import ValidationError
import base64, threading

DEFAULT_MESSAGE = "Default message"

SUCCESS = "success"
DANGER = "danger"
WARNING = "warning"
INFO = "info"
DEFAULT = "default"


class WebsiteImport(models.Model):
    _name = "website.import"

    name = fields.Char(
        string='Name',
        default=_('New')
    )
    model = fields.Char(
        string='Model'
    )
    attachment_id = fields.Many2one(
        'ir.attachment',
        string='Attachment',
        attachment=True
    )
    state = fields.Selection([
        ('draft', 'New'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('failed', 'Failed')],
        string='State',
        default='draft'
    )

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code(
                'website.import') or _('New')
        return super().create(values)

    def _do_import(self):
        threaded_compute = threading.Thread(target=self._async_do_import, args=())
        threaded_compute.start()
        return True

    def _async_do_import(self):
        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            try:
                cr = registry(self._cr.dbname).cursor()
                self = self.with_env(self.env(cr=cr))
                self.do_import_data()
            finally:
                try:
                    self._cr.close()
                except Exception:
                    pass
            new_cr.close()
            return {}

    @api.model
    def do_import_data(self):
        options = {'quoting': '"', 'separator': ',', 'headers': True}
        datas = base64.b64decode(self.attachment_id.datas)
        fields = columns = datas.decode().split("\n")[0].split(',')
        import_id = self.env['base_import.import'].create({
            'res_model': self.model,
            'file': datas,
            'file_name': self.attachment_id.name,
            'file_type': self.attachment_id.mimetype
            })
        self.state = 'progress'
        self._notify_channel(INFO, "Your data is being imported", '[INFO] Import Users', True)
        self._cr.commit()
        try:
            import_id.do(fields, columns, options, False)
            self.state = 'done'
            self._notify_channel(SUCCESS, "Your data has been imported", '[SUCCESS] Import Users', True)
            self._cr.commit()
        except Exception as e:
            self.state = 'failed'
            self._notify_channel(DANGER, "Your data failed to import", '[FAILED] Import Users', True)
            self._cr.commit()
        return True

    def _notify_channel(self, type_message=DEFAULT, message=DEFAULT_MESSAGE, title=None, sticky=False):
        bus_message = {
            "type": type_message,
            "message": message,
            "title": title,
            "sticky": sticky,
        }
        notifications = [('notify_{}_{}'.format(type_message, self.create_uid.id), bus_message)]
        self.env["bus.bus"].sendmany(notifications)


# class Users(models.Model):
#     _inherit = 'res.users'

#     @api.model
#     def _import_website(self, attachment_id):
#         attachment = self.env['ir.attachment'].browse(attachment_id)
#         options = {'quoting': '"', 'separator': ',', 'headers': True}
#         datas = base64.b64decode(attachment.datas)
#         fields = columns = datas.decode().split("\n")[0].split(',')
#         import_id = self.env['base_import.import'].create({
#             'res_model': 'res.users',
#             'file': datas,
#             'file_name': attachment.name,
#             'file_type': attachment.mimetype
#             })
#         return import_id.do(fields, columns, options, False)