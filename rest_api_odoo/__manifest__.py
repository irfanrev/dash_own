# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Sruthi Pavithran (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    "name": "Odoo REST API + Owner Dashboard",
    "version": "17.0.2.0.0",
    "category": "Tools",
    "summary": """REST API endpoints including Owner Dashboard for Resort/Hospitality business monitoring""",
    "description": """
        REST API Module with Owner Dashboard
        ====================================

        This module provides:
        - Standard REST API endpoints (GET, POST, PUT, DELETE)
        - Owner Dashboard API endpoint (/api/owner_dashboard/summary)

        Owner Dashboard Features:
        - KPI Summary (Revenue, Orders, Customers, Cash Balance)
        - Finance Summary (Receivables, Payables, Assets, Liabilities, Equity)
        - Logistics Summary (Inventory Value, Low Stock, Pending Deliveries)
        - Recent Transactions from Invoices and POS
        - 6-Month Sales Trend
        - Top Products and Revenue by Category
        - Cashflow Analysis
        - Income Statement
        - Balance Sheet
        - POS Summary (Today, Week, Month)

        Supported Modules (optional):
        - Sale (for B2B orders)
        - Point of Sale (for retail transactions)
        - Purchase (for procurement)
        - Stock (for inventory)
        - Account (for financial data)

        Note: Dashboard works with whatever modules are installed.
        Missing modules will show zero/empty data for those sections.
    """,
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    "depends": ['base', 'web', 'account'],
    "external_dependencies": {
        "python": ["dateutil"],
    },
    "data": [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/connection_api_views.xml'
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
