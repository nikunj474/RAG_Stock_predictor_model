
# postgresql configuration and index creation
# m is the number of bi-directional links created for each element during each layer phase--the max degree of the graph
# ef_construction is the number of candidate vertices to evaluate during the construction of the graph
# To max them out, I had to edit configuration settings to increase working memory and parrallel workers
'''
CREATE INDEX ON news USING hnsw (embedding vector_cosine_ops)
WITH (m = 32, ef_construction = 500);

-- Memory configuration
SELECT name, setting || ' ' || unit AS value
FROM pg_settings
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem', 'effective_cache_size');

-- CPU configuration
SELECT name, setting
FROM pg_settings
WHERE name IN ('max_parallel_workers', 'max_parallel_maintenance_workers', 'max_worker_processes');

-- Total memory (from OS statistics)
SELECT pg_size_pretty(total_memory::bigint) AS total_memory
FROM (SELECT (SELECT setting::bigint FROM pg_settings WHERE name = 'shared_buffers') * (SELECT current_setting('block_size')::bigint) AS total_memory) t;

-- CPU count (logical cores)
SELECT count(*) AS cpu_count
FROM pg_stat_activity
WHERE state IS NOT NULL;

CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Check active queries and resource usage
SELECT total_exec_time, shared_blks_hit, shared_blks_read
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;


SET maintenance_work_mem = '128MB';
SET work_mem = '8MB';
SHOW shared_buffers;

SET effective_cache_size = '128MB';
SET max_parallel_maintenance_workers = 1;
SET max_parallel_workers = 2;

'''


#ACTUAL USED
'''
SET maintenance_work_mem = '256MB';
-- Memory configuration
SELECT name, setting || ' ' || unit AS value
FROM pg_settings
WHERE name IN ('shared_buffers', 'work_mem', 'maintenance_work_mem', 'effective_cache_size');

-- CPU configuration
SELECT name, setting
FROM pg_settings
WHERE name IN ('max_parallel_workers', 'max_parallel_maintenance_workers', 'max_worker_processes');


-- Total memory (from OS statistics)
SELECT pg_size_pretty(total_memory::bigint) AS total_memory
FROM (SELECT (SELECT setting::bigint FROM pg_settings WHERE name = 'shared_buffers') * (SELECT current_setting('block_size')::bigint) AS total_memory) t;

-- CPU count (logical cores)
SELECT count(*) AS cpu_count
FROM pg_stat_activity
WHERE state IS NOT NULL;




-- Set maintenance_work_mem to 262144 (256MB)
SET maintenance_work_mem = '262144kB';

-- Set effective_cache_size to 524288 (4GB)
SET effective_cache_size = '524288kB';

-- Set max_parallel_maintenance_workers to 2
SET max_parallel_maintenance_workers = 2;

-- Set max_parallel_workers to 4
SET max_parallel_workers = 4;


-- Reload configuration to apply dynamic changes (doesn't require restart for dynamic parameters)
SELECT pg_reload_conf();



CREATE INDEX ON news USING hnsw (embedding vector_cosine_ops)
WITH (m = 12, ef_construction = 32);

SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%"
FROM pg_stat_progress_create_index;'''