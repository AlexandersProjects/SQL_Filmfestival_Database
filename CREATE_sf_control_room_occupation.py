USE Filmfestival
GO

DROP FUNCTION IF EXISTS [sf_Raum_belegt]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author: A. Blaschko-Schänzer, M. Heinrich
-- Create date: 22.07.2020
-- Description: Überprüft, ob der Raum für den kompletten übergebenen Zeitraum belegt ist
-- =============================================
CREATE FUNCTION [sf_Raum_belegt]
(
	@RaumID int,
	@Beginn_input datetime,
	@Ende_input datetime

)
RETURNS bit
AS
BEGIN
-- Returnvaribale deklarieren
	DECLARE @Beginn datetime;
	DECLARE @Ende datetime;
	DECLARE @Raum_Belegung int;
	DECLARE @Test int;

SET @Raum_Belegung = 1;

SELECT @Test = COUNT(*)
FROM dbo.Programm
WHERE dbo.Programm.RaumID = @RaumID
AND @Beginn_input BETWEEN dbo.Programm.Beginn AND dbo.Programm.Ende

IF @Test > 0
BEGIN
SET @Raum_Belegung = 0
END
ELSE
BEGIN
SELECT @Test = COUNT(*)
FROM dbo.Programm
WHERE dbo.Programm.RaumID = @RaumID
AND @Ende_input BETWEEN dbo.Programm.Beginn AND dbo.Programm.Ende

IF @Test > 0
BEGIN
SET @Raum_Belegung = 0
END

END

RETURN @Raum_Belegung

END
GO
