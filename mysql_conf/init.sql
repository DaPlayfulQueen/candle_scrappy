CREATE TABLE candle (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(100),
    link VARCHAR(300)
);

CREATE TABLE price (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candle_id VARCHAR(100),
    price FLOAT,
    date DATE,
    FOREIGN KEY (candle_id) REFERENCES candle(id)
);

ALTER USER 'admin'@'your_host' IDENTIFIED WITH 'caching_sha2_password' BY 'cAndleMaker!2024';
