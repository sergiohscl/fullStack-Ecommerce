import { createContext} from 'react';
import { CartProps } from './cartProvider'
import { ProductProps } from '../pages/home';

interface CartContextData {
    cart: CartProps[];
    cartAmount: number;
    addItemCart: (newItem: ProductProps) => void;
    removeItemCart: (product: CartProps) => void;
    addItemCartMais: (newItem: CartProps) => void;
    total: string;
    // setCart: Dispatch<SetStateAction<CartProps[]>>
}

export const CartContext = createContext({} as CartContextData);
