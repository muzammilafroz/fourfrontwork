import { useEffect, useState } from "react";
// import { useAuthStore } from "@/stores/authStore";
import { CardSkeleton } from "@/components/LoadingSkeleton";
import { EmptyState } from "@/components/EmptyState";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { Stethoscope, Calendar } from "lucide-react";

const CustomerDoctors = () => {
  // const { user, checkTokenExpiry } = useAuthStore();
  const [doctors, setDoctors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function getDoctors() {
      const url = "http://localhost:8000/api/doctors";

      try {
        const res = await fetch(url);
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Login failed.");
        }

        console.log("Doctors:", data);
        setDoctors(data || []);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching doctors:", error);
        setDoctors([]);
        setLoading(false);
      }
    }
    getDoctors();
  }, []);

  if (loading) return <CardSkeleton count={6} />;

  return (
    <div>
      <h1 className="text-2xl font-serif font-bold text-foreground mb-6">
        Available Doctors
      </h1>
      {doctors.length === 0 ? (
        <EmptyState
          title="No doctors available"
          description="Check back later for available doctors."
          icon={<Stethoscope className="h-8 w-8 text-muted-foreground" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {doctors.map((doc) => (
            <div
              key={doc.id}
              className="bg-card rounded-xl border border-border p-5 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  {doc.image_url ? (
                    <img
                      src={doc.image_url}
                      alt={doc.name}
                      className="w-12 h-12 rounded-full object-cover"
                    />
                  ) : (
                    <Stethoscope className="h-6 w-6 text-primary" />
                  )}
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">{doc.name}</h3>
                  <p className="text-sm text-muted-foreground">
                    {doc.specialization}
                  </p>
                </div>
              </div>
              <div className="space-y-1 text-sm text-muted-foreground mb-4">
                <p>📅 {doc.available_days || "N/A"}</p>
                <p>⏰ {doc.available_time || "N/A"}</p>
                <p className="text-primary font-medium">₹{doc.consultation_fee || 0}</p>
              </div>
              <Button
                className="w-full gap-2"
                onClick={() =>
                  navigate(`/customer/book-appointment?doctor=${doc.id}`)
                }
              >
                <Calendar className="h-4 w-4" /> Book Appointment
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CustomerDoctors;
