# -*- coding: utf-8 -*-

import json
import base64
import logging

from odoo import http, SUPERUSER_ID
from odoo.http import Root, HttpRequest
from odoo.http import request, Response

_logger = logging.getLogger(__name__)


class KsWooWebhookHandler(http.Controller):
    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/customer/create'], auth='none', csrf=False, methods=['POST'])
    def create_customer_webhook(self, db, woo_instance_id, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        request.env['ks.woo.partner'].sudo().ks_manage_woo_customer_import(woo_instance, data)
                        return 'ok'
            return 'ok'
        except Exception as e:
            _logger.info("Create of customer failed with exception through webhook failed "+str(e))
            return request.not_found()

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/customer/update'], auth='none', csrf=False, methods=['POST'])
    def update_customer_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        request.env['ks.woo.partner'].sudo().ks_manage_woo_customer_import(woo_instance, data)
                        return 'ok'
            return 'ok'
        except Exception as e:
            _logger.info("Update of customer failed through webhook failed "+str(e))
            return Response("The requested URL was not found on the server.", status=404)

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/coupon/create'], auth='none', csrf=False, methods=['POST'])
    def create_coupon_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        wcapi = woo_instance.ks_woo_api_authentication()
                        if wcapi.get('').status_code in [200, 201]:
                            request.env['ks.woo.coupons'].sudo().ks_manage_coupon_woo_data(woo_instance, data)
                            return 'ok'
                        else:
                            _logger.info("Coupon Create Failed, Fatal error")
            return 'ok'
        except Exception as e:
            _logger.info("Create of coupon failed through webhook failed "+str(e))
            return Response("The requested URL was not found on the server.", status=404)

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/coupon/update'], auth='none', csrf=False, methods=['POST'])
    def update_coupon_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        wcapi = woo_instance.ks_woo_api_authentication()
                        if wcapi.get('').status_code in [200, 201]:
                            request.env['ks.woo.coupons'].sudo().ks_manage_coupon_woo_data(woo_instance, data)
                        else:
                            _logger.info("Update of coupon failed , fatal error with api")
            return 'ok'
        except Exception as e:
            _logger.info("Update of coupon failed through webhook failed "+str(e))
            return Response("The requested URL was not found on the server.", status=404)

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/product/create'], auth='none', csrf=False, methods=['POST'])
    def create_product_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)

            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search(
                        [('id', '=', woo_instance_id)],
                        limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        wcapi = woo_instance.ks_woo_api_authentication()
                        if wcapi.get('').status_code in [200, 201]:
                            product_exist = request.env['ks.woo.product.template'].sudo().search(
                                [('ks_wc_instance', '=', woo_instance.id),
                                 ('ks_woo_product_id', '=', data.get("id"))])
                            product_exist.sudo().ks_manage_woo_product_template_import(woo_instance, data)
                        else:
                            _logger.info("Fatal Error with the wcapi()")
            return 'ok'
        except Exception as e:
            _logger.info("Create of product failed through webhook failed "+str(e))
            return request.not_found()

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/product/update'], auth='none', csrf=False, methods=['POST'])
    def update_product_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        wcapi = woo_instance.ks_woo_api_authentication()
                        if wcapi.get('').status_code in [200, 201]:
                            product_exist = request.env['ks.woo.product.template'].sudo().search(
                                [('ks_wc_instance', '=', woo_instance.id),
                                 ('ks_woo_product_id', '=', data.get("id"))])
                            # if product_exist:
                            #     product_exist.sudo().ks_woo_import_product_template(product_data)
                            # else:
                            #     product_exist.sudo().ks_manage_woo_product_template_import(woo_instance, product_data)
                            product = product_exist.sudo().ks_manage_woo_product_template_import(woo_instance, data)
                        else:
                            _logger.info("Fatal Error with wcapi()")
            return 'ok'
        except Exception as e:
            _logger.info("Update of product failed through webhook failed "+str(e))
            return request.not_found()

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/order/create'], auth='none', csrf=False, methods=['POST'])
    def create_order_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        wcapi = woo_instance.ks_woo_api_authentication()
                        if wcapi.get('').status_code in [200, 201]:
                            ks_woo_sync_status = woo_instance.ks_order_status.mapped('status')
                            if data.get('status', False) in ks_woo_sync_status:
                                request.env['sale.order'].sudo().with_context(
                                    {'uid': SUPERUSER_ID}).ks_woo_import_order_create(data, woo_instance)
                        else:
                            _logger.info("Fatal Error with wcapi ()")
            return 'ok'
        except Exception as e:
            _logger.info("Create of order failed through webhook failed "+str(e))
            return request.not_found()

    @http.route(['/woo_hook/<string:db>/<string:uid>/<int:woo_instance_id>/order/update'], auth='none', csrf=False, methods=['POST'])
    def update_order_webhook(self, woo_instance_id, db, uid, **post):
        try:
            encoded_db = db.strip()
            decoded_db = base64.urlsafe_b64decode(encoded_db)
            request.session.db = str(decoded_db, "utf-8")
            if uid:
                request.session.uid = int(uid)
                request.env.user = request.env['res.users'].browse(int(uid))
                request.env.uid = int(uid)
            data = request.httprequest.data
            if data:
                self._ks_check_user()
                if woo_instance_id:
                    woo_instance = request.env['ks.woo.connector.instance'].sudo().search([('id', '=', woo_instance_id)],
                                                                                          limit=1)
                    if woo_instance and data:
                        request.env.company = woo_instance.ks_company_id
                        request.env.companies = woo_instance.ks_company_id
                        wcapi = woo_instance.ks_woo_api_authentication()
                        if wcapi.get('').status_code in [200, 201]:
                            order_record_exist = request.env['sale.order'].sudo().search(
                                [('ks_wc_instance', '=', woo_instance.id),
                                 ('ks_woo_order_id', '=', data.get("id"))], limit=1)
                            if order_record_exist:
                                order_record_exist.sudo().with_context({'uid': SUPERUSER_ID}).ks_woo_import_order_update(
                                data)
                        else:
                            _logger.info("Fatal Error with wcapi ()")
            return 'ok'
        except Exception as e:
            _logger.info("Update of order through webhook failed "+str(e))
            return request.not_found()

    def _ks_check_user(self):
        if request.env.user.has_group('base.group_public'):
            request.env.user = request.env['res.users'].browse(SUPERUSER_ID)
            request.env.uid = SUPERUSER_ID
        return request.env.user


old_get_request = Root.get_request


def get_request(self, httprequest):
    is_json = httprequest.args.get('jsonp') or httprequest.mimetype in ("application/json", "application/json-rpc")
    httprequest.data = {}
    woo_hook_path = ks_match_the_url_path(httprequest.path)
    if woo_hook_path and is_json:
        request = httprequest.get_data().decode(httprequest.charset)
        httprequest.data = json.loads(request)
        return HttpRequest(httprequest)
    return old_get_request(self, httprequest)


Root.get_request = get_request


def ks_match_the_url_path(path):
    if path:
        path_list = path.split('/')
        if path_list[1] == 'woo_hook' and path_list[5] in ['customer', 'coupon', 'product',
                                                                                 'order'] and path_list[6] in ['create',
                                                                                                               'update']:
            return True
        else:
            return False
