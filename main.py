# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID, tools
import logging
_logger = logging.getLogger(__name__)

class HttpIntegrateController(http.Controller):
    @http.route('/post-crm-api',type='http', auth='public', methods=['POST'], csrf=False)
    def post_api(self, **kwargs):
        print('post-api invoked....')
        ctx = "post-api triggred..."
        odoobot_id = request.env['res.partner'].sudo().search([('id', '=', 3)])[0]
        mail_channel = request.env["mail.channel"].sudo().search([('uuid', '=', odoobot_id.id)], limit=1)
        # customer_no = request.httprequest.headers['phone_number']
        # odoobot_id = request.env['res.partner'].sudo().search([('phone', '=', customer_no)])[0]
        if not mail_channel:
            mail_channel = request.env['mail.channel'].sudo().create({
                'channel_partner_ids': [(4, odoobot_id.id)],
                'public': 'private',
                'channel_type': 'chat',
                'name': ctx,
                'display_name': ctx,
            })

        # msg =('Create a new lead (/lead lead title')
        # channel._redirect_to_messaging(odoobot_id, msg)
        # channel.message_post(
        #     body=ctx,
        #     author_id=odoobot_id.id,
        #     message_type="comment",
        #     subtype="mail.mt_comment",
        # )
        # customer_no.message_post(
        #     body=ctx,
        # )

        # mail_channel = request.env["mail.channel"].sudo().search([('uuid', '=', 2)], limit=1)


        # find the author from the user session
        # if request.session.uid:
        author = request.env['res.users'].sudo().browse(request.uid).partner_id
        author_id = author.id
        #     email_from = author.email_formatted
        # # else:  # If Public User, use catchall email from company
        # #     author_id = False
        # email_from = mail_channel.create_uid.company_id.catchall_formatted
        # post a message without adding followers to the channel. email_from=False avoid to get author from email data
        ctx = "post-api triggred..."
        body = tools.plaintext2html(ctx)
        message = mail_channel.message_post(
            author_id=author_id,
            # email_from=email_from,
            body=body,
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )
        # return message.id if message else False


    @http.route('/get-api',type='http', auth='none', methods=['GET'], csrf=False)
    def get_api(self, **kwargs):
        print('get-api invoked....')
        ctx = dict(self.env['whatsapp.message.wizard']._context)
        ctx['message'] = "get-api triggred..."
        return '{Status: triggered, get-api: Add user or password}'

    def button_print(self):
        print("git push")

