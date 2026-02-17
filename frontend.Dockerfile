FROM node:16-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci

# Copy app
COPY frontend/ .

# Build
RUN npm run build

# Serve with serve package
RUN npm install -g serve
EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
