FROM mongo:8.0.0-rc4-jammy

WORKDIR /app

# Этот ARG будет использоваться для передачи переменных среды
ARG MONGO_INITDB_ROOT_USERNAME
ARG MONGO_INITDB_ROOT_PASSWORD

# Задаем переменные среды внутри контейнера
ENV MONGO_INITDB_ROOT_USERNAME=$MONGO_INITDB_ROOT_USERNAME
ENV MONGO_INITDB_ROOT_PASSWORD=$MONGO_INITDB_ROOT_PASSWORD

COPY ./app/data/sample_collection.bson /data
COPY ./Docker/Mongo/load_data.sh /app