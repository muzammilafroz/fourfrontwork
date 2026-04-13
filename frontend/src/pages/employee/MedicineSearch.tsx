import { useState, useEffect } from "react";
import { useAuthStore } from "@/stores/authStore";

import { CardSkeleton } from "@/components/LoadingSkeleton";
import { EmptyState } from "@/components/EmptyState";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Search, Pill } from "lucide-react";

// TODO: Make the search query hit the backend.
const MedicineSearch = () => {
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [medicines, setMedicines] = useState<any[]>([]);
  const [filtered, setFiltered] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const API_BASE = "http://localhost:8000/api";

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch(`${API_BASE}/medicines`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        const safe = Array.isArray(data) ? data : [];
        setMedicines(safe);
        setFiltered(safe);
      } catch {
        toast.error("Failed to load medicines");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (!search.trim()) {
        setFiltered(medicines);
      } else {
        const q = search.toLowerCase();
        setFiltered(
          medicines.filter(
            (m) =>
              m.name.toLowerCase().includes(q) ||
              m.composition?.toLowerCase().includes(q) ||
              m.brand?.toLowerCase().includes(q),
          ),
        );
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [search, medicines]);

  const handlePreorder = async (med: any) => {
    try {
      const payload = {
        medicine_name: med.name,
        composition: med.composition,
        requested_date: new Date(),
        status: "pending",
        customer_name: user.name,
        customer_phone: user.phone,
      };
      console.log(payload);

      const res = await fetch(`${API_BASE}/medicine-requests`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error();
      toast.success("Request submitted!");
    } catch {
      toast.error("Failed to submit request");
    }
    // console.log("TODO: Implement pre-orders.", med);
  };

  if (loading) return <CardSkeleton count={8} />;

  const getStockBadge = (qty: number) => {
    if (qty === 0)
      return { label: "🔴 Out of Stock", color: "text-destructive" };
    if (qty <= 10) return { label: "🟡 Low Stock", color: "text-warning" };
    return { label: "🟢 In Stock", color: "text-success" };
  };

  return (
    <div>
      <h1 className="text-2xl font-serif font-bold text-foreground mb-4">
        Medicine Search
      </h1>
      <div className="relative mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search by name, composition, or brand"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-10"
        />
      </div>

      {filtered.length === 0 ? (
        <EmptyState
          title="No medicines found"
          description={
            search
              ? "Try a different search term."
              : "No medicines in inventory yet."
          }
          icon={<Pill className="h-8 w-8 text-muted-foreground" />}
        />
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filtered.map((med) => {
            const stock = getStockBadge(med.stock_quantity);
            // Find alternatives with same composition
            const alternatives = med.composition
              ? medicines
                  .filter(
                    (m) =>
                      m.medicine_id !== med.medicine_id &&
                      m.composition === med.composition,
                  )
                  .slice(0, 3)
              : [];
            return (
              <div
                key={med.id}
                className="bg-card rounded-xl border border-border p-4 hover:shadow-md transition-shadow"
              >
                <h3 className="font-semibold text-foreground">{med.name}</h3>
                <p className="text-xs text-muted-foreground mb-1">
                  {med.brand}
                </p>
                {/*<p className="text-xs text-muted-foreground mb-2">
                  {med.composition}
                </p>*/}
                <p className="text-xs text-muted-foreground mb-2 truncate max-w-[200px]">
                  {med.composition}
                </p>
                <p className="text-primary font-medium mb-1">
                  ₹ {med.price.toFixed(2)}
                </p>
                <p className={`text-xs font-medium mb-1 ${stock.color}`}>
                  {stock.label} ({med.stock_quantity})
                </p>
                <p className="text-xs text-muted-foreground mb-3">
                  Exp: {med.expiry_date || "N/A"}
                </p>

                {/*TODO: Implement a medicine request feature.*/}
                <Button
                  size="sm"
                  variant="outline"
                  className="w-full mb-2"
                  onClick={() => handlePreorder(med)}
                >
                  Request Medicine
                </Button>

                {/*{med.stock_quantity === 0 && (
                  <Button
                    size="sm"
                    variant="outline"
                    className="w-full mb-2"
                    onClick={() => handlePreorder(med)}
                  >
                    Request Preorder
                  </Button>
                )}*/}

                {alternatives.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {alternatives.map((alt) => (
                      <span
                        key={alt.id}
                        className="px-2 py-0.5 bg-muted rounded text-[10px] text-muted-foreground"
                      >
                        {alt.name}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default MedicineSearch;
