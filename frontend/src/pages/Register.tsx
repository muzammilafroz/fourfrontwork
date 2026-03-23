import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
// import { supabase } from '@/integrations/supabase/client';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Pill, ShoppingBag, UserCog, Eye, EyeOff } from 'lucide-react';
import { toast } from 'sonner';
import bcrypt from 'bcryptjs';
import { z } from 'zod';

const schema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  email: z.string().email('Invalid email').max(255),
  phone: z.string().min(10, 'Phone must be at least 10 digits').max(15),
  password: z.string().min(6, 'Password must be at least 6 characters').max(100),
});

const Register = () => {
  const [role, setRole] = useState<'customer' | 'employee'>('customer');
  const [form, setForm] = useState({ name: '', email: '', phone: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const strength = form.password.length >= 8 ? (form.password.match(/[A-Z]/) && form.password.match(/[0-9]/) ? 3 : 2) : form.password.length >= 6 ? 1 : 0;
  const strengthLabels = ['Weak', 'Fair', 'Good', 'Strong'];
  const strengthColors = ['bg-destructive', 'bg-warning', 'bg-info', 'bg-success'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const result = schema.safeParse(form);
    if (!result.success) {
      const errs: Record<string, string> = {};
      result.error.issues.forEach((i) => { errs[i.path[0] as string] = i.message; });
      setErrors(errs);
      return;
    }
    setErrors({});
    setLoading(true);

    try {
      const hash = bcrypt.hashSync(form.password, 10);

      // Customer Registration
      if (role === 'customer') {
        // const { data, error } = await supabase
        //   .from('users')
        //   .insert({ name: form.name, email: form.email, phone: form.phone, password: hash, role: 'customer' })
        //   .select()
        //   .single();

        const data = {
          "email": "vikram@gmail.com",
          "name": "Vikram",
          "password": hash,
          "status": "valid",
          "user_id": 1,
          "role": "customer",
          "phone": ""
        }
        const error = false;

        // if (error) {
        //   if (error.message.includes('duplicate')) { toast.error('Email already registered'); }
        //   else throw error;
        //   return;
        // }

        login({ user_id: data.user_id, name: data.name, email: data.email, role: 'customer', phone: data.phone || '', status: 'active' });
        toast.success('Account created! Welcome to MedEase.');
        navigate('/customer/doctors');
      } else {
        // Employee Registration
        // const { error } = await supabase
        //   .from('employee_signup_requests')
        //   .insert({ name: form.name, email: form.email, phone: form.phone, password_hash: hash });
        // if (error) throw error;
        // toast.success('Request submitted! The owner will review your application.');
        // setTimeout(() => navigate('/login'), 3000);
      }
    } catch (err) {
      toast.error(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="absolute top-4 right-4"><ThemeToggle /></div>
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-4">
            <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
              <Pill className="h-5 w-5 text-primary-foreground" />
            </div>
            <span className="font-serif text-2xl font-bold text-foreground">MedEase</span>
          </Link>
          <p className="text-muted-foreground">Create your account</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-card rounded-xl border border-border p-6 space-y-4 shadow-sm">
          {/* Role selection */}
          <div className="grid grid-cols-2 gap-3">
            {([['customer', '🛍️ Customer', ShoppingBag], ['employee', '🧑‍⚕️ Employee', UserCog]] as const).map(([r, label]) => (
              <button
                key={r}
                type="button"
                onClick={() => setRole(r)}
                className={`p-4 rounded-lg border-2 text-center transition-all ${
                  role === r ? 'border-primary bg-primary/5' : 'border-border hover:border-muted-foreground/30'
                }`}
              >
                <div className="text-2xl mb-1">{label.split(' ')[0]}</div>
                <div className="text-sm font-medium text-foreground">{label.split(' ')[1]}</div>
              </button>
            ))}
          </div>

          <div>
            <Label>Full Name</Label>
            <Input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            {errors.name && <p className="text-xs text-destructive mt-1">{errors.name}</p>}
          </div>
          <div>
            <Label>Email</Label>
            <Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            {errors.email && <p className="text-xs text-destructive mt-1">{errors.email}</p>}
          </div>
          <div>
            <Label>Phone</Label>
            <Input value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            {errors.phone && <p className="text-xs text-destructive mt-1">{errors.phone}</p>}
          </div>
          <div>
            <Label>Password</Label>
            <div className="relative">
              <Input type={showPassword ? 'text' : 'password'} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
              <button type="button" className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
            {errors.password && <p className="text-xs text-destructive mt-1">{errors.password}</p>}
            {form.password && (
              <div className="mt-2 flex gap-1 items-center">
                {[0, 1, 2, 3].map((i) => (
                  <div key={i} className={`h-1.5 flex-1 rounded-full ${i <= strength ? strengthColors[strength] : 'bg-muted'}`} />
                ))}
                <span className="text-xs text-muted-foreground ml-2">{strengthLabels[strength]}</span>
              </div>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating...' : role === 'customer' ? 'Create Account' : 'Submit Request'}
          </Button>
          <p className="text-center text-sm text-muted-foreground">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:underline">Sign In</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Register;
