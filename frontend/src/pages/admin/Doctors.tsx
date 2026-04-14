import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { EmptyState } from "@/components/EmptyState";
import { LoadingSkeleton } from "@/components/LoadingSkeleton";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { Plus, Pencil, Trash2, Stethoscope } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";

const API = "http://localhost:8000/api/doctors";

const DoctorsManagement = () => {
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [doctors, setDoctors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [editDoc, setEditDoc] = useState<any>(null);
  const [deleteDoc, setDeleteDoc] = useState<any>(null);
  const [showAdd, setShowAdd] = useState(false);
  const [form, setForm] = useState({
    name: "",
    specialization: "",
    available_days: "",
    available_time: "",
    consultation_fee: "",
    image_url: "",
  });

  const fetchDoctors = async () => {
    try {
      const res = await fetch(API, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error("Failed to fetch doctors");

      const data = await res.json();
      console.log(data);
      setDoctors(Array.isArray(data) ? data : []);
      // setFilteredDoctors(Array.isArray(data) ? data : []);
    } catch (err: any) {
      toast.error(err.message || "Error loading doctors");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) fetchDoctors();
    else {
      setLoading(false);
      toast.error("Not authenticated");
    }
  }, [token]);

  const handleSave = async () => {
    if (!form.name || !form.specialization) {
      toast.error("Name & specialization required");
      return;
    }

    const payload = {
      name: form.name,
      specialization: form.specialization || null,
      available_days: form.available_days || null,
      available_time: form.available_time || null,
      consultation_fee: parseFloat(form.consultation_fee) || 0,
      image_url: form.image_url || null,
    };

    try {
      const res = await fetch(editDoc ? `${API}/${editDoc.id}` : API, {
        method: editDoc ? "PATCH" : "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) throw new Error("Save failed");

      toast.success(
        editDoc ? "Doctor updated successfully!" : "Doctor added successfully!",
      );

      setForm({
        name: "",
        specialization: "",
        available_days: "",
        available_time: "",
        consultation_fee: "",
        image_url: "",
      });
      setEditDoc(null);
      setShowAdd(false);
      fetchDoctors();
    } catch (err: any) {
      toast.error(err.message || "Save error");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!deleteDoc) return;

    try {
      const res = await fetch(`${API}/${deleteDoc.id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!res.ok) throw new Error("Delete failed");
      toast.success("Doctor deleted successfully!");

      setDoctors((prev) => prev.filter((d) => d.id !== deleteDoc.id));
    } catch (err: any) {
      toast.error(err.message || "Delete error");
    } finally {
      setDeleteDoc(null);
    }
  };

  if (loading) return <LoadingSkeleton />;

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-serif font-bold text-foreground">
          Doctors Management
        </h1>
        <Button
          onClick={() => {
            setForm({
              name: "",
              specialization: "",
              available_days: "",
              available_time: "",
              consultation_fee: "",
              image_url: "",
            });
            setShowAdd(true);
          }}
        >
          <Plus className="h-4 w-4 mr-2" /> Add Doctor
        </Button>
      </div>

      {doctors.length === 0 ? (
        <EmptyState
          title="No doctors"
          description="Add your first doctor."
          icon={<Stethoscope className="h-8 w-8 text-muted-foreground" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {doctors.map((d) => (
            <div
              key={d.id}
              className="bg-card rounded-xl border border-border p-4"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  {d.image_url ? (
                    <img
                      src={d.image_url}
                      alt={d.name}
                      className="w-12 h-12 rounded-full object-cover"
                    />
                  ) : (
                    <Stethoscope className="h-6 w-6 text-primary" />
                  )}
                </div>
                <div>
                  <h3 className="font-semibold text-foreground">{d.name}</h3>
                  <p className="text-sm text-muted-foreground">
                    {d.specialization}
                  </p>
                </div>
              </div>
              {/*<p className="text-sm text-muted-foreground">
                📅 {d.available_days || "N/A"} | ⏰ {d.available_time || "N/A"}
              </p>*/}
              <div>
                <p className="text-xs text-muted-foreground mb-1">
                  Available Days
                </p>
                <div className="flex flex-wrap gap-1">
                  {d.available_days ? (
                    d.available_days.split(",").map((day) => (
                      <span
                        key={day}
                        className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary"
                      >
                        {day}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-muted-foreground">
                      Not set
                    </span>
                  )}
                </div>
              </div>
              <div className="flex flex-wrap gap-0.5 mt-2 flex-col">
                <p className="text-xs text-muted-foreground mb-1">Timings</p>
                <p className="text-sm text-muted-foreground">
                  {d.available_time}
                </p>
              </div>

              <p className="text-primary font-medium">₹{d.consultation_fee.toLocaleString()}</p>
              <div className="flex gap-2 mt-4 pt-3 border-t border-border">
                <Button
                  size="sm"
                  variant="outline"
                  className="flex-1 gap-1 h-8 text-xs"
                  onClick={() => {
                    setForm({
                      name: d.name,
                      specialization: d.specialization || "",
                      available_days: d.available_days || "",
                      available_time: d.available_time || "",
                      consultation_fee: String(d.consultation_fee),
                      image_url: d.image_url || "",
                    });
                    setEditDoc(d);
                  }}
                >
                  <Pencil className="h-3 w-3" /> Edit
                </Button>
                <Button
                  size="sm"
                  variant="destructive"
                  onClick={() => setDeleteDoc(d)}
                  className="flex-1 gap-1 h-8 text-xs"
                >
                  <Trash2 className="h-3 w-3" /> Delete
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      <Dialog
        open={showAdd || !!editDoc}
        onOpenChange={() => {
          setShowAdd(false);
          setEditDoc(null);
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editDoc ? "Edit Doctor" : "Add Doctor"}</DialogTitle>
          </DialogHeader>
          <div className="space-y-3">
            {(
              [
                "name",
                "specialization",
                "available_days",
                "available_time",
                "image_url",
              ] as const
            ).map((f) => (
              <div key={f}>
                <Label className="capitalize">{f.replace("_", " ")}</Label>
                <Input
                  value={form[f]}
                  onChange={(e) => setForm({ ...form, [f]: e.target.value })}
                />
              </div>
            ))}
            <div>
              <Label>Fee (₹)</Label>
              <Input
                type="number"
                value={form.consultation_fee}
                onChange={(e) =>
                  setForm({ ...form, consultation_fee: e.target.value })
                }
              />
            </div>
          </div>
          <DialogFooter>
            <Button onClick={handleSave}>Save</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={!!deleteDoc} onOpenChange={() => setDeleteDoc(null)}>
        <DialogContent className="sm:max-w-sm">
          <DialogHeader>
            <DialogTitle className="text-base font-semibold">
              Confirm Deletion
            </DialogTitle>
          </DialogHeader>

          <p className="text-sm text-muted-foreground">
            Are you sure you want to delete{" "}
            <span className="font-medium text-foreground">
              {deleteDoc?.name}
            </span>
            ? This action cannot be undone.
          </p>

          <DialogFooter className="gap-2 mt-2">
            <Button
              variant="outline"
              onClick={() => setDeleteDoc(null)}
              className="h-8 text-xs"
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              className="h-8 text-xs gap-1.5"
            >
              <Trash2 className="h-3 w-3" />
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default DoctorsManagement;
