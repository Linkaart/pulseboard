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
  mrr: string;
  churn_rate: number;
  conversion_rate: number;
  arpu: string;
  new_customers: number;
}

interface ChartPoint {
  period: string;
  mrr: string;
  new_customers: number;
  churn_rate: number;
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
    queryKey: ['dashboard-summary'],
    queryFn: async () => (await apiClient.get('/dashboard/summary/')).data,
  });

  const { data: chartData, isLoading: chartLoading } = useQuery<ChartPoint[]>({
    queryKey: ['dashboard-charts'],
    queryFn: async () => (await apiClient.get('/dashboard/charts/')).data,
  });

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="MRR" value={kpisLoading ? '...' : `$${kpis?.mrr ?? 0}`} />
        <StatCard
          label="New Customers"
          value={kpisLoading ? '...' : kpis?.new_customers ?? 0}
        />
        <StatCard
          label="Churn Rate"
          value={kpisLoading ? '...' : `${kpis?.churn_rate ?? 0}%`}
        />
        <StatCard
          label="ARPU"
          value={kpisLoading ? '...' : `$${kpis?.arpu ?? 0}`}
        />
      </div>
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">Revenue Trend</h2>
        {chartLoading ? (
          <p className="text-sm text-gray-500">Loading chart...</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="mrr" stroke="#1e293b" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}

export default DashboardPage;
