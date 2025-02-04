export interface UserProps {
    id: number;
    username: string;
    email: string;
    avatar: string;
    token: string;
}

export type AuthContextData = {
    is_active: boolean;
    loadingAuth: boolean;
    user: UserProps | null;
    handleLogin: (email: string, password: string) => void;
    handleLogout: () => void;
    setLoadingAuth: React.Dispatch<React.SetStateAction<boolean>>;
};
