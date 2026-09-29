/*
==================================================
DDL Script: Create Silver Tables
==================================================
Script Purpose: 
  This script creates tables in the 'silver' schema, dropping existing tables if they already exist. 
  Run this script to re-define the DDL structure of 'bronze' tables.
==================================================
*/

if object_id ('silver.Frequency','U') is not null
	drop table silver.Frequency;
go
	
create table silver.Frequency(
	IDpol int not null,
    ClaimNb int not null,
    Exposure decimal(10,6) not null, 
    VehPower int not null,
    VehAge int not null, 
    DrivAge int not null,
    BonusMalus int not null,
    VehBrand varchar(20) not null, 
    VehGas varchar(20) not null, 
    Area varchar(5) not null, 
    Density int not null, 
    Region varchar(50) not null
);
go

if object_id ('silver.Severity','U') is not null
	drop table silver.Severity;
go
	
create table silver.Severity(
	IDpol int not null,
	ClaimAmount decimal(18, 2) not null
);
go 
