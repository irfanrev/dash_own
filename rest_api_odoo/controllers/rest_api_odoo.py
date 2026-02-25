import json
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class RestApi(http.Controller):
    """Controller for REST API requests including Owner Dashboard"""

    def auth_api_key(self, api_key):
        """Authenticate API key"""
        user_id = request.env['res.users'].sudo().search([('api_key', '=', api_key)])
        if api_key is not None and user_id:
            return True
        elif not user_id:
            return '<html><body><h2>Invalid <i>API Key</i>!</h2></body></html>'
        else:
            return '<html><body><h2>No <i>API Key</i> Provided!</h2></body></html>'

    # ==================== OWNER DASHBOARD HELPER METHODS ====================

    def _get_date_ranges(self):
        """Get common date ranges for queries"""
        today = datetime.now().date()

        # Start of periods
        start_of_today = datetime.combine(today, datetime.min.time())
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        # Last 6 months for trends
        months = []
        for i in range(5, -1, -1):
            month_date = today - relativedelta(months=i)
            months.append({
                'name': month_date.strftime('%b'),
                'start': month_date.replace(day=1),
                'end': (month_date.replace(day=1) + relativedelta(months=1)) - timedelta(days=1)
            })

        return {
            'today': today,
            'start_of_today': start_of_today,
            'start_of_week': start_of_week,
            'start_of_month': start_of_month,
            'start_of_year': start_of_year,
            'months': months
        }

    def _get_kpi_data(self):
        """Fetch KPI data from sale.order, pos.order, and account"""
        kpi = {
            'total_revenue': 0,
            'total_orders': 0,
            'active_customers': 0,
            'cash_balance': 0
        }

        try:
            dates = self._get_date_ranges()
            year_start = dates['start_of_year'].strftime('%Y-%m-%d')

            # Total Revenue from Sale Orders (confirmed/done)
            SaleOrder = request.env['sale.order'].sudo()
            sales = SaleOrder.search([
                ('state', 'in', ['sale', 'done']),
                ('date_order', '>=', year_start)
            ])
            sale_revenue = sum(sales.mapped('amount_total'))
            sale_count = len(sales)

            # Total Revenue from POS Orders
            pos_revenue = 0
            pos_count = 0
            try:
                PosOrder = request.env['pos.order'].sudo()
                pos_orders = PosOrder.search([
                    ('state', 'in', ['paid', 'done', 'invoiced']),
                    ('date_order', '>=', year_start)
                ])
                pos_revenue = sum(pos_orders.mapped('amount_total'))
                pos_count = len(pos_orders)
            except Exception:
                _logger.info("POS module not installed, skipping POS data")

            kpi['total_revenue'] = sale_revenue + pos_revenue
            kpi['total_orders'] = sale_count + pos_count

            # Active Customers (customers with transactions this year)
            Partner = request.env['res.partner'].sudo()
            customers = Partner.search_count([
                ('customer_rank', '>', 0),
                '|',
                ('sale_order_ids.date_order', '>=', year_start),
                ('pos_order_ids.date_order', '>=', year_start)
            ])
            # Fallback if the above doesn't work
            if customers == 0:
                customers = Partner.search_count([('customer_rank', '>', 0)])
            kpi['active_customers'] = customers

            # Cash & Bank Balance from account.account
            try:
                Account = request.env['account.account'].sudo()
                # Get cash and bank accounts (typically code starts with 1 for assets, 11 for cash/bank)
                cash_accounts = Account.search([
                    ('account_type', 'in', ['asset_cash', 'asset_bank'])
                ])
                if cash_accounts:
                    MoveLine = request.env['account.move.line'].sudo()
                    lines = MoveLine.search([
                        ('account_id', 'in', cash_accounts.ids),
                        ('parent_state', '=', 'posted')
                    ])
                    kpi['cash_balance'] = sum(lines.mapped('balance'))
            except Exception as e:
                _logger.warning("Error fetching cash balance: %s", str(e))

        except Exception as e:
            _logger.error("Error in _get_kpi_data: %s", str(e))

        return kpi

    def _get_finance_data(self):
        """Fetch finance summary from account.move and account.account"""
        finance = {
            'accounts_receivable': 0,
            'accounts_payable': 0,
            'net_profit': 0,
            'expenses': 0,
            'assets': 0,
            'liabilities': 0,
            'equity': 0
        }

        try:
            MoveLine = request.env['account.move.line'].sudo()
            Account = request.env['account.account'].sudo()

            # Accounts Receivable
            ar_accounts = Account.search([('account_type', '=', 'asset_receivable')])
            if ar_accounts:
                ar_lines = MoveLine.search([
                    ('account_id', 'in', ar_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('reconciled', '=', False)
                ])
                finance['accounts_receivable'] = sum(ar_lines.mapped('balance'))

            # Accounts Payable
            ap_accounts = Account.search([('account_type', '=', 'liability_payable')])
            if ap_accounts:
                ap_lines = MoveLine.search([
                    ('account_id', 'in', ap_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('reconciled', '=', False)
                ])
                finance['accounts_payable'] = abs(sum(ap_lines.mapped('balance')))

            # Calculate Assets, Liabilities, Equity from account balances
            # Assets (account_type starts with 'asset')
            asset_accounts = Account.search([('account_type', 'like', 'asset%')])
            if asset_accounts:
                asset_lines = MoveLine.search([
                    ('account_id', 'in', asset_accounts.ids),
                    ('parent_state', '=', 'posted')
                ])
                finance['assets'] = sum(asset_lines.mapped('balance'))

            # Liabilities (account_type starts with 'liability')
            liability_accounts = Account.search([('account_type', 'like', 'liability%')])
            if liability_accounts:
                liability_lines = MoveLine.search([
                    ('account_id', 'in', liability_accounts.ids),
                    ('parent_state', '=', 'posted')
                ])
                finance['liabilities'] = abs(sum(liability_lines.mapped('balance')))

            # Equity
            equity_accounts = Account.search([('account_type', '=', 'equity')])
            if equity_accounts:
                equity_lines = MoveLine.search([
                    ('account_id', 'in', equity_accounts.ids),
                    ('parent_state', '=', 'posted')
                ])
                finance['equity'] = abs(sum(equity_lines.mapped('balance')))

            # Revenue & Expenses for this year
            dates = self._get_date_ranges()
            year_start = dates['start_of_year'].strftime('%Y-%m-%d')

            # Revenue
            income_accounts = Account.search([('account_type', 'in', ['income', 'income_other'])])
            if income_accounts:
                income_lines = MoveLine.search([
                    ('account_id', 'in', income_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ])
                total_revenue = abs(sum(income_lines.mapped('balance')))

            # Expenses
            expense_accounts = Account.search([('account_type', 'in', ['expense', 'expense_depreciation', 'expense_direct_cost'])])
            if expense_accounts:
                expense_lines = MoveLine.search([
                    ('account_id', 'in', expense_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ])
                finance['expenses'] = sum(expense_lines.mapped('balance'))

            # Net Profit = Revenue - Expenses (simplified)
            finance['net_profit'] = total_revenue - finance['expenses'] if 'total_revenue' in dir() else 0

        except Exception as e:
            _logger.error("Error in _get_finance_data: %s", str(e))

        return finance

    def _get_logistics_data(self):
        """Fetch logistics summary from stock and purchase models"""
        logistics = {
            'pending_deliveries': 0,
            'low_stock_items': 0,
            'inventory_value': 0
        }

        try:
            # Pending Deliveries (Purchase Orders in progress)
            try:
                PurchaseOrder = request.env['purchase.order'].sudo()
                pending_po = PurchaseOrder.search_count([
                    ('state', 'in', ['purchase', 'sent'])
                ])
                logistics['pending_deliveries'] = pending_po
            except Exception:
                _logger.info("Purchase module not available")

            # Inventory Value from stock.quant
            try:
                StockQuant = request.env['stock.quant'].sudo()
                quants = StockQuant.search([
                    ('location_id.usage', '=', 'internal'),
                    ('quantity', '>', 0)
                ])
                logistics['inventory_value'] = sum(q.quantity * q.product_id.standard_price for q in quants)

                # Low Stock Items (below reorder point)
                try:
                    OrderPoint = request.env['stock.warehouse.orderpoint'].sudo()
                    orderpoints = OrderPoint.search([])
                    low_stock_count = 0
                    for op in orderpoints:
                        product_qty = sum(StockQuant.search([
                            ('product_id', '=', op.product_id.id),
                            ('location_id', '=', op.location_id.id)
                        ]).mapped('quantity'))
                        if product_qty < op.product_min_qty:
                            low_stock_count += 1
                    logistics['low_stock_items'] = low_stock_count
                except Exception:
                    _logger.info("Orderpoint not available")
            except Exception:
                _logger.info("Stock module not available")

        except Exception as e:
            _logger.error("Error in _get_logistics_data: %s", str(e))

        return logistics

    def _get_recent_transactions(self, limit=10):
        """Fetch recent transactions from invoices and POS orders"""
        transactions = []

        try:
            # Get recent invoices
            AccountMove = request.env['account.move'].sudo()
            invoices = AccountMove.search([
                ('move_type', 'in', ['out_invoice', 'in_invoice', 'out_refund', 'in_refund']),
                ('state', '=', 'posted')
            ], order='invoice_date desc', limit=limit)

            for inv in invoices:
                trx_type = ""
                amount = inv.amount_total_signed

                if inv.move_type == 'out_invoice':
                    trx_type = f"Penjualan - {inv.partner_id.name or 'Customer'}"
                elif inv.move_type == 'in_invoice':
                    trx_type = f"Pembelian - {inv.partner_id.name or 'Vendor'}"
                    amount = -abs(amount)
                elif inv.move_type == 'out_refund':
                    trx_type = f"Retur Penjualan"
                    amount = -abs(amount)
                elif inv.move_type == 'in_refund':
                    trx_type = f"Retur Pembelian"

                transactions.append({
                    'id': inv.id,
                    'type': trx_type[:50],
                    'amount': amount,
                    'date': inv.invoice_date.strftime('%Y-%m-%d') if inv.invoice_date else '',
                    'status': 'Completed' if inv.payment_state == 'paid' else 'Pending'
                })

            # Add POS orders if available
            try:
                PosOrder = request.env['pos.order'].sudo()
                pos_orders = PosOrder.search([
                    ('state', 'in', ['paid', 'done', 'invoiced'])
                ], order='date_order desc', limit=5)

                for pos in pos_orders:
                    transactions.append({
                        'id': pos.id,
                        'type': f"POS - {pos.session_id.config_id.name or 'Point of Sale'}",
                        'amount': pos.amount_total,
                        'date': pos.date_order.strftime('%Y-%m-%d') if pos.date_order else '',
                        'status': 'Completed'
                    })
            except Exception:
                pass

            # Sort by date and limit
            transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)[:limit]

        except Exception as e:
            _logger.error("Error in _get_recent_transactions: %s", str(e))

        return transactions

    def _get_sales_trend(self):
        """Get sales trend for the last 6 months"""
        sales_trend = []

        try:
            dates = self._get_date_ranges()

            for month in dates['months']:
                month_start = month['start'].strftime('%Y-%m-%d')
                month_end = month['end'].strftime('%Y-%m-%d')

                # Sales Orders
                SaleOrder = request.env['sale.order'].sudo()
                sales = SaleOrder.search([
                    ('state', 'in', ['sale', 'done']),
                    ('date_order', '>=', month_start),
                    ('date_order', '<=', month_end)
                ])
                sale_total = sum(sales.mapped('amount_total'))

                # POS Orders
                pos_total = 0
                try:
                    PosOrder = request.env['pos.order'].sudo()
                    pos_orders = PosOrder.search([
                        ('state', 'in', ['paid', 'done', 'invoiced']),
                        ('date_order', '>=', month_start),
                        ('date_order', '<=', month_end)
                    ])
                    pos_total = sum(pos_orders.mapped('amount_total'))
                except Exception:
                    pass

                sales_trend.append({
                    'name': month['name'],
                    'revenue': sale_total + pos_total
                })

        except Exception as e:
            _logger.error("Error in _get_sales_trend: %s", str(e))

        return sales_trend

    def _get_sales_detail(self):
        """Get detailed sales data including top products and revenue by category"""
        dates = self._get_date_ranges()
        year_start = dates['start_of_year'].strftime('%Y-%m-%d')

        sales_detail = {
            'pos_revenue': 0,
            'b2b_revenue': 0,
            'pos_transactions': 0,
            'b2b_orders': 0,
            'top_products': [],
            'revenue_by_unit': []
        }

        try:
            # B2B Revenue from Sale Orders
            SaleOrder = request.env['sale.order'].sudo()
            sales = SaleOrder.search([
                ('state', 'in', ['sale', 'done']),
                ('date_order', '>=', year_start)
            ])
            sales_detail['b2b_revenue'] = sum(sales.mapped('amount_total'))
            sales_detail['b2b_orders'] = len(sales)

            # POS Revenue
            try:
                PosOrder = request.env['pos.order'].sudo()
                pos_orders = PosOrder.search([
                    ('state', 'in', ['paid', 'done', 'invoiced']),
                    ('date_order', '>=', year_start)
                ])
                sales_detail['pos_revenue'] = sum(pos_orders.mapped('amount_total'))
                sales_detail['pos_transactions'] = len(pos_orders)
            except Exception:
                pass

            # Top Products from Sale Order Lines
            SaleOrderLine = request.env['sale.order.line'].sudo()
            top_lines = SaleOrderLine.read_group(
                domain=[
                    ('order_id.state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '>=', year_start)
                ],
                fields=['product_id', 'product_uom_qty:sum', 'price_subtotal:sum'],
                groupby=['product_id'],
                orderby='price_subtotal desc',
                limit=5
            )

            for line in top_lines:
                if line['product_id']:
                    product = request.env['product.product'].sudo().browse(line['product_id'][0])
                    category_name = product.categ_id.name if product.categ_id else 'Lainnya'
                    sales_detail['top_products'].append({
                        'name': line['product_id'][1][:40],
                        'qty': int(line['product_uom_qty']),
                        'revenue': line['price_subtotal'],
                        'category': category_name[:20]
                    })

            # Revenue by Product Category
            category_revenue = SaleOrderLine.read_group(
                domain=[
                    ('order_id.state', 'in', ['sale', 'done']),
                    ('order_id.date_order', '>=', year_start)
                ],
                fields=['product_id', 'price_subtotal:sum'],
                groupby=['product_id.categ_id'],
                orderby='price_subtotal desc',
                limit=5
            )

            colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444']
            for idx, cat in enumerate(category_revenue):
                cat_name = cat.get('product_id.categ_id')
                if cat_name:
                    sales_detail['revenue_by_unit'].append({
                        'name': cat_name[1] if isinstance(cat_name, tuple) else str(cat_name)[:20],
                        'value': cat['price_subtotal'],
                        'color': colors[idx % len(colors)]
                    })

        except Exception as e:
            _logger.error("Error in _get_sales_detail: %s", str(e))

        return sales_detail

    def _get_finance_detail(self):
        """Get detailed finance data including cashflow, expenses, income statement, balance sheet"""
        dates = self._get_date_ranges()
        year_start = dates['start_of_year'].strftime('%Y-%m-%d')

        finance_detail = {
            'cashflow': [],
            'expense_breakdown': [],
            'income_statement': {
                'revenue': 0,
                'cogs': 0,
                'gross_profit': 0,
                'operating_expenses': 0,
                'depreciation': 0,
                'net_profit_before_tax': 0,
                'tax': 0,
                'net_profit': 0
            },
            'balance_sheet': self._get_balance_sheet()
        }

        try:
            Account = request.env['account.account'].sudo()
            MoveLine = request.env['account.move.line'].sudo()

            # Cashflow per month (last 6 months)
            for month in dates['months']:
                month_start = month['start'].strftime('%Y-%m-%d')
                month_end = month['end'].strftime('%Y-%m-%d')

                # Cash In (revenue/income accounts)
                income_accounts = Account.search([('account_type', 'in', ['income', 'income_other'])])
                cash_in = 0
                if income_accounts:
                    in_lines = MoveLine.search([
                        ('account_id', 'in', income_accounts.ids),
                        ('parent_state', '=', 'posted'),
                        ('date', '>=', month_start),
                        ('date', '<=', month_end)
                    ])
                    cash_in = abs(sum(in_lines.mapped('credit')))

                # Cash Out (expense accounts)
                expense_accounts = Account.search([('account_type', 'like', 'expense%')])
                cash_out = 0
                if expense_accounts:
                    out_lines = MoveLine.search([
                        ('account_id', 'in', expense_accounts.ids),
                        ('parent_state', '=', 'posted'),
                        ('date', '>=', month_start),
                        ('date', '<=', month_end)
                    ])
                    cash_out = abs(sum(out_lines.mapped('debit')))

                finance_detail['cashflow'].append({
                    'name': month['name'],
                    'in': cash_in,
                    'out': cash_out
                })

            # Expense Breakdown by category (using analytic or account groups)
            expense_accounts = Account.search([('account_type', 'like', 'expense%')])
            expense_by_account = MoveLine.read_group(
                domain=[
                    ('account_id', 'in', expense_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ],
                fields=['account_id', 'debit:sum'],
                groupby=['account_id'],
                orderby='debit desc',
                limit=5
            )

            colors = ['#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981']
            for idx, exp in enumerate(expense_by_account):
                if exp['account_id']:
                    finance_detail['expense_breakdown'].append({
                        'name': exp['account_id'][1][:25],
                        'value': exp['debit'],
                        'color': colors[idx % len(colors)]
                    })

            # Income Statement
            # Revenue
            income_accounts = Account.search([('account_type', 'in', ['income', 'income_other'])])
            if income_accounts:
                revenue_lines = MoveLine.search([
                    ('account_id', 'in', income_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ])
                finance_detail['income_statement']['revenue'] = abs(sum(revenue_lines.mapped('balance')))

            # COGS
            cogs_accounts = Account.search([('account_type', '=', 'expense_direct_cost')])
            if cogs_accounts:
                cogs_lines = MoveLine.search([
                    ('account_id', 'in', cogs_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ])
                finance_detail['income_statement']['cogs'] = abs(sum(cogs_lines.mapped('balance')))

            # Gross Profit
            finance_detail['income_statement']['gross_profit'] = (
                finance_detail['income_statement']['revenue'] -
                finance_detail['income_statement']['cogs']
            )

            # Operating Expenses
            op_expense_accounts = Account.search([('account_type', '=', 'expense')])
            if op_expense_accounts:
                op_lines = MoveLine.search([
                    ('account_id', 'in', op_expense_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ])
                finance_detail['income_statement']['operating_expenses'] = abs(sum(op_lines.mapped('balance')))

            # Depreciation
            depreciation_accounts = Account.search([('account_type', '=', 'expense_depreciation')])
            if depreciation_accounts:
                dep_lines = MoveLine.search([
                    ('account_id', 'in', depreciation_accounts.ids),
                    ('parent_state', '=', 'posted'),
                    ('date', '>=', year_start)
                ])
                finance_detail['income_statement']['depreciation'] = abs(sum(dep_lines.mapped('balance')))

            # Net Profit Before Tax
            finance_detail['income_statement']['net_profit_before_tax'] = (
                finance_detail['income_statement']['gross_profit'] -
                finance_detail['income_statement']['operating_expenses'] -
                finance_detail['income_statement']['depreciation']
            )

            # Tax (simplified - 25% of profit before tax if positive)
            if finance_detail['income_statement']['net_profit_before_tax'] > 0:
                finance_detail['income_statement']['tax'] = finance_detail['income_statement']['net_profit_before_tax'] * 0.25

            # Net Profit
            finance_detail['income_statement']['net_profit'] = (
                finance_detail['income_statement']['net_profit_before_tax'] -
                finance_detail['income_statement']['tax']
            )

        except Exception as e:
            _logger.error("Error in _get_finance_detail: %s", str(e))

        return finance_detail

    def _get_balance_sheet(self):
        """Get balance sheet data from account.account"""
        balance_sheet = {
            'current_assets': {
                'cash_and_bank': 0,
                'accounts_receivable': 0,
                'inventory': 0,
                'prepaid_expenses': 0,
                'total': 0
            },
            'non_current_assets': {
                'property_equipment': 0,
                'accumulated_depreciation': 0,
                'intangible_assets': 0,
                'other_assets': 0,
                'total': 0
            },
            'total_assets': 0,
            'current_liabilities': {
                'accounts_payable': 0,
                'accrued_expenses': 0,
                'short_term_debt': 0,
                'taxes_payable': 0,
                'total': 0
            },
            'non_current_liabilities': {
                'long_term_debt': 0,
                'other_liabilities': 0,
                'total': 0
            },
            'total_liabilities': 0,
            'equity': {
                'capital_stock': 0,
                'retained_earnings': 0,
                'total': 0
            }
        }

        try:
            Account = request.env['account.account'].sudo()
            MoveLine = request.env['account.move.line'].sudo()

            def get_balance(account_types):
                accounts = Account.search([('account_type', 'in', account_types)])
                if not accounts:
                    return 0
                lines = MoveLine.search([
                    ('account_id', 'in', accounts.ids),
                    ('parent_state', '=', 'posted')
                ])
                return sum(lines.mapped('balance'))

            # Current Assets
            balance_sheet['current_assets']['cash_and_bank'] = get_balance(['asset_cash'])
            balance_sheet['current_assets']['accounts_receivable'] = get_balance(['asset_receivable'])
            balance_sheet['current_assets']['inventory'] = get_balance(['asset_current'])
            balance_sheet['current_assets']['prepaid_expenses'] = get_balance(['asset_prepayments'])
            balance_sheet['current_assets']['total'] = sum([
                balance_sheet['current_assets']['cash_and_bank'],
                balance_sheet['current_assets']['accounts_receivable'],
                balance_sheet['current_assets']['inventory'],
                balance_sheet['current_assets']['prepaid_expenses']
            ])

            # Non-Current Assets
            balance_sheet['non_current_assets']['property_equipment'] = get_balance(['asset_fixed'])
            balance_sheet['non_current_assets']['accumulated_depreciation'] = get_balance(['asset_non_current'])  # This needs adjustment based on your COA
            balance_sheet['non_current_assets']['total'] = (
                balance_sheet['non_current_assets']['property_equipment'] +
                balance_sheet['non_current_assets']['accumulated_depreciation']
            )

            balance_sheet['total_assets'] = (
                balance_sheet['current_assets']['total'] +
                balance_sheet['non_current_assets']['total']
            )

            # Current Liabilities
            balance_sheet['current_liabilities']['accounts_payable'] = abs(get_balance(['liability_payable']))
            balance_sheet['current_liabilities']['accrued_expenses'] = abs(get_balance(['liability_current']))
            balance_sheet['current_liabilities']['total'] = sum([
                balance_sheet['current_liabilities']['accounts_payable'],
                balance_sheet['current_liabilities']['accrued_expenses'],
                balance_sheet['current_liabilities']['short_term_debt'],
                balance_sheet['current_liabilities']['taxes_payable']
            ])

            # Non-Current Liabilities
            balance_sheet['non_current_liabilities']['long_term_debt'] = abs(get_balance(['liability_non_current']))
            balance_sheet['non_current_liabilities']['total'] = (
                balance_sheet['non_current_liabilities']['long_term_debt'] +
                balance_sheet['non_current_liabilities']['other_liabilities']
            )

            balance_sheet['total_liabilities'] = (
                balance_sheet['current_liabilities']['total'] +
                balance_sheet['non_current_liabilities']['total']
            )

            # Equity
            equity_balance = abs(get_balance(['equity', 'equity_unaffected']))
            balance_sheet['equity']['capital_stock'] = equity_balance * 0.75  # Simplified split
            balance_sheet['equity']['retained_earnings'] = equity_balance * 0.25
            balance_sheet['equity']['total'] = equity_balance

        except Exception as e:
            _logger.error("Error in _get_balance_sheet: %s", str(e))

        return balance_sheet

    def _get_logistics_detail(self):
        """Get detailed logistics data"""
        logistics_detail = {
            'inventory_by_category': [],
            'low_stock_alerts': [],
            'pending_orders': [],
            'delivery_status': {
                'in_transit': 0,
                'processing': 0,
                'confirmed': 0,
                'completed_this_week': 0
            }
        }

        try:
            # Inventory by Category
            try:
                StockQuant = request.env['stock.quant'].sudo()
                ProductCategory = request.env['product.category'].sudo()

                categories = ProductCategory.search([], limit=10)
                colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4', '#ec4899', '#84cc16']

                for idx, cat in enumerate(categories):
                    quants = StockQuant.search([
                        ('product_id.categ_id', 'child_of', cat.id),
                        ('location_id.usage', '=', 'internal'),
                        ('quantity', '>', 0)
                    ])
                    if quants:
                        value = sum(q.quantity * q.product_id.standard_price for q in quants)
                        item_count = len(set(quants.mapped('product_id.id')))
                        if value > 0:
                            logistics_detail['inventory_by_category'].append({
                                'name': cat.name[:20],
                                'value': value,
                                'items': item_count,
                                'color': colors[idx % len(colors)]
                            })

                # Sort by value
                logistics_detail['inventory_by_category'] = sorted(
                    logistics_detail['inventory_by_category'],
                    key=lambda x: x['value'],
                    reverse=True
                )[:5]

            except Exception as e:
                _logger.info("Stock module issue: %s", str(e))

            # Low Stock Alerts
            try:
                OrderPoint = request.env['stock.warehouse.orderpoint'].sudo()
                StockQuant = request.env['stock.quant'].sudo()

                orderpoints = OrderPoint.search([], limit=20)
                for op in orderpoints:
                    quants = StockQuant.search([
                        ('product_id', '=', op.product_id.id),
                        ('location_id', '=', op.location_id.id)
                    ])
                    current_qty = sum(quants.mapped('quantity'))

                    if current_qty < op.product_min_qty:
                        logistics_detail['low_stock_alerts'].append({
                            'name': op.product_id.name[:30],
                            'current_stock': current_qty,
                            'min_stock': op.product_min_qty,
                            'unit': op.product_id.uom_id.name if op.product_id.uom_id else 'Unit',
                            'category': op.product_id.categ_id.name[:20] if op.product_id.categ_id else 'Lainnya'
                        })

                logistics_detail['low_stock_alerts'] = logistics_detail['low_stock_alerts'][:5]

            except Exception as e:
                _logger.info("Orderpoint issue: %s", str(e))

            # Pending Purchase Orders
            try:
                PurchaseOrder = request.env['purchase.order'].sudo()
                pending_pos = PurchaseOrder.search([
                    ('state', 'in', ['draft', 'sent', 'to approve', 'purchase'])
                ], order='date_order desc', limit=5)

                for po in pending_pos:
                    status_map = {
                        'draft': 'Processing',
                        'sent': 'Processing',
                        'to approve': 'Processing',
                        'purchase': 'Confirmed'
                    }

                    # Check if there's a picking in transit
                    picking_status = 'Processing'
                    if po.picking_ids:
                        for picking in po.picking_ids:
                            if picking.state == 'assigned':
                                picking_status = 'In Transit'
                                break

                    logistics_detail['pending_orders'].append({
                        'id': po.name,
                        'vendor': po.partner_id.name[:25] if po.partner_id else 'N/A',
                        'items': len(po.order_line),
                        'total': po.amount_total,
                        'expected_date': po.date_planned.strftime('%Y-%m-%d') if po.date_planned else '',
                        'status': picking_status if po.state == 'purchase' else status_map.get(po.state, 'Processing')
                    })

            except Exception as e:
                _logger.info("Purchase order issue: %s", str(e))

            # Delivery Status from stock.picking
            try:
                StockPicking = request.env['stock.picking'].sudo()
                dates = self._get_date_ranges()
                week_start = dates['start_of_week'].strftime('%Y-%m-%d')

                # Incoming pickings (from purchases)
                incoming_type = request.env['stock.picking.type'].sudo().search([
                    ('code', '=', 'incoming')
                ], limit=1)

                if incoming_type:
                    logistics_detail['delivery_status']['in_transit'] = StockPicking.search_count([
                        ('picking_type_id', '=', incoming_type.id),
                        ('state', '=', 'assigned')
                    ])

                    logistics_detail['delivery_status']['processing'] = StockPicking.search_count([
                        ('picking_type_id', '=', incoming_type.id),
                        ('state', 'in', ['draft', 'waiting', 'confirmed'])
                    ])

                    logistics_detail['delivery_status']['confirmed'] = StockPicking.search_count([
                        ('picking_type_id', '=', incoming_type.id),
                        ('state', '=', 'assigned')
                    ])

                    logistics_detail['delivery_status']['completed_this_week'] = StockPicking.search_count([
                        ('picking_type_id', '=', incoming_type.id),
                        ('state', '=', 'done'),
                        ('date_done', '>=', week_start)
                    ])

            except Exception as e:
                _logger.info("Stock picking issue: %s", str(e))

        except Exception as e:
            _logger.error("Error in _get_logistics_detail: %s", str(e))

        return logistics_detail

    def _get_pos_summary(self):
        """Get POS summary for today, this week, this month"""
        dates = self._get_date_ranges()

        pos_summary = {
            'today': {'transactions': 0, 'revenue': 0, 'avg_ticket': 0},
            'this_week': {'transactions': 0, 'revenue': 0, 'avg_ticket': 0},
            'this_month': {'transactions': 0, 'revenue': 0, 'avg_ticket': 0}
        }

        try:
            PosOrder = request.env['pos.order'].sudo()

            # Today
            today_orders = PosOrder.search([
                ('state', 'in', ['paid', 'done', 'invoiced']),
                ('date_order', '>=', dates['start_of_today'].strftime('%Y-%m-%d %H:%M:%S'))
            ])
            pos_summary['today']['transactions'] = len(today_orders)
            pos_summary['today']['revenue'] = sum(today_orders.mapped('amount_total'))
            if pos_summary['today']['transactions'] > 0:
                pos_summary['today']['avg_ticket'] = pos_summary['today']['revenue'] / pos_summary['today']['transactions']

            # This Week
            week_orders = PosOrder.search([
                ('state', 'in', ['paid', 'done', 'invoiced']),
                ('date_order', '>=', dates['start_of_week'].strftime('%Y-%m-%d'))
            ])
            pos_summary['this_week']['transactions'] = len(week_orders)
            pos_summary['this_week']['revenue'] = sum(week_orders.mapped('amount_total'))
            if pos_summary['this_week']['transactions'] > 0:
                pos_summary['this_week']['avg_ticket'] = pos_summary['this_week']['revenue'] / pos_summary['this_week']['transactions']

            # This Month
            month_orders = PosOrder.search([
                ('state', 'in', ['paid', 'done', 'invoiced']),
                ('date_order', '>=', dates['start_of_month'].strftime('%Y-%m-%d'))
            ])
            pos_summary['this_month']['transactions'] = len(month_orders)
            pos_summary['this_month']['revenue'] = sum(month_orders.mapped('amount_total'))
            if pos_summary['this_month']['transactions'] > 0:
                pos_summary['this_month']['avg_ticket'] = pos_summary['this_month']['revenue'] / pos_summary['this_month']['transactions']

        except Exception as e:
            _logger.info("POS module not available or error: %s", str(e))

        return pos_summary

    # ==================== MAIN DASHBOARD ENDPOINT ====================

    @http.route(['/api/owner_dashboard/summary'], type='http', auth='none', cors='*', methods=['GET'], csrf=False)
    def fetch_dashboard_summary(self, **kw):
        """Main endpoint for Owner Dashboard - fetches all data from Odoo models"""

        try:
            # Collect all dashboard data
            kpi_data = self._get_kpi_data()
            finance_data = self._get_finance_data()
            logistics_data = self._get_logistics_data()
            recent_transactions = self._get_recent_transactions()
            sales_trend = self._get_sales_trend()
            sales_detail = self._get_sales_detail()
            finance_detail = self._get_finance_detail()
            logistics_detail = self._get_logistics_detail()
            pos_summary = self._get_pos_summary()

            dashboard_data = {
                "status": "success",
                "data": {
                    "kpi": kpi_data,
                    "finance": finance_data,
                    "logistics": logistics_data,
                    "recent_transactions": recent_transactions,
                    "sales_trend": sales_trend,
                    "sales_detail": sales_detail,
                    "finance_detail": finance_detail,
                    "logistics_detail": logistics_detail,
                    "pos_summary": pos_summary
                },
                "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            _logger.info("Dashboard data generated successfully")

        except Exception as e:
            _logger.error("Critical error generating dashboard data: %s", str(e))
            # Return minimal fallback data
            dashboard_data = {
                "status": "error",
                "message": str(e),
                "data": {
                    "kpi": {"total_revenue": 0, "total_orders": 0, "active_customers": 0, "cash_balance": 0},
                    "finance": {"accounts_receivable": 0, "accounts_payable": 0, "net_profit": 0, "expenses": 0, "assets": 0, "liabilities": 0, "equity": 0},
                    "logistics": {"pending_deliveries": 0, "low_stock_items": 0, "inventory_value": 0},
                    "recent_transactions": [],
                    "sales_trend": [],
                    "sales_detail": {"pos_revenue": 0, "b2b_revenue": 0, "pos_transactions": 0, "b2b_orders": 0, "top_products": [], "revenue_by_unit": []},
                    "finance_detail": {"cashflow": [], "expense_breakdown": [], "income_statement": {}, "balance_sheet": {}},
                    "logistics_detail": {"inventory_by_category": [], "low_stock_alerts": [], "pending_orders": [], "delivery_status": {}},
                    "pos_summary": {"today": {}, "this_week": {}, "this_month": {}}
                }
            }

        return request.make_response(
            json.dumps(dashboard_data, default=str),
            headers=[('Content-Type', 'application/json')]
        )

    # ==================== OTHER EXISTING ENDPOINTS ====================

    def generate_response(self, method, model, rec_id):
        """Generate response based on request type and parameters"""
        option = request.env['connection.api'].search([('model_id', '=', model)], limit=1)
        model_name = option.model_id.model

        if not option:
            return '<html><body><h2>No Record Created for the model</h2></body></html>'

        if method == 'GET':
            if not option.is_get:
                return '<html><body><h2>Method Not Allowed</h2></body></html>'

            fields_param = request.params.get('fields', '')
            if not fields_param:
                return '<html><body><h2>No fields selected for the model</h2></body></html>'

            fields = [field.strip() for field in fields_param.split(',')]

            try:
                domain = [('id', '=', rec_id)] if rec_id != 0 else []
                records = request.env[str(model_name)].search_read(domain=domain, fields=fields)

                for record in records:
                    for key, value in record.items():
                        if isinstance(value, datetime):
                            record[key] = value.isoformat()

                return request.make_response(json.dumps({'records': records}))
            except Exception as e:
                return f'<html><body><h2>Error processing request: {str(e)}</h2></body></html>'

    @http.route(['/send_request'], type='http', auth='none', cors='*',
                methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'], csrf=False)
    def fetch_data(self, **kw):
        http_method = request.httprequest.method
        api_key = request.httprequest.headers.get('api-key')
        auth_api = self.auth_api_key(api_key)
        model = kw.get('model')
        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')

        try:
            request.session.authenticate(request.session.db, username, password)
        except Exception:
            return '<html><body><h2>Authentication failed</h2></body></html>'

        model_id = request.env['ir.model'].search([('model', '=', model)])
        if not model_id:
            return '<html><body><h3>Invalid model</h3></body></html>'

        if auth_api:
            rec_id = int(kw.get('Id', 0))
            return self.generate_response(http_method, model_id.id, rec_id)
        return auth_api

    @http.route(['/odoo_connect'], type='http', auth='none', csrf=False, methods=['GET'])
    def odoo_connect(self, **kw):
        """Initialize API transaction by generating api-key"""
        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
        db = request.httprequest.headers.get('db')

        try:
            request.session.update(http.get_default_session(), db=db)
            auth = request.session.authenticate(request.session.db, username, password)
            user = request.env['res.users'].browse(auth)
            api_key = request.env.user.generate_api(username)
            return request.make_response(json.dumps({
                "Status": "auth successful",
                "User": user.name,
                "api-key": api_key
            }))
        except Exception:
            return '<html><body><h2>Wrong login credentials</h2></body></html>'
