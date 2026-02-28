import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LayoutDashboard,
  TrendingUp,
  CreditCard,
  Package,
  Activity,
  DollarSign,
  Users,
  ShoppingCart,
  Wallet,
  ArrowUpRight,
  ArrowDownRight,
  Store,
  Tag,
  BarChart2,
  PieChart as PieChartIcon,
  Menu,
  X,
  AlertTriangle,
  Truck,
  ClipboardList,
  Building2
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  BarChart,
  Bar
} from 'recharts';

// Mock data fallback in case Odoo API goes down or CORS fails
const mockDataFallback = {
  kpi: {
    total_revenue: 1250000000,
    total_orders: 3450,
    active_customers: 1200,
    cash_balance: 450000000
  },
  finance: {
    accounts_receivable: 25000000,
    accounts_payable: 15000000,
    net_profit: 350000000,
    expenses: 120000000,
    assets: 2500000000,
    liabilities: 500000000,
    equity: 2000000000
  },
  logistics: {
    pending_deliveries: 45,
    low_stock_items: 12,
    inventory_value: 310000000
  },
  recent_transactions: [
    { id: 1, type: "Penjualan Resort", amount: 15000000, date: "2026-02-20", status: "Completed" },
    { id: 2, type: "Resto & Cafe", amount: 2500000, date: "2026-02-20", status: "Completed" },
    { id: 3, type: "Wahana Tiket", amount: 8000000, date: "2026-02-19", status: "Completed" },
    { id: 4, type: "Pembelian Bahan Baku", amount: -4500000, date: "2026-02-19", status: "Pending" },
    { id: 5, type: "Food Court", amount: 1200000, date: "2026-02-18", status: "Completed" }
  ],
  sales_trend: [
    { name: "Jan", revenue: 100000000 },
    { name: "Feb", revenue: 120000000 },
    { name: "Mar", revenue: 95000000 },
    { name: "Apr", revenue: 150000000 },
    { name: "May", revenue: 180000000 },
    { name: "Jun", revenue: 140000000 }
  ],
  sales_detail: {
    pos_revenue: 850000000,
    b2b_revenue: 400000000,
    pos_transactions: 3100,
    b2b_orders: 350,
    top_products: [
      { name: "Tiket Masuk Wahana", qty: 1500, revenue: 150000000, category: "Wahana" },
      { name: "Kamar Deluxe Resort", qty: 350, revenue: 350000000, category: "Resort" },
      { name: "Paket Nasi Timbel Komplit", qty: 850, revenue: 42500000, category: "Resto" },
      { name: "Sewa Gazebo", qty: 420, revenue: 42000000, category: "Resort" },
      { name: "Es Kelapa Muda Jeruk", qty: 1200, revenue: 24000000, category: "Resto" }
    ],
    revenue_by_unit: [
      { name: "Resort", value: 650000000, color: "#10b981" },
      { name: "Wahana", value: 350000000, color: "#3b82f6" },
      { name: "Resto & Cafe", value: 180000000, color: "#f59e0b" },
      { name: "Food Court", value: 70000000, color: "#8b5cf6" }
    ]
  },
  finance_detail: {
    cashflow: [
      { name: "Jan", in: 120000000, out: 85000000 },
      { name: "Feb", in: 135000000, out: 90000000 },
      { name: "Mar", in: 115000000, out: 105000000 },
      { name: "Apr", in: 160000000, out: 95000000 },
      { name: "May", in: 190000000, out: 110000000 },
      { name: "Jun", in: 145000000, out: 120000000 }
    ],
    expense_breakdown: [
      { name: "Gaji & Tunjangan", value: 55000000, color: "#ef4444" },
      { name: "Operasional", value: 35000000, color: "#f59e0b" },
      { name: "Marketing", value: 15000000, color: "#8b5cf6" },
      { name: "Utility", value: 15000000, color: "#06b6d4" }
    ],
    income_statement: {
      revenue: 1250000000,
      cogs: 450000000,
      gross_profit: 800000000,
      operating_expenses: 350000000,
      depreciation: 50000000,
      net_profit_before_tax: 400000000,
      tax: 50000000,
      net_profit: 350000000
    },
    balance_sheet: {
      current_assets: {
        cash_and_bank: 450000000,
        accounts_receivable: 25000000,
        inventory: 310000000,
        prepaid_expenses: 15000000,
        total: 800000000
      },
      non_current_assets: {
        property_equipment: 1500000000,
        accumulated_depreciation: -200000000,
        intangible_assets: 100000000,
        other_assets: 300000000,
        total: 1700000000
      },
      total_assets: 2500000000,
      current_liabilities: {
        accounts_payable: 15000000,
        accrued_expenses: 35000000,
        short_term_debt: 50000000,
        taxes_payable: 20000000,
        total: 120000000
      },
      non_current_liabilities: {
        long_term_debt: 350000000,
        other_liabilities: 30000000,
        total: 380000000
      },
      total_liabilities: 500000000,
      equity: {
        capital_stock: 1500000000,
        retained_earnings: 500000000,
        total: 2000000000
      }
    }
  },
  logistics_detail: {
    inventory_by_category: [
      { name: "Bahan Makanan", value: 120000000, items: 245, color: "#10b981" },
      { name: "Minuman", value: 45000000, items: 120, color: "#3b82f6" },
      { name: "Perlengkapan Kamar", value: 85000000, items: 180, color: "#f59e0b" },
      { name: "Alat Kebersihan", value: 25000000, items: 95, color: "#8b5cf6" },
      { name: "Spare Part Wahana", value: 35000000, items: 45, color: "#ef4444" }
    ],
    low_stock_alerts: [
      { name: "Beras Premium 25kg", current_stock: 5, min_stock: 20, unit: "Karung", category: "Bahan Makanan" },
      { name: "Minyak Goreng 18L", current_stock: 8, min_stock: 25, unit: "Jerigen", category: "Bahan Makanan" },
      { name: "Handuk Mandi Putih", current_stock: 15, min_stock: 50, unit: "Pcs", category: "Perlengkapan Kamar" },
      { name: "Sabun Cair 5L", current_stock: 3, min_stock: 15, unit: "Galon", category: "Alat Kebersihan" },
      { name: "Tisu Toilet 12 Roll", current_stock: 10, min_stock: 40, unit: "Pack", category: "Perlengkapan Kamar" }
    ],
    pending_orders: [
      { id: "PO-2026-0245", vendor: "CV Sumber Pangan", items: 15, total: 12500000, expected_date: "2026-02-27", status: "In Transit" },
      { id: "PO-2026-0244", vendor: "PT Linen Indonesia", items: 8, total: 8500000, expected_date: "2026-02-28", status: "Processing" },
      { id: "PO-2026-0243", vendor: "UD Bersih Cemerlang", items: 12, total: 4200000, expected_date: "2026-03-01", status: "Processing" },
      { id: "PO-2026-0242", vendor: "PT Wahana Parts", items: 5, total: 15000000, expected_date: "2026-03-02", status: "Confirmed" }
    ],
    delivery_status: {
      in_transit: 3,
      processing: 8,
      confirmed: 5,
      completed_this_week: 12
    }
  },
  pos_summary: {
    today: { transactions: 156, revenue: 28500000, avg_ticket: 182692 },
    this_week: { transactions: 892, revenue: 165000000, avg_ticket: 185022 },
    this_month: { transactions: 3100, revenue: 850000000, avg_ticket: 274193 }
  }
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
};

