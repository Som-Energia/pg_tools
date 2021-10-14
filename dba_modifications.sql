-- Vacuum operations need to be executed outside transaction.
END TRANSACTION;
-- Put your dba maintaince operations here:
--
-- 
-- VACUUM FULL;
REINDEX index account_account_active_index;
--
--
-- End of your operations
BEGIN TRANSACTION;
-- No empty line at the end of the file
