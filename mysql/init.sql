CREATE TABLE candle (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100),
    link VARCHAR(300)
);

CREATE TABLE price (
    id INT,
    candle_id VARCHAR(100),
    price FLOAT,
    date DATE,
    FOREIGN KEY (candle_id) REFERENCES candle(id)
);
