# -*- encoding: utf-8 -*-
##############################################################################
#
#    Branch Cubic ERP, Enterprise Management Software
#    Copyright (C) 2013 Cubic ERP - Teradata SAC (<http://cubicerp.com>).
#
#    This program can only be used with a valid Branch Cubic ERP agreement,
#    it is forbidden to publish, distribute, modify, sublicense or sell 
#    copies of the program.
#
#    The adove copyright notice must be included in all copies or 
#    substancial portions of the program.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT WARRANTY OF ANY KIND; without even the implied warranty
#    of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

from openerp.osv import osv, fields
from openerp import models
from openerp import fields as fields8
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
import time

class stock_move(osv.osv):
    _inherit = "stock.move"
    _columns = {
            'period_id': fields.many2one('account.period','Account Period', states={'done': [('readonly', True)]},
                                         domain=[('state','=','draft')]),
            'account_move_id': fields.many2one('account.move','Account Move', readonly=True, copy=False),
        }
    
class stock_quant(osv.osv):
    _inherit = "stock.quant"
    
    def _get_account_move(self, cr, uid, move, period_id, journal_id, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        if move.picking_id and move.picking_id.picking_type_id.journal_id:
            journal_id = move.picking_id.picking_type_id.journal_id.id
        if move.period_id:
            period_id = move.period_id.id
            ctx['force_period'] = period_id
        if not move.account_move_id:
            ctx['cbc_account_move_id'] = self.pool.get('account.move').create(cr, uid, {'journal_id': journal_id,
                                      'period_id': period_id,
                                      'date': time.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                      'ref': move.picking_id.name}, context=context)
            self.pool.get('stock.move').write(cr, uid, [move.id], {'account_move_id': ctx['cbc_account_move_id'],
                                                                   'period_id': period_id}, context=context)
        else:
            ctx['cbc_account_move_id'] = move.account_move_id.id
        return super(stock_quant,self)._get_account_move(cr, uid, move, period_id, journal_id, context=ctx)
        
class stock_picking_type(osv.osv):
    _inherit = "stock.picking.type"
    
    _columns = {
            'journal_id': fields.many2one('account.journal', 'Account Journal'),
        }
