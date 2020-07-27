USE [Filmfestival]
GO

/****** Object:  StoredProcedure [dbo].[sp_Backup_Festival_mit_OUTPUT_Param_mit_Fehlermeldung]    Script Date: 27.07.2020 08:50:40 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- =============================================
-- Author:		A.Blaschko-Schänzer und M. Heinrich
-- Create date: 23.07.2020
-- Description:	Backup Prozedur mit Fehlermeldung
-- =============================================
CREATE PROCEDURE [dbo].[sp_Backup_Festival_mit_OUTPUT_Param_mit_Fehlermeldung]
	@Dateiname varchar(max), -- Filmfestival_backup
	-- @Pfad ungefähr: -- 'C:\Users\Blaschko\Alfatraining_SQL Kurs\SQL-Kurs\Filmfestival\Finale_Ordner_Struktur\SQL-Filmfestival-Blaschko Schänzer-Alexander\007-BackUp\Filmfestival_backup.bak'
	@Rückmeldung varchar(max) OUTPUT --Parameter
AS
BEGIN
	-- SET NOCOUNT ON added to prevent extra result sets from
	-- interfering with SELECT statements.
	SET NOCOUNT ON;
	DECLARE @path VARCHAR(MAX);
	DECLARE @backupFile VARCHAR(MAX);
	DECLARE @fileDate VARCHAR(8);
	DECLARE @fileTime VARCHAR(9);
	DECLARE @fileDateTime VARCHAR(18);

	BEGIN TRY
		---- SET PATH ------------
		SET @path = N'C:\DB\Filmfestival\Backup_Filmfestival\' --'F:\Filmfestival_Backup'
		---- Datum- und Zeitstempel und BACKUP
		SET @fileDate = CONVERT(VARCHAR(20), GETDATE(),112); -- 20200226
		SET @fileTime = REPLACE(CONVERT(VARCHAR(40), GETDATE(),114),':',''); --114336113
		----------- Dateiname ---------------
		SET @fileDateTime = @fileDate + '-' + @fileTime;

		SET @backupFile = @path + @Dateiname + '-' + @fileDateTime + '.bak' -- mit DatumZeit

		-- Backup erstellen hier: 'C:\Users\Blaschko\Alfatraining_SQL Kurs\SQL-Kurs\Filmfestival\Finale_Ordner_Struktur\SQL-Filmfestival-Blaschko Schänzer-Alexander\007-BackUp\Filmfestival_backup.bak'
		BACKUP DATABASE [Filmfestival] TO DISK = @backupFile; -- DB sichern
		SET @Rückmeldung = 'Datenbank gesichert!'


	END TRY
	BEGIN CATCH
		SET @Rückmeldung = 'Fehler Nr. ' + CONVERT(varchar, ERROR_NUMBER())+
			' ' + ERROR_MESSAGE();
	END CATCH

END
GO
