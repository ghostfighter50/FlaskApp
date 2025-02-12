import React, { ReactNode, useState } from "react";
import { AuthContext, AuthContextProps } from "../contexts/authContext";

interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Provides authentication context to descendant components and manages user authentication state.
 *
 * @param {AuthProviderProps} props - The props for the AuthProvider component.
 * @param {React.ReactNode} props.children - The child components that will receive the auth context.
 *
 * @returns {JSX.Element} A context provider wrapping the child components with authentication functionality.
 */
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState();
  const [user, setUser] = useState();

  const value: AuthContextProps = {
    isAuthenticated,
    setIsAuthenticated,
    user ,
    setUser,
  };

  console.log("AuthProvider", value);
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
