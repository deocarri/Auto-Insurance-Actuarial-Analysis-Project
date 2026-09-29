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
	IDpol int, 
  
);
go
