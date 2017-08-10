set linesize 500
column TABNAME format a50
column FIELDNAME format a50
select SAPSR3.DD03L.tabname, SAPSR3.DD03L.fieldname from SAPSR3.DD03L inner join SAPSR3.DD02L on SAPSR3.DD02L.tabname = SAPSR3.DD03L.tabname where ( SAPSR3.DD03L.domname IN ( 'LOGSYS' , 'EDI_PARNUM' , 'ADDRLOGSYS' )) and SAPSR3.DD02L.tabclass = 'TRANSP';
