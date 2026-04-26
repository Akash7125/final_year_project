"""
Performance Metrics Dashboard
Displays real-time performance metrics and analytics
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from utils.performance_metrics import PerformanceMetrics
from plotly.subplots import make_subplots


class PerformanceDashboard:
    """Dashboard for displaying performance metrics"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.colors = {
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'warning': '#FFA726',
            'danger': '#F44336',
            'info': '#00BCD4',
            'success': '#66BB6A'
        }
    
    def apply_dashboard_style(self):
        """Apply custom CSS styling"""
        st.markdown("""
            <style>
            .metric-card {
                background: linear-gradient(135deg, #2D2D2D 0%, #1E1E1E 100%);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 0.5rem 0;
                border-left: 4px solid #4CAF50;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            }
            
            .metric-value {
                font-size: 2rem;
                font-weight: bold;
                color: #4CAF50;
                margin: 0.5rem 0;
            }
            
            .metric-label {
                font-size: 0.9rem;
                color: #B0B0B0;
            }
            
            .metric-change {
                font-size: 0.85rem;
                margin-top: 0.5rem;
            }
            
            .positive {
                color: #4CAF50;
            }
            
            .negative {
                color: #F44336;
            }
            
            .health-excellent { color: #4CAF50; }
            .health-good { color: #8BC34A; }
            .health-fair { color: #FFA726; }
            .health-poor { color: #F44336; }
            </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render dashboard header"""
        st.markdown("""
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h1 style='color: #4CAF50; margin-bottom: 0.5rem;'>📊 Performance Metrics Dashboard</h1>
                <p style='color: #B0B0B0; font-size: 0.95rem;'>Real-time analytics and system health monitoring</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_key_metrics(self, hours: int = 24):
        """Render key performance metrics in cards"""
        doc_stats = self.metrics.get_document_processing_stats(hours)
        analysis_stats = self.metrics.get_analysis_performance_stats(hours)
        health = self.metrics.get_system_health(hours)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📄 Documents Processed",
                f"{doc_stats['total_documents']}",
                delta=f"{doc_stats['success_rate']:.1f}% success",
                delta_color="normal"
            )
        
        with col2:
            avg_time = doc_stats['avg_processing_time_ms']
            st.metric(
                "⏱️ Avg Processing Time",
                f"{avg_time:.0f}ms",
                delta=f"Min: {doc_stats['min_processing_time_ms']:.0f}ms"
            )
        
        with col3:
            st.metric(
                "🎯 Avg ATS Score",
                f"{analysis_stats['avg_ats_score']:.1f}",
                delta=f"{analysis_stats['successful_analyses']} analyses",
                delta_color="normal"
            )
        
        with col4:
            health_score = health['overall_health_score']
            if health_score >= 90:
                status = "🟢 Excellent"
            elif health_score >= 70:
                status = "🟡 Good"
            elif health_score >= 50:
                status = "🟠 Fair"
            else:
                status = "🔴 Poor"
            
            st.metric(
                "🏥 System Health",
                f"{health_score:.1f}%",
                delta=status
            )
    
    def render_document_processing_chart(self, hours: int = 24):
        """Render document processing performance chart"""
        trends = self.metrics.get_performance_trends('document', hours)
        
        if not trends:
            st.info("No document processing data available")
            return
        
        df = pd.DataFrame(trends)
        df.rename(columns={'metric1': 'Documents Processed', 'metric2': 'Avg Time (ms)'}, inplace=True)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=df['date'], y=df['Documents Processed'], 
                  name='Documents Processed',
                  marker_color='#4CAF50'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['Avg Time (ms)'],
                      name='Avg Processing Time',
                      mode='lines+markers',
                      line=dict(color='#2196F3', width=3)),
            secondary_y=True
        )
        
        fig.update_layout(
            title='📊 Document Processing Trends',
            hovermode='x unified',
            template='plotly_dark',
            height=400,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Document Count", secondary_y=False)
        fig.update_yaxes(title_text="Avg Time (ms)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_analysis_performance_chart(self, hours: int = 24):
        """Render analysis performance metrics"""
        trends = self.metrics.get_performance_trends('analysis', hours)
        
        if not trends:
            st.info("No analysis data available")
            return
        
        df = pd.DataFrame(trends)
        df.rename(columns={'metric1': 'Avg Time (ms)', 'metric2': 'Avg ATS Score'}, inplace=True)
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['Avg Time (ms)'],
                      name='Execution Time',
                      mode='lines+markers',
                      line=dict(color='#FFA726', width=2),
                      fill='tozeroy'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df['date'], y=df['Avg ATS Score'],
                      name='ATS Score',
                      mode='lines+markers',
                      line=dict(color='#00BCD4', width=3)),
            secondary_y=True
        )
        
        fig.update_layout(
            title='📈 Resume Analysis Performance Trends',
            hovermode='x unified',
            template='plotly_dark',
            height=400,
            showlegend=True
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Execution Time (ms)", secondary_y=False)
        fig.update_yaxes(title_text="ATS Score", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_feature_popularity(self, hours: int = 24):
        """Render feature usage statistics"""
        features = self.metrics.get_feature_popularity(hours)
        
        if not features:
            st.info("No feature usage data available")
            return
        
        df = pd.DataFrame([
            {
                'Feature': f['feature'],
                'Usage Count': f['usage_count'],
                'Avg Time (ms)': f['avg_time_ms']
            }
            for f in features
        ])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df['Feature'],
            y=df['Usage Count'],
            name='Usage Count',
            marker_color='#4CAF50',
            text=df['Usage Count'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title='🔥 Most Used Features',
            xaxis_title='Feature',
            yaxis_title='Usage Count',
            template='plotly_dark',
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_document_type_distribution(self, hours: int = 24):
        """Render document type distribution"""
        distribution = self.metrics.get_document_type_distribution(hours)
        
        if not distribution:
            st.info("No document data available")
            return
        
        doc_types = list(distribution.keys())
        counts = [distribution[dtype]['count'] for dtype in doc_types]
        
        fig = go.Figure(data=[go.Pie(
            labels=doc_types,
            values=counts,
            marker=dict(colors=['#4CAF50', '#2196F3', '#FFA726', '#F44336']),
            textposition='inside',
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title='📁 Document Type Distribution',
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_api_performance(self, hours: int = 24):
        """Render API performance statistics"""
        api_stats = self.metrics.get_api_performance_stats(hours=hours)
        
        st.subheader("🌐 API Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total API Calls", f"{api_stats['total_api_calls']}")
        
        with col2:
            st.metric(
                "Avg Response Time",
                f"{api_stats['avg_response_time_ms']:.0f}ms"
            )
        
        with col3:
            st.metric(
                "Success Rate",
                f"{api_stats['success_rate']:.1f}%"
            )
        
        with col4:
            st.metric(
                "Successful Calls",
                f"{api_stats['successful_calls']}"
            )
    
    def render_detailed_statistics(self, hours: int = 24):
        """Render detailed statistics tables"""
        st.subheader("📋 Detailed Statistics")
        
        tab1, tab2, tab3 = st.tabs(["Document Processing", "Analysis Performance", "User Activity"])
        
        with tab1:
            doc_stats = self.metrics.get_document_processing_stats(hours)
            df = pd.DataFrame([doc_stats])
            st.dataframe(df.T, use_container_width=True)
        
        with tab2:
            analysis_stats = self.metrics.get_analysis_performance_stats(hours)
            df = pd.DataFrame([analysis_stats])
            st.dataframe(df.T, use_container_width=True)
        
        with tab3:
            user_stats = self.metrics.get_user_activity_stats(hours)
            df = pd.DataFrame([user_stats])
            st.dataframe(df.T, use_container_width=True)
    
    def render_dashboard(self):
        """Render the complete dashboard"""
        self.apply_dashboard_style()
        self.render_header()
        
        # Time range selector
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            hours = st.selectbox(
                "Time Range",
                [1, 6, 24, 7*24],
                format_func=lambda x: f"Last {x} hours" if x <= 24 else f"Last {x//24} days"
            )
        
        # Key metrics
        st.markdown("### 📌 Key Metrics")
        self.render_key_metrics(hours)
        
        st.divider()
        
        # Charts
        st.markdown("### 📊 Performance Trends")
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_document_processing_chart(hours)
        
        with col2:
            self.render_analysis_performance_chart(hours)
        
        st.divider()
        
        # Usage and distribution
        st.markdown("### 🎯 Usage Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_feature_popularity(hours)
        
        with col2:
            self.render_document_type_distribution(hours)
        
        st.divider()
        
        # API Performance
        self.render_api_performance(hours)
        
        st.divider()
        
        # Detailed statistics
        self.render_detailed_statistics(hours)
        
        # Footer
        st.markdown(f"""
            <div style='text-align: center; margin-top: 2rem; color: #B0B0B0; font-size: 0.85rem;'>
                Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)
