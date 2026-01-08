# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (if applicable, e.g., for HTTP transport)
# The MCP server itself uses stdio transport by default, but if it exposes HTTP endpoints, this would be needed.
# EXPOSE 3000

# Run the server
CMD ["node", "server.js"]
