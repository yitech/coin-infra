CREATE TABLE OrderBookEntry (
    entry_id INT AUTO_INCREMENT,
    request_id INT,
    price DECIMAL(14, 4),
    size DECIMAL(14, 4),
    type ENUM('ask', 'bid'),
    PRIMARY KEY (entry_id),
    FOREIGN KEY (request_id) REFERENCES OrderBookRequest(request_id)
);
