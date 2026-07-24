import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';

interface Customer {
  id: number;
  name: string;
  email: string;
  status: string;
  mrr: number;
  created_at: string;
}

interface PaginatedResponse {
  count: number;
  results: Customer[];
}

function CustomersPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');

  const { data, isLoading } = useQuery<PaginatedResponse>({
    queryKey: ['customers', page, search],
    queryFn: async () =>
      (
        await apiClient.get('/customers/', {
          params: { page, search },
        })
      ).data,
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Customers</h1>
        <input
          type="text"
          placeholder="Search customers..."
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-slate-500"
        />
      </div>
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">MRR</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {isLoading ? (
              <tr>
                <td className="px-6 py-4 text-sm text-gray-500" colSpan={4}>
                  Loading...
                </td>
              </tr>
            ) : (
              data?.results.map((c) => (
                <tr key={c.id}>
                  <td className="px-6 py-4 text-sm text-slate-900">{c.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{c.email}</td>
                  <td className="px-6 py-4 text-sm">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        c.status === 'active'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-gray-100 text-gray-700'
                      }`}
                    >
                      {c.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">${c.mrr}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between items-center mt-4">
        <button
          onClick={() => setPage((p) => Math.max(1, p - 1))}
          disabled={page === 1}
          className="px-3 py-1 text-sm border rounded-md disabled:opacity-50"
        >
          Previous
        </button>
        <span className="text-sm text-gray-500">Page {page}</span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={!data || data.results.length === 0}
          className="px-3 py-1 text-sm border rounded-md disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default CustomersPage;
