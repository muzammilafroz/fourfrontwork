import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
import { ThemeToggle } from '@/components/ThemeToggle';
import {
  Menu, X, LogOut, Calendar, ShoppingCart, FileText, MessageCircle,
  Star, Pill, PlusCircle, ClipboardList, BarChart3, Users, UserCheck,
  Package, Stethoscope, MessageSquare, LayoutDashboard, Receipt
} from 'lucide-react';
import { Button } from '@/components/ui/button';

const customerLinks = [
  { to: '/customer/doctors', label: 'Doctors', icon: Stethoscope },
  { to: '/customer/book-appointment', label: 'Book Appointment', icon: Calendar },
  { to: '/customer/appointments', label: 'My Appointments', icon: ClipboardList },
  { to: '/customer/orders', label: 'Track Orders', icon: ShoppingCart },
  { to: '/customer/prescription', label: 'Prescription Reader', icon: FileText },
  { to: '/customer/ask-mochi', label: 'Ask Mochi 🤖', icon: MessageCircle },
  { to: '/customer/feedback', label: 'Feedback', icon: Star },
];

const employeeLinks = [
  { to: '/employee/medicines', label: 'Medicine Search', icon: Pill },
  { to: '/employee/add-medicine', label: 'Add Medicine', icon: PlusCircle },
  { to: '/employee/appointments', label: 'Appointments', icon: Calendar },
  { to: '/employee/preorders', label: 'Preorder Requests', icon: ClipboardList },
  { to: '/employee/create-order', label: 'Create Order', icon: Receipt },
  { to: '/employee/prescription', label: 'Prescription Reader', icon: FileText },
  { to: '/employee/ask-mochi', label: 'Ask Mochi 🤖', icon: MessageCircle },
];

const ownerLinks = [
  { to: '/owner/overview', label: 'Overview', icon: LayoutDashboard },
  { to: '/owner/sales', label: 'Sales & Billing', icon: BarChart3 },
  { to: '/owner/inventory', label: 'Inventory', icon: Package },
  { to: '/owner/doctors', label: 'Doctors', icon: Stethoscope },
  { to: '/owner/employee-requests', label: 'Employee Requests', icon: UserCheck },
  { to: '/owner/users', label: 'User Management', icon: Users },
  { to: '/owner/appointments', label: 'Appointments', icon: Calendar },
  { to: '/owner/medicine-requests', label: 'Medicine Requests', icon: ClipboardList },
  { to: '/owner/feedback', label: 'Feedback', icon: MessageSquare },
  { to: '/owner/prescription', label: 'Prescription Reader', icon: FileText },
  { to: '/owner/ask-mochi', label: 'Ask Mochi 🤖', icon: MessageCircle },
];

export const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const links = user?.role === 'owner' ? ownerLinks : user?.role === 'employee' ? employeeLinks : customerLinks;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {sidebarOpen && (
        <div className="fixed inset-0 z-40 bg-foreground/20 md:hidden" onClick={() => setSidebarOpen(false)} />
      )}

      <aside className={`no-print fixed z-50 md:static md:z-auto flex flex-col h-full w-64 bg-card border-r border-border transition-transform duration-300 ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <div className="flex items-center justify-between p-4 border-b border-border">
          <NavLink to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
              <Pill className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="font-serif text-lg font-bold text-foreground">MedEase</span>
          </NavLink>
          <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setSidebarOpen(false)}>
            <X className="h-5 w-5" />
          </Button>
        </div>

        <div className="p-3 border-b border-border">
          <div className="text-sm font-medium text-foreground">{user?.name}</div>
          <div className="text-xs text-muted-foreground capitalize">{user?.role}</div>
        </div>

        <nav className="flex-1 overflow-y-auto p-2 space-y-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive
                    ? 'bg-primary text-primary-foreground'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                }`
              }
            >
              <link.icon className="h-4 w-4 shrink-0" />
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="p-3 border-t border-border">
          <Button variant="ghost" className="w-full justify-start gap-2 text-destructive" onClick={handleLogout}>
            <LogOut className="h-4 w-4" /> Logout
          </Button>
        </div>
      </aside>

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="no-print flex items-center justify-between px-4 py-3 border-b border-border bg-card">
          <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setSidebarOpen(true)}>
            <Menu className="h-5 w-5" />
          </Button>
          <div className="hidden md:block" />
          <div className="flex items-center gap-2">
            <ThemeToggle />
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-4 md:p-6">
          {children}
        </main>
      </div>
    </div>
  );
};
