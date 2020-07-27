USE [Filmfestival]
GO

/****** Object:  UserDefinedFunction [dbo].[tf_Zeit_fuer_Aufgaben]    Script Date: 22.07.2020 12:06:03 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

DROP FUNCTION IF EXISTS [dbo].[tf_Zeit_fuer_Aufgaben]
GO

-- AUFGABE: anpassen! (Datum von - bis)
CREATE FUNCTION [dbo].[tf_Zeit_fuer_Aufgaben]
(
-- Add the parameters for the function here
-- @AufgabenID int,
-- @Aufgabenbeginn datetime,
-- @Aufgabenende datetime
-- TO DO Tag Monat als Parameter bzw Datum
	@Arbeitszeit_min nvarchar(100)
)
RETURNS TABLE
AS
RETURN
(
-- Add the SELECT statement with parameter references here
SELECT dbo.Aufgabenzuordnung.AufgabenID, dbo.Aufgaben.Bezeichnung AS Aufgabe, dbo.Aufgaben.Aufgabenbeginn AS Beginn,
dbo.Aufgaben.Aufgabenende AS Ende, COUNT(dbo.Personal.PersonalID) AS Mitarbeiter,
DATEDIFF(MINUTE, dbo.Aufgaben.Aufgabenbeginn, dbo.Aufgaben.Aufgabenende) * COUNT(dbo.Personal.PersonalID) AS 'Gesamte Arbeitszeit pro Aufgabe'
FROM dbo.Aufgaben
INNER JOIN dbo.Aufgabenzuordnung
	ON dbo.Aufgaben.AufgabenID = dbo.Aufgabenzuordnung.AufgabenID
INNER JOIN dbo.Personal
	ON dbo.Aufgabenzuordnung.PersonalID = dbo.Personal.PersonalID
GROUP BY dbo.Aufgaben.Bezeichnung, dbo.Aufgabenzuordnung.AufgabenID, dbo.Aufgaben.Aufgabenbeginn, dbo.Aufgaben.Aufgabenende
-- ORDER BY dbo.Aufgabenzuordnung.AufgabenID DESC
HAVING DATEDIFF(MINUTE, dbo.Aufgaben.Aufgabenbeginn, dbo.Aufgaben.Aufgabenende) * COUNT(dbo.Personal.PersonalID) >= @Arbeitszeit_min
)
GO
