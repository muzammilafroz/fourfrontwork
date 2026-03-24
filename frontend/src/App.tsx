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

// // Customer
// import CustomerDoctors from "./pages/customer/Doctors";
// import BookAppointment from "./pages/customer/BookAppointment";
// import AppointmentHistory from "./pages/customer/AppointmentHistory";
// import TrackOrders from "./pages/customer/TrackOrders";
// import PrescriptionReader from "./pages/customer/PrescriptionReader";
// import CustomerAskMochi from "./pages/customer/AskMochi";
// import CustomerFeedback from "./pages/customer/Feedback";

// // Employee
// import MedicineSearch from "./pages/employee/MedicineSearch";
// import AddMedicine from "./pages/employee/AddMedicine";
// import EmployeeAppointments from "./pages/employee/Appointments";
// import EmployeePreorders from "./pages/employee/Preorders";
// import CreateOrder from "./pages/employee/CreateOrder";
// import EmployeeAskMochi from "./pages/employee/AskMochi";
// import EmployeePrescriptionReader from "./pages/employee/PrescriptionReader";

// // Owner
// import Overview from "./pages/owner/Overview";
// import Sales from "./pages/owner/Sales";
// import Inventory from "./pages/owner/Inventory";
// import DoctorsManagement from "./pages/owner/Doctors";
// import EmployeeRequests from "./pages/owner/EmployeeRequests";
// import UserManagement from "./pages/owner/Users";
// import OwnerAppointments from "./pages/owner/Appointments";
// import MedicineRequests from "./pages/owner/MedicineRequests";
// import OwnerFeedback from "./pages/owner/Feedback";
// import OwnerAskMochi from "./pages/owner/AskMochi";
// import OwnerPrescriptionReader from "./pages/owner/PrescriptionReader";

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
          {/*<Route path="/customer/doctors" element={<Dash roles={['customer']}><CustomerDoctors /></Dash>} />
          <Route path="/customer/book-appointment" element={<Dash roles={['customer']}><BookAppointment /></Dash>} />
          <Route path="/customer/appointments" element={<Dash roles={['customer']}><AppointmentHistory /></Dash>} />
          <Route path="/customer/orders" element={<Dash roles={['customer']}><TrackOrders /></Dash>} />
          <Route path="/customer/prescription" element={<Dash roles={['customer']}><PrescriptionReader /></Dash>} />
          <Route path="/customer/ask-mochi" element={<Dash roles={['customer']}><CustomerAskMochi /></Dash>} />
          <Route path="/customer/feedback" element={<Dash roles={['customer']}><CustomerFeedback /></Dash>} />*/}

          {/* Employee */}
          {/*<Route path="/employee/medicines" element={<Dash roles={['employee']}><MedicineSearch /></Dash>} />
          <Route path="/employee/add-medicine" element={<Dash roles={['employee']}><AddMedicine /></Dash>} />
          <Route path="/employee/appointments" element={<Dash roles={['employee']}><EmployeeAppointments /></Dash>} />
          <Route path="/employee/preorders" element={<Dash roles={['employee']}><EmployeePreorders /></Dash>} />
          <Route path="/employee/create-order" element={<Dash roles={['employee']}><CreateOrder /></Dash>} />
          <Route path="/employee/prescription" element={<Dash roles={['employee']}><EmployeePrescriptionReader /></Dash>} />
          <Route path="/employee/ask-mochi" element={<Dash roles={['employee']}><EmployeeAskMochi /></Dash>} />*/}

          {/* Owner */}
          {/*<Route path="/owner/overview" element={<Dash roles={['owner']}><Overview /></Dash>} />
          <Route path="/owner/sales" element={<Dash roles={['owner']}><Sales /></Dash>} />
          <Route path="/owner/inventory" element={<Dash roles={['owner']}><Inventory /></Dash>} />
          <Route path="/owner/doctors" element={<Dash roles={['owner']}><DoctorsManagement /></Dash>} />
          <Route path="/owner/employee-requests" element={<Dash roles={['owner']}><EmployeeRequests /></Dash>} />
          <Route path="/owner/users" element={<Dash roles={['owner']}><UserManagement /></Dash>} />
          <Route path="/owner/appointments" element={<Dash roles={['owner']}><OwnerAppointments /></Dash>} />
          <Route path="/owner/medicine-requests" element={<Dash roles={['owner']}><MedicineRequests /></Dash>} />
          <Route path="/owner/feedback" element={<Dash roles={['owner']}><OwnerFeedback /></Dash>} />
          <Route path="/owner/prescription" element={<Dash roles={['owner']}><OwnerPrescriptionReader /></Dash>} />
          <Route path="/owner/ask-mochi" element={<Dash roles={['owner']}><OwnerAskMochi /></Dash>} />*/}

          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
