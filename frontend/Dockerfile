# Etapa 1: Build (si quieres hacerlo todo en uno)
# FROM node:20-alpine as build
# WORKDIR /app
# COPY . .
# RUN npm install && npm run build

# Etapa 2: Nginx para servir archivos
FROM nginx:1.25-alpine

# Borra configuración por defecto
RUN rm -rf /usr/share/nginx/html/*

# Copia tu build estático
COPY dist/ /usr/share/nginx/html/pronosticos/

# Copia tu configuración Nginx personalizada
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Arranca nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]

