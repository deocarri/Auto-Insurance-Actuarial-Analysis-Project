/*
=============================================
Validation Checks
=============================================
Script Purpose: 
  This double checks some of the verified information to ensure the information from the silver tables were transfered 
  and joined properly. It also completes a simple calculation to ensure data can be used properly. 
*/
-- Gold table validations

-- Determine policy amount which should be the same amount as policy amount in frequency dataset
select count(*) as PolicyCount from gold.PolicyRisk;

-- Double check some of the data 
select
	sum(Exposure) as TotalExposure,
	sum(ClaimNb) as TotalClaims, 
	sum(TotalClaimAmount) as TotalClaimAmount
from gold.PolicyRisk;

select 
	DriverAgeBand, 
	count(*) as Policies, 
	sum(Exposure) as TotalExposure,
	sum(ClaimNb) as TotalClaims,
	sum(ClaimNb) / sum(Exposure) as ClaimFrequency
from gold.PolicyRisk
group by DriverAgeBand
order by DriverAgeBand;

