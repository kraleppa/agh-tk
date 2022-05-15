# Use an official node runtime as a parent image
FROM node:16

WORKDIR /app

# Install dependencies
COPY package.json /app

RUN npm install -g npm@8.10.0
RUN npm install

# Add rest of the client code
COPY . /app

EXPOSE 3000

CMD npm start