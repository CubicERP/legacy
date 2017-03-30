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
{
    "name": "Account and Stock Extend",
    "version": "1.0",
    "description": """
Add enhacements to accounting on stock moves.
    """,
    "author": "Cubic ERP",
    "website": "http://cubicERP.com",
    "category": "Warehouse Management",
    "depends": [
            "stock_account",
            "report_excel",
	    ],
	"data":[
            "stock_view.xml",
            "report/stock_valuation.xml",
	    ],
    "demo_xml": [
	    ],
    "active": False,
    "installable": True,
}
