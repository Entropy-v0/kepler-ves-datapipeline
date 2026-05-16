# ─── Stage 1: Build ──────────────────────────────────────────────────────────
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app

# Copiar solo el pom primero para cachear dependencias
COPY pom.xml .
RUN mvn dependency:go-offline -q

# Copiar fuentes y compilar fat-jar
COPY src ./src
RUN mvn package -DskipTests -q

# ─── Stage 2: Runtime (imagen ligera) ────────────────────────────────────────
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Crear directorios de salida
RUN mkdir -p /app/data/analytics /app/logs

COPY --from=builder /app/target/analytics-engine-1.0-SNAPSHOT.jar app.jar

CMD ["java", "-jar", "app.jar"]
