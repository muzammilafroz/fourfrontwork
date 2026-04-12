import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useAuthStore } from "@/stores/authStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { motion } from "framer-motion";
import { CheckCircle } from "lucide-react";

const BookAppointment = () => {
  const [searchParams] = useSearchParams();
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [doctors, setDoctors] = useState<any[]>([]);
  const [selectedDoctor, setSelectedDoctor] = useState(
    searchParams.get("doctor") || "",
  );
  const [patientName, setPatientName] = useState(user?.name || "");
  const [patientPhone, setPatientPhone] = useState(user?.phone || "");
  const [date, setDate] = useState(new Date().toISOString().split("T")[0]);
  const [time, setTime] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

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

  const selectedDoc = doctors.find(
    (d) => String(d.doctor_id) === selectedDoctor,
  );

  const timeSlots = [
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDoctor || !date || !time || !patientName || !patientPhone) {
      toast.error("Please fill all fields");
      return;
    }
    let errorMessage = "";
    setLoading(true);
    try {
      // Double-booking check
      // const { data: existing } = await supabase
      //   .from("appointments")
      //   .select("appointment_id")
      //   .eq("doctor_id", parseInt(selectedDoctor))
      //   .eq("appointment_date", date)
      //   .eq("appointment_time", time + ":00")
      //   .neq("status", "cancelled");

      // if (existing && existing.length > 0) {
      //   toast.error("This time slot is already booked. Please choose another.");
      //   setLoading(false);
      //   return;
      // }

      const url = "http://localhost:8000/api/appointments";

      const res = await fetch(url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();

      errorMessage = "Error fetching appointments";
      if (!res.ok) {
        throw new Error(data.detail || errorMessage);
      }

      console.log("Appointments:", data);

      // if (data.length > 0) {
      //   toast.error("This time slot is already booked. Please choose another.");
      //   setLoading(false);
      //   return;
      // }

      const payload = {
        patient_name: patientName,
        patient_phone: patientPhone,
        doctor_id: selectedDoctor,
        appointment_date: date,
        appointment_time: time,
      };

      const response = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      errorMessage = "Error creating an appointment";
      if (!response.ok) {
        throw new Error(data.detail || errorMessage);
      }

      const postData = await response.json();
      console.log(postData);

      setSuccess(true);
      toast.success("Appointment booked successfully!");

      setTimeout(() => setSuccess(false), 3000);
      setDate("");
      setTime("");
    } catch (error: any) {
      toast.error(error.message);
      console.error("Error fetching appointments:", error);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="flex flex-col items-center justify-center py-20"
      >
        <CheckCircle className="h-16 w-16 text-success mb-4" />
        <h2 className="text-2xl font-serif font-bold text-foreground">
          Appointment Booked!
        </h2>
        <p className="text-muted-foreground mt-2">
          You'll receive confirmation shortly.
        </p>
      </motion.div>
    );
  }

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-2xl font-serif font-bold text-foreground mb-6">
        Book an Appointment
      </h1>
      <form
        onSubmit={handleSubmit}
        className="bg-card rounded-xl border border-border p-6 space-y-4"
      >
        <div>
          <Label>Patient Name</Label>
          <Input
            value={patientName}
            onChange={(e) => setPatientName(e.target.value)}
          />
        </div>
        <div>
          <Label>Phone</Label>
          <Input
            value={patientPhone}
            onChange={(e) => setPatientPhone(e.target.value)}
          />
        </div>
        <div>
          <Label>Doctor</Label>
          <Select value={selectedDoctor} onValueChange={setSelectedDoctor}>
            <SelectTrigger>
              <SelectValue placeholder="Select a doctor" />
            </SelectTrigger>
            <SelectContent>
              {doctors.map((d) => (
                <SelectItem key={d.id} value={String(d.id)}>
                  {d.name} - {d.specialization}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          {selectedDoc && (
            <p className="text-xs text-muted-foreground mt-1">
              Available: {selectedDoc.available_days} | Fee: ₹{selectedDoc.fee}
            </p>
          )}
        </div>
        <div>
          <Label>Date</Label>
          <Input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            min={new Date().toISOString().split("T")[0]}
          />
        </div>
        <div>
          <Label>Time Slot</Label>
          <Select value={time} onValueChange={setTime}>
            <SelectTrigger>
              <SelectValue placeholder="Select time" />
            </SelectTrigger>
            <SelectContent>
              {timeSlots.map((t) => (
                <SelectItem key={t} value={t}>
                  {t}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? "Booking..." : "Book Appointment"}
        </Button>
      </form>
    </div>
  );
};

export default BookAppointment;
