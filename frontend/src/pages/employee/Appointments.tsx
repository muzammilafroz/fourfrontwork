import { useEffect, useState } from "react";
import { useAuthStore } from "@/stores/authStore";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { EmptyState } from "@/components/EmptyState";
import { Switch } from "@/components/ui/switch";
import { toast } from "sonner";
import { Calendar } from "lucide-react";

const EmployeeAppointments = () => {
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [appointments, setAppointments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
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
  };

  useEffect(() => {
    load();
  }, []);

  const toggleVisited = async (id: number, status: string) => {
    // Optimistic update
    let payload = {};
    if (status === "scheduled") {
      payload = { status: "completed" };
      setAppointments((prev) =>
        prev.map((a) => (a.id === id ? { ...a, status: "completed" } : a)),
      );
    } else {
      payload = { status: "scheduled" };
      setAppointments((prev) =>
        prev.map((a) => (a.id === id ? { ...a, status: "scheduled" } : a)),
      );
    }

    const response = await fetch(
      `http://localhost:8000/api/appointments/${id}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      },
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to update appointment");
    }

    let error = false;
    if (error) {
      toast.error("Failed to update");
      setAppointments((prev) =>
        prev.map((a) => (a.id === id ? { ...a, status: "scheduled" } : a)),
      );
    } else {
      toast.success("Updated visited status");
    }
  };

  if (loading) return <LoadingSkeleton />;

  return (
    <div>
      <h1 className="text-2xl font-serif font-bold text-foreground mb-6">
        Appointments
      </h1>
      {appointments.length === 0 ? (
        <EmptyState
          title="No appointments"
          description="No appointments scheduled."
          icon={<Calendar className="h-8 w-8 text-muted-foreground" />}
        />
      ) : (
        <div className="bg-card rounded-xl border border-border overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border bg-muted/50">
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Patient
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Phone
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Doctor
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Date
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Time
                </th>
                <th className="text-left p-3 font-medium text-muted-foreground">
                  Visited
                </th>
              </tr>
            </thead>
            <tbody>
              {appointments.map((a) => (
                <tr key={a.id} className="border-b border-border last:border-0">
                  <td className="p-3 text-foreground">{a.patient_name}</td>
                  <td className="p-3 text-muted-foreground">
                    {a.patient_phone}
                  </td>
                  <td className="p-3 text-foreground">
                    {(a.doctors as any)?.name}
                  </td>
                  <td className="p-3 text-foreground">{a.appointment_date}</td>
                  <td className="p-3 text-foreground">{a.appointment_time}</td>
                  <td className="p-3">
                    <Switch
                      checked={a.status === "completed"}
                      onCheckedChange={() => toggleVisited(a.id, a.status)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default EmployeeAppointments;
