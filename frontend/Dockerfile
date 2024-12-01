# Usa una imagen base de Node.js
FROM node:20

# Establece el directorio de trabajo
WORKDIR /usr/src/app

# Copia los archivos del frontend
COPY package*.json ./
COPY . .

# Instala las dependencias
RUN npm install

# Expone el puerto del servidor de desarrollo
EXPOSE 3000

# Comando para iniciar el frontend
CMD ["npm", "start"]
