import { createContext, useContext, useState } from "react";
import { login as apiLogin, logout as apiLogout } from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(
    () => localStorage.getItem("token")
  );

  const login = async (email, password) => {
    const data = await apiLogin(email, password);

    if (!data.access_token) {
      throw new Error("Login succeeded but no access token was returned.");
    }

    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);

    return data;
  };

  const logout = () => {
    apiLogout();
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        isAuthenticated: Boolean(token),
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
