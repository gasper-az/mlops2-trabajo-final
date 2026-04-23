from wine_grpc_server.config import GRPC_PORT
from wine_grpc_server.postgres import ensure_tables
from wine_grpc_server.server import create_server

def main():
    server = create_server()
    server.start()
    ensure_tables()
    print(f"Servidor gRPC corriendo en el puerto {GRPC_PORT}.")
    server.wait_for_termination()

if __name__ == "__main__":
    main()