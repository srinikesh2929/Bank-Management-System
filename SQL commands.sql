-- Creating Account --
CREATE TABLE Account (
    account_number INT PRIMARY KEY,
    name VARCHAR(100),
    phone_number VARCHAR(15),
    address VARCHAR(255),
    balance FLOAT
);

-- Crating transactions --
CREATE TABLE Transaction (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_number INT,
    transaction_type VARCHAR(10),  -- 'Deposit' or 'Withdraw'
    amount FLOAT,
    transaction_date DATE,
    FOREIGN KEY (account_number) REFERENCES Account(account_number)
);

INSERT INTO Account (name, account_number, phone_number, address, balance) VALUES
('S.Srinikesh', 11111, '8148572908', 'no.12 Poes Garden, Chennai', 1000000),
('S.Bhuwanesh', 99999, '7904554480', 'no.1 Vadachennai, Chennai', 10),
('V. Lakshana', 12067, '6383078880','no. 18, ECR, Chennai', 15000000);

