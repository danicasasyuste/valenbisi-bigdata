# 🚲 Valenbisi Real-Time Monitor

Pipeline de Big Data para monitorizar en tiempo real las estaciones de bicicletas Valenbisi de Valencia.

## Arquitectura

<img width="1608" height="705" alt="image" src="https://github.com/user-attachments/assets/fb3a7282-04c4-4d03-bcca-ada0261ac094" />


## Herramientas

| Herramienta | Versión | Función |
|-------------|---------|---------|
| Apache NiFi | latest | Ingesta automática desde la API cada 2 minutos |
| Apache Kafka | 7.3.3 | Cola de mensajes entre ingesta y procesamiento |
| Apache Spark | 3.5.8 | Procesamiento y transformación del JSON |
| PostgreSQL | 12.1 | Almacenamiento de los datos procesados |
| Grafana | latest | Dashboard de visualización en tiempo real |

## API

- **URL:** `https://api.citybik.es/v2/networks/valenbisi`
- **Sin registro ni autenticación**
- 277 estaciones de Valencia en tiempo real
- Campos: nombre, bicis libres, huecos vacíos, timestamp

## Dashboard

![Arquitectura](flujo%20BD.jpg)

- 📊 Bicis disponibles por estación (bar chart)
- 🔴 Estaciones sin bicis disponibles
- 🟢 Estaciones llenas sin huecos
- 📈 Métricas generales: total estaciones, media bicis, total bicis disponibles

## Requisitos

- Docker Desktop
- Apache NiFi corriendo en puerto 8443
- Los docker-compose de Kafka y Spark

## Ejecución

### 1. Levantar Kafka
```bash
cd "Documents/Flink BDA/Flink_code/Flink_code/Docker"
docker-compose up -d kafka zookeeper
```

### 2. Levantar Spark
```bash
cd Desktop/docker_spark/docker_spark
docker-compose up -d
```

### 3. Levantar Grafana
```bash
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

### 4. Crear el topic de Kafka
```bash
docker exec -it docker-kafka-1 kafka-topics --create --topic valenbisi \
  --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 5. Ejecutar el script de Spark
```bash
docker exec -it -u root spark-master /opt/spark/bin/spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8,org.postgresql:postgresql:42.6.0 \
  /data/valenbisi_spark.py
```

### 6. Acceder a los servicios

| Servicio | URL |
|----------|-----|
| NiFi | https://localhost:8443/nifi |
| Grafana | http://localhost:3000 |
| pgAdmin | http://localhost:5050 |
| Kafka UI | http://localhost:8090 |
| Spark Master | http://localhost:8080 |

## Esquema de la base de datos

```sql
CREATE TABLE valenbisi_stations (
    id TEXT,
    name TEXT,
    free_bikes INTEGER,
    empty_slots INTEGER,
    timestamp TEXT
);
```

## Autor

**Daniel Casas** 
