USE Filmfestival
GO

DROP PROCEDURE IF EXISTS [dbo].[sp_Programmpunkt_hinzufügen]
GO



SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- =============================================
-- Author: A. Blaschko-Schänzer, M. Heinrich
-- Create date: 22.07.2020
-- Description: Überprüfen, ob der Programmpunkt in der Vergangenheit liegt, der Raum existiert, ggf. der Film existiert und ob zu der Zeit kein anderer Programmpunkt den Raum belegt
-- =============================================
CREATE PROCEDURE sp_Programmpunkt_hinzufügen
-- Add the parameters for the stored procedure here
	@Bezeichnung nvarchar(50),
	@Beginn_input datetime,
	@Ende_input datetime,
	@RaumID int = NULL,
	@FilmID int = NULL,
	@Kommentar text = NULL,
	@Erfolg bit OUTPUT,
	@Rückmeldung VARCHAR(MAX) OUTPUT
AS
BEGIN
-- SET NOCOUNT ON added to prevent extra result sets from
-- interfering with SELECT statements.
SET NOCOUNT ON;
	DECLARE @Nachricht AS varchar(MAX);
	DECLARE @Ergebnis_date AS datetime;
	DECLARE @Ergebnis AS int;
-------------------------------------------------------------------
BEGIN TRY
	-- @Beginn_input liegt nicht in der Vergangenheit
	SET @Ergebnis_date = GETDATE()
	IF (@Ergebnis_date > @Beginn_input)
	THROW 50001, 'Start des Programmpunktes liegt in der Vergangenheit', 1;

	-- @Ende_input liegt nicht in der Vergangenheit
	IF (@Ergebnis_date > @Ende_input)
	THROW 50002, 'Ende des Programmpunktes liegt in der Vergangenheit', 1;

	IF(@RaumID IS NOT NULL)
	BEGIN
	SELECT @Ergebnis = COUNT(RaumID)
	FROM Programm
	WHERE dbo.Programm.RaumID = @RaumID
	IF (@Ergebnis = 0) -- PersonalID nicht gefunden, Fehler
	THROW 50003, 'RaumID nicht vorhanden', 1;
	END

	IF(@FilmID IS NOT NULL)
	BEGIN
		SELECT @Ergebnis = COUNT(FilmID)
		FROM Programm
		WHERE dbo.Programm.FilmID = @FilmID
		IF (@Ergebnis = 0) -- PersonalID nicht gefunden, Fehler
			THROW 50004, 'FilmID nicht vorhanden', 1;
	END

	IF(@FilmID IS NOT NULL AND @RaumID IS NULL)
			THROW 50005, 'FilmID vorhanden aber kein Raum übergeben', 1;

-- Raum belegt
IF dbo.sf_Raum_belegt(@RaumID, @Beginn_input, @Ende_input) = 0
THROW 50006, 'Der Raum ist zu der Zeit bereits belegt', 1;

-- INSERT INTO [dbo].[Programm]
INSERT INTO [dbo].[Programm]
(Bezeichnung, Beginn, Ende, FilmID, RaumID, Kommentar)
VALUES (@Bezeichnung, @Beginn_input, @Ende_input, @FilmID, @RaumID, @Kommentar);

SET @Erfolg = 1;
SET @Rückmeldung = 'Programmpunkt hinzugefügt';
END TRY
BEGIN CATCH
SET @Erfolg = 0; -- nicht geklappt--
-- @Feedback text OUTPUT --Fehlermeldungen etc.
SET @Rückmeldung =
'Fehler Nr. ' + CONVERT(varchar, ERROR_NUMBER()) + ' ' +
ERROR_MESSAGE();
END CATCH;
END
GO
