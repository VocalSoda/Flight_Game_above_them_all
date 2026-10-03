CREATE TABLE IF NOT EXISTS save_files (
    number INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    score INT,
    did_win BOOLEAN,
    time DOUBLE
);