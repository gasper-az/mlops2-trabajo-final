# Drift Detection

Consume inferencias en tiempo real mediante eventos de Kafka del componente grpc-server:

1. Aggregate incoming feature data over sliding windows
1. Compara distribuciones entrandes vs estadisticas de referencia (training)
1. Detecta data drift
1. Emite alerts (por el momento, solo Logs)

Utiliza PSI o Population Stability Index