/*
============================================================
Create Database and Schemas
============================================================
Script Purpose: 
  This script creates a new database called 'AutoInsuranceActuarial' if it does not exist. 
  If it exists, it will drop the existing one and create a new, blank database. 
  The script also sets up three schemas: 'bronze', 'silver', and 'gold'. 

WARNING:
  Running this script will drop the entire 'AutoInsuranceActuarial' database if it exists. 
  All data in the database will be permanently deleted. Proceed with caution 
  and ensure you have proper backups before running this script. 
*/

USE master; 
GO

-- Drop and recreate the 'AutoInsuranceActuarial' database. 
if exists(select 1 from sys_databases where name = 'AutoInsuranceActuarial')
begin
  alter DATABASE AutoInsuranceActuarial set SINGLE_USER with rollback immediate;
  drop DATABASE AutoInsuranceActuarial;
end;
GO

--Create the 'AutoInsuranceActuarial' database
create DATABASE AutoInsuranceActuarial;
GO

USE AutoInsuranceActuarial;
GO

-- Create Schemas
create schema bronze;
GO
create schema silver; 
GO 
create schema gold;
GO
