# ── Stage 1: Build ──
FROM node:20-alpine AS build

WORKDIR /app

# Copy package files first for layer caching
COPY package.json package-lock.json* ./

RUN npm install

# Copy all source files
COPY . .

# Build for production
RUN npm run build

# ── Stage 2: Serve with Nginx ──
FROM nginx:1.27-alpine

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]