# Dockerfile dla bazy danych PostgreSQL
FROM postgres:latest

# Tworzenie użytkownika i bazy danych
ENV POSTGRES_USER=myUser
ENV POSTGRES_PASSWORD=myPass
ENV POSTGRES_DB=university