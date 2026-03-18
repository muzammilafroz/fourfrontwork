import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';
// import { supabase } from '@/integrations/supabase/client';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Pill, Eye, EyeOff } from 'lucide-react';
import { toast } from 'sonner';
import bcrypt from 'bcryptjs';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) { toast.error('Please fill all fields'); return; }
    setLoading(true);

    try {
      // const { data: users, error } = await supabase
      //   .from('users')
      //   .select('*')
      //   .eq('email', email)
      //   .limit(1);

      // JWT use here.
      const users = [
        {
          "email": "vikram@gmail.com",
          "name": "Vikram",
          "password": "vik",
          "status": "valid",
          "user_id": 1,
          "role": "customer",
          "phone": ""
        }
      ]

      const error = false;
      if (error) throw error;

      if (!users || users.length === 0) { toast.error('Invalid email or password'); return; }

      const user = users[0];
      const valid = bcrypt.compareSync(password, user.password);
      if (!valid) { toast.error('Invalid email or password'); return; }

      if (user.status === 'blocked') {
        toast.error('Your account has been blocked. Please contact the pharmacy.');
        return;
      }

      login({
        user_id: user.user_id,
        name: user.name,
        email: user.email,
        role: user.role,
        phone: user.phone || '',
        status: user.status,
      });

      toast.success(`Welcome back, ${user.name}!`);
      const path = user.role === 'owner' ? '/owner/overview' : user.role === 'employee' ? '/employee/medicines' : '/customer/doctors';
      navigate(path);
    } catch (err) {
      toast.error(err.message || 'Login failed');
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
          <p className="text-muted-foreground">Sign in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="bg-card rounded-xl border border-border p-6 space-y-4 shadow-sm">
          <div>
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
          </div>
          <div>
            <Label htmlFor="password">Password</Label>
            <div className="relative">
              <Input id="password" type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} />
              <button type="button" className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </Button>
          <p className="text-center text-sm text-muted-foreground">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary hover:underline">Register</Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Login;
