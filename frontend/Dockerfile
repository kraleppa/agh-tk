# Use an official node runtime as a parent image
FROM node:16.14.2-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
COPY package-lock.json ./

RUN npm install

# Add rest of the client code
COPY . /app

RUN chown -R node node_modules

EXPOSE 3000

CMD npm start