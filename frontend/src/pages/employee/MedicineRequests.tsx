import { useState, useEffect } from "react";
import { useAuthStore } from "@/stores/authStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { StatusBadge } from "@/components/StatusBadge";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import { toast } from "sonner";
import { ClipboardList, Send } from "lucide-react";

const API = "http://localhost:8000/api/medicine-requests";

type Request = {
  id: number;
  medicine_name: string;
  composition?: string;
  requested_date: string;

  customer_name?: string;
  customer_phone?: string;
  status: string;
};

const EmployeeMedicineRequest = () => {
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [customerName, setCustomerName] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [medicineName, setMedicineName] = useState("");
  const [composition, setComposition] = useState("");
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const load = async () => {
    try {
      const res = await fetch(API, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await res.json();
      console.log(data);
      setRequests(Array.isArray(data) ? data : []);
    } catch {
      toast.error("Failed to load requests");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) load();
    else setLoading(false);
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!medicineName.trim()) {
      toast.error("Medicine name is required");
      return;
    }
    setSubmitting(true);
    try {
      const res = await fetch(API, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          medicine_name: medicineName,
          composition,
          requested_date: new Date(),
          status: "pending",
          customer_name: customerName,
          customer_phone: customerPhone,
        }),
      });
      if (!res.ok) throw new Error();
      toast.success("Request submitted!");
      setMedicineName("");
      setComposition("");
      setCustomerName("");
      setCustomerPhone("");
      load();
    } catch {
      toast.error("Failed to submit request");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingSkeleton />;

  return (
    <div className="space-y-4">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">
            Medicine Requests
          </h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Log medicine requests not currently in stock
          </p>
        </div>
        {requests.length > 0 && (
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground bg-muted/50 px-2.5 py-1 rounded-full border border-border">
            <ClipboardList className="h-3 w-3" />
            {requests.length} request{requests.length !== 1 ? "s" : ""}
          </div>
        )}
      </div>

      {/* Form Card */}
      <div className="bg-card rounded-xl border border-border overflow-hidden">
        <div className="px-4 py-3 border-b border-border">
          <h2 className="font-semibold text-sm text-foreground">New Request</h2>
          <p className="text-xs text-muted-foreground">
            Fields marked * are required
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
            <div className="space-y-1">
              <Label
                htmlFor="customerName"
                className="text-xs text-muted-foreground"
              >
                Customer Name
              </Label>
              <Input
                id="customerName"
                placeholder="Enter patient name"
                value={customerName}
                onChange={(e) => setCustomerName(e.target.value)}
                className="h-9 text-sm bg-muted/30 border-border/60"
              />
            </div>

            <div className="space-y-1">
              <Label
                htmlFor="customerPhone"
                className="text-xs text-muted-foreground"
              >
                Phone Number
              </Label>
              <Input
                id="customerPhone"
                placeholder="Enter phone number"
                value={customerPhone}
                onChange={(e) => setCustomerPhone(e.target.value)}
                className="h-9 text-sm bg-muted/30 border-border/60"
              />
            </div>

            <div className="space-y-1">
              <Label
                htmlFor="medicineName"
                className="text-xs text-muted-foreground"
              >
                Medicine Name <span className="text-primary">*</span>
              </Label>
              <Input
                id="medicineName"
                placeholder="e.g. Amoxicillin 500mg"
                value={medicineName}
                onChange={(e) => setMedicineName(e.target.value)}
                className="h-9 text-sm bg-muted/30 border-border/60"
                required
              />
            </div>

            <div className="space-y-1">
              <Label
                htmlFor="composition"
                className="text-xs text-muted-foreground"
              >
                Composition
              </Label>
              <Input
                id="composition"
                placeholder="Active ingredients"
                value={composition}
                onChange={(e) => setComposition(e.target.value)}
                className="h-9 text-sm bg-muted/30 border-border/60"
              />
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button
              type="submit"
              disabled={submitting || !medicineName.trim()}
              size="sm"
              className="gap-1.5 font-medium"
            >
              {submitting ? (
                <>
                  <div className="h-3 w-3 animate-spin rounded-full border-2 border-current border-t-transparent" />
                  Submitting…
                </>
              ) : (
                <>
                  <Send className="h-3 w-3" />
                  Submit Request
                </>
              )}
            </Button>
          </div>
        </form>
      </div>

      {/* Table Card */}
      <div className="bg-card rounded-xl border border-border overflow-hidden">
        <div className="px-4 py-3 border-b border-border">
          <h2 className="font-semibold text-sm text-foreground">
            Request History
          </h2>
        </div>

        {requests.length === 0 ? (
          <div className="py-10 text-center">
            <ClipboardList className="h-8 w-8 text-muted-foreground/30 mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">No requests yet</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border bg-muted/20">
                  {[
                    "Medicine",
                    "Composition",
                    "Customer",
                    "Phone",
                    "Date",
                    "Status",
                  ].map((h) => (
                    <th
                      key={h}
                      className="px-4 py-2.5 text-left text-xs font-medium text-muted-foreground uppercase tracking-wide"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-border/50">
                {requests.map((r) => (
                  <tr
                    key={r.id}
                    className="hover:bg-muted/20 transition-colors"
                  >
                    <td className="px-4 py-2.5">
                      <p className="font-medium text-foreground leading-tight">
                        {r.medicine_name}
                      </p>
                    </td>
                    <td className="px-4 py-2.5 text-muted-foreground text-sm">
                      {r.composition || (
                        <span className="text-muted-foreground/30">—</span>
                      )}
                    </td>
                    <td className="px-4 py-2.5 text-sm">
                      {r.customer_name || (
                        <span className="text-muted-foreground/30">—</span>
                      )}
                    </td>
                    <td className="px-4 py-2.5 text-muted-foreground text-sm">
                      {r.customer_phone || (
                        <span className="text-muted-foreground/30">—</span>
                      )}
                    </td>
                    <td className="px-4 py-2.5 text-muted-foreground text-sm whitespace-nowrap">
                      {new Date(r.requested_date).toLocaleDateString("en-IN", {
                        day: "numeric",
                        month: "short",
                        year: "numeric",
                      })}
                    </td>
                    <td className="px-4 py-2.5">
                      <StatusBadge status={r.status} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmployeeMedicineRequest;
