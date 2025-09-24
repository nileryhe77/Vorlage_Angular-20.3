select c.column_name, data_type, is_nullable, case when P.column_name is null then false else true end as primary_key
from information_schema.columns C
left join (SELECT c.column_name, tc.table_name
FROM information_schema.table_constraints tc 
JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
  AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
WHERE constraint_type = 'PRIMARY KEY') P on C.column_name = P.column_name and C.table_name = P.table_name
where c.table_name = '__TABLE__NAME__HERE__'
order by ordinal_position