"""Database optimization utilities and index management."""
from sqlalchemy import Index, text
from app.database import engine
from app.models import User, Resume, Job
import logging

logger = logging.getLogger(__name__)


# Database index definitions
DATABASE_INDEXES = [
    # User table indexes
    {
        'name': 'idx_users_email',
        'table': 'users',
        'columns': ['email'],
        'unique': True
    },
    {
        'name': 'idx_users_subscription_plan',
        'table': 'users',
        'columns': ['subscription_plan']
    },
    {
        'name': 'idx_users_created_at',
        'table': 'users',
        'columns': ['created_at']
    },
    {
        'name': 'idx_users_is_active',
        'table': 'users',
        'columns': ['is_active']
    },
    
    # Resume table indexes
    {
        'name': 'idx_resumes_user_id',
        'table': 'resumes',
        'columns': ['user_id']
    },
    {
        'name': 'idx_resumes_created_at',
        'table': 'resumes',
        'columns': ['created_at']
    },
    {
        'name': 'idx_resumes_user_created',
        'table': 'resumes',
        'columns': ['user_id', 'created_at']
    },
    
    # Job table indexes
    {
        'name': 'idx_jobs_user_id',
        'table': 'jobs',
        'columns': ['user_id']
    },
    {
        'name': 'idx_jobs_created_at',
        'table': 'jobs',
        'columns': ['created_at']
    },
    {
        'name': 'idx_jobs_status',
        'table': 'jobs',
        'columns': ['status'] 
    },
    {
        'name': 'idx_jobs_user_status',
        'table': 'jobs',
        'columns': ['user_id', 'status']
    },
    
    # Match table indexes
    {
        'name': 'idx_matches_resume_id',
        'table': 'candidate_matches',
        'columns': ['resume_id']
    },
    {
        'name': 'idx_matches_job_id',
        'table': 'candidate_matches',
        'columns': ['job_id']
    },
    {
        'name': 'idx_matches_score',
        'table': 'candidate_matches',
        'columns': ['score']
    },
    {
        'name': 'idx_matches_resume_job',
        'table': 'candidate_matches',
        'columns': ['resume_id', 'job_id'],
        'unique': True
    }
]


def create_indexes():
    """Create all defined indexes in the database."""
    with engine.connect() as conn:
        for idx_def in DATABASE_INDEXES:
            try:
                columns_str = ', '.join(idx_def['columns'])
                unique_str = 'UNIQUE' if idx_def.get('unique') else ''
                
                query = text(f"""
                    CREATE {unique_str} INDEX IF NOT EXISTS {idx_def['name']}
                    ON {idx_def['table']} ({columns_str})
                """)
                
                conn.execute(query)
                conn.commit()
                logger.info(f"Index {idx_def['name']} created successfully")
            except Exception as e:
                logger.error(f"Error creating index {idx_def['name']}: {str(e)}")
                conn.rollback()


def drop_indexes():
    """Drop all defined indexes from the database."""
    with engine.connect() as conn:
        for idx_def in DATABASE_INDEXES:
            try:
                query = text(f"DROP INDEX IF EXISTS {idx_def['name']}")
                conn.execute(query)
                conn.commit()
                logger.info(f"Index {idx_def['name']} dropped successfully")
            except Exception as e:
                logger.error(f"Error dropping index {idx_def['name']}: {str(e)}")
                conn.rollback()


