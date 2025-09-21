-- Initialize databases for all services
CREATE DATABASE selgo_auth;
CREATE DATABASE selgo_boat;
CREATE DATABASE selgo_job;
CREATE DATABASE selgo_motorcycle;
CREATE DATABASE selgo_property;
CREATE DATABASE selgo_car;
CREATE DATABASE selgo_square;
CREATE DATABASE selgo_chat;
CREATE DATABASE selgo_travel;
CREATE DATABASE selgo_electronics;
CREATE DATABASE selgo_commercial;

-- Enable PostGIS extension for location-based features
\c selgo_property;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_boat;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_car;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_motorcycle;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_square;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_travel;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_electronics;
CREATE EXTENSION IF NOT EXISTS postgis;

\c selgo_commercial;
CREATE EXTENSION IF NOT EXISTS postgis;