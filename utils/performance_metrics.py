"""
Real-time Performance Metrics Tracker
Captures and calculates performance metrics for the resume analyzer application
"""

import time
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any
from config.database import get_database_connection
import statistics


class PerformanceMetrics:
    """Track and calculate real-time performance metrics"""
    
    def __init__(self):
        self.conn = get_database_connection()
        self.init_performance_tables()
        
    def init_performance_tables(self):
        """Initialize performance tracking tables"""
        cursor = self.conn.cursor()
        
        # Create performance metrics table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_ms REAL,
            status TEXT
        )
        ''')
        
        # Create API response times table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT NOT NULL,
            response_time_ms REAL,
            status_code INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            error_message TEXT
        )
        ''')
        
        # Create document processing metrics
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS document_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_type TEXT,
            file_size_mb REAL,
            processing_time_ms REAL,
            pages_count INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN
        )
        ''')
        
        # Create analysis performance metrics
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_type TEXT,
            execution_time_ms REAL,
            ats_score REAL,
            keyword_match REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN
        )
        ''')
        
        # Create user activity metrics
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            feature_name TEXT,
            duration_ms REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN
        )
        ''')
        
        self.conn.commit()
    
    def track_document_processing(self, file_type: str, file_size_mb: float, 
                                 processing_time_ms: float, pages_count: int, 
                                 success: bool = True, error_msg: str = None):
        """Track document processing metrics"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO document_metrics 
            (file_type, file_size_mb, processing_time_ms, pages_count, success)
            VALUES (?, ?, ?, ?, ?)
            ''', (file_type, file_size_mb, processing_time_ms, pages_count, success))
            self.conn.commit()
        except Exception as e:
            print(f"Error tracking document metrics: {e}")
    
    def track_analysis_performance(self, analysis_type: str, execution_time_ms: float,
                                  ats_score: float, keyword_match: float, 
                                  success: bool = True):
        """Track resume analysis performance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO analysis_performance 
            (analysis_type, execution_time_ms, ats_score, keyword_match, success)
            VALUES (?, ?, ?, ?, ?)
            ''', (analysis_type, execution_time_ms, ats_score, keyword_match, success))
            self.conn.commit()
        except Exception as e:
            print(f"Error tracking analysis performance: {e}")
    
    def track_api_call(self, api_name: str, response_time_ms: float, 
                      status_code: int = 200, error_msg: str = None):
        """Track API call performance"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO api_performance 
            (api_name, response_time_ms, status_code, error_message)
            VALUES (?, ?, ?, ?)
            ''', (api_name, response_time_ms, status_code, error_msg))
            self.conn.commit()
        except Exception as e:
            print(f"Error tracking API performance: {e}")
    
    def track_user_activity(self, action: str, feature_name: str, 
                          duration_ms: float, success: bool = True):
        """Track user activity and feature usage"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
            INSERT INTO user_activity 
            (action, feature_name, duration_ms, success)
            VALUES (?, ?, ?, ?)
            ''', (action, feature_name, duration_ms, success))
            self.conn.commit()
        except Exception as e:
            print(f"Error tracking user activity: {e}")
    
    # ===== METRICS CALCULATION METHODS =====
    
    def get_average_document_processing_time(self, hours: int = 24) -> float:
        """Calculate average document processing time in the last N hours"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT AVG(processing_time_ms) FROM document_metrics 
        WHERE timestamp > ? AND success = 1
        ''', (time_threshold,))
        
        result = cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_document_processing_stats(self, hours: int = 24) -> Dict:
        """Get comprehensive document processing statistics"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT 
            COUNT(*) as total_documents,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
            AVG(processing_time_ms) as avg_time,
            MIN(processing_time_ms) as min_time,
            MAX(processing_time_ms) as max_time,
            AVG(file_size_mb) as avg_size
        FROM document_metrics 
        WHERE timestamp > ?
        ''', (time_threshold,))
        
        row = cursor.fetchone()
        return {
            'total_documents': row[0] or 0,
            'successful_uploads': row[1] or 0,
            'avg_processing_time_ms': row[2] or 0.0,
            'min_processing_time_ms': row[3] or 0.0,
            'max_processing_time_ms': row[4] or 0.0,
            'avg_file_size_mb': row[5] or 0.0,
            'success_rate': (row[1] / row[0] * 100) if row[0] else 0
        }
    
    def get_average_ats_score(self, hours: int = 24) -> float:
        """Get average ATS score from recent analyses"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT AVG(ats_score) FROM analysis_performance 
        WHERE timestamp > ? AND success = 1
        ''', (time_threshold,))
        
        result = cursor.fetchone()[0]
        return result if result else 0.0
    
    def get_analysis_performance_stats(self, hours: int = 24) -> Dict:
        """Get comprehensive analysis performance statistics"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT 
            COUNT(*) as total_analyses,
            AVG(execution_time_ms) as avg_time,
            MIN(execution_time_ms) as min_time,
            MAX(execution_time_ms) as max_time,
            AVG(ats_score) as avg_ats,
            AVG(keyword_match) as avg_keyword_match,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful
        FROM analysis_performance 
        WHERE timestamp > ?
        ''', (time_threshold,))
        
        row = cursor.fetchone()
        return {
            'total_analyses': row[0] or 0,
            'avg_execution_time_ms': row[1] or 0.0,
            'min_execution_time_ms': row[2] or 0.0,
            'max_execution_time_ms': row[3] or 0.0,
            'avg_ats_score': row[4] or 0.0,
            'avg_keyword_match': row[5] or 0.0,
            'successful_analyses': row[6] or 0,
            'success_rate': (row[6] / row[0] * 100) if row[0] else 0
        }
    
    def get_api_performance_stats(self, api_name: str = None, hours: int = 24) -> Dict:
        """Get API performance statistics"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        if api_name:
            cursor.execute('''
            SELECT 
                COUNT(*) as total_calls,
                AVG(response_time_ms) as avg_response,
                MIN(response_time_ms) as min_response,
                MAX(response_time_ms) as max_response,
                SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful
            FROM api_performance 
            WHERE api_name = ? AND timestamp > ?
            ''', (api_name, time_threshold))
        else:
            cursor.execute('''
            SELECT 
                COUNT(*) as total_calls,
                AVG(response_time_ms) as avg_response,
                MIN(response_time_ms) as min_response,
                MAX(response_time_ms) as max_response,
                SUM(CASE WHEN status_code = 200 THEN 1 ELSE 0 END) as successful
            FROM api_performance 
            WHERE timestamp > ?
            ''', (time_threshold,))
        
        row = cursor.fetchone()
        return {
            'total_api_calls': row[0] or 0,
            'avg_response_time_ms': row[1] or 0.0,
            'min_response_time_ms': row[2] or 0.0,
            'max_response_time_ms': row[3] or 0.0,
            'successful_calls': row[4] or 0,
            'success_rate': (row[4] / row[0] * 100) if row[0] else 0
        }
    
    def get_user_activity_stats(self, hours: int = 24) -> Dict:
        """Get user activity statistics"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT 
            COUNT(*) as total_actions,
            COUNT(DISTINCT feature_name) as unique_features,
            AVG(duration_ms) as avg_duration,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_actions
        FROM user_activity 
        WHERE timestamp > ?
        ''', (time_threshold,))
        
        row = cursor.fetchone()
        return {
            'total_actions': row[0] or 0,
            'unique_features_used': row[1] or 0,
            'avg_action_duration_ms': row[2] or 0.0,
            'successful_actions': row[3] or 0,
            'success_rate': (row[3] / row[0] * 100) if row[0] else 0
        }
    
    def get_feature_popularity(self, hours: int = 24) -> List[Dict]:
        """Get most used features"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT 
            feature_name,
            COUNT(*) as usage_count,
            AVG(duration_ms) as avg_time
        FROM user_activity 
        WHERE timestamp > ?
        GROUP BY feature_name
        ORDER BY usage_count DESC
        LIMIT 10
        ''', (time_threshold,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'feature': row[0],
                'usage_count': row[1],
                'avg_time_ms': row[2]
            })
        return results
    
    def get_document_type_distribution(self, hours: int = 24) -> Dict:
        """Get distribution of document types processed"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
        SELECT 
            file_type,
            COUNT(*) as count,
            AVG(processing_time_ms) as avg_time
        FROM document_metrics 
        WHERE timestamp > ?
        GROUP BY file_type
        ''', (time_threshold,))
        
        results = {}
        for row in cursor.fetchall():
            results[row[0]] = {
                'count': row[1],
                'avg_processing_time_ms': row[2]
            }
        return results
    
    def get_system_health(self, hours: int = 24) -> Dict:
        """Get overall system health metrics"""
        doc_stats = self.get_document_processing_stats(hours)
        analysis_stats = self.get_analysis_performance_stats(hours)
        api_stats = self.get_api_performance_stats(hours=hours)
        user_stats = self.get_user_activity_stats(hours)
        
        # Calculate overall health score (0-100)
        health_components = [
            doc_stats.get('success_rate', 0),
            analysis_stats.get('success_rate', 0),
            api_stats.get('success_rate', 0),
            user_stats.get('success_rate', 0)
        ]
        
        overall_health = statistics.mean(health_components) if health_components else 0
        
        return {
            'overall_health_score': overall_health,
            'document_processing': doc_stats,
            'analysis_performance': analysis_stats,
            'api_performance': api_stats,
            'user_activity': user_stats,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_performance_trends(self, metric_type: str = 'analysis', hours: int = 24) -> List[Dict]:
        """Get performance trends over time"""
        cursor = self.conn.cursor()
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        if metric_type == 'analysis':
            cursor.execute('''
            SELECT 
                DATE(timestamp) as date,
                AVG(execution_time_ms) as avg_time,
                AVG(ats_score) as avg_score
            FROM analysis_performance 
            WHERE timestamp > ?
            GROUP BY DATE(timestamp)
            ORDER BY date
            ''', (time_threshold,))
        
        elif metric_type == 'document':
            cursor.execute('''
            SELECT 
                DATE(timestamp) as date,
                COUNT(*) as doc_count,
                AVG(processing_time_ms) as avg_time
            FROM document_metrics 
            WHERE timestamp > ?
            GROUP BY DATE(timestamp)
            ORDER BY date
            ''', (time_threshold,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'date': row[0],
                'metric1': row[1],
                'metric2': row[2]
            })
        return results
    
    def cleanup_old_metrics(self, days: int = 30):
        """Clean up metrics older than N days"""
        cursor = self.conn.cursor()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        tables = [
            'performance_metrics',
            'api_performance',
            'document_metrics',
            'analysis_performance',
            'user_activity'
        ]
        
        for table in tables:
            cursor.execute(f'''
            DELETE FROM {table} WHERE timestamp < ?
            ''', (cutoff_date,))
        
        self.conn.commit()


# Timer context manager for tracking execution time
class PerformanceTimer:
    """Context manager for tracking execution time"""
    
    def __init__(self, metrics_tracker: PerformanceMetrics, metric_name: str):
        self.metrics = metrics_tracker
        self.metric_name = metric_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_ms = (time.time() - self.start_time) * 1000
        success = exc_type is None
        self.metrics.track_user_activity(
            action='execution',
            feature_name=self.metric_name,
            duration_ms=elapsed_ms,
            success=success
        )
