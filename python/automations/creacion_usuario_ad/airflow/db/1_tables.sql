USE SPN;
GO

CREATE TABLE dbo.PendingADUsers (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    EmpID INT,
    Nombre NVARCHAR(100),
    Apellido NVARCHAR(100),
    Email NVARCHAR(150),
    Username NVARCHAR(100),
    Procesado BIT DEFAULT 0,
    FechaRegistro DATETIME DEFAULT GETDATE()
);
GO
