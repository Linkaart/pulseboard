import { useQuery } from '@tanstack/react-query';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import apiClient from '../api/client';

interface KpiSummary {
  total_customers: number;
  active_customers: number;
  monthly_revenue: number;
  churn_rate: number;
}

interface RevenuePoint {
  month: string;
  revenue: number;
}

function StatCard({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-slate-900 mt-1">{value}</p>
    </div>
  );
}

function DashboardPage() {
  const { data: kpis, isLoading: kpisLoading } = useQuery<KpiSummary>({
    queryKey: ['kpi-summary'],
    queryFn: async () => (await apiClient.get('/analytics/kpi-summary/')).data,
  });

  const { data: revenue, isLoading: revenueLoading } = useQuery<RevenuePoint[]>({
    queryKey: ['revenue-trend'],
    queryFn: async () => (await apiClient.get('/analytics/revenue-trend/')).data,
  });

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total Customers" value={kpisLoading ? '...' : kpis?.total_customers ?? 0} />
        <StatCard label="Active Customers" value={kpisLoading ? '...' : kpis?.active_customers ?? 0} />
        <StatCard
          label="Monthly Revenue"
          value={kpisLoading ? '...' : `$${kpis?.monthly_revenue ?? 0}`}
        />
        <StatCard
          label="Churn Rate"
          value={kpisLoading ? '...' : `${kpis?.churn_rate ?? 0}%`}
        />
      </div>
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Revenue Trend</h2>
        {revenueLoading ? (
          <p className="text-sm text-gray-500">Loading chart...</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenue}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" stroke="#1e293b" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
