USE SPN;
GO

CREATE TRIGGER trg_NewEmployee_AD
ON dbo.Empleados
AFTER INSERT
AS
BEGIN
    INSERT INTO dbo.PendingADUsers (EmpID, Nombre, Apellido, Email, Username)
    SELECT 
        i.EMP_ID,
        i.Nombre,
        i.Apellido,
        i.Email,
        LOWER(LEFT(i.Nombre,1) + i.Apellido)
    FROM inserted i;
END;
GO
