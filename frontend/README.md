## tailwindcss
  https://tailwindcss.com/docs/installation

## ReactRouter
    npm install react-router-dom localforage match-sorter sort-by

## react-icons
  https://react-icons.github.io/react-icons/

    npm install react-icons

## react-hook-form
  https://www.react-hook-form.com/get-started

    npm install react-hook-form

  ### schema-validation
    npm install @hookform/resolvers

  ### zod
    npm install zod
  
  ### Toast
    https://react-hot-toast.com/

    npm install react-hot-toast

  ### json-server
    https://www.npmjs.com/package/json-server

    npm install -g json-server

# Rodando projeto em Docker

## criando imagem docker build
    docker build -t sergiohscl/react-ecommerce-image .

## rodando o container com imagem
    docker run -d -p 5173:5173 --name frontend-react --network library-network sergiohscl/react-ecommerce-image