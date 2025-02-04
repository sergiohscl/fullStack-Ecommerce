import { useContext, useEffect, useState } from 'react'
import { BsCartPlus } from 'react-icons/bs'
import { CartContext } from '../../contexts/cartContext';
import toast from 'react-hot-toast'
import { Link } from 'react-router-dom';
import { Container } from '../../components/container';
import { AuthContext } from '../../contexts/AuthContext';
import { api_cart } from '../../services/api_cart';

export interface ProductProps{
    id: number;
    name: string;
    title: string;
    description: string;
    price: number;
    cover: string;
}

export function Home(){
    const { addItemCart} = useContext(CartContext)
    const { is_active } = useContext(AuthContext)
    const [products, setProducts] = useState<ProductProps[]>([])

    useEffect(() => {
        async function getProducts() {
            try {
                const response = await api_cart.get("/products/");
                setProducts(response.data.results);
            } catch (error) {
                console.error("Erro ao buscar os produtos:", error);
            }
        }
        getProducts();
    }, []);
    

    function handleAddCartItem(product: ProductProps){
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
        
        toast.success('Produto adicionado no carrinho.', {
            style:{
                borderRadius: 10,
                backgroundColor: '#121212',
                color: '#fff'
            }
        })
        addItemCart(product);
    }

    return(
        <div>
            <Container>
                <h1 className="font-bold text-2xl mb-4 mt-10 text-center">Produtos em alta</h1>

                <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-5">
                    {products.map( (product) => (
                        <section key={product.id} className="w-full">
                            <Link to={`/product/${product.id}`}>
                                <img
                                    className="w-full rounded-lg max-h-70 mb-2 cursor-pointer"
                                    src={product.cover}
                                    alt={product.title}
                                />
                            </Link>
                            <p className="font-medium mt-1 mb-2">{product.title}</p>
                
                            <div className="flex gap-3 items-center">
                                <strong className="text-zinc-700/90">
                                    {product.price.toLocaleString("pt-BR", {
                                    style: "currency",
                                    currency: "BRL"
                                    })}
                                </strong>
                                
                                <button className="bg-zinc-900 p-1 rounded" onClick={ () => handleAddCartItem(product) }>
                                    <BsCartPlus size={20} color="#FFF"/>
                                </button>
                            </div>
                        </section>
                    ))}

                </div>
            </Container>
        </div>
    )
}