# Use a imagem oficial do Node.js como base
FROM node:18 AS build

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos de pacotes para instalar as dependências
COPY package.json package-lock.json ./

# Instale as dependências da aplicação
RUN npm install --force

# Copie o restante dos arquivos da aplicação para o container
COPY . .

# Exponha a porta do Vite (5173)
EXPOSE 5173

# Comando para iniciar a aplicação em modo de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]
