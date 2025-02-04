import { useState, useEffect, useContext } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ProductProps } from '../home'
import { BsCartPlus } from 'react-icons/bs'
import { CartContext } from '../../contexts/cartContext'
import toast from 'react-hot-toast'
import { AuthContext } from '../../contexts/AuthContext'
import { api_cart } from '../../services/api_cart'

export function ProductDetail(){
    const { id } = useParams();
    const [product, setProduct] = useState<ProductProps>()
    const { addItemCart } = useContext(CartContext);
    const { is_active } = useContext(AuthContext)
    const navigate = useNavigate();

    useEffect(() => {
        async function getProduct(){
            try {
                const response = await api_cart.get(`/products/${id}/`)
                setProduct(response.data);
            } catch (error) {
                console.error("Erro ao buscar o produto:", error);
            }
        }
        getProduct();
    }, [id])

    function handleAddItem(product: ProductProps){
        if (!is_active) {
            toast.error('Você precisa estar logado para adicionar itens ao carrinho.', {
                style: {
                borderRadius: 10,
                backgroundColor: '#FF0000',
                color: '#FFF',
                },
            });
        return;
        }

        toast.success("Produto adicionado no carrinho.", {
        style:{
            borderRadius: 10,
            backgroundColor: "#121212",
            color: "#FFF"
        }
        })
        addItemCart(product)

        navigate("/cart")
    }

    return(
        <div>
            <main className="w-full max-w-7xl px-4 mx-auto my-6">
                {product && (
                <section className="w-full">
                    <div className="flex flex-col lg:flex-row">
                    <img
                        className="flex-1 w-full max-h-72 object-contain"
                        src={product?.cover}
                        alt={product?.title}
                    />

                    <div className="flex-1">
                        <p className="font-bold text-2xl mt-4 mb-2">{product?.title}</p>
                        <p className="my-4">{product?.description}</p>
                        <strong className="text-zinc-700/90 text-xl">
                        {product.price.toLocaleString("pt-BR", {
                            style: "currency",
                            currency: "BRL"
                        })}
                        </strong>
                        <button className="bg-zinc-900 p-1 rounded ml-3" onClick={ () => handleAddItem(product) }>
                        <BsCartPlus size={20} color="#FFF" />
                        </button>
                    </div>

                    </div>
                </section>
                )}
            </main>
        </div>
    )
}