# Makefile

# Docker
DOCKER_COMPOSE=docker compose -f docker/docker-compose.yml

# Paths
CONFIG_DIR=src/lib
CONFIG_EXAMPLE=$(CONFIG_DIR)/config_example.py
CONFIG=$(CONFIG_DIR)/config.py

# DB connection info
DB_HOST=localhost
DB_PORT=5004
DB_USER=user
DB_PWD=pass
DB_DATABASE=mydb

.DEFAULT_GOAL := help

help:
	@echo "Usage:"
	@echo "  make db           Run MySQL database in Docker"
	@echo "  make config       Generate config.py from config_example.py"
	@echo "  make setup        Run full setup: db + config (prompt BOT_TOKEN)"
	@echo "  make stop         Stop and remove Docker containers"
	@echo "  make run          start the bot"

# Run MySQL docker
db:
	$(DOCKER_COMPOSE) up -d

# Generate config.py with DB info and prompt BOT_TOKEN
config:
	@echo "Generating $(CONFIG) from $(CONFIG_EXAMPLE)..."
	cp $(CONFIG_EXAMPLE) $(CONFIG)
	@sed -i.bak "s/^DB_HOST *=.*/DB_HOST = '$(DB_HOST)'/" $(CONFIG)
	@sed -i.bak "s/^DB_PORT *=.*/DB_PORT = $(DB_PORT)/" $(CONFIG)
	@sed -i.bak "s/^DB_USER *=.*/DB_USER = '$(DB_USER)'/" $(CONFIG)
	@sed -i.bak "s/^DB_PWD *=.*/DB_PWD = '$(DB_PWD)'/" $(CONFIG)
	@sed -i.bak "s/^DB_DATABASE *=.*/DB_DATABASE = '$(DB_DATABASE)'/" $(CONFIG)
	@rm -f $(CONFIG).bak
	@read -p "Enter your BOT_TOKEN: " token; \
	sed -i.bak "s/^BOT_TOKEN *=.*/BOT_TOKEN = '$$token'/" $(CONFIG); \
	rm -f $(CONFIG).bak
	@read -p "Enter your GUILD_ID: " id; \
	sed -i.bak "s/^GUILD_ID *=.*/GUILD_ID = '$$id'/" $(CONFIG); \
	rm -f $(CONFIG).bak
	@echo "$(CONFIG) created."

# Run all setup
setup: db config
	@echo "download requirements..."
	@pip install -r requirement.txt
	@echo "Setup complete. You can now run the app."

# Stop docker
stop:
	$(DOCKER_COMPOSE) down

# Run Python main
run:
	@echo "starting bot..."
	@python3 main.py

