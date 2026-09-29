/*
========================================================================
Stored Procedure: Load Bronze Layer (Source -> Bronze) 
========================================================================
Script Purpose: 
  This stored procedure loads data into the 'bronze' schema from external CSV files.
  It performs the following actions: 
  - Truncates the bronze tables before loading data. 
  - Uses the 'BULK INSERT' command to load data from csv files to bronze tables. 

Parameters: 
  None. 
  This stored procedure does not accept any parameters or return any values. 

Usage Example: 
  EXEC bronze.load_bronze;
=========================================================================
*/

create or alter procedure bronze.load_bronze as
begin
	declare @start_time datetime, @end_time datetime, @batch_start_time datetime, @batch_end_time datetime;
	begin try
		set @batch_start_time = getdate()
		print '================================';
		print 'Loading Bronze Layer';
		print '================================';


		print '--------------------------------';
		print 'Loading Frequency Table';
		print '--------------------------------';

		set @start_time = getdate();
		print '>> Truncating Table: bronze.Frequency';
		truncate table bronze.Frequency;

		print '>> Inserting Data Into: bronze.Frequency';
		bulk insert bronze.Frequency
		from 'C:\SQL Data\freMTPL2freq.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print ' >> Load Duration ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';

		print '--------------------------------';
		print 'Loading Severity Table';
		print '--------------------------------';

		set @start_time = getdate();
		print '>> Truncating Table: bronze.Severity';
		truncate table bronze.Severity;

		print '>> Inserting Data Into: bronze.Severity';
		bulk insert bronze.Frequency
		from 'C:\SQL Data\freMTPL2sev.csv'
		with (
			firstrow = 2,
			fieldterminator = ',',
			tablock
		);
		set @end_time = getdate();
		print ' >> Load Duration ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';

		set @batch_end_time = getdate()
		print '================================================'
		print ' >>>> Total Load Duration ' + cast(datediff(second, @batch_start_time, @batch_end_time) as nvarchar) + ' seconds';
		print '================================================'
	end try
	begin catch 
		print '====================================';
		print 'ERROR OCCURED DURING LOADING BRONZE LAYER';
		print 'Error Message' + ERROR_MESSAGE();
		print 'Error Message' + CAST(ERROR_NUMBER() as nvarchar);
		print 'Error Message' + CAST(ERROR_STATE() as nvarchar);
		print '====================================';
	end catch
end