function InitialLoadingScreen() {
  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-100 flex items-center justify-center relative overflow-hidden">
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-[120px] pointer-events-none"></div>

      <div className="relative z-10 w-full max-w-lg mx-4 rounded-2xl border border-slate-700/60 bg-[#1e293b]/80 backdrop-blur-md p-8 text-center shadow-2xl">
        <div className="mx-auto mb-6 h-14 w-14 rounded-full border-2 border-slate-700 border-t-emerald-400 animate-spin"></div>
        <h1 className="text-2xl font-semibold text-white">Memuat dashboard owner</h1>
        <p className="mt-3 text-slate-300">Data sedang diproses. Mohon tunggu beberapa saat.</p>
        <p className="mt-2 text-sm text-slate-400">Dataset awal cukup besar sehingga proses sinkronisasi bisa memerlukan waktu lebih lama.</p>
      </div>
    </div>
  );
}

export default function App() {
  const [data, setData] = useState(mockDataFallback);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    // Fetch from Odoo custom API endpoint
    const fetchData = async () => {
      try {
        const response = await axios.get('https://103.187.114.7:1314/api/owner_dashboard/summary');
        if (response.data && response.data.status === 'success') {
          // If the structure diverges, we map it, but the python controller provides it cleanly:
          setData(response.data.data);
        }
      } catch (err) {
        console.warn("Failed to fetch from Odoo API, using mock data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case 'penjualan':
        return <PenjualanTab data={data} />;
      case 'keuangan':
        return <KeuanganTab data={data} />;
      case 'logistik':
        return <LogistikTab data={data} />;
      case 'dashboard':
      default:
        return <DashboardOverview data={data} />;
    }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setMobileMenuOpen(false);
  };

  if (loading) {
    return <InitialLoadingScreen />;
  }

  return (
    <div className="flex h-screen bg-[#0f172a] text-slate-100 font-sans overflow-hidden">
      {/* Mobile Menu Overlay */}
      {mobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar - Desktop */}
      <aside className="w-64 bg-[#1e293b] border-r border-slate-700/50 hidden md:flex flex-col z-20">
        <div className="h-16 flex items-center px-6 border-b border-slate-700/50">
          <div className="flex items-center gap-2 text-emerald-400">
            <Activity className="w-6 h-6" />
            <span className="text-xl font-bold tracking-tight text-white">GTP<span className="text-emerald-400 font-light">Owner</span></span>
          </div>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <SidebarItem
            icon={<LayoutDashboard className="w-5 h-5" />}
            label="Dashboard"
            active={activeTab === 'dashboard'}
            onClick={() => handleTabChange('dashboard')}
          />
          <SidebarItem
            icon={<ShoppingCart className="w-5 h-5" />}
            label="Penjualan & POS"
            active={activeTab === 'penjualan'}
            onClick={() => handleTabChange('penjualan')}
          />
          <SidebarItem
            icon={<TrendingUp className="w-5 h-5" />}
            label="Keuangan"
            active={activeTab === 'keuangan'}
            onClick={() => handleTabChange('keuangan')}
          />
          <SidebarItem
            icon={<Package className="w-5 h-5" />}
            label="Logistik"
            active={activeTab === 'logistik'}
            onClick={() => handleTabChange('logistik')}
          />
        </nav>
        <div className="p-4 border-t border-slate-700/50">
          <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-slate-800/50">
            <div className="w-10 h-10 rounded-full bg-linear-to-tr from-emerald-400 to-cyan-500 flex items-center justify-center text-white font-bold">
              OW
            </div>
            <div>
              <p className="text-sm font-semibold text-white">Owner</p>
              <p className="text-xs text-slate-400">Super Admin</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Mobile Sidebar */}
      <aside className={`fixed top-0 left-0 h-full w-64 bg-[#1e293b] border-r border-slate-700/50 flex flex-col z-40 transform transition-transform duration-300 md:hidden ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-700/50">
          <div className="flex items-center gap-2 text-emerald-400">
            <Activity className="w-6 h-6" />
            <span className="text-xl font-bold tracking-tight text-white">GTP<span className="text-emerald-400 font-light">Owner</span></span>
          </div>
          <button onClick={() => setMobileMenuOpen(false)} className="p-2 text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <SidebarItem
            icon={<LayoutDashboard className="w-5 h-5" />}
            label="Dashboard"
            active={activeTab === 'dashboard'}
            onClick={() => handleTabChange('dashboard')}
          />
          <SidebarItem
            icon={<ShoppingCart className="w-5 h-5" />}
            label="Penjualan & POS"
            active={activeTab === 'penjualan'}
            onClick={() => handleTabChange('penjualan')}
          />
          <SidebarItem
            icon={<TrendingUp className="w-5 h-5" />}
            label="Keuangan"
            active={activeTab === 'keuangan'}
            onClick={() => handleTabChange('keuangan')}
          />
          <SidebarItem
            icon={<Package className="w-5 h-5" />}
            label="Logistik"
            active={activeTab === 'logistik'}
            onClick={() => handleTabChange('logistik')}
          />
        </nav>
        <div className="p-4 border-t border-slate-700/50">
          <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-slate-800/50">
            <div className="w-10 h-10 rounded-full bg-linear-to-tr from-emerald-400 to-cyan-500 flex items-center justify-center text-white font-bold">
              OW
            </div>
            <div>
              <p className="text-sm font-semibold text-white">Owner</p>
              <p className="text-xs text-slate-400">Super Admin</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-y-auto w-full relative">
        {/* Background glow effects */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-emerald-500/5 rounded-full blur-[100px] pointer-events-none"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none"></div>

        {/* Header */}
        <header className="h-16 bg-[#1e293b]/50 backdrop-blur-md border-b border-slate-700/50 flex shrink-0 items-center justify-between px-4 md:px-6 sticky top-0 z-10">
          <div className="flex items-center gap-3">
            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(true)}
              className="p-2 text-slate-400 hover:text-white md:hidden"
            >
              <Menu className="w-6 h-6" />
            </button>
            <div>
              <h1 className="text-lg md:text-xl font-semibold text-white capitalize">
                {activeTab === 'dashboard' ? 'Ringkasan Bisnis' :
                  activeTab === 'penjualan' ? 'Analisis Penjualan & POS' :
                    activeTab === 'keuangan' ? 'Laporan Keuangan' : 'Manajemen Logistik'}
              </h1>
              <p className="text-xs text-slate-400 hidden sm:block">
                {activeTab === 'dashboard' ? 'Ikhtisar performa seluruh unit usaha (Resort, Resto, Wahana).' :
                  activeTab === 'penjualan' ? 'Rincian transaksi POS, produk terlaris, dan distribusi pendapatan.' :
                    activeTab === 'keuangan' ? 'Detail arus kas, laba rugi, dan rasio keuangan.' :
                      'Pantauan inventaris, stok, dan purchase order.'}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 md:gap-4 text-sm">
            <div className="bg-slate-800 px-2 md:px-3 py-1.5 rounded-full border border-slate-700 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-slate-300 hidden sm:inline">Live Update</span>
            </div>
          </div>
        </header>

        <div className="p-6 space-y-6 max-w-7xl mx-auto w-full relative z-10">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

function SidebarItem({ icon, label, active, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all text-left ${active
        ? 'bg-emerald-500/10 text-emerald-400 font-medium'
        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 font-medium'
        }`}
    >
      {icon}
      <span>{label}</span>
      {active && <div className="ml-auto w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.8)]"></div>}
    </button>
  );
}

