import {useContext, useEffect} from "react";
import {AuthContext} from "../context/AuthContext.tsx";
import {emailKeyName, emailTokenKey, roleKeyName, tokenKeyName} from "../constants/constants.ts";
import {jwtDecode, JwtPayload} from "jwt-decode";
import api from '../api/api.ts';

interface CustomJwtPayload extends JwtPayload {
    [key: string]: any; // Allowing dynamic keys if necessary
}

const useAuth = () => {
    const { token, setToken, email, setEmail, setRole  } = useContext(AuthContext);
    const isLoggedIn = !!token;

    const login = async (email: string, password: string) => {
            try {
                const res = await api.Auth.login(email, password);
                setToken(res.data.token);
                localStorage.setItem(tokenKeyName, res.data.token); 

                const decodedToken = jwtDecode<CustomJwtPayload>(res.data.token);
                const userRole = decodedToken.roles?.[0]?.name;
                setRole(userRole);
                localStorage.setItem(roleKeyName, userRole);    

                setEmail(email); 
                localStorage.setItem(emailKeyName, email);
            } catch (err) {
                throw err;
            }
        };
    
    const logout = () => {
        localStorage.clear();
        setToken(null);
    }

    const loginKata = (token: string) => {
        setToken(token); localStorage.setItem(tokenKeyName, token);
        const decodedToken = jwtDecode<CustomJwtPayload>(token);
        const tempEmail = decodedToken[emailTokenKey];
        localStorage.setItem(emailKeyName, tempEmail); setEmail(tempEmail);
    }

    useEffect(() => {

    }, []);

    return {login, logout, loginKata, token, email, isLoggedIn};
}

export default useAuth;