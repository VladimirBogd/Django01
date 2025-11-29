FROM node:24.11-alpine AS build

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

COPY . .

RUN npm run build

FROM nginx:1.29.3-alpine

COPY --from=build /app/dist/ /usr/share/nginx/html
COPY nginx_static.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
