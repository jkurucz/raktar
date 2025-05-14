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

    const login = (email: string, password: string) => {
        api.Auth.login(email, password).then(res => {
            setToken(res.data.token);
            localStorage.setItem(tokenKeyName, res.data.token);
            // const decodedToken: never = jwtDecode(res.data.token);
            // const role = decodedToken['http://schemas.microsoft.com/ws/2008/06/identity/claims/role'];
            // setRole(role);
            // localStorage.setItem(roleKeyName, role);
            // setEmail(email);
            // localStorage.setItem(emailKeyName, email);




            const decodedToken = jwtDecode(res.data.token);
            //console.log(decodedToken);
            const userRole = decodedToken.roles?.[0]?.name;
            setRole(userRole);
            localStorage.setItem(roleKeyName, userRole);

            const tokenFromBE = res.data.token;
            setToken(tokenFromBE); 
            localStorage.setItem(tokenKeyName, tokenFromBE);
            setEmail(email); 
            localStorage.setItem(emailKeyName, email);

            
        });
    }

    
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