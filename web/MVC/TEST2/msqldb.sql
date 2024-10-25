-- Department Table
CREATE TABLE Department (
    DepartmentID INT PRIMARY KEY IDENTITY(1,1),
    DepartmentName NVARCHAR(100) NOT NULL
);

-- Product Table
CREATE TABLE Product (
    ProductID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(100) NOT NULL,
    Category NVARCHAR(50) NOT NULL,
    Quantity INT NOT NULL,
    DepartmentID INT NULL,
    ProductionStatus NVARCHAR(20) NOT NULL CHECK (ProductionStatus IN ('Pending', 'InProgress', 'Completed')),
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE(),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- User Table
CREATE TABLE [User] (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(100) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(256) NOT NULL,
    Role NVARCHAR(20) NOT NULL CHECK (Role IN ('Admin', 'User'))
);


-- Insert sample data into the Department table
INSERT INTO Department (DepartmentName)
VALUES 
    ('Cutting'),
    ('Sewing'),
    ('Pressing'),
    ('Quality Control'),
    ('Packaging');

-- Insert sample data into the Product table
INSERT INTO Product (Name, Category, Quantity, DepartmentID, ProductionStatus, CreatedDate)
VALUES 
    ('T-Shirt', 'Top', 100, 1, 'Pending', GETDATE()),       -- Cutting
    ('Jeans', 'Bottom', 50, 2, 'InProgress', GETDATE()),    -- Sewing
    ('Hoodie', 'Top', 75, 3, 'Completed', GETDATE()),       -- Pressing
    ('Shorts', 'Bottom', 60, 1, 'Pending', GETDATE()),       -- Cutting
    ('Jacket', 'Outerwear', 30, 2, 'InProgress', GETDATE()), -- Sewing
    ('Hat', 'Accessory', 150, 4, 'Completed', GETDATE());    -- Quality Control

-- Insert sample data into the User table
INSERT INTO [User] (Username, PasswordHash, Role)
VALUES 
    ('admin@example.com', HASHBYTES('SHA2_256', 'Admin123!'), 'Admin'),
    ('user1@example.com', HASHBYTES('SHA2_256', 'User123!'), 'User'),
    ('user2@example.com', HASHBYTES('SHA2_256', 'User123!'), 'User'),
    ('manager@example.com', HASHBYTES('SHA2_256', 'Manager123!'), 'Admin');
