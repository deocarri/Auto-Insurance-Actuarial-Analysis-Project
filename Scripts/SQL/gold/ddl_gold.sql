/*
=====================================================================
DDL Script: Create Gold Table
=====================================================================
Script Purpose: 
  This script creates tables in the 'gold' schema, dropping existing tables if they already exist. 
  Run this script to re-define the DDL structure of 'silver' tables.
*/

-- Drop the gold layer table if it exists and create table for gold layer 
if object_id ('gold.PolicyRisk','U') is not null
	drop table gold.PolicyRisk;
go

create table gold.PolicyRisk(
	IDpol int not null,
	Exposure decimal(10, 6) not null, 
	ClaimNumber int, 
	TotalClaimAmount decimal(18, 2),
	ClaimFrequency decimal(18, 2), 
	AverageClaimSeverity decimal(18,2), 
	ExpectedLoss decimal(18,2),
	VehiclePower int, 
	VehicleAge int, 
	DriverAge int, 
	BonusMalus int, 
	VehicleBrand varchar(5),
	VehicleGas varchar(20), 
	Area varchar(5),
	Density int, 
	Region varchar(50),
	DriverAgeBand varchar(10), 
	BonusMalusBand varchar(10)
);
