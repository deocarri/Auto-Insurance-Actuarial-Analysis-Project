/*
========================================================================
Stored Procedure: Load Silver Layer (Bronze -> Silver) 
========================================================================
Script Purpose: 
  This stored procedure performs the ETL (Extract, Transform, Load) process to 
  populate the 'silver' schema tables from the 'bronze'schema.
  It performs the following actions: 
  - Truncates Silver tables. 
  - Transforms and cleanses data from the Bronze layer and inserts it into Silver
	layer. 

Parameters: 
  None. 
  This stored procedure does not accept any parameters or return any values. 

Usage Example: 
  EXEC silver.load_silver;
=========================================================================
*/

create or alter procedure silver.load_silver as
begin
	declare @start_time datetime, @end_time datetime, @batch_start_time datetime, @batch_end_time datetime;
	begin try
		set @batch_start_time = getdate();
		print '================================';
		print 'Loading Silver Layer';
		print '================================';


		print '--------------------------------';
		print 'Loading Frequency Table';
		print '--------------------------------';

		set @start_time = getdate();
		print '>> Truncating Table: silver.Frequency';
		truncate table silver.Frequency;
		print '>> Inserting Data Into: silver.Frequency';
		insert into silver.Frequency(
			IDpol,
      ClaimNb,
      Exposure, 
      VehPower,
      VehAge, 
      DrivAge,
      BonusMalus,
      VehBrand, 
      VehGas, 
      Area, 
      Density, 
      Region)
		select
		  IDpol,
      ClaimNb as ClaimNumber, 
		  cast(Exposure as decimal(18,2)), 
      VehPower as VehiclePower, 
      VehAge as VehicleAge, 
      DrivAge as DriverAge, 
      BonusMalus, 
      trim(VehBrand) as VehicleBrand, 
      trim(VehGas) as VehicleGas,
      trim(Area), 
      Density, 
      trim(Region)
		set @end_time = getdate();
		print ' >> Load Duration ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '>>----------------------------';

    print '--------------------------------';
		print 'Loading Severity Table';
		print '--------------------------------';

		set @start_time = getdate();
		print '>> Truncating Table: silver.Severity';
		truncate table silver.Severity;
		print '>> Inserting Data Into: silver.Severity';
		insert into silver.Severity(
			IDpol,
      ClaimAmount)
    select
      IDpol,
      ClaimAmount
    set @end_time = getdate();
    print ' >> Load Duration ' + cast(datediff(second, @start_time, @end_time) as nvarchar) + ' seconds';
		print '>>----------------------------';

    set @batch_end_time = getdate();
		print '================================================';
		print ' >>>> Total Load Duration ' + cast(datediff(second, @batch_start_time, @batch_end_time) as nvarchar) + ' seconds';
		print '================================================';
	end try
	begin catch
		print '====================================';
		print 'ERROR OCCURED DURING LOADING SILVER LAYER';
		print 'Error Message' + ERROR_MESSAGE();
		print 'Error Message' + CAST(ERROR_NUMBER() as nvarchar);
		print 'Error Message' + CAST(ERROR_STATE() as nvarchar);
		print '====================================';
	end catch
end
