PYTHON ?= python

PROTO_DIR := proto
PROTOGEN_PY_DIR := protogen/python
PROTO_FILES := $(wildcard $(PROTO_DIR)/*.proto)

DRIFT_TRAFFIC_FILE := scripts/generate_traffic.py

.PHONY: proto

proto:
	@echo "Generando codigo gRPC..."
	@mkdir -p $(PROTOGEN_PY_DIR)
	@$(PYTHON) -m grpc_tools.protoc \
		-I $(PROTO_DIR) \
		--python_out=$(PROTOGEN_PY_DIR) \
		--grpc_python_out=$(PROTOGEN_PY_DIR) \
		$(PROTO_FILES)
	@find $(PROTOGEN_PY_DIR) -type d -exec touch {}/__init__.py \;
	@echo "Codigo gRPC generado!!!"

up:
	@docker compose up -d

up-build:
	@docker compose up --build -d

build-no-cache:
	@docker compose build --no-cache

down:
	@docker compose down -v

drift-traffic:
	@$(PYTHON) $(DRIFT_TRAFFIC_FILE)