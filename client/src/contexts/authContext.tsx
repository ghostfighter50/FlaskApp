import { createContext } from "react";

export interface AuthContextProps {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    isAuthenticated: any;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    setIsAuthenticated: React.Dispatch<React.SetStateAction<any>>
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    user: any;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    setUser: React.Dispatch<React.SetStateAction<any>>;
  }

export const AuthContext = createContext<AuthContextProps | undefined>(undefined);
