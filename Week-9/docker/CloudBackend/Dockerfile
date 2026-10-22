# FROM lets us base our Docker image off of an existing one
# Base image — provides Java 21 runtime without needing to install it manually
# eclipse-temurin is the official OpenJDK distribution, -jre means runtime only (smaller than -jdk)
FROM eclipse-temurin:21-jre

# Set the working directory inside the container
# All subsequent commands run from here
WORKDIR /app

# Copy the built JAR from your local machine into the container
# Left side = path on your machine, right side = path inside the container
COPY target/DockerBackend-0.0.1-SNAPSHOT.jar app.jar

# The command that runs when the container starts
ENTRYPOINT ["java", "-jar", "app.jar"]