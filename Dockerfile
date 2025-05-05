# Step 1: Use a Node.js base image
FROM node:18-alpine AS builder

# Step 2: Set working directory
WORKDIR /app

# Step 3: Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Step 4: Install dependencies (cached if package.json or package-lock.json hasn't changed)
RUN npm install

# Step 5: Copy application files (separately to avoid cache busting)
COPY . .

# Step 6: Build the Next.js app
RUN npm run build

# Step 7: Use a lightweight Node.js image for production
FROM node:18-alpine

# Step 8: Set working directory
WORKDIR /app

# Step 9: Copy build output and necessary files for production
COPY --from=builder /app .

# Step 10: Remove unnecessary files and install only production dependencies
RUN npm prune --production

# Step 11: Expose the application port
EXPOSE 3000

# Step 12: Start the Next.js app
CMD ["npm", "start"]