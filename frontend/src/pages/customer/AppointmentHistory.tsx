import { useEffect, useState } from "react";
// import { supabase } from '@/integrations/supabase/client';
import { useAuthStore } from "@/stores/authStore";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { EmptyState } from "@/components/EmptyState";
import { StatusBadge } from "@/components/StatusBadge";
import { Calendar } from "lucide-react";

const AppointmentHistory = () => {
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [appointments, setAppointments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    async function getAppointments() {
      const url = "http://localhost:8000/api/appointments";

      const res = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      const errorMessage = "Error fetching appointments";

      if (!res.ok) {
        throw new Error(data.detail || errorMessage);
      }

      console.log("Appointments:", data);
      setAppointments(data || []);
      setLoading(false);
    }

    getAppointments();
  }, [user]);

  if (loading) return <LoadingSkeleton />;

  return (
    <div>
      <h1 className="text-2xl font-serif font-bold text-foreground mb-6">
        Appointment History
      </h1>
      {appointments.length === 0 ? (
        <EmptyState
          title="No appointments yet"
          description="Book your first appointment to see it here."
          icon={<Calendar className="h-8 w-8 text-muted-foreground" />}
        />
      ) : (
        <div className="bg-card rounded-xl border border-border overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Doctor
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Specialization
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Date
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Time
                </th>
                <th className="text-center p-3 font-medium text-muted-foreground">
                  Status
                </th>
                <th className="text-center p-3 font-medium text-muted-foreground">
                  Visited
                </th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((a) => (
                <tr
                  key={a.id}
                  className="border-b border-border last:border-0"
                >
                  <td className="p-3 text-foreground">
                    {a.doctor.name}
                  </td>
                  <td className="p-3 text-muted-foreground">
                    {a.doctor.specialization}
                  </td>
                  <td className="p-3 text-foreground">{a.appointment_date}</td>
                  <td className="p-3 text-foreground">{a.appointment_time.slice(0, -3)}</td>
                  <td className="p-3 text-center">
                    <StatusBadge status={a.status} />
                  </td>
                  <td className="p-3 text-center">{a.visited ? "✅" : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AppointmentHistory;
