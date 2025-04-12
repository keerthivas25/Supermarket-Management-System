-- Create and use the database
CREATE DATABASE IF NOT EXISTS sup;
USE sup;
-- drop database sup;
-- Supplier Table with surrogate primary key
CREATE TABLE Supplier (
    SupplierID INT primary KEY,
    ProductID INT unique,
    SupplierName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Address TEXT NOT NULL,
    ContactNumber VARCHAR(100) NOT NULL UNIQUE,
    Category VARCHAR(50) NOT NULL,
    UnitCost DECIMAL(10,2) NOT NULL CHECK (UnitCost >= 0),
    Quantity INT NOT NULL CHECK (Quantity >= 0)
);

-- Warehouse Table
CREATE TABLE Warehouse (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    ProductID INT,
    ProductName VARCHAR(100) NOT NULL,
    ArrivalDate DATE NOT NULL,
    ExpiryDate DATE NOT NULL,
    AvailableStock INT NOT NULL CHECK (AvailableStock >= 0),
    GSTNo VARCHAR(100) NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES Supplier(ProductID) ON DELETE CASCADE
);

-- Supermarket Table
CREATE TABLE Supermarket (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    GSTNo VARCHAR(100) NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    IsNeeded BOOLEAN NOT NULL DEFAULT TRUE,
    ExpiryDate DATE NOT NULL,
    Perishable BOOLEAN NOT NULL
);

-- Customer Table
CREATE TABLE Customer (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    PhoneNumber VARCHAR(100) NOT NULL UNIQUE,
    Cost DECIMAL(15,2) NOT NULL CHECK (Cost >= 0),
    PurchaseDateTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Finance Table
CREATE TABLE Finance (
    FinanceID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionType VARCHAR(50) NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL,
    TransactionDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Amount DECIMAL(15,2) NOT NULL CHECK (Amount >= 0),
    SupplierID INT NOT NULL,
    CustomerID INT,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE CASCADE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE SET NULL
);

-- Stock Feedback Table
CREATE TABLE StockFeedback (
    ProductID INT PRIMARY KEY,
    QuantityNeeded INT NOT NULL CHECK (QuantityNeeded >= 0),
    BadReview VARCHAR(255),
    FOREIGN KEY (ProductID) REFERENCES Supermarket(ProductID) ON DELETE CASCADE
);

-- Transactions Table
CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierID INT NOT NULL,
    SupplierName VARCHAR(100) NOT NULL,
    TransactionDate DATE NOT NULL,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID) ON DELETE CASCADE
);

