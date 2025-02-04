import axios from 'axios'

export const api_cart = axios.create({
    baseURL: 'http://localhost:8000/api/v1',
    headers: {
        'Content-Type': 'application/json',
    }
})

export const registerUser = async (
    data: {
        username: string,
        email: string,
        password: string,
        password2: string,
        avatar: File | null
    }
) => {
    try {
        const formData = new FormData();
        formData.append('username', data.username);
        formData.append('email', data.email);
        formData.append('password', data.password);
        formData.append('password2', data.password2);
        
        // Adiciona o avatar somente se ele estiver presente
        if (data.avatar) {
            formData.append('avatar', data.avatar);
        }
        const response = await api_cart.post('/register/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        // console.log(response.data)
        return response.data
        
    } catch (error) {
        if (axios.isAxiosError(error)) {
            //console.error('Erro completo:', error.response)
            throw new Error(error.response?.data?.message || 'Erro ao cadastrar usuário');
        }
        throw new Error('Erro inesperado');
    }
}

export const loginUser = async (data: { email: string; password: string }) => {
    const formData = new FormData();
    formData.append('email', data.email);
    formData.append('password', data.password);

    try {
        const response = await api_cart.post('/login/', formData);
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error('Erro completo:', error.response)
            throw new Error(error.response?.data?.detail || 'Erro ao logar usuário');
        }
        throw new Error('Erro inesperado');
    }
};
