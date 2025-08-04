# Use Node.js 18 Alpine image
FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev dependencies for build)
RUN npm install

# Fix Tailwind CSS v4 native modules for Alpine Linux
RUN npm uninstall lightningcss @tailwindcss/oxide && \
    npm install lightningcss@latest @tailwindcss/oxide@latest --force && \
    npm rebuild lightningcss @tailwindcss/oxide --update-binary

# Copy project files
COPY . .

# Build the application
RUN npm run build

# Remove dev dependencies after build
RUN npm prune --omit=dev

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
