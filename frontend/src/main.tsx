import React from 'react'
import ReactDOM from 'react-dom/client'
import { router } from './App'
import { RouterProvider } from 'react-router-dom'
import './index.css'
import { Toaster } from 'react-hot-toast'
import CartProvider from './contexts/cartProvider'
import AuthProvider from './contexts/AuthProvider' // Importe o AuthProvider

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
      <AuthProvider>  {/* Envolva a aplicação com o AuthProvider */}
        <CartProvider>
          <Toaster
            position="top-center"
            reverseOrder={false}
          />
          <RouterProvider router={router} />
        </CartProvider>
      </AuthProvider>
  </React.StrictMode>,
)
