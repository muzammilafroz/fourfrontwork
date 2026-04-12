import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { RouteGuard } from "@/components/RouteGuard";
import { DashboardLayout } from "@/components/DashboardLayout";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import NotFound from "./pages/NotFound";
import PrescriptionReader from "./pages/PrescriptionReader";

// Customer
import CustomerDoctors from "./pages/customer/Doctors";
import BookAppointment from "./pages/customer/BookAppointment";
import AppointmentHistory from "./pages/customer/AppointmentHistory";
import TrackOrders from "./pages/customer/TrackOrders";
import CustomerAskChatbot from "./pages/customer/AskChatbot";
// import CustomerFeedback from "./pages/customer/Feedback";

// Employee
import MedicineSearch from "./pages/employee/MedicineSearch";
import AddMedicine from "./pages/employee/AddMedicine";
import EmployeeAppointments from "./pages/employee/Appointments";
// import EmployeePreorders from "./pages/employee/Preorders";
// import CreateOrder from "./pages/employee/CreateOrder";
// import EmployeeAskChatbot from "./pages/employee/AskChatbot";

// Admin
import Overview from "./pages/admin/Overview";
import Sales from "./pages/admin/Sales";
import Inventory from "./pages/admin/Inventory";
import DoctorsManagement from "./pages/admin/Doctors";
// import EmployeeRequests from "./pages/admin/EmployeeRequests";
import UserManagement from "./pages/admin/Users";
import AdminAppointments from "./pages/admin/Appointments";
import MedicineRequests from "./pages/admin/MedicineRequests";
// import adminFeedback from "./pages/admin/Feedback";
import AskChatbot from "./pages/admin/AskChatbot";
// import adminPrescriptionReader from "./pages/admin/PrescriptionReader";

const queryClient = new QueryClient();

const Dash = ({ children, roles }: { children: React.ReactNode; roles: string[] }) => (
  <RouteGuard allowedRoles={roles}><DashboardLayout>{children}</DashboardLayout></RouteGuard>
);

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          {/* Open Routes */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          {/*<Route path="/prescription-reader" element={<PrescriptionReader />} />*/}

          {/* Customer */}
          <Route path="/customer/doctors" element={<Dash roles={['customer']}><CustomerDoctors /></Dash>} />
          <Route path="/customer/book-appointment" element={<Dash roles={['customer']}><BookAppointment /></Dash>} />
          <Route path="/customer/appointments" element={<Dash roles={['customer']}><AppointmentHistory /></Dash>} />
          <Route path="/customer/orders" element={<Dash roles={['customer']}><TrackOrders /></Dash>} />
          <Route path="/customer/prescription" element={<Dash roles={['customer']}><PrescriptionReader /></Dash>} />
          <Route path="/customer/ask-chatbot" element={<Dash roles={['customer']}><CustomerAskChatbot /></Dash>} />
          {/*<Route path="/customer/feedback" element={<Dash roles={['customer']}><CustomerFeedback /></Dash>} />*/}

          {/* Employee */}
          <Route path="/employee/medicines" element={<Dash roles={['employee']}><MedicineSearch /></Dash>} />
          <Route path="/employee/add-medicine" element={<Dash roles={['employee']}><AddMedicine /></Dash>} />
          <Route path="/employee/appointments" element={<Dash roles={['employee']}><EmployeeAppointments /></Dash>} />
          {/*<Route path="/employee/preorders" element={<Dash roles={['employee']}><EmployeePreorders /></Dash>} />*/}
          {/*<Route path="/employee/create-order" element={<Dash roles={['employee']}><CreateOrder /></Dash>} />*/}
          <Route path="/employee/prescription" element={<Dash roles={['employee']}><PrescriptionReader /></Dash>} />
          {/*<Route path="/employee/ask-chatbot" element={<Dash roles={['employee']}><EmployeeAskChatbot /></Dash>} />*/}

          {/* Admin */}
          <Route path="/admin/overview" element={<Dash roles={['admin']}><Overview /></Dash>} />
          <Route path="/admin/sales" element={<Dash roles={['admin']}><Sales /></Dash>} />
          <Route path="/admin/inventory" element={<Dash roles={['admin']}><Inventory /></Dash>} />
          <Route path="/admin/doctors" element={<Dash roles={['admin']}><DoctorsManagement /></Dash>} />
          {/*<Route path="/admin/employee-requests" element={<Dash roles={['admin']}><EmployeeRequests /></Dash>} />*/}
          <Route path="/admin/users" element={<Dash roles={['admin']}><UserManagement /></Dash>} />
          <Route path="/admin/appointments" element={<Dash roles={['admin']}><AdminAppointments /></Dash>} />
          <Route path="/admin/medicine-requests" element={<Dash roles={['admin']}><MedicineRequests /></Dash>} />
          {/*<Route path="/admin/feedback" element={<Dash roles={['admin']}><adminFeedback /></Dash>} />*/}
           <Route path="/admin/prescription" element={<Dash roles={['admin']}><PrescriptionReader /></Dash>} />
          <Route path="/admin/ask-chatbot" element={<Dash roles={['admin']}><AskChatbot /></Dash>} />

          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
