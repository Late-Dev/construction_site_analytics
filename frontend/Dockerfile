FROM node:lts-alpine
RUN npm install -g http-server
RUN npm install -g @vuepic/vue-datepicker
WORKDIR /app
COPY package*.json ./
COPY yarn.lock ./
RUN npm install
COPY . .
RUN npm run build 
EXPOSE 8080
CMD [ "http-server", "dist" ]