def analyze_table_performance(table_name: str):
    """Analyze table performance and suggest optimizations.
    
    Args:
        table_name: Name of the table to analyze
        
    Returns:
        Dictionary with performance metrics
    """
    with engine.connect() as conn:
        try:
            # Get table size
            size_query = text(f"""
                SELECT 
                    pg_size_pretty(pg_total_relation_size('{table_name}')) as total_size,
                    pg_size_pretty(pg_relation_size('{table_name}')) as table_size,
                    pg_size_pretty(pg_indexes_size('{table_name}')) as indexes_size
            """)
            size_result = conn.execute(size_query).fetchone()
            
            # Get row count
            count_query = text(f"SELECT COUNT(*) FROM {table_name}")
            count_result = conn.execute(count_query).fetchone()
            
            # Get index usage statistics
            index_query = text(f"""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan,
                    idx_tup_read,
                    idx_tup_fetch
                FROM pg_stat_user_indexes
                WHERE tablename = '{table_name}'
            """)
            index_results = conn.execute(index_query).fetchall()
            
            return {
                'table_name': table_name,
                'total_size': size_result[0] if size_result else 'N/A',
                'table_size': size_result[1] if size_result else 'N/A',
                'indexes_size': size_result[2] if size_result else 'N/A',
                'row_count': count_result[0] if count_result else 0,
                'indexes': [
                    {
                        'name': row[2],
                        'scans': row[3],
                        'rows_read': row[4],
                        'rows_fetched': row[5]
                    }
                    for row in index_results
                ]
            }
        except Exception as e:
            logger.error(f"Error analyzing table {table_name}: {str(e)}")
            return {'error': str(e)}


def vacuum_analyze():
    """Run VACUUM ANALYZE to optimize database."""
    with engine.connect() as conn:
        try:
            # PostgreSQL specific
            conn.execute(text("VACUUM ANALYZE"))
            conn.commit()
            logger.info("VACUUM ANALYZE completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error running VACUUM ANALYZE: {str(e)}")
            return False


def optimize_query(query_str: str):
    """Analyze query execution plan and suggest optimizations.
    
    Args:
        query_str: SQL query string to analyze
        
    Returns:
        Query execution plan
    """
    with engine.connect() as conn:
        try:
            explain_query = text(f"EXPLAIN ANALYZE {query_str}")
            result = conn.execute(explain_query)
            plan = [row[0] for row in result]
            return {'plan': plan, 'query': query_str}
        except Exception as e:
            logger.error(f"Error analyzing query: {str(e)}")
            return {'error': str(e)}


def get_slow_queries(limit: int = 10):
    """Get slowest queries from database logs.
    
    Args:
        limit: Number of queries to return
        
    Returns:
        List of slow queries with execution times
    """
    with engine.connect() as conn:
        try:
            # PostgreSQL pg_stat_statements extension required
            query = text(f"""
                SELECT 
                    query,
                    calls,
                    total_exec_time,
                    mean_exec_time,
                    max_exec_time
                FROM pg_stat_statements
                ORDER BY mean_exec_time DESC
                LIMIT {limit}
            """)
            results = conn.execute(query).fetchall()
            
            return [
                {
                    'query': row[0],
                    'calls': row[1],
                    'total_time_ms': float(row[2]),
                    'mean_time_ms': float(row[3]),
                    'max_time_ms': float(row[4])
                }
                for row in results
            ]
        except Exception as e:
            logger.warning(f"Could not fetch slow queries: {str(e)}")
            return []


def get_database_stats():
    """Get overall database statistics.
    
    Returns:
        Dictionary with database metrics
    """
    with engine.connect() as conn:
        try:
            stats_query = text("""
                SELECT 
                    pg_size_pretty(pg_database_size(current_database())) as db_size,
                    (SELECT count(*) FROM pg_stat_activity) as connections,
                    (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections
            """)
            result = conn.execute(stats_query).fetchone()
            
            return {
                'database_size': result[0],
                'total_connections': result[1],
                'active_connections': result[2]
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            return {'error': str(e)}


if __name__ == '__main__':
    # Create all indexes
    logger.info("Creating database indexes...")
    create_indexes()
    
    # Run VACUUM ANALYZE
    logger.info("Running VACUUM ANALYZE...")
    vacuum_analyze()
    
    # Get database statistics
    logger.info("Fetching database statistics...")
    stats = get_database_stats()
    logger.info(f"Database stats: {stats}")