-- Purchase Table
CREATE TABLE Purchase (
    CustomerID INT NOT NULL,
    ProductID INT,
    Quantity INT NOT NULL CHECK (Quantity >= 0),
    PurchaseDateTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (CustomerID, ProductID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Supermarket(ProductID) ON DELETE CASCADE
);


-- Supplier (15 entries with varied Indian details)
INSERT INTO Supplier(SupplierID, ProductID, SupplierName, Email, Address, ContactNumber, Category, UnitCost, Quantity) VALUES
(1, 101, 'FreshFarm Foods', 'freshfarm@gmail.com', 'Chennai', '9876543210', 'Vegetables', 25.00, 100),
(2, 102, 'Spice World', 'spiceworld@gmail.com', 'Coimbatore', '8765432109', 'Spices', 40.00, 50),
(3, 103, 'DairyPure', 'dairypure@gmail.com', 'Madurai', '7654321098', 'Dairy', 30.00, 120),
(4, 104, 'Sunrise Grains', 'sungrains@gmail.com', 'Salem', '6543210987', 'Grains', 20.00, 200),
(5, 105, 'Fruit Fiesta', 'fruitfiesta@gmail.com', 'Trichy', '5432109876', 'Fruits', 15.00, 150),
(6, 106, 'Ocean Catch', 'oceancatch@gmail.com', 'Tuticorin', '4321098765', 'Seafood', 55.00, 80),
(7, 107, 'GreenLeaf', 'greenleaf@gmail.com', 'Erode', '3210987654', 'Leafy Greens', 8.00, 200),
(8, 108, 'Daily Eggs', 'dailyeggs@gmail.com', 'Karur', '2109876543', 'Poultry', 5.50, 300),
(9, 109, 'Flourish Grains', 'flourishgrains@gmail.com', 'Namakkal', '1098765432', 'Grains', 18.00, 180),
(10, 110, 'ChocoDelight', 'chocodelight@gmail.com', 'Ooty', '9988776655', 'Confectionery', 60.00, 90),
(11, 111, 'Masala Mart', 'masalamart@gmail.com', 'Kochi', '9876501234', 'Spices', 45.00, 100),
(12, 112, 'Organic Fields', 'organicfields@gmail.com', 'Thrissur', '8765409876', 'Organic Veggies', 22.00, 110),
(13, 113, 'EggPro', 'eggpro@gmail.com', 'Tirunelveli', '7654309876', 'Poultry', 6.00, 400),
(14, 114, 'Mithai Magic', 'mithaimagic@gmail.com', 'Hyderabad', '6543209876', 'Sweets', 70.00, 50),
(15, 115, 'Tandoor Treats', 'tandoortreats@gmail.com', 'Mumbai', '5432109870', 'Baked Goods', 85.00, 60);


-- Warehouse (15 entries)
INSERT INTO Warehouse(ProductID, ProductName, ArrivalDate, ExpiryDate, AvailableStock, GSTNo) VALUES
(101, 'Tomato', '2025-04-01', '2025-04-06', 100, '33GST1234A1Z1'),
(102, 'Chili Powder', '2025-04-02', '2025-12-31', 50, '33GST1234B1Z2'),
(103, 'Milk', '2025-04-03', '2025-04-07', 120, '33GST1234C1Z3'),
(104, 'Wheat', '2025-04-04', '2025-10-10', 200, '33GST1234D1Z4'),
(105, 'Banana', '2025-04-05', '2025-04-08', 150, '33GST1234E1Z5'),
(106, 'Prawns', '2025-04-06', '2025-04-09', 80, '33GST1234F1Z6'),
(107, 'Spinach', '2025-04-07', '2025-04-10', 200, '33GST1234G1Z7'),
(108, 'Eggs', '2025-04-08', '2025-04-20', 300, '33GST1234H1Z8'),
(109, 'Barley', '2025-04-09', '2025-08-31', 180, '33GST1234I1Z9'),
(110, 'Dark Chocolate', '2025-04-10', '2026-04-10', 90, '33GST1234J1Z0'),
(111, 'Garam Masala', '2025-04-11', '2026-01-01', 100, '33GST5678A1Z1'),
(112, 'Organic Carrot', '2025-04-12', '2025-04-20', 110, '33GST5678B1Z2'),
(113, 'Duck Eggs', '2025-04-13', '2025-04-27', 400, '33GST5678C1Z3'),
(114, 'Kaju Katli', '2025-04-14', '2025-05-01', 50, '33GST5678D1Z4'),
(115, 'Naan Bread', '2025-04-15', '2025-04-17', 60, '33GST5678E1Z5');

-- Supermarket (15 entries)
INSERT INTO Supermarket(ProductID, ProductName, GSTNo, Quantity, IsNeeded, ExpiryDate, Perishable) VALUES
(101, 'Tomato', '33GST1234A1Z1', 95, TRUE, '2025-04-06', TRUE),
(102, 'Chili Powder', '33GST1234B1Z2', 48, TRUE, '2025-12-31', FALSE),
(103, 'Milk', '33GST1234C1Z3', 100, TRUE, '2025-04-07', TRUE),
(104, 'Wheat', '33GST1234D1Z4', 180, TRUE, '2025-10-10', FALSE),
(105, 'Banana', '33GST1234E1Z5', 140, TRUE, '2025-04-08', TRUE),
(106, 'Prawns', '33GST1234F1Z6', 70, TRUE, '2025-04-09', TRUE),
(107, 'Spinach', '33GST1234G1Z7', 190, TRUE, '2025-04-10', TRUE),
(108, 'Eggs', '33GST1234H1Z8', 290, TRUE, '2025-04-20', TRUE),
(109, 'Barley Milk', '33GST1234I1Z9', 170, FALSE, '2025-08-31', FALSE),
(110, 'Dark Chocolate', '33GST1234J1Z0', 85, TRUE, '2026-04-10', FALSE),
(111, 'Garam Masala', '33GST5678A1Z1', 95, TRUE, '2026-01-01', FALSE),
(112, 'Organic Carrot', '33GST5678B1Z2', 105, TRUE, '2025-04-20', TRUE),
(113, 'Duck Eggs', '33GST5678C1Z3', 390, TRUE, '2025-04-27', TRUE),
(114, 'Kaju Katli', '33GST5678D1Z4', 45, TRUE, '2025-05-01', FALSE),
(115, 'Naan Bread', '33GST5678E1Z5', 58, TRUE, '2025-04-17', TRUE);

-- Customer (15 entries)
INSERT INTO Customer(Name, PhoneNumber, Cost) VALUES
('Amit', '9123456780', 200.00),
('Bhavna', '9234567891', 150.50),
('Chetan', '9345678902', 300.75),
('Divya', '9456789013', 180.20),
('Eshan', '9567890124', 220.90),
('Fatima', '9678901235', 175.60),
('Gopal', '9789012346', 390.00),
('Harini', '9890123457', 160.00),
('Ishaan', '9901234568', 195.25),
('Jyoti', '9012345679', 140.80),
('Karan', '8123456781', 310.45),
('Lakshmi', '8234567892', 205.30),
('Manav', '8345678903', 280.00),
('Neha', '8456789014', 235.75),
('Omkar', '8567890125', 185.50);

-- Finance (15 entries: 10 supply + 5 purchase)
INSERT INTO Finance(TransactionType, PaymentMethod, Amount, SupplierID, CustomerID) VALUES
('Purchase', 'UPI', 200.00, 1, 1),
('Purchase', 'Card', 150.50, 2, 2),
('Purchase', 'Cash', 300.75, 3, 3),
('Purchase', 'UPI', 180.20, 4, 4),
('Purchase', 'Card', 220.90, 5, 5),
('Supply', 'UPI', 2500.00, 6, NULL),
('Supply', 'Bank Transfer', 1600.00, 7, NULL),
('Supply', 'Cheque', 1700.00, 8, NULL),
('Supply', 'UPI', 1800.00, 9, NULL),
('Supply', 'Bank Transfer', 5400.00, 10, NULL),
('Supply', 'Cash', 4500.00, 11, NULL),
('Supply', 'Card', 2200.00, 12, NULL),
('Supply', 'Cheque', 2400.00, 13, NULL),
('Supply', 'Bank Transfer', 3500.00, 14, NULL),
('Supply', 'UPI', 3900.00, 15, NULL);

-- StockFeedback (Only 4 bad reviews out of 15)
INSERT INTO StockFeedback(ProductID, QuantityNeeded, BadReview) VALUES
(101, 90, 'Tomatoes had dents and bruises'),  -- Bad
(102, 45, NULL),
(103, 110, 'Milk was sour on arrival'),       -- Bad
(104, 180, NULL),
(105, 140, NULL),
(106, 65, NULL),
(107, 180, NULL),
(108, 280, NULL),
(109, 160, 'Barley was infested with insects'),  -- Bad
(110, 80, NULL),
(111, 90, NULL),
(112, 100, NULL),
(113, 380, NULL),
(114, 40, NULL),
(115, 50, 'Naan bread was stale and dry');     -- Bad

-- Transactions (15 entries)
INSERT INTO Transactions(SupplierID, SupplierName, TransactionDate) VALUES
(1, 'FreshFarm Foods', '2025-04-01'),
(2, 'Spice World', '2025-04-02'),
(3, 'DairyPure', '2025-04-03'),
(4, 'Sunrise Grains', '2025-04-04'),
(5, 'Fruit Fiesta', '2025-04-05'),
(6, 'Ocean Catch', '2025-04-06'),
(7, 'GreenLeaf', '2025-04-07'),
(8, 'Daily Eggs', '2025-04-08'),
(9, 'Flourish Grains', '2025-04-09'),
(10, 'ChocoDelight', '2025-04-10'),
(11, 'Masala Mart', '2025-04-11'),
(12, 'Organic Fields', '2025-04-12'),
(13, 'EggPro', '2025-04-13'),
(14, 'Mithai Magic', '2025-04-14'),
(15, 'Tandoor Treats', '2025-04-15');

-- Purchase (15 entries)
INSERT INTO Purchase(CustomerID, ProductID, Quantity) VALUES
(1, 101, 10),
(2, 102, 5),
(3, 103, 12),
(4, 104, 9),
(5, 105, 8),
(6, 106, 6),
(7, 107, 18),
(8, 108, 30),
(9, 109, 10),
(10, 110, 6),
(11, 111, 4),
(12, 112, 11),
(13, 113, 20),
(14, 114, 7),
(15, 115, 9);

-- Insert into Finance after new stock is added (Warehouse = Supply)
DELIMITER $$

CREATE TRIGGER trg_finance_after_warehouse_insert
AFTER INSERT ON Warehouse
FOR EACH ROW
BEGIN
    DECLARE supID INT;
    DECLARE amount DECIMAL(15,2);

    SELECT SupplierID, UnitCost * Quantity INTO supID, amount
    FROM Supplier
    WHERE ProductID = NEW.ProductID;

    INSERT INTO Finance(TransactionType, PaymentMethod, Amount, SupplierID)
    VALUES ('Supply', 'Bank Transfer', amount, supID);
END $$

DELIMITER ;

-- Insert into Finance after a customer purchase
DELIMITER $$

CREATE TRIGGER trg_finance_after_purchase_insert
AFTER INSERT ON Purchase
FOR EACH ROW
BEGIN
    DECLARE cost DECIMAL(15,2);
    DECLARE supID INT;

    SET cost = NEW.Quantity * 50.00; -- Assume ₹50/unit
    SELECT SupplierID INTO supID FROM Supplier WHERE ProductID = NEW.ProductID;

    INSERT INTO Finance(TransactionType, PaymentMethod, Amount, SupplierID, CustomerID)
    VALUES ('Purchase', 'Cash', cost, supID, NEW.CustomerID);
END $$

DELIMITER ;

-- Insert into Transactions whenever new Warehouse stock is added
DELIMITER $$

CREATE TRIGGER trg_transaction_after_warehouse_insert
AFTER INSERT ON Warehouse
FOR EACH ROW
BEGIN
    DECLARE supID INT;
    DECLARE supName VARCHAR(100);

    SELECT SupplierID, SupplierName INTO supID, supName
    FROM Supplier
    WHERE ProductID = NEW.ProductID;

    INSERT INTO Transactions(SupplierID, SupplierName, TransactionDate)
    VALUES (supID, supName, CURDATE());
END $$

DELIMITER ;

-- Update AvailableStock in Warehouse when a purchase happens
DELIMITER $$

CREATE TRIGGER trg_reduce_stock_after_purchase
AFTER INSERT ON Purchase
FOR EACH ROW
BEGIN
    UPDATE Warehouse
    SET AvailableStock = AvailableStock - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END $$

DELIMITER ;

-- Validate stock availability BEFORE purchase
DELIMITER $$

CREATE TRIGGER trg_check_stock_before_purchase
BEFORE INSERT ON Purchase
FOR EACH ROW
BEGIN
    DECLARE available INT;

    SELECT AvailableStock INTO available
    FROM Warehouse
    WHERE ProductID = NEW.ProductID;

    IF available IS NULL OR available < NEW.Quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not enough stock available for the requested purchase';
    END IF;
END $$

DELIMITER ;

-- Auto-calculate Cost in Customer table when inserting new customer
DELIMITER $$

CREATE TRIGGER trg_autofill_cost_in_customer
BEFORE INSERT ON Customer
FOR EACH ROW
BEGIN
    IF NEW.Cost IS NULL THEN
        SET NEW.Cost = 0.00;
    END IF;
END $$

DELIMITER ;

-- Suggest replenishment in StockFeedback if stock goes below a threshold
DELIMITER $$

CREATE TRIGGER trg_auto_feedback_on_low_stock
AFTER UPDATE ON Warehouse
FOR EACH ROW
BEGIN
    IF NEW.AvailableStock < 20 THEN
        INSERT INTO StockFeedback(ProductID, QuantityNeeded, BadReview)
        VALUES (NEW.ProductID, 100, 'Stock too low — needs urgent restock')
        ON DUPLICATE KEY UPDATE QuantityNeeded = 100, BadReview = 'Stock too low — needs urgent restock';
    END IF;
END $$

DELIMITER ;

-- Set IsNeeded to TRUE in Supermarket if stock falls below threshold
DELIMITER $$

CREATE TRIGGER trg_update_isneeded_on_low_stock
AFTER UPDATE ON Supermarket
FOR EACH ROW
BEGIN
    IF NEW.Quantity < 30 THEN
        UPDATE Supermarket
        SET IsNeeded = TRUE
        WHERE ProductID = NEW.ProductID;
    END IF;
END $$

DELIMITER ;

-- Trigger to update Supermarket quantity when any product is purchased
DELIMITER $$

CREATE TRIGGER trg_update_product_quantity
AFTER INSERT ON Purchase
FOR EACH ROW
BEGIN
    UPDATE Supermarket
    SET Quantity = Quantity - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END $$

DELIMITER ;
