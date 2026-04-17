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
  // const [appointments, setAppointments] = useState<any[]>([]);
  const [selectedDoctor, setSelectedDoctor] = useState(
    searchParams.get("doctor") || "",
  );
  const [patientName, setPatientName] = useState(user?.name || "");
  const [patientPhone, setPatientPhone] = useState(user?.phone || "");
  const [date, setDate] = useState(
    new Date(new Date().setDate(new Date().getDate() + 1))
      .toISOString()
      .split("T")[0],
  );
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
    // getAppointments();
  }, []);

  const selectedDoc = doctors.find((d) => String(d.id) === selectedDoctor);

  const DAYS = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  function parseAvailableDays(str) {
    if (!str) return [];

    // Range: "Monday - Friday"
    if (str.includes("-")) {
      const [start, end] = str.split("-").map((s) => s.trim());
      const startIdx = DAYS.indexOf(start);
      const endIdx = DAYS.indexOf(end);

      if (startIdx === -1 || endIdx === -1) return [];

      return DAYS.slice(startIdx, endIdx + 1);
    }

    // Comma: "Monday, Wednesday"
    return str.split(",").map((d) => d.trim());
  }

  function isDateAllowed(dateStr, availableDays) {
    const date = new Date(dateStr);
    const dayName = DAYS[date.getDay()];
    return availableDays.includes(dayName);
  }

  const availableDays = parseAvailableDays(selectedDoc?.available_days);

  function generateTimeSlots(range: string, interval = 30): string[] {
    const [startStr, endStr] = range.split(" - ");

    const parseTime = (timeStr: string) => {
      const [time, modifier] = timeStr.split(" ");
      let [hours, minutes] = time.split(":").map(Number);

      if (modifier === "PM" && hours !== 12) hours += 12;
      if (modifier === "AM" && hours === 12) hours = 0;

      return new Date(0, 0, 0, hours, minutes);
    };

    const formatTime = (date: Date) => {
      let hours = date.getHours();
      const minutes = date.getMinutes();
      const modifier = hours >= 12 ? "PM" : "AM";

      hours = hours % 12 || 12;

      return `${hours}:${minutes.toString().padStart(2, "0")} ${modifier}`;
    };

    const start = parseTime(startStr);
    const end = parseTime(endStr);

    const slots: string[] = [];
    const current = new Date(start);

    while (current < end) {
      slots.push(formatTime(current));
      current.setMinutes(current.getMinutes() + interval);
    }

    return slots;
  }

  const timeSlots = selectedDoc?.available_time
    ? generateTimeSlots(selectedDoc.available_time, 30)
    : [];

  function to24Hour(timeStr: string): string {
    const [time, modifier] = timeStr.split(" ");
    let [hours, minutes] = time.split(":").map(Number);

    if (modifier === "PM" && hours !== 12) hours += 12;
    if (modifier === "AM" && hours === 12) hours = 0;

    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}`;
  }

  function isSlotBooked(appointments, date, time) {
    return appointments.some(
      (appt) =>
        appt.appointment_date === date && appt.appointment_time === time,
    );
  }

  async function getAppointments() {
    // Double-booking check
    const url = "http://localhost:8000/api/appointments";
    const params = new URLSearchParams();
    params.append("doctor_id", selectedDoctor);
    console.log(`${url}?${params}`);

    let alreadyBooked = false;

    try {
      const res = await fetch(`${url}?${params}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await res.json();
      let errorMessage = "Error fetching appointments";
      if (!res.ok) {
        throw new Error(data.detail || errorMessage);
      }

      console.log("Appointments:", data);
      console.log(date, to24Hour(time));

      if (isSlotBooked(data, date, `${to24Hour(time)}:00`)) {
        alreadyBooked = true;
        setLoading(false);
      }
    } catch (error) {
      console.error("Error fetching doctors:", error);
    }

    if (alreadyBooked) {
      throw new Error(
        "This time slot is already booked. Please choose another.",
      );
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDoctor || !date || !time || !patientName || !patientPhone) {
      toast.error("Please fill all fields");
      return;
    }
    let errorMessage = "";
    setLoading(true);

    try {
      await getAppointments();
      const url = "http://localhost:8000/api/appointments";
      const payload = {
        patient_name: patientName,
        patient_phone: patientPhone,
        doctor_id: selectedDoctor,
        appointment_date: date,
        appointment_time: to24Hour(time),
      };

      // console.log(payload);

      const response = await fetch(url, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      let errorMessage = "Error creating an appointment";
      if (!response.ok) {
        throw new Error(errorMessage);
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
              Available: {selectedDoc.available_days} | Timings:{" "}
              {selectedDoc.available_time}
            </p>
          )}
        </div>
        <div>
          <Label>Date</Label>
          <Input
            type="date"
            value={date}
            disabled={!selectedDoc}
            onChange={(e) => {
              const selected = e.target.value;

              if (!isDateAllowed(selected, availableDays)) {
                alert("This doctor is not available on the selected day.");
                return;
              }

              setDate(selected);
            }}
            min={
              new Date(new Date().setDate(new Date().getDate() + 1))
                .toISOString()
                .split("T")[0]
            }
          />
        </div>
        <div>
          <Label>Time Slot</Label>
          <Select value={time} onValueChange={setTime} disabled={!selectedDoc}>
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
