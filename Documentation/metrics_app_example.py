"""
Quick Integration Example for Performance Metrics
Add this to your app.py to enable metrics tracking
"""

import streamlit as st
import time
from utils.performance_metrics import PerformanceMetrics, PerformanceTimer
from dashboard.performance_dashboard import PerformanceDashboard


# Initialize metrics globally
@st.cache_resource
def get_metrics_instance():
    """Get or create metrics instance"""
    return PerformanceMetrics()


def track_file_upload():
    """Example: Track resume file upload"""
    metrics = get_metrics_instance()
    
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose a resume file (PDF or DOCX)")
    
    if uploaded_file is not None:
        file_size_mb = len(uploaded_file.getbuffer()) / (1024 * 1024)
        start_time = time.time()
        
        try:
            # Simulate processing (replace with actual processing logic)
            from utils.resume_parser import ResumeParser
            parser = ResumeParser()
            text = parser.extract_text(uploaded_file)
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            # Track the metric
            metrics.track_document_processing(
                file_type=uploaded_file.name.split('.')[-1].upper(),
                file_size_mb=file_size_mb,
                processing_time_ms=processing_time_ms,
                pages_count=len(text.split('\n')),  # Approximate
                success=True
            )
            
            st.success(f"✅ File processed in {processing_time_ms:.1f}ms")
            st.info(f"File size: {file_size_mb:.2f} MB")
            
            return text
            
        except Exception as e:
            processing_time_ms = (time.time() - start_time) * 1000
            metrics.track_document_processing(
                file_type=uploaded_file.name.split('.')[-1].upper(),
                file_size_mb=file_size_mb,
                processing_time_ms=processing_time_ms,
                pages_count=0,
                success=False
            )
            st.error(f"Error processing file: {e}")
            return None


def track_resume_analysis():
    """Example: Track resume analysis"""
    metrics = get_metrics_instance()
    
    st.subheader("🔍 Analyze Resume")
    
    resume_text = st.text_area("Paste resume text here")
    target_role = st.selectbox("Target Role", ["Software Engineer", "Data Scientist", "Product Manager"])
    
    if st.button("Analyze Resume"):
        start_time = time.time()
        
        try:
            # Simulate analysis (replace with actual analysis logic)
            from utils.resume_analyzer import ResumeAnalyzer
            analyzer = ResumeAnalyzer()
            
            # Simple scoring (replace with actual logic)
            ats_score = 75.5 + len(resume_text) % 10
            keyword_match = 65.3 + len(target_role) % 5
            
            execution_time_ms = (time.time() - start_time) * 1000
            
            # Track the metric
            metrics.track_analysis_performance(
                analysis_type='ai_analysis',
                execution_time_ms=execution_time_ms,
                ats_score=ats_score,
                keyword_match=keyword_match,
                success=True
            )
            
            # Track user activity
            metrics.track_user_activity(
                action='resume_analysis',
                feature_name='analyzer',
                duration_ms=execution_time_ms,
                success=True
            )
            
            st.success("✅ Analysis Complete!")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ATS Score", f"{ats_score:.1f}", delta="out of 100")
            with col2:
                st.metric("Keyword Match", f"{keyword_match:.1f}%", delta="coverage")
            with col3:
                st.metric("Processing Time", f"{execution_time_ms:.1f}ms", delta="duration")
                
        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            metrics.track_analysis_performance(
                analysis_type='ai_analysis',
                execution_time_ms=execution_time_ms,
                ats_score=0,
                keyword_match=0,
                success=False
            )
            st.error(f"Error analyzing resume: {e}")


def track_resume_building():
    """Example: Track resume builder usage"""
    metrics = get_metrics_instance()
    
    st.subheader("✏️ Build Resume")
    
    start_time = time.time()
    
    with st.form("resume_form"):
        st.text_input("Full Name")
        st.text_input("Email")
        st.text_input("Phone")
        st.text_area("Professional Summary")
        st.selectbox("Template", ["Modern", "Professional", "Minimal", "Creative"])
        
        submitted = st.form_submit_button("Generate Resume")
        
        if submitted:
            duration_ms = (time.time() - start_time) * 1000
            
            # Track the feature usage
            metrics.track_user_activity(
                action='resume_build',
                feature_name='resume_builder',
                duration_ms=duration_ms,
                success=True
            )
            
            st.success("✅ Resume generated successfully!")


def show_performance_dashboard():
    """Show the performance metrics dashboard"""
    dashboard = PerformanceDashboard()
    dashboard.render_dashboard()


def show_quick_stats():
    """Show quick performance statistics"""
    metrics = get_metrics_instance()
    
    st.subheader("⚡ Quick Performance Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get stats
    doc_stats = metrics.get_document_processing_stats(hours=24)
    analysis_stats = metrics.get_analysis_performance_stats(hours=24)
    health = metrics.get_system_health(hours=24)
    
    with col1:
        st.metric(
            "📄 Documents",
            doc_stats['total_documents'],
            f"{doc_stats['success_rate']:.0f}% success"
        )
    
    with col2:
        st.metric(
            "⏱️ Avg Time",
            f"{doc_stats['avg_processing_time_ms']:.0f}ms",
            "processing"
        )
    
    with col3:
        st.metric(
            "🎯 ATS Score",
            f"{analysis_stats['avg_ats_score']:.1f}",
            f"{analysis_stats['total_analyses']} analyses"
        )
    
    with col4:
        health_score = health['overall_health_score']
        status = "🟢 Good" if health_score >= 70 else "🟡 Fair" if health_score >= 50 else "🔴 Poor"
        st.metric(
            "🏥 Health",
            f"{health_score:.0f}%",
            status
        )


# ============================================================================
# MAIN APP INTEGRATION
# ============================================================================

def main():
    """Main application with metrics integration"""
    
    st.set_page_config(
        page_title="Smart Resume AI with Metrics",
        page_icon="🚀",
        layout="wide"
    )
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Smart Resume AI")
        st.divider()
        
        page = st.radio(
            "Select Feature",
            [
                "🏠 Home",
                "📄 Upload Resume",
                "🔍 Analyze Resume",
                "✏️ Build Resume",
                "📈 Performance Metrics",
                "⚡ Quick Stats"
            ]
        )
    
    # Render selected page
    if page == "🏠 Home":
        st.title("Welcome to Smart Resume AI")
        st.write("This application includes real-time performance metrics tracking!")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📄 **Upload & Process** resumes")
        with col2:
            st.info("🔍 **Analyze** content & scores")
        with col3:
            st.info("📊 **Track** performance metrics")
    
    elif page == "📄 Upload Resume":
        track_file_upload()
    
    elif page == "🔍 Analyze Resume":
        track_resume_analysis()
    
    elif page == "✏️ Build Resume":
        track_resume_building()
    
    elif page == "📈 Performance Metrics":
        show_performance_dashboard()
    
    elif page == "⚡ Quick Stats":
        show_quick_stats()
    
    # Footer
    st.divider()
    st.caption("Smart Resume AI with Real-Time Performance Metrics | Built with Streamlit")


if __name__ == "__main__":
    main()
