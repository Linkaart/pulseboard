import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import apiClient from '../api/client';

interface AuditEntry {
  id: number;
  user: number;
  action: string;
  entity_type: string;
  entity_id: number;
  created_at: string;
}

interface PaginatedResponse {
  count: number;
  results: AuditEntry[];
}

function AuditLogPage() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery<PaginatedResponse>({
    queryKey: ['audit-log', page],
    queryFn: async () =>
      (await apiClient.get('/audit/activitylog/', { params: { page } })).data,
  });

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900 mb-6">Audit Log</h1>
      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Entity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
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
              data?.results.map((entry) => (
                <tr key={entry.id}>
                  <td className="px-6 py-4 text-sm text-slate-900">{entry.user}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{entry.action}</td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {entry.entity_type} #{entry.entity_id}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {new Date(entry.created_at).toLocaleString()}
                  </td>
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

export default AuditLogPage;
