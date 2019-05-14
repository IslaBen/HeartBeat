FROM node:8

#Create API directory
WORKDIR /usr/src/API

# Install app dependencies
COPY package*.json ./
RUN npm install

# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 4000

CMD [ "npm", "start" ]