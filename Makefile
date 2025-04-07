# jaljalgotcha Makefile

.PHONY: help server server-venv client start start-venv install-deps build-client

help:
	@echo "Available commands:"
	@echo "  make server         - Start the Python server with system Python"
	@echo "  make client         - Start the frontend client dev server"
	@echo "  make start          - Start both server (system Python) and client"
	@echo "  make install-deps   - Install dependencies for both server and client"
	@echo "  make build-client   - Build the client for production"

# Start the Python server with system Python
server:
	cd server && .venv/bin/python -m flask --app src.jaljalgotcha.main run --debug

# Start the client dev server
client:
	cd client && npm run dev

# Start both server and client (using system Python)
start:
	@echo "Starting server and client..."
	@make server & make client

# Install dependencies for both projects
install-deps:
	@echo "Installing server dependencies..."
	cd server && pip install -r requirements.txt
	@echo "Installing client dependencies..."
	cd client && npm install

# Build the client for production
build-client:
	cd client && npm run build
