CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id SERIAL PRIMARY KEY,
    customer_hash TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_drink (
    drink_id SMALLSERIAL PRIMARY KEY,
    drink_name TEXT UNIQUE,
    category TEXT
);

CREATE TABLE IF NOT EXISTS dim_branch (
    branch_id SMALLSERIAL PRIMARY KEY,
    branch_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_payment (
    payment_id SMALLSERIAL PRIMARY KEY,
    payment_type TEXT,
    bank_prefix TEXT
);

CREATE TABLE IF NOT EXISTS dim_datetime (
    datetime_id SERIAL PRIMARY KEY,
    iso_date TIMESTAMP,
    year INT,
    month INT,
    day INT,
    weekday TEXT
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id UUID PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    drink_id SMALLINT REFERENCES dim_drink(drink_id),
    branch_id SMALLINT REFERENCES dim_branch(branch_id),
    payment_id SMALLINT REFERENCES dim_payment(payment_id),
    datetime_id INT REFERENCES dim_datetime(datetime_id),
    price NUMERIC(10,2),
    load_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

