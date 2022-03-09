CREATE DATABASE DjangoWeatherReminder;

CREATE USER tester with PASSWORD 'tester';
ALTER USER tester CREATEDB;

GRANT ALL PRIVILEGES ON DATABASE DjangoWeatherReminder to tester;
