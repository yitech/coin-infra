CREATE TABLE OrderBookRequest (
    request_id INT AUTO_INCREMENT,
    request_time TIMESTAMP,
    response_time TIMESTAMP,
    exchange VARCHAR(20),
    symbol VARCHAR(20),
    PRIMARY KEY (request_id)
);
