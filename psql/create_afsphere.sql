
CREATE ROLE pizzamozzarella WITH LOGIN PASSWORD 'gotica';
CREATE DATABASE afsphere OWNER pizzamozzarella;
GRANT ALL PRIVILEGES ON DATABASE afsphere TO pizzamozzarella;
