/*
===========================================================
Quality Checks
===========================================================
Script Purpose: 
  This script performs various quality checks for data consistency, accuracy,
  and standardization across the 'silver' schemas. This includes:
  - Null or duplicate primary keys. 
  - Unwanted spaces in string fields
  - Data standardization and consistency. 
  - Data consistency between related fields. 

Usage Notes: 
  - These can be used before and after loading the Silver Layer by 
    switching bronze to silver or vice versa. 
  - Investigate and resolve any discrepancies found during the checks.
=============================================================
*/

-- Frequency row count
select count(*) as TotalRows from bronze.Frequency;

-- Unique policies
select count(distinct IDpol) as UniquePolicies from bronze.Frequency;

-- Duplicate policies
select 
	IDpol,
	count(*) as RecordCount,
from bronze.Frequency
group by IDpol
having count(*) > 1;

-- Missing value check for frequency
select 
	sum(case when IDpol is null then 1 else 0 end) as MissingID, 
	sum(case when ClaimNb is null then 1 else 0 end) as MissingClaimNb,
	sum(case when Exposure is null then 1 else 0 end) as MissingExposure,
	sum(case when DrivAge is null then 1 else 0 end) as MissingDrivAge,
	sum(case when BonusMalus is null then 1 else 0 end) as MissingBonusMalus,
from bronze.Frequency;

-- Missing value check for severity
select 
	sum(case when IDpol is null then 1 else 0 end) as MissingID,
	sum(case when ClaimAmount is null then 1 else 0 end) as MissingClaimAmount
from bronze.Severity;

-- Important Exposure ranges
select 
	min(Exposure) as MinExposure, 
	max(Exposure) as MaxExposure, 
	avg(Exposure) as AvgExposure
from bronze.Frequency;

-- Important Driver Age ranges
select 
	min(DrivAge) as MinDriverAge,
	max(DrivAge) as MaxDriverAge
from bronze.Frequency;

-- Important Vehicle Age ranges
select 
	min(VehAge) as MinVehicleAge,
	max(VehAge) as MaxVehicleAge
from bronze.Frequency

-- Important Claim count ranges
select 
	min(ClaimNb) as MinClaims,
	max(ClaimNb) as MaxClaims,
	sum(ClaimNb) as TotalClaims
from bronze.Frequency;

-- Important Claim severity ranges
select
	min(ClaimAmount) as MinClaim,
	max(ClaimAmount) as MaxClaim, 
	avg(ClaimAmount) as AvgClaim,
	sum(ClaimAmount) as TotalClaimsPaid
from bronze.Severity;
