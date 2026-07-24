import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const navItems = [
  { to: '/', label: 'Dashboard', end: true },
  { to: '/customers', label: 'Customers' },
  { to: '/audit', label: 'Audit Log' },
];

function Layout() {
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <aside className="w-64 bg-slate-900 text-white flex flex-col">
        <div className="px-6 py-5 text-xl font-bold border-b border-slate-700">
          PulseBoard
        </div>
        <nav className="flex-1 px-2 py-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `block px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-slate-700 text-white'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="px-4 py-4 border-t border-slate-700">
          <p className="text-sm text-slate-300 truncate">{user?.email}</p>
          <button
            onClick={handleLogout}
            className="mt-2 w-full text-left text-sm text-red-400 hover:text-red-300"
          >
            Logout
          </button>
        </div>
      </aside>
      <main className="flex-1 p-8 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}

export default Layout;
