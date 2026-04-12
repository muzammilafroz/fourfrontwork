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
  /** Validates token expiry and returns the token or null */
  getAuthToken: () => string | null;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,

      login: (user) => {
        if (user.status === "inactive") {
          console.error("Login failed: User is inactive");
          return;
        }
        set({ user, isAuthenticated: true });
      },

      logout: () => {
        set({ user: null, isAuthenticated: false });
        // Optional: clear local storage specifically if persist doesn't catch it fast enough
        if (typeof window !== "undefined") {
          window.location.href = "/";
        }
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
            console.warn("Token expired. Logging out...");
            get().logout();
          }
        } catch (error) {
          console.error("Invalid token found. Logging out...");
          get().logout();
        }
      },

      getAuthToken: () => {
        // 1. Run the validation logic
        get().checkTokenExpiry();

        // 2. Get the user from the current state (might be null if checkTokenExpiry logged them out)
        const currentUser = get().user;

        return currentUser ? currentUser.auth_token : null;
      },
    }),
    { name: "medease-auth" },
  ),
);
