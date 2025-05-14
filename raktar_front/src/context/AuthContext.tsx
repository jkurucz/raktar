import { createContext } from "react";
import {emailKeyName, tokenKeyName, roleKeyName} from "../constants/constants.ts";

interface AuthContext {
    token: string | null;
    setToken: (token: string | null) => void;
    email: string | null;
    setEmail: (email: string | null) => void;
    role: string | null;
    setRole: (role: string | null) => void;
}

export const AuthContext = createContext<AuthContext>({
    token: localStorage.getItem(tokenKeyName),
    setToken: () => {},
    email: localStorage.getItem(emailKeyName),
    setEmail: () => {},
    role: localStorage.getItem(roleKeyName),
    setRole: () => {}
});