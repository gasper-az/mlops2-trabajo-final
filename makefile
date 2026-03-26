PYTHON := python

PROTO_FILE=proto/prediction.proto
PROTO_OUT=generated

.PHONY: proto up down

proto:
	@echo "Generando codigo gRPC..."
	$(PYTHON) -m grpc_tools.protoc \
		-I proto \
		--python_out=$(PROTO_OUT) \
		--grpc_python_out=$(PROTO_OUT) \
		$(PROTO_FILE)
	
	@echo "Arreglando imports..."
	sed -i 's/^import prediction_pb2/from generated import prediction_pb2/' \
		$(PROTO_OUT)/prediction_pb2_grpc.py
	
	@echo "Codigo gRPC generado!!!"

up:
	@docker compose up --build -d

down:
	@docker compose down