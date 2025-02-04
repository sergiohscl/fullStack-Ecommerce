import { createBrowserRouter } from 'react-router-dom'
import { Home } from './pages/home'
import { Cart } from './pages/cart'
import { Layout } from './components/layout';
import { ProductDetail } from './pages/detail';
import { Login } from './pages/login';
import { Register } from './pages/register';
import { Products } from './pages/products';
import { Private } from './routes/Private';

const router = createBrowserRouter([
  {
    element: <Layout/>,
    children:[
      {
        path: "/",
        element: <Home/>
      },
      {
        path: "/cart",
        element: <Private><Cart/></Private>
      },
      {
        path: "/product/:id",
        element: <ProductDetail/>
      },
      {
        path: "/products",
        element: <Private><Products/></Private>
      },
    ]
  },
  {
    path: "/login",
    element: <Login/>
  },
  {
    path: "/register",
    element: <Register/>
  }
])

export { router };