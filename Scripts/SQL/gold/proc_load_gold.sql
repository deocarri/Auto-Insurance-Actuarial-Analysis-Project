/*
========================================================================
Stored Procedure: Load Gold Layer (Silver -> Gold) 
========================================================================
Script Purpose: 
  This stored procedure transfers cleaned data from both silver layer tables to the gold layer, as well as adding data 
  that proves useful in consolidating and reporting data. 
  It performs the following actions: 
  - Truncates Gold table. 
  - Aggregates Silver severity table by policy
  - Joins Silver severity and frequency tables by IDpol. 
  - Adds additional columns useful for reporting. 

Parameters: 
  None. 
  This stored procedure does not accept any parameters or return any values. 

Usage Example: 
  EXEC gold.load_gold;
=========================================================================
*/

-- Aggregate severity to create a severity by policy CTE before joining to frequency
create or alter procedure gold.load_gold as
begin
	declare @batch_start_time datetime, @batch_end_time datetime;
	begin try
		set @batch_start_time = getdate();
		print '================================';
		print 'Loading Gold Layer';
		print '================================';

		print '>> Truncating Table: gold.PolicyRisk';
		truncate table gold.PolicyRisk;
		print '>> Inserting Data Into: gold.PolicyRisk';

    -- Aggregate severity to create a severity by policy CTE before joining to frequency
    with SeverityByPolicy as(
    	select 
    		IDpol,
    		sum(ClaimAmount) as TotalClaimAmount
    	from silver.Severity
    	group by IDpol
    )
    insert into gold.PolicyRisk(
    	IDpol,
    	Exposure, 
    	ClaimNb,
    	TotalClaimAmount,
    	ClaimFrequency,
    	AverageClaimSeverity,
    	ExpectedLoss,
    	VehPower,
    	VehAge,
    	DrivAge,
    	BonusMalus,
    	VehBrand,
    	VehGas,
    	Area,
    	Density,
    	Region,
    	DriverAgeBand,
    	BonusMalusBand
    )
    select 
    	f.IDpol,
    	f.Exposure,
    	f.ClaimNb,
    	coalesce(s.TotalClaimAmount, 0) as TotalClaimAmount,
    	f.ClaimNb / nullif(f.Exposure, 0) as ClaimFrequency, 
    	case 
    		when f.ClaimNb > 0 
    		then s.TotalClaimAmount / f.ClaimNb
    		else null
    	end as AverageClaimSeverity,
    	case 
    		when f.ClaimNb > 0 and s.TotalClaimAmount is not null
    		then (f.ClaimNb / nullif(f.Exposure, 0)) * (s.TotalClaimAmount / f.ClaimNb)
    		else null
    	end as ExpectedLoss,
    	f.VehPower, 
    	f.VehAge, 
    	f.DrivAge, 
    	f.BonusMalus,
    	f.VehBrand,
    	f.VehGas,
    	f.Area,
    	f.Density,
    	f.Region,
    	case 
    		when f.DrivAge between 18 and 24 then '18-24'
    		when f.DrivAge between 25 and 34 then '18-24'
    		when f.DrivAge between 35 and 44 then '18-24'
    		when f.DrivAge between 45 and 54 then '18-24'
    		when f.DrivAge between 54 and 64 then '18-24'
    		when f.DrivAge between 64 and 74 then '18-24'
    		when f.DrivAge >= 75 then '75+'
    	end as DriverAgeBand,
    	case
    		when f.BonusMalus < 80 then '<80'
    		when f.BonusMalus between 80 and 99 then '80-99'
    		when f.BonusMalus between 100 and 119 then '100-119'
    		when f.BonusMalus between 120 and 139 then '120-139'
    		when f.BonusMalus between 140 and 159 then '140-159'
    		when f.BonusMalus >= 160 then '160+'
    	end as BonusMalusBand
    from silver.Frequency f 
    left join silver.Severity s
    on f.IDpol = s.IDpol; 

		set @batch_end_time = getdate()
		print '================================================'
		print ' >>>> Total Load Duration ' + cast(datediff(second, @batch_start_time, @batch_end_time) as nvarchar) + ' seconds';
		print '================================================'
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
exec gold.load_gold
