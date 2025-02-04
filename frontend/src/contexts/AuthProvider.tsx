import { ReactNode, useEffect, useState } from "react";
import { AuthContext } from "./AuthContext";
import { UserProps } from "./types";
import { loginUser } from "../services/api_cart";

interface AuthProviderProps{
    children: ReactNode
}

function AuthProvider({ children }: AuthProviderProps){

    const [user, setUser] = useState<UserProps | null>(null);
    const [loadingAuth, setLoadingAuth] = useState(false);

    async function handleLogin(email: string, password: string) {
        setLoadingAuth(true);
        try {
            const data = await loginUser({ email, password });
            
            const { user: userData, token } = data;

            setUser({
                id: userData.id,
                username: userData.username,
                email: userData.email,
                avatar: userData.avatar,
                token,
            });

            // Salvar os dados no localStorage para persistência
            localStorage.setItem("@user", JSON.stringify(userData));
            localStorage.setItem("@token", token);

        } catch (error) {
            console.error("Erro ao fazer login:", error);
            throw error; // Opcional, caso queira tratar erros na UI
        } finally {
            setLoadingAuth(false);
        }
    }

    function handleLogout() {
        setUser(null);
        localStorage.removeItem("@user");
        localStorage.removeItem("@token");
    }

    useEffect(() => {
        const storedUser = localStorage.getItem("@user");
        const storedToken = localStorage.getItem("@token");

        if (storedUser && storedToken) {
            setUser(JSON.parse(storedUser));
        }
    }, []);

    return(
        <AuthContext.Provider
        value={{
            is_active: !!user,
            loadingAuth,
            user,
            handleLogin,
            handleLogout,
            setLoadingAuth,
        }}
        >
            { children }
        </AuthContext.Provider>
    )
}
export default AuthProvider