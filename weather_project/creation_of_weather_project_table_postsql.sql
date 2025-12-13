CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    temp_k REAL,
    temp_c REAL,
    temp_f REAL,
    temp_min_k REAL,
    temp_min_c REAL,
    temp_min_f REAL,
    temp_max_k REAL,
    temp_max_c REAL,
    temp_max_f REAL,
    temp_feels_k REAL,
    temp_feels_c REAL,
    temp_feels_f REAL,
    humidity INTEGER,
    wind_speed REAL
);

