# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from lxml import etree
from openerp import models, fields, api

class payment_purchase(models.TransientModel):
    """
    Create a payment object with lines corresponding to the purchase orders
    to advance or pay according to the date and the mode provided by the user.
    """

    _name = 'payment.purchase'
    entries = fields.Many2many('purchase.order', string='Purchase Orders')

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        line_ids = self.pool['purchase.order'].search(cr, uid, [('state','in',['approved','except_picking','except_invoice']),('invoiced','=',False)])
        res = super(payment_purchase, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=False)
        if line_ids:
            doc = etree.XML(res['arch'])
            nodes = doc.xpath("//field[@name='entries']")
            for node in nodes:
                node.set('domain', '[("id", "in", '+ str(line_ids)+')]')
            res['arch'] = etree.tostring(doc)
        return res

    def create_payment(self, cr, uid, ids, context=None):
        order_obj = self.pool.get('payment.order')
        line_obj = self.pool.get('purchase.order')
        payment_obj = self.pool.get('payment.line')
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]
        line_ids = [entry.id for entry in data.entries]
        if not line_ids:
            return {'type': 'ir.actions.act_window_close'}

        payment = order_obj.browse(cr, uid, context['active_id'], context=context)
        bank_type = self.pool.get('payment.mode').suitable_bank_types(cr, uid, None, context=context)
        for line in line_obj.browse(cr, uid, line_ids, context=context):
            date_to_pay = payment.date_scheduled
            bank_id = False
            for bank in line.partner_id.bank_ids:
                if bank.state in bank_type:
                    bank_id = bank.id
                    break
            if not bank_id and line.partner_id.bank_ids:
                bank_id = line.partner_id.bank_ids[0].id
            payment_obj.create(cr, uid,{
                    'purchase_id': line.id,
                    'amount_currency': line.amount_total,
                    'bank_id': bank_id,
                    'order_id': payment.id,
                    'partner_id': line.partner_id.id,
                    'communication': line.name,
                    'state': 'normal',
                    'date': date_to_pay,
                    'currency': line.currency_id.id,
                }, context=context)
        return {'type': 'ir.actions.act_window_close'}

