FROM node:14.17.1-alpine

WORKDIR /app

COPY package.json ./
RUN npm i

COPY . ./
ENTRYPOINT ["npm", "start"]
