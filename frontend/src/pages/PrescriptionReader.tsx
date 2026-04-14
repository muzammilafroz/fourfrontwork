import { useState, useEffect, useCallback } from "react";
import { useAuthStore } from "@/stores/authStore";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/EmptyState";
import { StatusBadge } from "@/components/StatusBadge";
import { toast } from "sonner";

import {
  Upload,
  FileText,
  Loader2,
  Pill,
  ShoppingCart,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  ScanLine,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

// interface ScannedMedicine {
//   name: string;
//   dosage: string;
//   frequency: string;
//   stockStatus: "in-stock" | "low-stock" | "out-of-stock";
//   stockQuantity: number;
//   price: number | null;
//   medicineId: number | null;
// }

// interface ScanResult {
//   medicines: ScannedMedicine[];
//   summary: string;
// }

interface Medication {
  name: string;
  dosage: string;
  frequency: string;
  duration: string;
}

interface Prescription {
  id: number;
  customer_id: number;
  created_at: string;
  diagnosis: string;
  image_base64: string;
  summary: string;
  medications: Medication[];
}

const PrescriptionReader = () => {
  const { user, checkTokenExpiry } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<Prescription | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [selectedPrescription, setSelectedPrescription] = useState<any>(null);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    if (!user) return;
    checkTokenExpiry();

    async function getCustomerPrescriptions() {
      const url = "http://localhost:8000/api/prescriptions";

      try {
        const res = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Login failed.");
        }

        console.log("Prescriptions for customer:", data);
        setHistory(data || []);
        setLoadingHistory(false);
      } catch (error) {
        console.error("Error fetching customer prescriptions:", error);
        setHistory([]);
        setLoadingHistory(false);
      }
    }
    getCustomerPrescriptions();
  }, [user]);

  const processFile = (f: File) => {
    if (
      !f.type.match(/^image\/(jpeg|png|webp|jpg)$/) &&
      f.type !== "application/pdf"
    ) {
      toast.error("Please upload a JPG, PNG, or PDF file.");
      return;
    }
    setFile(f);
    const reader = new FileReader();
    reader.onload = () => setPreview(reader.result as string);
    reader.readAsDataURL(f);
    setResult(null);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) processFile(f);
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) processFile(f);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback(() => setIsDragging(false), []);

  const handleScan = async () => {
    if (!file || !user) return;
    setScanning(true);
    setResult(null);

    try {
      const reader = new FileReader();
      const base64Full = await new Promise<string>((res) => {
        reader.onload = () => res(reader.result as string);
        reader.readAsDataURL(file);
      });

      // Save prescription image.
      async function uploadPrescription(base64Image: string) {
        const url = "http://localhost:8000/api/prescriptions/create";

        try {
          const payload = {
            image_base64: base64Image,
          };
          const response = await fetch(url, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          });

          const data = await response.json();
          console.log(data);
          data.image_base64 = preview;

          setHistory([data, ...history]);
          setResult(data);
        } catch (error) {
          console.error("Error creating customer prescription:", error);
        }
      }

      await uploadPrescription(base64Full);
      toast.success("Prescription scanned successfully!");
    } catch (err: any) {
      toast.error(err.message || "Failed to scan prescription.");
    } finally {
      setScanning(false);
    }
  };

  // const handleRequestMedicine = async (med: ScannedMedicine) => {
  //   if (!user) return;
  //   try {
  //     const { error } = await supabase.from("medicine_requests").insert({
  //       medicine_name: med.name,
  //       customer_name: user.name,
  //       customer_phone: user.phone,
  //       requested_by: user.user_id,
  //       composition: med.dosage,
  //     });
  //     if (error) throw error;
  //     toast.success(`${med.name} request submitted!`);
  //   } catch (err: any) {
  //     toast.error(err.message);
  //   }
  // };

  // const handleRequestAll = async () => {
  //   if (!result || !user) return;
  //   const unavailable = result.medicines.filter(
  //     (m) => m.stockStatus === "out-of-stock",
  //   );
  //   if (unavailable.length === 0) return;
  //   try {
  //     const rows = unavailable.map((m) => ({
  //       medicine_name: m.name,
  //       customer_name: user.name,
  //       customer_phone: user.phone,
  //       requested_by: user.user_id,
  //       composition: m.dosage,
  //     }));
  //     const { error } = await supabase.from("medicine_requests").insert(rows);
  //     if (error) throw error;
  //     toast.success(`${unavailable.length} medicine(s) requested!`);
  //   } catch (err: any) {
  //     toast.error(err.message);
  //   }
  // };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "in-stock":
        return <CheckCircle2 className="h-4 w-4 text-green-500" />;
      case "low-stock":
        return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      default:
        return <XCircle className="h-4 w-4 text-destructive" />;
    }
  };

  // const getStatusLabel = (status: string) => {
  //   switch (status) {
  //     case "in-stock":
  //       return "✅ In Stock";
  //     case "low-stock":
  //       return "⚠️ Low Stock";
  //     default:
  //       return "❌ Out of Stock";
  //   }
  // };

  // const availableCount = result
  //   ? result.medicines.filter((m) => m.stockStatus !== "out-of-stock").length
  //   : 0;
  // const totalCount = result ? result.medicines.length : 0;
  // const unavailableCount = totalCount - availableCount;

  return (
    <div>
      <h1 className="text-2xl font-serif font-bold text-foreground mb-6">
        💊 Prescription Reader
      </h1>

      {/* Upload Area */}
      <div className="bg-card rounded-xl border border-border p-6 mb-6">
        <div
          className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all duration-300 ${
            isDragging
              ? "border-primary bg-primary/5 scale-[1.01]"
              : "border-border hover:border-primary/50 hover:bg-muted/30"
          }`}
          onClick={() => document.getElementById("rx-upload")?.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <div className="flex flex-col items-center gap-3">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
              <Upload className="h-7 w-7 text-primary" />
            </div>
            <div>
              <p className="text-sm font-medium text-foreground">
                Drop your prescription here or click to upload
              </p>
              <p className="text-xs text-muted-foreground mt-1">
                Supports JPG, PNG, PDF
              </p>
            </div>
          </div>
          <input
            id="rx-upload"
            type="file"
            accept="image/jpeg,image/png,image/webp,application/pdf"
            className="hidden"
            onChange={handleFileChange}
          />
        </div>

        {preview && (
          <div className="mt-5 flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <img
              src={preview}
              alt="Prescription preview"
              className="w-28 h-28 rounded-xl object-cover border border-border shadow-sm"
            />
            <div className="flex flex-col gap-2">
              <p className="text-sm text-muted-foreground">{file?.name}</p>
              <Button
                onClick={handleScan}
                disabled={scanning}
                className="gap-2"
              >
                {scanning ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" /> Scanning...
                  </>
                ) : (
                  <>
                    <ScanLine className="h-4 w-4" /> Scan Prescription
                  </>
                )}
              </Button>
            </div>
          </div>
        )}

        {scanning && (
          <div className="mt-6 space-y-3">
            <div className="flex items-center gap-3 text-sm text-muted-foreground">
              <Loader2 className="h-4 w-4 animate-spin text-primary" />
              <span>AI is reading your prescription...</span>
            </div>
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className="h-16 rounded-xl bg-muted/60 animate-pulse"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </div>
        )}

        {result && !scanning && (
          <div className="mt-6 space-y-5">
            <div className="p-4 bg-primary/5 border border-primary/10 rounded-xl">
              <p className="text-xs font-semibold text-primary uppercase tracking-wide mb-1">
                AI Summary
              </p>
              <p className="text-sm text-foreground">
                {result.summary || "No Summary"}
              </p>
            </div>

            <div className="w-full overflow-hidden rounded-xl border border-border bg-card">
              <table className="w-full text-sm text-left border-collapse">
                <thead className="bg-muted/50 text-muted-foreground font-medium border-b border-border">
                  <tr>
                    <th className="px-4 py-3 font-medium">Medication</th>
                    <th className="px-4 py-3 font-medium">Dosage</th>
                    <th className="px-4 py-3 font-medium">Frequency</th>
                    <th className="px-4 py-3 font-medium">Duration</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {result.medications.map((med, i) => (
                    <tr
                      key={i}
                      className="hover:bg-muted/30 transition-colors group"
                    >
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <Pill className="h-4 w-4 text-primary shrink-0" />
                          <span className="font-medium text-foreground">
                            {med.name}
                          </span>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">
                        {med.dosage ? med.dosage : "—"}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">
                        {med.frequency ? med.frequency : "—"}
                      </td>
                      <td className="px-4 py-3 text-muted-foreground">
                        {med.duration ? med.duration : "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Summary */}
            {/*<div className="p-3 bg-muted/50 rounded-lg text-sm text-muted-foreground text-center">
              {availableCount} of {totalCount} medicines available in our store
            </div>*/}

            {/*{unavailableCount > 0 && (
              <Button
                onClick={handleRequestAll}
                variant="outline"
                className="w-full gap-2"
              >
                <ShoppingCart className="h-4 w-4" /> Request All Unavailable (
                {unavailableCount})
              </Button>
            )}*/}
          </div>
        )}
      </div>

      {/* History */}
      <h2 className="text-lg font-serif font-semibold text-foreground mb-4">
        Prescription History
      </h2>

      {loadingHistory ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="border border-border rounded-xl p-4 space-y-3 animate-pulse"
            >
              <div className="h-32 bg-muted rounded-lg w-full" />
              <div className="flex justify-between">
                <div className="h-3 bg-muted rounded w-1/4" />
                <div className="h-3 bg-muted rounded w-1/4" />
              </div>
              <div className="h-4 bg-muted rounded w-full" />
              <div className="h-8 bg-muted rounded w-20 ml-auto" />
            </div>
          ))}
        </div>
      ) : history.length === 0 ? (
        <EmptyState
          title="No prescriptions yet"
          description="Upload your first one above."
          icon={<FileText className="h-8 w-8 text-muted-foreground" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {history.map((p) => (
            <div
              key={p.id}
              className="group bg-card border border-border rounded-xl p-4 transition-all duration-200 flex flex-col"
            >
              {p.image_base64 ? (
                <img
                  src={p.image_base64}
                  alt="Prescription Scan"
                  className="w-full h-32 object-cover rounded-lg mb-3 bg-muted"
                />
              ) : (
                <div className="w-full h-32 bg-muted rounded-lg mb-3 flex items-center justify-center">
                  <FileText className="h-6 w-6 text-muted-foreground/40" />
                </div>
              )}

              <div className="flex items-center justify-between gap-2 mb-2">
                <time className="text-[10px] uppercase tracking-wider font-medium text-muted-foreground">
                  {new Date(p.created_at).toLocaleDateString(undefined, {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                  })}
                </time>
                <span className="text-[10px] font-mono text-muted-foreground/70 bg-muted px-1.5 py-0.5 rounded">
                  Customer ID: {p.customer_id}
                </span>
              </div>

              <p className="text-sm text-foreground line-clamp-2 mb-4 flex-grow leading-relaxed">
                {p.summary || (
                  <span className="text-muted-foreground italic">
                    No summary available
                  </span>
                )}
              </p>

              <div className="flex items-center justify-end pt-2 border-t border-border/50">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setResult(p)}
                  className="transition-colors"
                >
                  View Details
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Detail Modal */}
      <Dialog
        open={!!selectedPrescription}
        onOpenChange={() => setSelectedPrescription(null)}
      >
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Prescription Details</DialogTitle>
          </DialogHeader>
          {/*{selectedPrescription && (
            <div className="space-y-4">
              {selectedPrescription.image_base64 && (
                <img
                  src={`data:image/jpeg;base64,${selectedPrescription.image_base64}`}
                  alt="Prescription"
                  className="w-full rounded-lg"
                />
              )}
              <p className="text-sm text-muted-foreground">
                {new Date(selectedPrescription.scan_date).toLocaleString()}
              </p>
              <p className="text-sm text-foreground">
                {selectedPrescription.ai_summary}
              </p>
              {selectedPrescription.extracted_medicines && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-2">
                    Extracted Medicines:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {(selectedPrescription.extracted_medicines as string[]).map(
                      (m: string) => (
                        <span
                          key={m}
                          className="px-2 py-1 bg-muted rounded text-xs text-foreground"
                        >
                          {m}
                        </span>
                      ),
                    )}
                  </div>
                </div>
              )}
              <StatusBadge status={selectedPrescription.status} />
            </div>
          )}*/}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PrescriptionReader;
