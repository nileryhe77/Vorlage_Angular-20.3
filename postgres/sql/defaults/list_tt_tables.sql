SELECT tablename 
FROM pg_catalog.pg_tables 
WHERE schemaname = 'public' 
    AND tableowner = 'postgres' 
    AND tablename LIKE 'tt_%';