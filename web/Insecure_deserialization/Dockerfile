FROM node:18-slim

# Create app directory
WORKDIR /app

# Copy package.json and install
COPY package.json .
RUN npm install --only=production

# Copy app code
COPY app.js .

# Expose port
EXPOSE 5000

# Run app
CMD ["node", "app.js"]
