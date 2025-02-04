import { useContext, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { FiLogIn, FiShoppingCart, FiUser, FiMenu, FiX } from 'react-icons/fi'
import { CartContext } from '../../contexts/cartContext'
import { AuthContext } from '../../contexts/AuthContext'
import logoImg from "../../assets/logoEcomerce_transparent.png"

export function Header() {
    const { cartAmount } = useContext(CartContext)
    const navigate = useNavigate();
    const { is_active, loadingAuth, user, handleLogout } = useContext(AuthContext)
    const [showPopup, setShowPopup] = useState(false)
    const [menuOpen, setMenuOpen] = useState(false)

    const photo = user?.avatar

    const logout = () => {
        handleLogout();
        setShowPopup(false);
        navigate('/')
    };

    return (
        <header className="w-full bg-slate-200 shadow-md">
            <nav className="w-full max-w-7xl h-14 flex items-center justify-between px-5 mx-auto">
                <Link className="font-bold text-2xl" to="/">
                    <img src={logoImg} alt="Logo do site" className="w-24 h-24 object-contain" />
                </Link>
                
                {/* Menu Mobile */}
                <button className="sm:hidden" onClick={() => setMenuOpen(!menuOpen)}>
                    {menuOpen ? <FiX size={28} /> : <FiMenu size={28} />}
                </button>
                
                {/* Itens de Navegação */}
                <div className={`absolute sm:static top-16 left-0 w-full sm:w-auto bg-slate-200 sm:bg-transparent flex flex-col sm:flex-row sm:items-center gap-6 p-4 md:p-0 transition-all duration-300 ${menuOpen ? 'block' : 'hidden sm:flex'}`}>
                    {!loadingAuth && is_active && (
                        <Link className="text-blue-600 font-medium hover:underline hover:text-blue-800" to="/products">
                            Produtos
                        </Link>
                    )}
                    
                    <Link className="relative" to="/cart">
                        <FiShoppingCart size={24} color="#121212" />
                        {!loadingAuth && is_active && cartAmount > 0 && (
                            <span className="absolute -top-3 -right-3 px-2.5 bg-sky-500 rounded-full w-6 h-6 flex items-center justify-center text-white text-xs">
                                {cartAmount}
                            </span>
                        )}
                    </Link>

                    {!loadingAuth && is_active ? (
                        <div className="relative">
                            <div className="border-2 rounded-full p-1 border-gray-900 overflow-hidden flex items-center justify-center cursor-pointer" onClick={() => setShowPopup(!showPopup)}>
                                {user?.avatar ? (
                                    <img src={`http://127.0.0.1:8000/${photo}`} alt="Avatar do usuário" className="w-8 h-8 rounded-full object-cover" />
                                ) : (
                                    <FiUser size={22} color="#000" />
                                )}
                            </div>
                            {showPopup && (
                                <div className="absolute right-0 mt-2 bg-white shadow-md rounded-lg p-3 z-10">
                                    <button onClick={logout} className="text-sm text-red-600 hover:underline font-bold">
                                        Sair
                                    </button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <Link to="/login" className="border-2 rounded-full p-1 border-gray-900">
                            <FiLogIn size={22} color="#000" />
                        </Link>
                    )}
                </div>
            </nav>
        </header>
    )
}
