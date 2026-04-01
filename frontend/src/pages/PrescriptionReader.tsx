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

interface ScannedMedicine {
  name: string;
  dosage: string;
  frequency: string;
  stockStatus: "in-stock" | "low-stock" | "out-of-stock";
  stockQuantity: number;
  price: number | null;
  medicineId: number | null;
}

interface ScanResult {
  medicines: ScannedMedicine[];
  summary: string;
}

const PrescriptionReader = () => {
  const { user, checkTokenExpiry } = useAuthStore();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [selectedPrescription, setSelectedPrescription] = useState<any>(null);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const [isDragging, setIsDragging] = useState(false);

  useEffect(() => {
    if (!user) return;
    checkTokenExpiry();

    async function getCustomerPrescriptions() {
      const url = "http://localhost:8000/prescriptions";

      try {
        const res = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: `Bearer ${user.auth_token}`,
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
        const url = "http://localhost:8000/prescriptions/create";

        try {
          const payload = {
            image_base64: base64Image,
          };
          const response = await fetch(url, {
            method: "POST",
            headers: {
              Authorization: `Bearer ${user.auth_token}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
          });
          const data = await response.json();
          console.log(data);
          setHistory([data, ...history]);
        } catch (error) {
          console.error("Error creating customer prescription:", error);
        }
      }

      await uploadPrescription(base64Full);

      // const scanResult: ScanResult = data;
      // setResult(scanResult);

      // // Update prescription record
      // if (prescription) {
      //   await supabase
      //     .from("prescriptions")
      //     .update({
      //       extracted_medicines: scanResult.medicines.map((m) => m.name),
      //       ai_summary: scanResult.summary,
      //       status: "done",
      //     })
      //     .eq("prescription_id", prescription.prescription_id);
      // }

      // Refresh history
      // const { data: histData } = await supabase
      //   .from("prescriptions")
      //   .select("*")
      //   .eq("customer_id", user.user_id)
      //   .order("scan_date", { ascending: false });
      // setHistory(histData || []);

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

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "in-stock":
        return "✅ In Stock";
      case "low-stock":
        return "⚠️ Low Stock";
      default:
        return "❌ Out of Stock";
    }
  };

  const availableCount = result
    ? result.medicines.filter((m) => m.stockStatus !== "out-of-stock").length
    : 0;
  const totalCount = result ? result.medicines.length : 0;
  const unavailableCount = totalCount - availableCount;

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
              <p className="text-sm text-foreground">{result.summary}</p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {result.medicines.map((med, i) => (
                <div
                  key={i}
                  className="bg-card border border-border rounded-xl p-4 flex flex-col gap-3 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <Pill className="h-4 w-4 text-primary shrink-0" />
                      <div>
                        <p className="font-medium text-foreground text-sm">
                          {med.name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {med.dosage !== "N/A" ? med.dosage : ""}{" "}
                          {med.frequency !== "N/A" ? `• ${med.frequency}` : ""}
                        </p>
                      </div>
                    </div>
                    {getStatusIcon(med.stockStatus)}
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span
                        className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                          med.stockStatus === "in-stock"
                            ? "bg-green-500/10 text-green-600"
                            : med.stockStatus === "low-stock"
                              ? "bg-yellow-500/10 text-yellow-600"
                              : "bg-destructive/10 text-destructive"
                        }`}
                      >
                        {getStatusLabel(med.stockStatus)}
                      </span>
                      {med.stockQuantity > 0 && (
                        <span className="text-xs text-muted-foreground">
                          Qty: {med.stockQuantity}
                        </span>
                      )}
                    </div>
                    {med.price && (
                      <span className="text-xs font-medium text-foreground">
                        ₹{med.price}
                      </span>
                    )}
                  </div>

                  {/*{med.stockStatus === "out-of-stock" && (
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-full gap-1 text-xs"
                      onClick={() => handleRequestMedicine(med)}
                    >
                      <ShoppingCart className="h-3 w-3" /> Request Order
                    </Button>
                  )}*/}
                </div>
              ))}
            </div>

            {/* Summary */}
            <div className="p-3 bg-muted/50 rounded-lg text-sm text-muted-foreground text-center">
              {availableCount} of {totalCount} medicines available in our store
            </div>

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
        <div className="space-y-3">
          {[1, 2].map((i) => (
            <div key={i} className="h-24 bg-muted rounded-xl animate-pulse" />
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
              key={p.prescription_id}
              className="bg-card border border-border rounded-xl p-4"
            >
              {p.image_base64 && (
                <img
                  src={`data:image/jpeg;base64,${p.image_base64}`}
                  alt="Prescription"
                  className="w-full h-32 object-cover rounded-lg mb-3"
                />
              )}
              <p className="text-xs text-muted-foreground mb-1">
                {new Date(p.scan_date).toLocaleDateString()}
              </p>
              <p className="text-sm text-foreground line-clamp-2 mb-2">
                {p.ai_summary || "No summary"}
              </p>
              <div className="flex items-center justify-between">
                <StatusBadge status={p.status} />
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedPrescription(p)}
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
          {selectedPrescription && (
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
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default PrescriptionReader;
