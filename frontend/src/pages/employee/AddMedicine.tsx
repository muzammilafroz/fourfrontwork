import { useAuthStore } from "@/stores/authStore";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { z } from "zod";

const schema = z.object({
  name: z.string().min(1, "Name required").max(200),
  composition: z.string().max(500).optional(),
  brand: z.string().max(200).optional(),
  price: z.number().positive("Price must be positive"),
  stock_quantity: z.number().int().min(0),
  expiry_date: z.string().optional(),
  supplier: z.string().max(200).optional(),
});

const AddMedicine = () => {
  const { user } = useAuthStore();
  const token = useAuthStore((state) => state.getAuthToken());

  const [form, setForm] = useState({
    name: "",
    composition: "",
    brand: "",
    price: "",
    stock_quantity: "",
    expiry_date: "",
    supplier: "",
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [medicines, setMedicines] = useState<any[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    const load = async () => {
      const url = "http://localhost:8000/api/medicines";
      try {
        const res = await fetch(url, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Failed to fetch medicines");
        }

        console.log(data);
        const safe = Array.isArray(data) ? data : [];

        setMedicines(safe);
      } catch {
        toast.error("Failed to fetch medicines");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const parsed = schema.safeParse({
      ...form,
      price: parseFloat(form.price) || 0,
      stock_quantity: parseInt(form.stock_quantity) || 0,
      composition: form.composition || undefined,
      brand: form.brand || undefined,
      expiry_date: form.expiry_date || undefined,
      supplier: form.supplier || undefined,
    });
    if (!parsed.success) {
      const errs: Record<string, string> = {};
      parsed.error.issues.forEach((i) => {
        errs[i.path[0] as string] = i.message;
      });
      setErrors(errs);
      return;
    }
    setErrors({});
    setLoading(true);
    try {
      const payload = {
        name: form.name,
        composition: form.composition || "No information",
        brand: form.brand || form.name,
        price: parseFloat(form.price),
        stock_quantity: parseInt(form.stock_quantity) || 0,
        expiry_date:
          form.expiry_date ||
          new Date(Date.now() + 365 * 24 * 60 * 60 * 1000)
            .toISOString()
            .split("T")[0],
      };

      try {
        console.log(payload);
        const res = await fetch("http://localhost:8000/api/medicines", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(payload),
        });
        const data = await res.json();

        if (!res.ok) {
          throw new Error(data.detail || "Failed to add medicine");
        }

        console.log("Success:", data);
        toast.success("Medicine added successfully!");
      } catch (error) {
        console.error("Error:", error.message);
        toast.error("Error: Something went wrong.");
      }

      setForm({
        name: "",
        composition: "",
        brand: "",
        price: "",
        stock_quantity: "",
        expiry_date: "",
        supplier: "",
      });
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  const filtered = search
    ? medicines.filter((m) =>
        m.name.toLowerCase().includes(search.toLowerCase()),
      )
    : medicines;

  const getStockBadge = (qty: number) => {
    if (qty <= 20) return { label: "🔴", color: "text-destructive" };
    if (qty <= 100) return { label: "🟡", color: "text-warning" };
    return { label: "🟢", color: "text-success" };
  };

  return (
    <div>
      <h1 className="text-2xl font-serif font-bold text-foreground mb-6">
        Add Medicine to Inventory
      </h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <form
          onSubmit={handleSubmit}
          className="bg-card rounded-xl border border-border p-6 space-y-4"
        >
          {(["name", "composition", "brand", "supplier"] as const).map(
            (field) => (
              <div key={field}>
                <Label className="capitalize">{field}</Label>
                <Input
                  value={form[field]}
                  onChange={(e) =>
                    setForm({ ...form, [field]: e.target.value })
                  }
                />
                {errors[field] && (
                  <p className="text-xs text-destructive mt-1">
                    {errors[field]}
                  </p>
                )}
              </div>
            ),
          )}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <Label>Price (₹)</Label>
              <Input
                type="number"
                step="0.50"
                value={form.price}
                onChange={(e) => setForm({ ...form, price: e.target.value })}
              />
              {errors.price && (
                <p className="text-xs text-destructive mt-1">{errors.price}</p>
              )}
            </div>
            <div>
              <Label>Stock Qty</Label>
              <Input
                type="number"
                step="50"
                value={form.stock_quantity}
                onChange={(e) =>
                  setForm({ ...form, stock_quantity: e.target.value })
                }
              />
            </div>
          </div>
          <div>
            <Label>Expiry Date</Label>
            <Input
              type="date"
              value={form.expiry_date}
              onChange={(e) =>
                setForm({ ...form, expiry_date: e.target.value })
              }
            />
          </div>
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Adding..." : "Add Medicine"}
          </Button>
        </form>

        <div>
          <div className="mb-3">
            <Input
              placeholder="Search inventory..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="bg-card rounded-xl border border-border overflow-x-auto max-h-[500px] overflow-y-auto">
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-card">
                <tr className="border-b border-border bg-muted/50">
                  <th className="text-left p-3 text-muted-foreground font-medium">
                    Name
                  </th>
                  <th className="text-left p-3 text-muted-foreground font-medium">
                    Brand
                  </th>
                  <th className="text-left p-3 text-muted-foreground font-medium">
                    Price
                  </th>
                  <th className="text-left p-3 text-muted-foreground font-medium">
                    Stock
                  </th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((m) => {
                  const stock = getStockBadge(m.stock_quantity);
                  return (
                    <tr
                      key={m.id}
                      className="border-b border-border last:border-0"
                    >
                      <td className="p-3 text-foreground">{m.name}</td>
                      <td className="p-3 text-muted-foreground">{m.brand}</td>
                      <td className="p-3 text-foreground text-right">
                        ₹ {m.price.toFixed(2)}
                      </td>
                      <td className="p-3 text-right">
                        <span className={stock.color}>{m.stock_quantity}</span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddMedicine;