// --- TAB: DASHBOARD OVERVIEW --- 
function DashboardOverview({ data }) {
  return (
    <>
      {/* KPI Cards Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Pendapatan"
          value={formatCurrency(data.kpi.total_revenue)}
          icon={<DollarSign className="w-5 h-5" />}
          trend="+12.5%"
          trendUp={true}
          gradient="from-emerald-500/20 to-teal-500/5"
          color="text-emerald-400"
        />
        <KPICard
          title="Total Transaksi"
          value={data.kpi.total_orders.toLocaleString()}
          icon={<ShoppingCart className="w-5 h-5" />}
          trend="+5.2%"
          trendUp={true}
          gradient="from-blue-500/20 to-indigo-500/5"
          color="text-blue-400"
        />
        <KPICard
          title="Laba Bersih"
          value={formatCurrency(data.finance.net_profit)}
          icon={<CreditCard className="w-5 h-5" />}
          trend="+18.4%"
          trendUp={true}
          gradient="from-purple-500/20 to-pink-500/5"
          color="text-purple-400"
        />
        <KPICard
          title="Kas & Bank"
          value={formatCurrency(data.kpi.cash_balance)}
          icon={<Wallet className="w-5 h-5" />}
          trend="-2.1%"
          trendUp={false}
          gradient="from-amber-500/20 to-orange-500/5"
          color="text-amber-400"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart Area */}
        <div className="lg:col-span-2 bg-[#1e293b] rounded-2xl border border-slate-700/50 p-6 shadow-xl relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl -mr-20 -mt-20 pointer-events-none group-hover:bg-emerald-500/10 transition-colors duration-500"></div>

          <div className="flex justify-between items-center mb-6 relative z-10">
            <div>
              <h2 className="text-lg font-semibold text-white">Tren Pendapatan 6 Bulan</h2>
              <p className="text-sm text-slate-400">Pertumbuhan stabil di seluruh unit.</p>
            </div>
            <select className="bg-slate-800 border border-slate-700 text-sm rounded-lg px-3 py-1.5 focus:ring-emerald-500 focus:border-emerald-500 outline-none">
              <option>Tahun ini</option>
              <option>6 Bulan Terakhir</option>
            </select>
          </div>
          <div className="h-72 relative z-10">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.sales_trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" opacity={0.5} />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} tickFormatter={(value) => `${value / 1000000}M`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }}
                  itemStyle={{ color: '#e2e8f0' }}
                  formatter={(value) => [formatCurrency(value), "Pendapatan"]}
                />
                <Area type="monotone" dataKey="revenue" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorRevenue)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Neraca Keuangan Summary */}
        <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 p-6 shadow-xl flex flex-col justify-between relative overflow-hidden">
          <div className="absolute top-0 right-0 w-40 h-40 bg-blue-500/5 rounded-full blur-2xl -mr-10 -mt-10 pointer-events-none"></div>

          <div>
            <h2 className="text-lg font-semibold text-white mb-1">Neraca Keuangan</h2>
            <p className="text-sm text-slate-400 mb-6">Ringkasan aset & kewajiban saat ini.</p>

            <div className="space-y-4">
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Total Aset</span>
                  <span className="font-semibold text-blue-400">{formatCurrency(data.finance.assets)}</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-1.5 mt-2">
                  <div className="bg-blue-400 h-1.5 rounded-full" style={{ width: '100%' }}></div>
                </div>
              </div>

              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Kewajiban (Hutang)</span>
                  <span className="font-semibold text-rose-400">{formatCurrency(data.finance.liabilities)}</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-1.5 mt-2">
                  {/* Calculate ratio roughly 20% for demo UI width */}
                  <div className="bg-rose-400 h-1.5 rounded-full" style={{ width: `${(data.finance.liabilities / data.finance.assets) * 100}%` }}></div>
                </div>
              </div>

              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-400">Ekuitas (Modal)</span>
                  <span className="font-semibold text-emerald-400">{formatCurrency(data.finance.equity)}</span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-1.5 mt-2">
                  <div className="bg-emerald-400 h-1.5 rounded-full" style={{ width: `${(data.finance.equity / data.finance.assets) * 100}%` }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-8">
        {/* Recent Transactions */}
        <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 shadow-xl overflow-hidden">
          <div className="p-6 border-b border-slate-700/50 flex justify-between items-center bg-slate-800/20">
            <h2 className="text-lg font-semibold text-white">Transaksi Terbaru</h2>
            <button className="text-sm text-emerald-400 hover:text-emerald-300 transition-colors">Lihat Semua</button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase bg-slate-800/50">
                <tr>
                  <th className="px-6 py-3 font-medium">Keterangan</th>
                  <th className="px-6 py-3 font-medium">Tanggal</th>
                  <th className="px-6 py-3 font-medium">Status</th>
                  <th className="px-6 py-3 font-medium text-right">Nilai</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_transactions.map((trx, idx) => (
                  <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 font-medium text-slate-200">{trx.type}</td>
                    <td className="px-6 py-4 text-slate-400">{trx.date}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2.5 py-1 rounded-full text-xs font-medium border ${trx.status === 'Completed' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-amber-500/10 text-amber-400 border-amber-500/20'}`}>
                        {trx.status}
                      </span>
                    </td>
                    <td className={`px-6 py-4 text-right font-medium ${trx.amount < 0 ? 'text-rose-400' : 'text-slate-200'}`}>
                      {formatCurrency(trx.amount)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Logistics Status */}
        <div className="bg-gradient-to-br from-indigo-900/40 to-slate-900 rounded-2xl border border-slate-700/50 p-6 shadow-xl relative overflow-hidden">
          <div className="absolute -bottom-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

          <h2 className="text-lg font-semibold text-white mb-1 relative z-10">Status Logistik & Inventaris</h2>
          <p className="text-sm text-slate-400 mb-6 relative z-10">Pantauan pengadaan bahan baku resort & resto.</p>

          <div className="grid grid-cols-2 gap-4 relative z-10">
            <div className="bg-slate-800/60 p-5 rounded-2xl border border-slate-700/50 backdrop-blur-sm hover:border-indigo-500/30 transition-colors">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-full bg-amber-500/10 flex items-center justify-center text-amber-400">
                  <Package className="w-5 h-5" />
                </div>
                <span className="text-sm font-medium text-slate-300">Menunggu Kirim</span>
              </div>
              <p className="text-3xl font-bold text-white">{data.logistics.pending_deliveries}</p>
              <p className="text-xs text-slate-400 mt-1">PO aktif</p>
            </div>

            <div className="bg-slate-800/60 p-5 rounded-2xl border border-slate-700/50 backdrop-blur-sm hover:border-indigo-500/30 transition-colors">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-10 rounded-full bg-rose-500/10 flex items-center justify-center text-rose-400">
                  <TrendingUp className="w-5 h-5 transform rotate-180" />
                </div>
                <span className="text-sm font-medium text-slate-300">Stok Menipis</span>
              </div>
              <p className="text-3xl font-bold text-white">{data.logistics.low_stock_items}</p>
              <p className="text-xs text-slate-400 mt-1">Item butuh restock</p>
            </div>

            <div className="col-span-2 bg-slate-800/60 p-5 rounded-2xl border border-slate-700/50 backdrop-blur-sm mt-2 flex items-center justify-between hover:border-indigo-500/30 transition-colors group">
              <div>
                <span className="text-sm font-medium text-slate-400 block mb-1">Total Nilai Inventaris</span>
                <p className="text-2xl font-bold text-indigo-300">{formatCurrency(data.logistics.inventory_value)}</p>
              </div>
              <div className="w-12 h-12 rounded-full bg-indigo-500/10 flex items-center justify-center text-indigo-400 group-hover:bg-indigo-500/20 group-hover:scale-110 transition-all">
                <Package className="w-6 h-6" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
// --- TAB: PENJUALAN & POS ---
function PenjualanTab({ data }) {
  const [pieActiveIndex, setPieActiveIndex] = useState(0);

  const onPieEnter = (_, index) => {
    setPieActiveIndex(index);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-linear-to-br from-[#1e293b] to-slate-800 rounded-2xl border border-slate-700/50 p-6 shadow-xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 rounded-lg bg-emerald-500/10 text-emerald-400"><Store className="w-6 h-6" /></div>
            <div>
              <p className="text-sm font-medium text-slate-400">Pendapatan Ritel & POS</p>
              <h3 className="text-2xl font-bold text-white">{formatCurrency(data.sales_detail.pos_revenue)}</h3>
            </div>
          </div>
          <div className="flex justify-between items-center pt-4 border-t border-slate-700/50">
            <span className="text-sm text-slate-400">Total Transaksi POS</span>
            <span className="font-semibold text-emerald-400">{data.sales_detail.pos_transactions.toLocaleString()}</span>
          </div>
        </div>

        <div className="bg-linear-to-br from-[#1e293b] to-slate-800 rounded-2xl border border-slate-700/50 p-6 shadow-xl">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-3 rounded-lg bg-blue-500/10 text-blue-400"><Tag className="w-6 h-6" /></div>
            <div>
              <p className="text-sm font-medium text-slate-400">Pendapatan B2B & Kontrak</p>
              <h3 className="text-2xl font-bold text-white">{formatCurrency(data.sales_detail.b2b_revenue)}</h3>
            </div>
          </div>
          <div className="flex justify-between items-center pt-4 border-t border-slate-700/50">
            <span className="text-sm text-slate-400">Total Reservasi/Order</span>
            <span className="font-semibold text-blue-400">{data.sales_detail.b2b_orders.toLocaleString()}</span>
          </div>
        </div>

        <div className="bg-linear-to-br from-[#1e293b] to-slate-800 rounded-2xl border border-slate-700/50 p-6 shadow-xl flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-slate-400 mb-2">Rata-rata Nilai Transaksi</p>
            <div className="flex items-end gap-2">
              <h3 className="text-3xl font-bold text-white">{formatCurrency((data.sales_detail.pos_revenue + data.sales_detail.b2b_revenue) / (data.sales_detail.pos_transactions + data.sales_detail.b2b_orders))}</h3>
            </div>
            <div className="mt-3 inline-flex items-center text-xs font-semibold px-2 py-1 rounded border border-emerald-500/20 text-emerald-400 bg-emerald-400/10">
              <TrendingUp className="w-3 h-3 mr-1" /> Stabil
            </div>
          </div>
          <PieChartIcon className="w-16 h-16 text-slate-700" />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 bg-[#1e293b] rounded-2xl border border-slate-700/50 p-6 shadow-xl">
          <h2 className="text-lg font-semibold text-white mb-6">Distribusi per Unit</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data.sales_detail.revenue_by_unit}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  onMouseEnter={onPieEnter}
                >
                  {data.sales_detail.revenue_by_unit.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value) => formatCurrency(value)}
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-2 bg-[#1e293b] rounded-2xl border border-slate-700/50 p-6 shadow-xl">
          <h2 className="text-lg font-semibold text-white mb-6">Top 5 Produk Terlaris</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase bg-slate-800/50">
                <tr>
                  <th className="px-6 py-3 font-medium rounded-tl-lg">Nama Produk</th>
                  <th className="px-6 py-3 font-medium">Kategori</th>
                  <th className="px-6 py-3 font-medium text-right">Terjual (Qty)</th>
                  <th className="px-6 py-3 font-medium text-right rounded-tr-lg">Total Pendapatan</th>
                </tr>
              </thead>
              <tbody>
                {data.sales_detail.top_products.map((item, idx) => (
                  <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                    <td className="px-6 py-4 font-medium text-slate-200">{item.name}</td>
                    <td className="px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium border
                            ${item.category === 'Resort' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                          item.category === 'Resto' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                            'bg-blue-500/10 text-blue-400 border-blue-500/20'}`}>
                        {item.category}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right text-slate-300">{item.qty.toLocaleString()}</td>
                    <td className="px-6 py-4 text-right font-medium text-emerald-400">{formatCurrency(item.revenue)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

// --- TAB: KEUANGAN ---
function KeuanganTab({ data }) {
  const balanceSheet = data.finance_detail?.balance_sheet;

  // Calculate financial ratios
  const currentRatio = balanceSheet ? (balanceSheet.current_assets.total / balanceSheet.current_liabilities.total).toFixed(2) : 0;
  const debtToEquity = balanceSheet ? (balanceSheet.total_liabilities / balanceSheet.equity.total).toFixed(2) : 0;
  const quickRatio = balanceSheet ? ((balanceSheet.current_assets.total - balanceSheet.current_assets.inventory) / balanceSheet.current_liabilities.total).toFixed(2) : 0;

  return (
    <div className="space-y-6 animate-in fade-in duration-500 pb-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Revenue" value={formatCurrency(data.finance_detail.income_statement.revenue)} icon={<TrendingUp className="w-5 h-5" />} trend="+10%" trendUp={true} gradient="from-blue-500/20" color="text-blue-400" />
        <KPICard title="HPP (COGS)" value={formatCurrency(data.finance_detail.income_statement.cogs)} icon={<Package className="w-5 h-5" />} trend="-2%" trendUp={true} gradient="from-slate-500/20" color="text-slate-400" />
        <KPICard title="Biaya Operasional" value={formatCurrency(data.finance_detail.income_statement.operating_expenses)} icon={<Activity className="w-5 h-5" />} trend="+5%" trendUp={false} gradient="from-rose-500/20" color="text-rose-400" />
        <KPICard title="EBITDA" value={formatCurrency(data.finance_detail.income_statement.net_profit_before_tax)} icon={<BarChart2 className="w-5 h-5" />} trend="+15%" trendUp={true} gradient="from-emerald-500/20" color="text-emerald-400" />
      </div>

      {/* Cashflow & P&L */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-[#1e293b] rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-white">Arus Kas (Cashflow)</h2>
            <p className="text-sm text-slate-400">Pemasukan vs Pengeluaran per bulan.</p>
          </div>
          <div className="h-64 md:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.finance_detail.cashflow} margin={{ top: 20, right: 10, left: -10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" opacity={0.5} />
                <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
                <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} tickFormatter={(value) => `${value / 1000000}M`} />
                <Tooltip
                  cursor={{ fill: '#334155', opacity: 0.2 }}
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(value) => formatCurrency(value)}
                />
                <Legend />
                <Bar dataKey="in" name="Uang Masuk" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="out" name="Uang Keluar" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-1 bg-[#1e293b] rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl flex flex-col justify-between">
          <div>
            <h2 className="text-lg font-semibold text-white mb-6">Laporan Laba Rugi</h2>
            <div className="space-y-3">
              <div className="flex justify-between text-sm py-2 border-b border-slate-700">
                <span className="text-slate-300">Pendapatan Kotor</span>
                <span className="font-medium text-emerald-400">{formatCurrency(data.finance_detail.income_statement.revenue)}</span>
              </div>
              <div className="flex justify-between text-sm py-2 border-b border-slate-700">
                <span className="text-slate-400">- Harga Pokok Penjualan</span>
                <span className="text-rose-400">{formatCurrency(data.finance_detail.income_statement.cogs)}</span>
              </div>
              <div className="flex justify-between text-sm py-2 bg-slate-800/50 px-2 rounded font-semibold">
                <span className="text-slate-200">Laba Kotor</span>
                <span className="text-blue-400">{formatCurrency(data.finance_detail.income_statement.gross_profit)}</span>
              </div>
              <div className="flex justify-between text-sm py-2 border-b border-slate-700 mt-4">
                <span className="text-slate-400">- Biaya Operasional</span>
                <span className="text-rose-400">{formatCurrency(data.finance_detail.income_statement.operating_expenses)}</span>
              </div>
              <div className="flex justify-between text-sm py-2 border-b border-slate-700">
                <span className="text-slate-400">- Depresiasi & Pajak</span>
                <span className="text-rose-400">{formatCurrency(data.finance_detail.income_statement.depreciation + data.finance_detail.income_statement.tax)}</span>
              </div>
              <div className="flex justify-between text-base py-3 mt-4 border-t-2 border-slate-600 font-bold">
                <span className="text-white">Net Laba Bersih</span>
                <span className="text-emerald-400">{formatCurrency(data.finance_detail.income_statement.net_profit)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Balance Sheet Section */}
      {balanceSheet && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Assets */}
          <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400">
                <Building2 className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white">Aset</h2>
                <p className="text-xs text-slate-400">Total: {formatCurrency(balanceSheet.total_assets)}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-300">Aset Lancar</span>
                  <span className="text-sm font-bold text-blue-400">{formatCurrency(balanceSheet.current_assets.total)}</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Kas & Bank</span>
                    <span>{formatCurrency(balanceSheet.current_assets.cash_and_bank)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Piutang Usaha</span>
                    <span>{formatCurrency(balanceSheet.current_assets.accounts_receivable)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Persediaan</span>
                    <span>{formatCurrency(balanceSheet.current_assets.inventory)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Biaya Dibayar Dimuka</span>
                    <span>{formatCurrency(balanceSheet.current_assets.prepaid_expenses)}</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-300">Aset Tidak Lancar</span>
                  <span className="text-sm font-bold text-indigo-400">{formatCurrency(balanceSheet.non_current_assets.total)}</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Properti & Peralatan</span>
                    <span>{formatCurrency(balanceSheet.non_current_assets.property_equipment)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Akum. Penyusutan</span>
                    <span className="text-rose-400">{formatCurrency(balanceSheet.non_current_assets.accumulated_depreciation)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Aset Tak Berwujud</span>
                    <span>{formatCurrency(balanceSheet.non_current_assets.intangible_assets)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Aset Lainnya</span>
                    <span>{formatCurrency(balanceSheet.non_current_assets.other_assets)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Liabilities */}
          <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400">
                <CreditCard className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white">Kewajiban</h2>
                <p className="text-xs text-slate-400">Total: {formatCurrency(balanceSheet.total_liabilities)}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-300">Kewajiban Lancar</span>
                  <span className="text-sm font-bold text-amber-400">{formatCurrency(balanceSheet.current_liabilities.total)}</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Hutang Usaha</span>
                    <span>{formatCurrency(balanceSheet.current_liabilities.accounts_payable)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Biaya Akrual</span>
                    <span>{formatCurrency(balanceSheet.current_liabilities.accrued_expenses)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Hutang Jangka Pendek</span>
                    <span>{formatCurrency(balanceSheet.current_liabilities.short_term_debt)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Pajak Terutang</span>
                    <span>{formatCurrency(balanceSheet.current_liabilities.taxes_payable)}</span>
                  </div>
                </div>
              </div>

              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-300">Kewajiban Jk. Panjang</span>
                  <span className="text-sm font-bold text-rose-400">{formatCurrency(balanceSheet.non_current_liabilities.total)}</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Hutang Jangka Panjang</span>
                    <span>{formatCurrency(balanceSheet.non_current_liabilities.long_term_debt)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Kewajiban Lainnya</span>
                    <span>{formatCurrency(balanceSheet.non_current_liabilities.other_liabilities)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Equity & Ratios */}
          <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
                <Wallet className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white">Ekuitas & Rasio</h2>
                <p className="text-xs text-slate-400">Modal: {formatCurrency(balanceSheet.equity.total)}</p>
              </div>
            </div>

            <div className="space-y-4">
              <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/30">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-sm font-medium text-slate-300">Ekuitas</span>
                  <span className="text-sm font-bold text-emerald-400">{formatCurrency(balanceSheet.equity.total)}</span>
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-slate-400">
                    <span>Modal Disetor</span>
                    <span>{formatCurrency(balanceSheet.equity.capital_stock)}</span>
                  </div>
                  <div className="flex justify-between text-slate-400">
                    <span>Laba Ditahan</span>
                    <span>{formatCurrency(balanceSheet.equity.retained_earnings)}</span>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-slate-800/80 to-slate-900/50 p-4 rounded-xl border border-slate-700/30">
                <span className="text-sm font-medium text-slate-300 block mb-4">Rasio Keuangan</span>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-400">Current Ratio</span>
                    <span className={`text-sm font-bold ${parseFloat(currentRatio) >= 1.5 ? 'text-emerald-400' : parseFloat(currentRatio) >= 1 ? 'text-amber-400' : 'text-rose-400'}`}>
                      {currentRatio}x
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-400">Quick Ratio</span>
                    <span className={`text-sm font-bold ${parseFloat(quickRatio) >= 1 ? 'text-emerald-400' : 'text-amber-400'}`}>
                      {quickRatio}x
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-xs text-slate-400">Debt to Equity</span>
                    <span className={`text-sm font-bold ${parseFloat(debtToEquity) <= 0.5 ? 'text-emerald-400' : parseFloat(debtToEquity) <= 1 ? 'text-amber-400' : 'text-rose-400'}`}>
                      {debtToEquity}x
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// --- TAB: LOGISTIK ---
function LogistikTab({ data }) {
  const logistics = data.logistics_detail || {
    inventory_by_category: [],
    low_stock_alerts: [],
    pending_orders: [],
    delivery_status: { in_transit: 0, processing: 0, confirmed: 0, completed_this_week: 0 }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500 pb-8">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Total Nilai Inventaris"
          value={formatCurrency(data.logistics.inventory_value)}
          icon={<Package className="w-5 h-5" />}
          trend="+3.2%"
          trendUp={true}
          gradient="from-indigo-500/20"
          color="text-indigo-400"
        />
        <KPICard
          title="Item Stok Menipis"
          value={data.logistics.low_stock_items.toString()}
          icon={<AlertTriangle className="w-5 h-5" />}
          trend="+2"
          trendUp={false}
          gradient="from-rose-500/20"
          color="text-rose-400"
        />
        <KPICard
          title="PO Menunggu Kirim"
          value={data.logistics.pending_deliveries.toString()}
          icon={<Truck className="w-5 h-5" />}
          trend="-5"
          trendUp={true}
          gradient="from-amber-500/20"
          color="text-amber-400"
        />
        <KPICard
          title="PO Selesai Minggu Ini"
          value={logistics.delivery_status.completed_this_week?.toString() || "12"}
          icon={<ClipboardList className="w-5 h-5" />}
          trend="+8"
          trendUp={true}
          gradient="from-emerald-500/20"
          color="text-emerald-400"
        />
      </div>

      {/* Inventory by Category & Delivery Status */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Inventory by Category Chart */}
        <div className="lg:col-span-2 bg-[#1e293b] rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-white">Nilai Inventaris per Kategori</h2>
            <p className="text-sm text-slate-400">Distribusi nilai stok berdasarkan kategori.</p>
          </div>
          <div className="h-64 md:h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={logistics.inventory_by_category}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#334155" opacity={0.5} />
                <XAxis type="number" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} tickFormatter={(value) => `${value / 1000000}M`} />
                <YAxis type="category" dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} width={100} />
                <Tooltip
                  cursor={{ fill: '#334155', opacity: 0.2 }}
                  contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '8px' }}
                  formatter={(value) => formatCurrency(value)}
                />
                <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                  {logistics.inventory_by_category.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Delivery Status */}
        <div className="bg-gradient-to-br from-indigo-900/40 to-slate-900 rounded-2xl border border-slate-700/50 p-4 md:p-6 shadow-xl relative overflow-hidden">
          <div className="absolute -bottom-24 -right-24 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

          <h2 className="text-lg font-semibold text-white mb-1 relative z-10">Status Pengiriman</h2>
          <p className="text-sm text-slate-400 mb-6 relative z-10">Overview status Purchase Order.</p>

          <div className="grid grid-cols-2 gap-4 relative z-10">
            <div className="bg-slate-800/60 p-4 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></div>
                <span className="text-xs font-medium text-slate-400">Dalam Perjalanan</span>
              </div>
              <p className="text-2xl font-bold text-blue-400">{logistics.delivery_status.in_transit}</p>
            </div>

            <div className="bg-slate-800/60 p-4 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-amber-400"></div>
                <span className="text-xs font-medium text-slate-400">Diproses</span>
              </div>
              <p className="text-2xl font-bold text-amber-400">{logistics.delivery_status.processing}</p>
            </div>

            <div className="bg-slate-800/60 p-4 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-emerald-400"></div>
                <span className="text-xs font-medium text-slate-400">Dikonfirmasi</span>
              </div>
              <p className="text-2xl font-bold text-emerald-400">{logistics.delivery_status.confirmed}</p>
            </div>

            <div className="bg-slate-800/60 p-4 rounded-2xl border border-slate-700/50 backdrop-blur-sm">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-2 h-2 rounded-full bg-slate-400"></div>
                <span className="text-xs font-medium text-slate-400">Selesai (7 hari)</span>
              </div>
              <p className="text-2xl font-bold text-slate-300">{logistics.delivery_status.completed_this_week}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Low Stock Alerts & Pending Orders */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Low Stock Alerts */}
        <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 shadow-xl overflow-hidden">
          <div className="p-4 md:p-6 border-b border-slate-700/50 flex justify-between items-center bg-rose-500/5">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-rose-500/10 text-rose-400">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white">Peringatan Stok Menipis</h2>
                <p className="text-xs text-slate-400">Item yang perlu segera di-restock.</p>
              </div>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase bg-slate-800/50">
                <tr>
                  <th className="px-4 md:px-6 py-3 font-medium">Item</th>
                  <th className="px-4 md:px-6 py-3 font-medium text-center">Stok</th>
                  <th className="px-4 md:px-6 py-3 font-medium text-center">Min</th>
                  <th className="px-4 md:px-6 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {logistics.low_stock_alerts.map((item, idx) => (
                  <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                    <td className="px-4 md:px-6 py-4">
                      <p className="font-medium text-slate-200 text-xs md:text-sm">{item.name}</p>
                      <p className="text-xs text-slate-500">{item.category}</p>
                    </td>
                    <td className="px-4 md:px-6 py-4 text-center">
                      <span className="text-rose-400 font-bold">{item.current_stock}</span>
                      <span className="text-slate-500 text-xs ml-1">{item.unit}</span>
                    </td>
                    <td className="px-4 md:px-6 py-4 text-center text-slate-400">{item.min_stock}</td>
                    <td className="px-4 md:px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium border ${(item.current_stock / item.min_stock) < 0.25
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/20'
                        : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                        }`}>
                        {(item.current_stock / item.min_stock) < 0.25 ? 'Kritis' : 'Rendah'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pending Purchase Orders */}
        <div className="bg-[#1e293b] rounded-2xl border border-slate-700/50 shadow-xl overflow-hidden">
          <div className="p-4 md:p-6 border-b border-slate-700/50 flex justify-between items-center bg-amber-500/5">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
                <ClipboardList className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white">Purchase Order Aktif</h2>
                <p className="text-xs text-slate-400">PO yang sedang diproses.</p>
              </div>
            </div>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-400 uppercase bg-slate-800/50">
                <tr>
                  <th className="px-4 md:px-6 py-3 font-medium">PO #</th>
                  <th className="px-4 md:px-6 py-3 font-medium">Vendor</th>
                  <th className="px-4 md:px-6 py-3 font-medium text-right">Total</th>
                  <th className="px-4 md:px-6 py-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody>
                {logistics.pending_orders.map((order, idx) => (
                  <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors">
                    <td className="px-4 md:px-6 py-4">
                      <p className="font-medium text-slate-200 text-xs md:text-sm">{order.id}</p>
                      <p className="text-xs text-slate-500">ETA: {order.expected_date}</p>
                    </td>
                    <td className="px-4 md:px-6 py-4 text-slate-300 text-xs md:text-sm">{order.vendor}</td>
                    <td className="px-4 md:px-6 py-4 text-right font-medium text-emerald-400 text-xs md:text-sm">{formatCurrency(order.total)}</td>
                    <td className="px-4 md:px-6 py-4">
                      <span className={`px-2 py-1 rounded text-xs font-medium border ${order.status === 'In Transit'
                        ? 'bg-blue-500/10 text-blue-400 border-blue-500/20'
                        : order.status === 'Processing'
                          ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
                          : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                        }`}>
                        {order.status === 'In Transit' ? 'Dikirim' : order.status === 'Processing' ? 'Diproses' : 'Dikonfirmasi'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

function KPICard({ title, value, icon, trend, trendUp, gradient, color }) {
  return (
    <div className={`bg-gradient-to-br ${gradient} bg-slate-800 border border-slate-700/50 rounded-2xl p-6 shadow-lg shadow-slate-900/20 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 backdrop-blur-sm relative overflow-hidden group`}>
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-400 mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-slate-100 tracking-tight">{value}</h3>
        </div>
        <div className={`p-2 rounded-lg bg-slate-900/50 ${color} shadow-inner`}>
          {icon}
        </div>
      </div>
      <div className="mt-4 flex items-center gap-2">
        <span className={`flex items-center text-xs font-semibold px-2 py-0.5 rounded-full ${trendUp ? 'text-emerald-400 bg-emerald-400/10' : 'text-rose-400 bg-rose-400/10'}`}>
          {trendUp ? <ArrowUpRight className="w-3 h-3 mr-1" /> : <ArrowDownRight className="w-3 h-3 mr-1" />}
          {trend}
        </span>
        <span className="text-xs text-slate-500">vs bulan lalu</span>
      </div>
      <div className={`absolute -bottom-1 -right-1 w-24 h-24 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-50 blur-2xl rounded-full transition-opacity duration-500 pointer-events-none`}></div>
    </div>
  );
}
