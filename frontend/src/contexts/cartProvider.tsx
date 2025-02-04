import { ReactNode, useContext, useEffect, useState } from 'react';
import { ProductProps } from '../pages/home';
import { CartContext } from './cartContext';
import { api_cart } from '../services/api_cart';
import { AuthContext } from './AuthContext';

export interface CartProps {
    id: number;
    name: string;
    title: string;
    description: string;
    price: number;
    cover: string;
    amount: number;
    subtotal: number;
}

interface CartProviderProps {
    children: ReactNode;
}

function CartProvider({ children }: CartProviderProps) {
    const { user } = useContext(AuthContext)
    const [cart, setCart] = useState<CartProps[]>([]);
    const [total, setTotal] = useState("");

    useEffect(() => {
        async function get_or_create_shop_cart() {
            const token = user?.token

            if (!token) {
                console.warn("Usuário não autenticado ou token ausente.");
                return;
            }

            try {
                // Fazer a requisição para garantir que o carrinho existe
                const response = await api_cart.post("/shop-cart/", {}, {
                    headers: { Authorization: `Token ${token}` },
                });

                const cartData = response.data.items || [];
                setCart(cartData);
                localStorage.setItem("@shop_cart", JSON.stringify(cartData));
                
                totalResultCart(cartData);
            } catch (error) {
                console.error("Erro ao buscar/criar carrinho:", error);
            }
        }

        get_or_create_shop_cart();
    }, [user?.token]);

    async function addItemCartMais(newItem: CartProps) {
        const token = localStorage.getItem("@token");
        
        if (!token) {
            console.warn("Usuário não autenticado ou token ausente.");
            return;
        }
        
        try {
            const response = await api_cart.post(`/shop-cart/add-item/${newItem.id}/1/`, {}, {
                headers: { Authorization: `Token ${token}` },
            });
            
            const updatedCart: CartProps[] = Object.values(response.data.shop_cart.itens || []);
            setCart(updatedCart);
            localStorage.setItem("@shop_cart", JSON.stringify(updatedCart));
            totalResultCart(updatedCart);
            
        } catch (error) {
            console.error("Erro ao adicionar item ao carrinho:", error);
        }
    }

    async function addItemCart(newItem: ProductProps) {
        const token = localStorage.getItem("@token");
        
        if (!token) {
            console.warn("Usuário não autenticado ou token ausente.");
            return;
        }
        
        try {
            const response = await api_cart.post(`/shop-cart/add-item/${newItem.id}/1/`, {}, {
                headers: { Authorization: `Token ${token}` },
            });
            
            const updatedCart: CartProps[] = Object.values(response.data.shop_cart.itens || []);
            setCart(updatedCart);
            localStorage.setItem("@shop_cart", JSON.stringify(updatedCart));
            totalResultCart(updatedCart);
            
        } catch (error) {
            console.error("Erro ao adicionar item ao carrinho:", error);
        }
    }

    async function removeItemCart(product: CartProps) {
        const token = localStorage.getItem("@token");
        if (!token) {
            console.warn("Usuário não autenticado ou token ausente.");
            return;
        }
    
        try {
            const formattedName = decodeURIComponent(product.name);
            const url = `/shop-cart/delete/${formattedName}/`;
            
    
            let updatedCart: CartProps[];
    
            if (product.amount > 1) {
                const updatedProduct = { ...product, amount: product.amount - 1 };
                updatedCart = updateCartLocally(updatedProduct);

            } else {
                updatedCart = removeItemLocally(product);
            }
    
            setCart(updatedCart);
            localStorage.setItem("@shop_cart", JSON.stringify(updatedCart));
            totalResultCart(updatedCart);

            await api_cart.delete(url, {
                headers: { Authorization: `Token ${token}` },
            });
    
        } catch (error) {
            console.error("Erro ao remover item do carrinho:", error);
        }
    }
    
    function updateCartLocally(updatedProduct: CartProps): CartProps[] {
        let cart: CartProps[] = JSON.parse(localStorage.getItem("@shop_cart") || "[]");
        
        updatedProduct.subtotal = updatedProduct.price * updatedProduct.amount;
        cart = cart.map((item: CartProps) =>
            item.name === updatedProduct.name ? updatedProduct : item
        );
        return cart;
    }
    
    function removeItemLocally(product: CartProps): CartProps[] {
        let cart: CartProps[] = JSON.parse(localStorage.getItem("@shop_cart") || "[]");
        cart = cart.filter((item: CartProps) => item.name !== product.name);
        return cart;
    }

    function totalResultCart(items: CartProps[]) {
        const myCart = items;
        const result = myCart.reduce((acc, obj) => acc + obj.subtotal, 0);
        const resultFormated = result.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
        setTotal(resultFormated);
    }

    return (
        <CartContext.Provider
            value={{
                cart,
                cartAmount: cart.length,
                addItemCart,
                removeItemCart,
                addItemCartMais,
                total
            }}
        >
            {children}
        </CartContext.Provider>
    );
}

export default CartProvider;
