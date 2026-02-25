import json
import logging
from datetime import datetime


from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)




class RestApi(http.Controller):
    """This is a controller which is used to generate responses based on the
    api requests"""


    def auth_api_key(self, api_key):
        """This function is used to authenticate the api-key when sending a
        request"""
        user_id = request.env['res.users'].sudo().search([('api_key', '=', api_key)])
        if api_key is not None and user_id:
             response = True
        elif not user_id:
            response = ('<html><body><h2>Invalid <i>API Key</i> '
                        '!</h2></body></html>')
        else:
            response = ("<html><body><h2>No <i>API Key</i> Provided "
                        "!</h2></body></html>")
        return response


    # def generate_response(self, method, model, rec_id):
    #     """This function is used to generate the response based on the type
    #     of request and the parameters given"""
    #     option = request.env['connection.api'].search(
    #         [('model_id', '=', model)], limit=1)
    #     model_name = option.model_id.model
    #     if method != 'DELETE':
    #         data = json.loads(request.httprequest.data)
    #     else:
    #         data = {}
    #     fields = []
    #     if data:
    #         for field in data['fields']:
    #             fields.append(field)
    #     if not fields and method != 'DELETE':
    #         return ("<html><body><h2>No fields selected for the model"
    #                 "</h2></body></html>")
    #     if not option:
    #         return ("<html><body><h2>No Record Created for the model"
    #                 "</h2></body></html>")
    #     try:
    #         if method == 'GET':
    #             fields = []
    #             for field in data['fields']:
    #                 fields.append(field)
    #             if not option.is_get:
    #                 return ("<html><body><h2>Method Not Allowed"
    #                         "</h2></body></html>")
    #             else:
    #                 datas = []
    #                 if rec_id != 0:
    #                     partner_records = request.env[
    #                         str(model_name)
    #                     ].search_read(
    #                         domain=[('id', '=', rec_id)],
    #                         fields=fields
    #                     )


    #                     # Manually convert datetime fields to string format
    #                     for record in partner_records:
    #                         for key, value in record.items():
    #                             if isinstance(value, datetime):
    #                                 record[key] = value.isoformat()
    #                     data = json.dumps({
    #                         'records': partner_records
    #                     })
    #                     datas.append(data)
    #                     return request.make_response(data=datas)
    #                 else:
    #                     partner_records = request.env[
    #                         str(model_name)
    #                     ].search_read(
    #                         domain=[],
    #                         fields=fields
    #                     )


    #                     # Manually convert datetime fields to string format
    #                     for record in partner_records:
    #                         for key, value in record.items():
    #                             if isinstance(value, datetime):
    #                                 record[key] = value.isoformat()


    #                     data = json.dumps({
    #                         'records': partner_records
    #                     })
    #                     datas.append(data)
    #                     return request.make_response(data=datas)
    #     except:
    #         return ("<html><body><h2>Invalid JSON Data"
    #                 "</h2></body></html>")




    #     if method == 'POST':
    #         if not option.is_post:
    #             return ("<html><body><h2>Method Not Allowed"
    #                     "</h2></body></html>")
    #         else:
    #             try:
    #                 data = json.loads(request.httprequest.data)
    #                 datas = []
    #                 new_resource = request.env[str(model_name)].create(
    #                     data['values'])
    #                 partner_records = request.env[
    #                     str(model_name)].search_read(
    #                     domain=[('id', '=', new_resource.id)],
    #                     fields=fields
    #                 )
    #                 new_data = json.dumps({'New resource': partner_records, })
    #                 datas.append(new_data)
    #                 return request.make_response(data=datas)
    #             except:
    #                 return ("<html><body><h2>Invalid JSON Data"
    #                         "</h2></body></html>")
    #     if method == 'PUT':
    #         if not option.is_put:
    #             return ("<html><body><h2>Method Not Allowed"
    #                     "</h2></body></html>")
    #         else:
    #             if rec_id == 0:
    #                 return ("<html><body><h2>No ID Provided"
    #                         "</h2></body></html>")
    #             else:
    #                 resource = request.env[str(model_name)].browse(
    #                     int(rec_id))
    #                 if not resource.exists():
    #                     return ("<html><body><h2>Resource not found"
    #                             "</h2></body></html>")
    #                 else:
    #                     try:
    #                         datas = []
    #                         data = json.loads(request.httprequest.data)
    #                         resource.write(data['values'])
    #                         partner_records = request.env[
    #                             str(model_name)].search_read(
    #                             domain=[('id', '=', resource.id)],
    #                             fields=fields
    #                         )
    #                         new_data = json.dumps(
    #                             {'Updated resource': partner_records,
    #                              })
    #                         datas.append(new_data)
    #                         return request.make_response(data=datas)


    #                     except:
    #                         return ("<html><body><h2>Invalid JSON Data "
    #                                 "!</h2></body></html>")
    #     if method == 'DELETE':
    #         if not option.is_delete:
    #             return ("<html><body><h2>Method Not Allowed"
    #                     "</h2></body></html>")
    #         else:
    #             if rec_id == 0:
    #                 return ("<html><body><h2>No ID Provided"
    #                         "</h2></body></html>")
    #             else:
    #                 resource = request.env[str(model_name)].browse(
    #                     int(rec_id))
    #                 if not resource.exists():
    #                     return ("<html><body><h2>Resource not found"
    #                             "</h2></body></html>")
    #                 else:


    #                     records = request.env[
    #                         str(model_name)].search_read(
    #                         domain=[('id', '=', resource.id)],
    #                         fields=['id', 'display_name']
    #                     )
    #                     remove = json.dumps(
    #                         {"Resource deleted": records,
    #                          })
    #                     resource.unlink()
    #                     return request.make_response(data=remove)


    # @http.route(['/send_request'], type='http',
    #             auth='none',
    #             methods=['GET', 'POST', 'PUT', 'DELETE'], csrf=False)
    # def fetch_data(self, **kw):
    #     """This controller will be called when sending a request to the
    #     specified url, and it will authenticate the api-key and then will
    #     generate the result"""
    #     http_method = request.httprequest.method
    #     api_key = request.httprequest.headers.get('api-key')
    #     auth_api = self.auth_api_key(api_key)
    #     model = kw.get('model')
    #     username = request.httprequest.headers.get('login')
    #     password = request.httprequest.headers.get('password')
    #     request.session.authenticate(request.session.db, username,
    #                                  password)
    #     model_id = request.env['ir.model'].search(
    #         [('model', '=', model)])
    #     if not model_id:
    #         return ("<html><body><h3>Invalid model, check spelling or maybe "
    #                 "the related "
    #                 "module is not installed"
    #                 "</h3></body></html>")


    #     if auth_api == True:
    #         if not kw.get('Id'):
    #             rec_id = 0
    #         else:
    #             rec_id = int(kw.get('Id'))
    #         result = self.generate_response(http_method, model_id.id, rec_id)
    #         return result
    #     else:
    #         return auth_api


    def generate_response(self, method, model, rec_id):
        """This function is used to generate the response based on the type
        of request and the parameters given"""
        option = request.env['connection.api'].search(
            [('model_id', '=', model)], limit=1)
        model_name = option.model_id.model
       
        if not option:
            return ("<html><body><h2>No Record Created for the model"
                    "</h2></body></html>")


        # Handle GET method with query parameters instead of body
        if method == 'GET':
            if not option.is_get:
                return ("<html><body><h2>Method Not Allowed</h2></body></html>")
           
            # Get fields from query parameter
            fields_param = request.params.get('fields', '')
            if not fields_param:
                return ("<html><body><h2>No fields selected for the model</h2></body></html>")
           
            # Parse fields from comma-separated string
            fields = [field.strip() for field in fields_param.split(',')]
           
            try:
                datas = []
                if rec_id != 0:
                    partner_records = request.env[str(model_name)].search_read(
                        domain=[('id', '=', rec_id)],
                        fields=fields
                    )
                else:
                    partner_records = request.env[str(model_name)].search_read(
                        domain=[],
                        fields=fields
                    )


                # Convert datetime fields to string format
                for record in partner_records:
                    for key, value in record.items():
                        if isinstance(value, datetime):
                            record[key] = value.isoformat()


                data = json.dumps({
                    'records': partner_records
                })
                datas.append(data)
                return request.make_response(data=datas)
            except Exception as e:
                return ("<html><body><h2>Error processing request: "
                        f"{str(e)}</h2></body></html>")

    def generate_new_res(self, http_method, model_id, rec_id=0):
        model_name = request.env['ir.model'].browse(model_id).model
        if model_name == 'sale.order.line':
            if http_method == 'GET':
                # Ambil data dari sale.order.line
                domain = []
                if rec_id > 0:
                    domain = [('id', '=', rec_id)]
                
                # Ambil field yang diperlukan
                fields = ['name','product_id', 'price_unit', 'product_uom_qty', 'order_id']
                sale_order_lines = request.env[model_name].search_read(domain, fields)
                
                # Format respons
                result = {
                    'status': 'success',
                    'data': sale_order_lines
                }
                return json.dumps(result)
            else:
                return json.dumps({'status': 'error', 'message': 'Method not allowed'})
        else:
            return json.dumps({'status': 'error', 'message': 'Unsupported model'})


    @http.route(['/send_request'], type='http',  
            auth='none',
            cors='*',
            methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],  
            csrf=False)  
    def fetch_data(self, **kw):  
        # # Definisikan asal yang diizinkan dengan lebih spesifik  
        # allowed_origins = [  
        #     'http://localhost:5173',  # Frontend Anda  
        #     'http://localhost:5173',    # Untuk development  
        #     'http://127.0.0.1:5173',
        #     '*'     # Tambahkan variasi localhost  
        # ]  
        # # Ambil origin dari request  
        # origin = request.httprequest.headers.get('Origin', '')  
       
        # # Siapkan headers CORS yang komprehensif  
        # headers = [  
        #     ('Access-Control-Allow-Origin', origin if origin in allowed_origins else allowed_origins[0]),  
        #     ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'),  
        #     ('Access-Control-Allow-Headers', 'login, password, api-key, Content-Type'),  
        #     ('Access-Control-Allow-Credentials', 'false'),  
        #     ('Vary', 'Origin')  # Penting untuk caching dan variasi origin  
        # ]  
       
        # # Handle preflight OPTIONS request dengan lebih baik  
        # if request.httprequest.method == 'OPTIONS':  
        #     return request.make_response('', headers=headers, status=200)  


        http_method = request.httprequest.method
        api_key = request.httprequest.headers.get('api-key')
        auth_api = self.auth_api_key(api_key)
        model = kw.get('model')
        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
       
        try:
            request.session.authenticate(request.session.db, username, password)
        except Exception as e:
            return ("<html><body><h2>Authentication failed</h2></body></html>")


        model_id = request.env['ir.model'].search([('model', '=', model)])
        if not model_id:
            return ("<html><body><h3>Invalid model, check spelling or maybe "
                    "the related module is not installed"
                    "</h3></body></html>")


        if auth_api:
            rec_id = int(kw.get('Id', 0))
            result = self.generate_response(http_method, model_id.id, rec_id)
            return result
            # result = self.generate_response(http_method, model_id.id, rec_id)
            # if isinstance(result, str):  # If result is HTML string
            #     return request.make_response(result, headers=headers)
            # return request.make_response(result.data, headers=headers)
        else:
            return auth_api
        

    @http.route(['/send_new_request'], type='http',  
            auth='none',
            cors='*',
            methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],   
            csrf=False)  
    def fetch_new_data(self, **kw):    
        http_method = request.httprequest.method
        api_key = request.httprequest.headers.get('api-key')
        auth_api = self.auth_api_key(api_key)
        model = kw.get('model')
        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
        
        try:
            request.session.authenticate(request.session.db, username, password)
        except Exception as e:
            return ("<html><body><h2>Authentication failed</h2></body></html>")

        model_id = request.env['ir.model'].search([('model', '=', model)])
        if not model_id:
            return ("<html><body><h3>Invalid model, check spelling or maybe "
                    "the related module is not installed"
                    "</h3></body></html>")

        if auth_api:
            rec_id = int(kw.get('Id', 0))
            result = self.generate_new_res(http_method, model_id.id, rec_id)
            return result
        else:
            return auth_api


    @http.route(['/odoo_connect'], type="http", auth="none", csrf=False,
                methods=['GET'])
    def odoo_connect(self, **kw):
        """This is the controller which initializes the api transaction by
        generating the api-key for specific user and database"""


        username = request.httprequest.headers.get('login')
        password = request.httprequest.headers.get('password')
        db = request.httprequest.headers.get('db')
        try:
            request.session.update(http.get_default_session(), db=db)
            auth = request.session.authenticate(request.session.db, username,
                                                password)
            user = request.env['res.users'].browse(auth)
            api_key = request.env.user.generate_api(username)
            datas = json.dumps({"Status": "auth successful",
                                "User": user.name,
                                "api-key": api_key})
            return request.make_response(data=datas)
        except:
            return ("<html><body><h2>wrong login credentials"
                    "</h2></body></html>")

    @http.route(['/api/owner_dashboard/summary'], type='http', auth='none', cors='*', methods=['GET'], csrf=False)
    def fetch_dashboard_summary(self, **kw):
        """Custom endpoint for the Owner Dashboard to fetch comprehensive data."""
        dashboard_data = {
            "status": "success",
            "data": {
                "kpi": {
                    "total_revenue": 1250000000,
                    "total_orders": 3450,
                    "active_customers": 1200,
                    "cash_balance": 450000000
                },
                "finance": {
                    "accounts_receivable": 25000000,
                    "accounts_payable": 15000000,
                    "net_profit": 350000000,
                    "expenses": 120000000,
                    "assets": 2500000000,
                    "liabilities": 500000000,
                    "equity": 2000000000
                },
                "logistics": {
                    "pending_deliveries": 45,
                    "low_stock_items": 12,
                    "inventory_value": 310000000
                },
                "recent_transactions": [
                    {"id": 1, "type": "Penjualan Resort", "amount": 15000000, "date": "2026-02-20", "status": "Completed"},
                    {"id": 2, "type": "Resto & Cafe", "amount": 2500000, "date": "2026-02-20", "status": "Completed"},
                    {"id": 3, "type": "Wahana Tiket", "amount": 8000000, "date": "2026-02-19", "status": "Completed"},
                    {"id": 4, "type": "Pembelian Bahan Baku", "amount": -4500000, "date": "2026-02-19", "status": "Pending"},
                    {"id": 5, "type": "Food Court", "amount": 1200000, "date": "2026-02-18", "status": "Completed"}
                ],
                "sales_trend": [
                    {"name": "Jan", "revenue": 100000000},
                    {"name": "Feb", "revenue": 120000000},
                    {"name": "Mar", "revenue": 95000000},
                    {"name": "Apr", "revenue": 150000000},
                    {"name": "May", "revenue": 180000000},
                    {"name": "Jun", "revenue": 140000000}
                ],
                "sales_detail": {
                    "pos_revenue": 850000000,
                    "b2b_revenue": 400000000,
                    "pos_transactions": 3100,
                    "b2b_orders": 350,
                    "top_products": [
                        {"name": "Tiket Masuk Wahana", "qty": 1500, "revenue": 150000000, "category": "Wahana"},
                        {"name": "Kamar Deluxe Resort", "qty": 350, "revenue": 350000000, "category": "Resort"},
                        {"name": "Paket Nasi Timbel Komplit", "qty": 850, "revenue": 42500000, "category": "Resto"},
                        {"name": "Sewa Gazebo", "qty": 420, "revenue": 42000000, "category": "Resort"},
                        {"name": "Es Kelapa Muda Jeruk", "qty": 1200, "revenue": 24000000, "category": "Resto"}
                    ],
                    "revenue_by_unit": [
                        {"name": "Resort", "value": 650000000, "color": "#10b981"},
                        {"name": "Wahana", "value": 350000000, "color": "#3b82f6"},
                        {"name": "Resto & Cafe", "value": 180000000, "color": "#f59e0b"},
                        {"name": "Food Court", "value": 70000000, "color": "#8b5cf6"}
                    ]
                },
                "finance_detail": {
                    "cashflow": [
                        {"name": "Jan", "in": 120000000, "out": 85000000},
                        {"name": "Feb", "in": 135000000, "out": 90000000},
                        {"name": "Mar", "in": 115000000, "out": 105000000},
                        {"name": "Apr", "in": 160000000, "out": 95000000},
                        {"name": "May", "in": 190000000, "out": 110000000},
                        {"name": "Jun", "in": 145000000, "out": 120000000}
                    ],
                    "expense_breakdown": [
                        {"name": "Gaji & Tunjangan", "value": 55000000, "color": "#ef4444"},
                        {"name": "Operasional & Maintenance", "value": 35000000, "color": "#f59e0b"},
                        {"name": "Marketing & Promosi", "value": 15000000, "color": "#8b5cf6"},
                        {"name": "Utility (Listrik/Air)", "value": 15000000, "color": "#06b6d4"}
                    ],
                    "income_statement": {
                        "revenue": 1250000000,
                        "cogs": 450000000,
                        "gross_profit": 800000000,
                        "operating_expenses": 350000000,
                        "depreciation": 50000000,
                        "net_profit_before_tax": 400000000,
                        "tax": 50000000,
                        "net_profit": 350000000
                    },
                    "balance_sheet": {
                        "current_assets": {
                            "cash_and_bank": 450000000,
                            "accounts_receivable": 25000000,
                            "inventory": 310000000,
                            "prepaid_expenses": 15000000,
                            "total": 800000000
                        },
                        "non_current_assets": {
                            "property_equipment": 1500000000,
                            "accumulated_depreciation": -200000000,
                            "intangible_assets": 100000000,
                            "other_assets": 300000000,
                            "total": 1700000000
                        },
                        "total_assets": 2500000000,
                        "current_liabilities": {
                            "accounts_payable": 15000000,
                            "accrued_expenses": 35000000,
                            "short_term_debt": 50000000,
                            "taxes_payable": 20000000,
                            "total": 120000000
                        },
                        "non_current_liabilities": {
                            "long_term_debt": 350000000,
                            "other_liabilities": 30000000,
                            "total": 380000000
                        },
                        "total_liabilities": 500000000,
                        "equity": {
                            "capital_stock": 1500000000,
                            "retained_earnings": 500000000,
                            "total": 2000000000
                        }
                    }
                },
                "logistics_detail": {
                    "inventory_by_category": [
                        {"name": "Bahan Makanan", "value": 120000000, "items": 245, "color": "#10b981"},
                        {"name": "Minuman", "value": 45000000, "items": 120, "color": "#3b82f6"},
                        {"name": "Perlengkapan Kamar", "value": 85000000, "items": 180, "color": "#f59e0b"},
                        {"name": "Alat Kebersihan", "value": 25000000, "items": 95, "color": "#8b5cf6"},
                        {"name": "Spare Part Wahana", "value": 35000000, "items": 45, "color": "#ef4444"}
                    ],
                    "low_stock_alerts": [
                        {"name": "Beras Premium 25kg", "current_stock": 5, "min_stock": 20, "unit": "Karung", "category": "Bahan Makanan"},
                        {"name": "Minyak Goreng 18L", "current_stock": 8, "min_stock": 25, "unit": "Jerigen", "category": "Bahan Makanan"},
                        {"name": "Handuk Mandi Putih", "current_stock": 15, "min_stock": 50, "unit": "Pcs", "category": "Perlengkapan Kamar"},
                        {"name": "Sabun Cair 5L", "current_stock": 3, "min_stock": 15, "unit": "Galon", "category": "Alat Kebersihan"},
                        {"name": "Tisu Toilet 12 Roll", "current_stock": 10, "min_stock": 40, "unit": "Pack", "category": "Perlengkapan Kamar"}
                    ],
                    "pending_orders": [
                        {"id": "PO-2026-0245", "vendor": "CV Sumber Pangan", "items": 15, "total": 12500000, "expected_date": "2026-02-27", "status": "In Transit"},
                        {"id": "PO-2026-0244", "vendor": "PT Linen Indonesia", "items": 8, "total": 8500000, "expected_date": "2026-02-28", "status": "Processing"},
                        {"id": "PO-2026-0243", "vendor": "UD Bersih Cemerlang", "items": 12, "total": 4200000, "expected_date": "2026-03-01", "status": "Processing"},
                        {"id": "PO-2026-0242", "vendor": "PT Wahana Parts", "items": 5, "total": 15000000, "expected_date": "2026-03-02", "status": "Confirmed"}
                    ],
                    "delivery_status": {
                        "in_transit": 3,
                        "processing": 8,
                        "confirmed": 5,
                        "completed_this_week": 12
                    }
                },
                "pos_summary": {
                    "today": {
                        "transactions": 156,
                        "revenue": 28500000,
                        "avg_ticket": 182692
                    },
                    "this_week": {
                        "transactions": 892,
                        "revenue": 165000000,
                        "avg_ticket": 185022
                    },
                    "this_month": {
                        "transactions": 3100,
                        "revenue": 850000000,
                        "avg_ticket": 274193
                    }
                }
            }
        }

        try:
            # Attempt to gather real data from Odoo if possible

            SaleOrder = request.env.get('sale.order')
            if SaleOrder is not None:
                sales = SaleOrder.sudo().search_read([('state', 'in', ['sale', 'done'])], ['amount_total'])
                real_revenue = sum(s['amount_total'] for s in sales)
                if real_revenue > 0:
                    dashboard_data['data']['kpi']['total_revenue'] = real_revenue
                    dashboard_data['data']['kpi']['total_orders'] = len(sales)

            AccountMove = request.env.get('account.move')
            if AccountMove is not None:
                invoices = AccountMove.sudo().search_read([('move_type', '=', 'out_invoice'), ('state', '=', 'posted')], ['amount_total_signed', 'amount_residual_signed'])
                dashboard_data['data']['finance']['accounts_receivable'] = sum(inv['amount_residual_signed'] for inv in invoices)

        except Exception as e:
            import logging
            _logger = logging.getLogger(__name__)
            _logger.warning("Could not fetch real Odoo data for dashboard summary: %s", str(e))

        return request.make_response(
            json.dumps(dashboard_data), 
            headers=[('Content-Type', 'application/json')]
        )