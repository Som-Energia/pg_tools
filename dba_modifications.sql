-- Vacuum operations need to be executed outside transaction.
END TRANSACTION;
-- Put your dba maintaince operations here:
--
-- 
-- VACUUM FULL;
REINDEX table account_invoice;
--
--
-- End of your operations
BEGIN TRANSACTION;
-- No empty line at the end of the file
