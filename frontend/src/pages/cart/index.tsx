import { useContext } from 'react'
import { Link } from 'react-router-dom'
import { CartContext } from '../../contexts/cartContext';
import { Container } from '../../components/container';
import { AuthContext } from '../../contexts/AuthContext';

export function Cart(){
    const { cart, total, addItemCartMais, removeItemCart } = useContext(CartContext);
    const { is_active, loadingAuth } = useContext(AuthContext)

    return(
        <Container>
            <h1 className="font-medium text-2xl text-center my-4">Meu carrinho</h1>

            {(!is_active || cart.length === 0) && !loadingAuth && (
                <div className="flex flex-col items-center justify-center">
                <p className="font-medium">Ops seu carrinho está vazio...</p>
                <Link
                    to="/"
                    className="bg-slate-600 my-3 p-1 px-3 text-white font-medium rounded"
                >
                    Acessar produtos
                </Link>
                </div>
            )}

            {!loadingAuth && is_active && cart.map( (item, index) => (
                <section  key={`${item.title}-${index}`}
                className="flex items-center justify-between border-b-2 border-gray-300">
                    <img
                        src={item.cover}
                        alt={item.title}
                        className="w-28"
                    />
            
                    <strong>Preço: {item.price}</strong>
            
                    <div className="flex items-center justify-center gap-3">
                        <button
                        onClick={ () => removeItemCart(item) }
                        className="bg-slate-600 px-2 rounded text-white font-medium flex items-center justify-center"
                        >
                        -
                        </button>
            
                        {item.amount}
            
                        <button
                        onClick={ () => addItemCartMais(item) }
                        className="bg-slate-600 px-2 rounded text-white font-medium flex items-center justify-center"
                        >
                        +
                        </button>
                    </div>
            
            
                    <strong className="float-right">
                        SubTotal: {item.subtotal.toLocaleString("pt-BR", {
                        style: "currency",
                        currency: "BRL"
                        })}
                    </strong>
                </section>
            ))}
            
            {!loadingAuth && is_active && cart.length !== 0 && <p className="font-bold mt-4">Total: {total}</p> }
            
        </Container>
    )
}