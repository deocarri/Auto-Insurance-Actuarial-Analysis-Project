/*
==================================================
DDL Script: Create Bronze Tables
==================================================
Script Purpose: 
  This script creates tables in the 'bronze' schema, dropping existing tables if they already exist. 
  Run this script to re-define the DDL structure of 'bronze' tables.
==================================================
*/

if object_id ('bronze.Frequency','U') is not null
	drop table bronze.Frequency;
create table bronze.Frequency(
	IDpol int, 
	ClaimNb int,
	Exposure decimal(10, 6),
	VehPower int,
	VehAge int,
	DrivAge int, 
	BonusMalus int, 
	VehBrand varchar(10),
	VehGas varchar(20), 
	Area varchar(10),
	Density int, 
	Region varchar(50)
);

if object_id ('bronze.Severity','U') is not null
	drop table bronze.Severity;
create table bronze.Severity(
	IDpol int, 
	ClaimAmount decimal(18, 6)
);
