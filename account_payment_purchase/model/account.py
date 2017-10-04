# -*- coding: utf-8 -*-
##############################################################################
#
#    Cubic ERP, Enterprise and Government Management Software
#    Copyright (C) 2017 Cubic ERP S.A.C. (<http://cubicerp.com>).
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

from openerp import models, fields


class payment_order(models.Model):
    _inherit = 'payment.order'

    def _get_reference(self, cr, uid, line, context=None):
        res = super(payment_order, self)._get_reference(cr, uid, line, context=context)
        if line.purchase_id:
            res = line.purchase_id.partner_ref
        return res


class payment_line(models.Model):
    _inherit = 'payment.line'
    
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order")