import { create } from "zustand";
import { persist } from "zustand/middleware";
import { jwtDecode } from "jwt-decode";

export interface AuthUser {
  user_id: number;
  name: string;
  email: string;
  role: string;
  phone: string;
  status: string;
  auth_token: string;
}

interface AuthState {
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (user: AuthUser) => void;
  logout: () => void;
  checkTokenExpiry: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,

      login: (user) => {
        if (user.status === "inactive") {
          // Prevent login for inactive users
          console.error("Login failed: User is inactive");
          return;
        }
        set({ user, isAuthenticated: true });
      },

      logout: () => {
        set({ user: null, isAuthenticated: false });
        window.location.href = "/";
      },

      checkTokenExpiry: () => {
        const user = get().user;
        if (!user) return;

        // Force logout if user is found to be inactive
        if (user.status === "inactive") {
          get().logout();
          return;
        }

        try {
          const decoded: any = jwtDecode(user.auth_token);
          const currentTime = Date.now() / 1000;

          if (decoded.exp < currentTime) {
            get().logout();
          }
        } catch (error) {
          get().logout();
        }
      },
    }),
    { name: "medease-auth" },
  ),
);
