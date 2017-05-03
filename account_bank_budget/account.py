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


from openerp import models, fields, api


class account_bank_statement(models.Model):
    _inherit = "account.bank.statement"

    budget_struct_id = fields.Many2one("account.budget.struct", string="Struct Budget",
                                     states={'confirm': [('readonly', True)]})

    @api.cr_uid_context
    def _prepare_bank_move_line(self, cr, uid, st_line, move_id, amount, company_currency_id, context=None):
        res = super(account_bank_statement, self)._prepare_bank_move_line(cr, uid, st_line, move_id, amount, company_currency_id, context=context)
        res['analytic_account_id'] = st_line.analytic_id.id
        res['budget_struct_id'] = st_line.budget_struct_id.id
        return res


class account_bank_statement_line(models.Model):
    _inherit = 'account.bank.statement.line'
    
    analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account")
    budget_struct_id = fields.Many2one('account.budget.struct', string="Struct Budget")
