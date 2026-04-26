# Detailed Section-wise Explanation: app.py & resume_analyzer.py

---

# **app.py - DETAILED BREAKDOWN**

## **SECTION 1: IMPORTS & DEPENDENCIES (Lines 1-40)**

```python
"""
SkillMatch - Main Application
"""
import time
from PIL import Image
from jobs.job_search import render_job_search
from datetime import datetime
from ui_components import (...)
from feedback.feedback import FeedbackManager
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from docx import Document
```

**Purpose:** Import all required libraries and modules

**Key Imports Explained:**

| Import | Purpose |
|--------|---------|
| `PIL.Image` | Handle image processing for resume |
| `datetime` | Track timestamps of resume uploads |
| `jobs.job_search` | Job search functionality |
| `ui_components` | Reusable UI elements (buttons, cards) |
| `feedback.FeedbackManager` | Handle user feedback |
| `python-docx` | Read/write DOCX files |
| `plotly` | Create interactive charts |
| `streamlit` | Web app framework |
| `pandas` | Data manipulation (Excel export) |
| `config.database` | SQLite database operations |
| `utils.ai_resume_analyzer` | AI analysis using Gemini API |
| `utils.resume_builder` | Resume template building |
| `utils.resume_analyzer` | Resume text analysis |

---

## **SECTION 2: PAGE CONFIGURATION (Lines 42-46)**

```python
# Set page config at the very beginning
st.set_page_config(
    page_title="SkillMatch",
    page_icon="🚀",
    layout="wide"
)
```

**Purpose:** Configure Streamlit app settings

**What it does:**
- `page_title`: Browser tab name = "SkillMatch"
- `page_icon`: Browser tab icon = 🚀
- `layout="wide"`: Use full width layout

---

## **SECTION 3: ResumeApp CLASS INITIALIZATION (Lines 48-125)**

```python
class ResumeApp:
    def __init__(self):
        """Initialize the application"""
```

### **3.1: Form Data Setup (Lines 50-67)**
```python
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'personal_info': {
            'full_name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'portfolio': ''
        },
        'summary': '',
        'experiences': [],
        'education': [],
        'projects': [],
        'skills_categories': {
            'technical': [],
            'soft': [],
            'languages': [],
            'tools': []
        }
    }
```

**Purpose:** Initialize empty form structure for resume builder

**What each field stores:**
- `personal_info`: Contact details
- `summary`: Professional summary
- `experiences`: List of past jobs
- `education`: School/university data
- `projects`: Past projects
- `skills_categories`: Organized skill types

---

### **3.2: Navigation & Admin State (Lines 69-84)**
```python
# Initialize navigation state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Initialize admin state
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

self.pages = {
    "🏠 HOME": self.render_home,
    "🔍 RESUME ANALYZER": self.render_analyzer,
    "📝 RESUME BUILDER": self.render_builder,
    "📊 DASHBOARD": self.render_dashboard,
    "🎯 JOB SEARCH": self.render_job_search,
    "💬 FEEDBACK": self.render_feedback_page,
    "ℹ️ ABOUT": self.render_about
}
```

**Purpose:** Create navigation menu and track admin access

**Pages Dictionary:**
- Maps page names to rendering functions
- Used to switch between different app sections

---

### **3.3: Initialize Core Objects (Lines 86-89)**
```python
# Initialize dashboard manager
self.dashboard_manager = DashboardManager()

self.analyzer = ResumeAnalyzer()
self.ai_analyzer = AIResumeAnalyzer()
self.builder = ResumeBuilder()
self.job_roles = JOB_ROLES
```

**Purpose:** Create instances of main analysis tools

| Object | Purpose |
|--------|---------|
| `DashboardManager()` | Manage analytics dashboard |
| `ResumeAnalyzer()` | Standard text-based analysis |
| `AIResumeAnalyzer()` | AI analysis via Gemini API |
| `ResumeBuilder()` | Create resume from templates |
| `JOB_ROLES` | Config with job role data |

---

### **3.4: Session State Variables (Lines 91-110)**
```python
# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = 'default_user'
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

# Initialize database
init_database()

# Load external CSS
with open('style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load Google Fonts
st.markdown("""
    <link href="...fonts.googleapis.com/css2?...">
    <link rel="stylesheet" href="...font-awesome...">
""", unsafe_allow_html=True)

if 'resume_data' not in st.session_state:
    st.session_state.resume_data = []
if 'ai_analysis_stats' not in st.session_state:
    st.session_state.ai_analysis_stats = {
        'score_distribution': {},
        'total_analyses': 0,
        'average_score': 0
    }
```

**Purpose:** Initialize persistent session variables and styling

**What happens:**
1. Create unique user ID (tracks current user)
2. Initialize database tables
3. Load custom CSS styles
4. Load Google Fonts (Roboto, Poppins)
5. Load Font Awesome icons
6. Create empty data containers

---

## **SECTION 4: UTILITY METHODS (Lines 127-407)**

### **4.1: load_lottie_url() - Lines 127-131**
```python
def load_lottie_url(self, url: str):
    """Load Lottie animation from URL"""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
```

**Purpose:** Fetch animated JSON files from URLs

**How it works:**
- Makes HTTP request to animation URL
- Returns JSON if successful, None if fails
- Used for decorative animations on pages

---

### **4.2: apply_global_styles() - Lines 133-370**
```python
def apply_global_styles(self):
    st.markdown("""
    <style>
    /* Custom Scrollbar */
    ::-webkit-scrollbar { ... }
    
    /* Global Styles */
    .main-header { ... }
    .template-card { ... }
    .action-button { ... }
    .form-section { ... }
    @keyframes slideIn { ... }
    @media (max-width: 768px) { ... }
    </style>
    """, unsafe_allow_html=True)
```

**Purpose:** Apply custom CSS styling to entire app

**Style Components:**

| Style | Purpose |
|-------|---------|
| `.main-header` | Top hero section with green gradient |
| `.template-card` | Resume template selection cards |
| `.action-button` | Call-to-action buttons with hover effects |
| `.form-section` | Form container styling |
| `.skill-tag` | Skill badges with hover effects |
| `.progress-circle` | ATS score progress visualization |
| `@keyframes slideIn` | Smooth entrance animations |
| `@media (max-width: 768px)` | Mobile responsiveness |

**Visual Effects:**
- Gradient backgrounds
- Hover animations (lift up on hover)
- Glass-morphism effect (blur + transparency)
- Smooth transitions

---

### **4.3: add_footer() - Lines 372-378**
```python
def add_footer(self):
    """Add a footer to all pages"""
    st.markdown("<hr style='...'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
```

**Purpose:** Add consistent footer to all pages

**What it includes:**
- Horizontal divider line
- 3-column layout
- Links to social media / resources

---

### **4.4: export_to_excel() - Lines 393-416**
```python
def export_to_excel(self):
    """Export resume data to Excel"""
    conn = get_database_connection()
    
    query = """
        SELECT
            rd.name, rd.email, rd.phone, rd.linkedin, rd.github, rd.portfolio,
            rd.summary, rd.target_role, rd.target_category,
            rd.education, rd.experience, rd.projects, rd.skills,
            ra.ats_score, ra.keyword_match_score, ra.format_score, ra.section_score,
            ra.missing_skills, ra.recommendations,
            rd.created_at
        FROM resume_data rd
        LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
    """
    
    df = pd.read_sql_query(query, conn)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Resume Data')
    
    return output.getvalue()
```

**Purpose:** Export all resume data to Excel file

**Process:**
1. Connect to SQLite database
2. Query all resumes + analysis scores
3. Convert to Pandas DataFrame
4. Write to Excel (.xlsx) format
5. Return binary file data

**Columns Exported:**
- Personal info (name, email, phone, LinkedIn, etc.)
- Resume content (summary, education, experience, projects, skills)
- Analysis scores (ATS, keyword match, format, etc.)
- Timestamp of upload

---

## **SECTION 5: RESUME UPLOAD & ANALYSIS (Lines 530-568)**

### **5.1: handle_resume_upload() - Lines 545-568**
```python
def handle_resume_upload(self):
    """Handle resume upload and analysis"""
    uploaded_file = st.file_uploader(
        "Upload your resume", type=['pdf', 'docx'])

    if uploaded_file is not None:
        try:
            # Extract text from resume
            if uploaded_file.type == "application/pdf":
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)

            # Store resume data
            st.session_state.resume_data = {
                'filename': uploaded_file.name,
                'content': resume_text,
                'upload_time': datetime.now().isoformat()
            }

            # Analyze resume
            analytics = self.analyze_resume(resume_text)
            return True
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")
            return False
    return False
```

**Purpose:** Upload and extract resume text

**Step-by-step:**
1. Create file uploader widget
2. Accept only PDF or DOCX files
3. Check file type
4. Extract text using appropriate method
5. Store in session state with metadata
6. Run analysis
7. Return success/failure status

---

## **SECTION 6: RESUME BUILDER (Lines 570-850)**

### **6.1: render_builder() - Entry Point**
```python
def render_builder(self):
    st.title("Resume Builder 📝")
    st.write("Create your professional resume")
```

### **6.2: Template Selection (Lines 575-577)**
```python
template_options = ["Modern", "Professional", "Minimal", "Creative"]
selected_template = st.selectbox(
    "Select Resume Template", template_options)
st.success(f"🎨 Currently using: {selected_template} Template")
```

**Purpose:** Allow user to choose resume design

**Templates:**
- Modern: Colorful, contemporary design
- Professional: Traditional corporate look
- Minimal: Clean, simple layout
- Creative: Unique, artistic layout

---

### **6.3: Personal Information Section (Lines 580-615)**
```python
st.subheader("Personal Information")

col1, col2 = st.columns(2)
with col1:
    existing_name = st.session_state.form_data['personal_info']['full_name']
    existing_email = st.session_state.form_data['personal_info']['email']
    existing_phone = st.session_state.form_data['personal_info']['phone']

    full_name = st.text_input("Full Name", value=existing_name)
    email = st.text_input("Email", value=existing_email, key="email_input")
    phone = st.text_input("Phone", value=existing_phone)

with col2:
    existing_location = st.session_state.form_data['personal_info']['location']
    existing_linkedin = st.session_state.form_data['personal_info']['linkedin']
    existing_portfolio = st.session_state.form_data['personal_info']['portfolio']

    location = st.text_input("Location", value=existing_location)
    linkedin = st.text_input("LinkedIn URL", value=existing_linkedin)
    portfolio = st.text_input("Portfolio Website", value=existing_portfolio)

# Update session state
st.session_state.form_data['personal_info'] = {
    'full_name': full_name,
    'email': email,
    'phone': phone,
    'location': location,
    'linkedin': linkedin,
    'portfolio': portfolio
}
```

**Purpose:** Collect basic contact information

**Features:**
- 2-column layout (left and right)
- Retrieve existing values from session state
- Auto-update session state when user types
- Input validation via key mechanism

---

### **6.4: Professional Summary (Lines 622-625)**
```python
st.subheader("Professional Summary")
summary = st.text_area("Professional Summary", 
                       value=st.session_state.form_data.get('summary', ''), 
                       height=150,
                       help="Write a brief summary highlighting your key skills and experience")
```

**Purpose:** Collect professional summary/objective

**Features:**
- Large text area (150px height)
- Help text guides user
- Stores multi-line text

---

### **6.5: Experience Section (Lines 627-717)**
```python
st.subheader("Work Experience")
if 'experiences' not in st.session_state.form_data:
    st.session_state.form_data['experiences'] = []

if st.button("Add Experience"):
    st.session_state.form_data['experiences'].append({
        'company': '',
        'position': '',
        'start_date': '',
        'end_date': '',
        'description': '',
        'responsibilities': [],
        'achievements': []
    })

for idx, exp in enumerate(st.session_state.form_data['experiences']):
    with st.expander(f"Experience {idx + 1}", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            exp['company'] = st.text_input("Company Name", key=f"company_{idx}", 
                                          value=exp.get('company', ''))
            exp['position'] = st.text_input("Position", key=f"position_{idx}", 
                                           value=exp.get('position', ''))
        with col2:
            exp['start_date'] = st.text_input("Start Date", key=f"start_date_{idx}", 
                                             value=exp.get('start_date', ''))
            exp['end_date'] = st.text_input("End Date", key=f"end_date_{idx}", 
                                           value=exp.get('end_date', ''))

        exp['description'] = st.text_area("Role Overview", key=f"desc_{idx}",
                                        value=exp.get('description', ''),
                                        help="Brief overview of your role and impact")

        # Responsibilities
        st.markdown("##### Key Responsibilities")
        resp_text = st.text_area("Enter responsibilities (one per line)",
                               key=f"resp_{idx}",
                               value='\n'.join(exp.get('responsibilities', [])),
                               height=100)
        exp['responsibilities'] = [r.strip() for r in resp_text.split('\n') if r.strip()]

        # Achievements
        st.markdown("##### Key Achievements")
        achv_text = st.text_area("Enter achievements (one per line)",
                               key=f"achv_{idx}",
                               value='\n'.join(exp.get('achievements', [])),
                               height=100)
        exp['achievements'] = [a.strip() for a in achv_text.split('\n') if a.strip()]

        if st.button("Remove Experience", key=f"remove_exp_{idx}"):
            st.session_state.form_data['experiences'].pop(idx)
            st.rerun()
```

**Purpose:** Collect work experience details

**Features:**
- Dynamic add/remove experience entries
- Expandable sections (collapsible)
- Fields:
  - Company name
  - Job position
  - Dates (start/end)
  - Role description
  - Responsibilities (line-separated)
  - Achievements (line-separated)
- Unique keys prevent data conflicts

---

### **6.6: Projects Section (Lines 719-787)**
Similar to Experience, but for projects:
- Project name
- Technologies used
- Project description
- Responsibilities in project
- Achievements
- Project link (GitHub, demo, etc.)

---

### **6.7: Education Section (Lines 789-850)**
Collects education details:
- School/University name
- Degree type (Bachelor, Master, etc.)
- Field of study
- Graduation date
- GPA (optional)
- Achievements

---

## **SECTION 7: RESUME ANALYZER PAGE (Lines 1189-1500+)**

```python
def render_analyzer(self):
    """Render the resume analyzer page"""
    apply_modern_styles()

    # Page Header
    page_header(
        "Resume Analyzer",
        "Get instant AI-powered feedback to optimize your resume"
    )

    # Create tabs for Normal Analyzer and AI Analyzer
    analyzer_tabs = st.tabs(["Standard Analyzer", "AI Analyzer"])
```

**Purpose:** Main resume analysis interface

**Structure:**
- Apply custom styles
- Display page header
- Create 2 tabs: Standard & AI analyzer

### **7.1: Standard Analyzer Tab**
```python
with analyzer_tabs[0]:
    # Job Role Selection
    categories = list(self.job_roles.keys())
    selected_category = st.selectbox("Job Category", categories, 
                                     key="standard_category")

    roles = list(self.job_roles[selected_category].keys())
    selected_role = st.selectbox("Specific Role", roles, 
                                key="standard_role")

    role_info = self.job_roles[selected_category][selected_role]
```

**Process:**
1. Display categories (Backend, Frontend, etc.)
2. Show roles in selected category
3. Fetch role requirements (skills, description)

### **7.2: File Upload (Lines 1240-1280)**
```python
uploaded_file = st.file_uploader("Upload your resume", 
                                type=['pdf', 'docx'], 
                                key="standard_file")

if uploaded_file:
    analyze_standard = st.button("🔍 Analyze My Resume",
                        type="primary",
                        use_container_width=True,
                        key="analyze_standard_button")

    if analyze_standard:
        with st.spinner("Analyzing your document..."):
            # Extract text
            text = ""
            try:
                if uploaded_file.type == "application/pdf":
                    text = self.analyzer.extract_text_from_pdf(uploaded_file)
                else:
                    text = self.analyzer.extract_text_from_docx(uploaded_file)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                return
```

**Process:**
1. File uploader widget
2. "Analyze" button
3. Show spinner while processing
4. Extract text from file
5. Handle errors gracefully

### **7.3: Analysis & Display (Lines 1280-1350)**
```python
# Analyze the document
analysis = self.analyzer.analyze_resume({'raw_text': text}, role_info)

if 'error' in analysis:
    st.error(analysis['error'])
    return

# Show snowflake effect
st.snow()

# Save resume data to database
resume_data = {
    'personal_info': {...},
    'summary': analysis.get('summary', ''),
    'target_role': selected_role,
    # ... more fields
}

resume_id = save_resume_data(resume_data)
save_analysis_data({
    'resume_id': resume_id,
    'ats_score': analysis['ats_score'],
    'keyword_match_score': analysis['keyword_match']['score'],
    'format_score': analysis['format_score'],
})
```

**Process:**
1. Call analyzer
2. Check for errors
3. Visual feedback (snowflake animation)
4. Save resume to database
5. Save analysis scores
6. Display results to user

---

# **resume_analyzer.py - DETAILED BREAKDOWN**

---

## **SECTION 1: CLASS INITIALIZATION (Lines 1-26)**

```python
class ResumeAnalyzer:
    def __init__(self):
        # Document type indicators
        self.document_types = {
            'resume': [
                'experience', 'education', 'skills', 'work', 'project', 'objective',
                'summary', 'employment', 'qualification', 'achievements'
            ],
            'marksheet': [
                'grade', 'marks', 'score', 'semester', 'cgpa', 'sgpa', 'examination',
                'result', 'academic year', 'percentage'
            ],
            'certificate': [
                'certificate', 'certification', 'awarded', 'completed', 'achievement',
                'training', 'course completion', 'qualified'
            ],
            'id_card': [
                'id card', 'identity', 'student id', 'employee id', 'valid until',
                'date of issue', 'identification'
            ]
        }
```

**Purpose:** Define keywords to identify document types

**What it does:**
- Stores lists of keywords for each document type
- Later used to detect if uploaded file is actually a resume
- Prevents non-resume documents from being analyzed

---

## **SECTION 2: DOCUMENT TYPE DETECTION (Lines 28-43)**

```python
def detect_document_type(self, text):
    """Detect type of document (resume, marksheet, certificate, etc)"""
    text = text.lower()
    scores = {}
    
    # Calculate score for each document type
    for doc_type, keywords in self.document_types.items():
        matches = sum(1 for keyword in keywords if keyword in text)
        density = matches / len(keywords)  # How many keywords found / total keywords
        frequency = matches / (len(text.split()) + 1)  # How many keywords / total words
        scores[doc_type] = (density * 0.7) + (frequency * 0.3)  # Weighted score
    
    # Get the highest scoring document type
    best_match = max(scores.items(), key=lambda x: x[1])
    
    # Only return a document type if the score is significant
    return best_match[0] if best_match[1] > 0.15 else 'unknown'
```

**Purpose:** Identify document type from uploaded file

**Algorithm Explanation:**

1. **Convert to lowercase** - Normalize text
2. **For each doc type:**
   - Count keyword matches
   - Calculate density = matched keywords / total keywords
   - Calculate frequency = matched keywords / total words
   - Final score = (density × 70%) + (frequency × 30%)
     - Density weighted more (70%) = quality over quantity
     - Frequency weighted less (30%) = doesn't require huge document

3. **Find highest score** - Which document type has most evidence?
4. **Return if significant** - Only if score > 0.15 threshold

**Example:**
```
Resume document with text: "John Doe\nExperience:\n..."

Keywords found: 'experience', 'education', 'skills' = 3/10 resume keywords
Density = 3/10 = 0.30
Frequency = 3/(text.split()) = 3/50 = 0.06
Score = (0.30 × 0.7) + (0.06 × 0.3) = 0.21 + 0.018 = 0.228

Since 0.228 > 0.15 → Return "resume" ✓
```

---

## **SECTION 3: KEYWORD MATCHING (Lines 45-65)**

```python
def calculate_keyword_match(self, resume_text, required_skills):
    """Calculate how many required skills are in the resume"""
    resume_text = resume_text.lower()
    found_skills = []
    missing_skills = []
    
    for skill in required_skills:
        skill_lower = skill.lower()
        # Check for exact match
        if skill_lower in resume_text:
            found_skills.append(skill)
        # Check for partial matches
        elif any(skill_lower in phrase for phrase in resume_text.split('.')):
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
            
    match_score = (len(found_skills) / len(required_skills)) * 100 if required_skills else 0
    
    return {
        'score': match_score,
        'found_skills': found_skills,
        'missing_skills': missing_skills
    }
```

**Purpose:** Match resume skills against job requirements

**Process:**
1. Convert to lowercase (case-insensitive matching)
2. For each required skill:
   - Check exact word match in resume
   - Check partial match (in sentence)
   - If found → add to `found_skills`
   - If not → add to `missing_skills`
3. Calculate percentage match
4. Return score + lists

**Example:**
```
Required skills: [Python, Java, Docker, Kubernetes]
Resume text: "Python expert with Docker experience"

Checking:
- "python" in resume? YES → found_skills.append('Python')
- "java" in resume? NO → missing_skills.append('Java')
- "docker" in resume? YES → found_skills.append('Docker')
- "kubernetes" in resume? NO → missing_skills.append('Kubernetes')

Result: {
    'score': 50,  # (2/4) * 100
    'found_skills': ['Python', 'Docker'],
    'missing_skills': ['Java', 'Kubernetes']
}
```

---

## **SECTION 4: SECTION CHECKING (Lines 67-79)**

```python
def check_resume_sections(self, text):
    """Check if resume has all essential sections"""
    text = text.lower()
    essential_sections = {
        'contact': ['email', 'phone', 'address', 'linkedin'],
        'education': ['education', 'university', 'college', 'degree', 'academic'],
        'experience': ['experience', 'work', 'employment', 'job', 'internship'],
        'skills': ['skills', 'technologies', 'tools', 'proficiencies', 'expertise']
    }
    
    section_scores = {}
    for section, keywords in essential_sections.items():
        found = sum(1 for keyword in keywords if keyword in text)
        # Score = (found keywords / total keywords) * 25
        # Each section worth max 25 points (4 sections × 25 = 100 total)
        section_scores[section] = min(25, (found / len(keywords)) * 25)
        
    return sum(section_scores.values())
```

**Purpose:** Check if resume has all required sections

**Scoring:**
- Each section = max 25 points
- 4 sections × 25 = 100 total
- Score = (found keywords / total keywords) × 25

**Example:**
```
Resume text: "John Doe\nemail@example.com\n...\nEducation: BSc IT\n..."

Contact section:
- Keywords: ['email', 'phone', 'address', 'linkedin']
- Found: 'email' ✓
- Score: (1/4) × 25 = 6.25

Education section:
- Keywords: ['education', 'university', 'college', 'degree', 'academic']
- Found: 'education', 'bsc'(matches degree?)
- Score: (2/5) × 25 = 10

Total score = 6.25 + 10 + ... = (out of 100)
```

---

## **SECTION 5: FORMAT CHECKING (Lines 81-120)**

```python
def check_formatting(self, text):
    """Check resume formatting quality"""
    lines = text.split('\n')
    score = 100
    deductions = []
    
    # Check for minimum content
    if len(text) < 300:
        score -= 30
        deductions.append("Resume is too short")
        
    # Check for section headers
    if not any(line.isupper() for line in lines):
        score -= 20
        deductions.append("No clear section headers found")
        
    # Check for bullet points
    if not any(line.strip().startswith(('•', '-', '*', '→')) for line in lines):
        score -= 20
        deductions.append("No bullet points found for listing details")
        
    # Check contact information format
    contact_patterns = [
        r'\b[\w\.-]+@[\w\.-]+\.\w+\b',  # email format
        r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # phone format
        r'linkedin\.com/\w+',  # LinkedIn URL
    ]
    if not any(re.search(pattern, text) for pattern in contact_patterns):
        score -= 15
        deductions.append("Missing or improperly formatted contact information")
        
    return max(0, score), deductions
```

**Purpose:** Check resume formatting quality

**Checks Performed:**
| Check | Deduction | Reason |
|-------|-----------|--------|
| Length < 300 chars | -30 | Too brief |
| No uppercase headers | -20 | No clear sections |
| No bullet points | -20 | Unorganized |
| No contact info | -15 | Can't contact candidate |

**Example:**
```
Resume: "John Doe Software Developer..."  (200 chars)

Checks:
- Length: 200 < 300 → score -= 30 (70 points)
- Headers: "EXPERIENCE" found (uppercase) → no deduction ✓
- Bullets: "• Python programming" found → no deduction ✓
- Contact: email found → no deduction ✓

Final score: 70/100
```

---

## **SECTION 6: PDF TEXT EXTRACTION (Lines 122-145)**

```python
def extract_text_from_pdf(self, file):
    """Extract text from PDF file"""
    try:
        import PyPDF2
        import io
        
        # Get file content as bytes
        if hasattr(file, 'read'):
            file_content = file.read()
            file.seek(0)  # Reset file pointer
        else:
            file_content = file
            
        # Create BytesIO from bytes content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
            
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")
```

**Purpose:** Extract text from PDF files

**Process:**
1. Import PyPDF2 library
2. Convert uploaded file to bytes
3. Create PDF reader object
4. Loop through each page
5. Extract text from each page
6. Concatenate all text
7. Return combined text

---

## **SECTION 7: DOCX TEXT EXTRACTION (Lines 147-154)**

```python
def extract_text_from_docx(self, docx_file):
    """Extract text from a DOCX file"""
    try:
        from docx import Document
        doc = Document(docx_file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        raise Exception(f"Error extracting text from DOCX file: {str(e)}")
```

**Purpose:** Extract text from DOCX files

**Process:**
1. Import python-docx
2. Load document
3. Iterate through paragraphs
4. Extract text from each paragraph
5. Join with newlines
6. Return combined text

---

## **SECTION 8: PERSONAL INFO EXTRACTION (Lines 156-178)**

```python
def extract_personal_info(self, text):
    """Extract personal information from resume text"""
    # Regex patterns
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'(\+\d{1,3}[-.]?)?\s*\(?\d{3}\)?[-.]?\s*\d{3}[-.]?\s*\d{4}'
    linkedin_pattern = r'linkedin\.com/in/[\w-]+'
    github_pattern = r'github\.com/[\w-]+'
    
    # Extract information
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    linkedin = re.search(linkedin_pattern, text)
    github = re.search(github_pattern, text)
    
    # Get the first line as name
    name = text.split('\n')[0].strip()
    
    return {
        'name': name if len(name) > 0 else 'Unknown',
        'email': email.group(0) if email else '',
        'phone': phone.group(0) if phone else '',
        'linkedin': linkedin.group(0) if linkedin else '',
        'github': github.group(0) if github else '',
        'portfolio': ''
    }
```

**Purpose:** Extract contact information

**Regex Patterns:**
| Pattern | Matches | Example |
|---------|---------|---------|
| Email | `word@domain.com` | `john@example.com` |
| Phone | `(123) 456-7890` | Various formats |
| LinkedIn | `linkedin.com/in/username` | `linkedin.com/in/johndoe` |
| GitHub | `github.com/username` | `github.com/johndoe` |

---

## **SECTION 9-14: EXTRACT SECTIONS**

### **SECTION 9: Extract Education (Lines 180-224)**

```python
def extract_education(self, text):
    """Extract education information from resume text"""
    education = []
    lines = text.split('\n')
    education_keywords = [
        'education', 'academic', 'qualification', 'degree', 'university', 'college',
        'school', 'institute', 'certification', 'diploma', 'bachelor', 'master',
        'phd', 'b.tech', 'm.tech', 'b.e', 'm.e', 'b.sc', 'm.sc','bca', 'mca', 'b.com',
        'm.com', 'b.cs-it', 'imca', 'bba', 'mba', 'honors', 'scholarship'
    ]
    in_education_section = False
    current_entry = []

    for line in lines:
        line = line.strip()
        # Check for section header
        if any(keyword.lower() in line.lower() for keyword in education_keywords):
            if not any(keyword.lower() == line.lower() for keyword in education_keywords):
                current_entry.append(line)
            in_education_section = True
            continue
        
        if in_education_section:
            # Check if we've hit another section
            if line and any(keyword.lower() in line.lower() for keyword in self.document_types['resume']):
                if not any(edu_key.lower() in line.lower() for edu_key in education_keywords):
                    in_education_section = False
                    if current_entry:
                        education.append(' '.join(current_entry))
                        current_entry = []
                    continue
            
            if line:
                current_entry.append(line)
            elif current_entry:
                education.append(' '.join(current_entry))
                current_entry = []
    
    if current_entry:
        education.append(' '.join(current_entry))
    
    return education
```

**Purpose:** Extract education section from resume

**Algorithm:**
1. Split text into lines
2. Look for education keywords
3. When found, mark section as active
4. Collect lines until next section
5. Stop when hitting another section keyword
6. Return list of education entries

---

### **SECTIONS 10-14: Extract Other Sections**

Similar patterns for:
- **Experience** (lines 226-267)
- **Projects** (lines 269-310)
- **Skills** (lines 312-365)
- **Summary** (lines 367-436)

Each follows the same algorithm:
1. Define keywords for section
2. Find section header
3. Collect content until next section
4. Return list/string of extracted data

---

## **SECTION 15: FULL RESUME ANALYSIS (Lines 438-615)**

```python
def analyze_resume(self, resume_data, job_requirements):
    """Analyze resume and return scores and recommendations"""
    try:
        text = resume_data.get('raw_text', '')
        
        # Extract personal information
        personal_info = self.extract_personal_info(text)
        
        # Detect document type
        doc_type = self.detect_document_type(text)
        if doc_type != 'resume':
            return {
                'ats_score': 0,
                'document_type': doc_type,
                'error': f"This appears to be a {doc_type}. Please upload a resume."
            }
            
        # Calculate keyword match
        required_skills = job_requirements.get('required_skills', [])
        keyword_match = self.calculate_keyword_match(text, required_skills)
        
        # Extract all sections
        education = self.extract_education(text)
        experience = self.extract_experience(text)
        projects = self.extract_projects(text)
        skills = list(self.extract_skills(text))
        summary = self.extract_summary(text)
        
        # Check resume sections
        section_score = self.check_resume_sections(text)
        
        # Check formatting
        format_score, format_deductions = self.check_formatting(text)
        
        # Generate recommendations
        # ... (lines 550+)
        
        # Calculate ATS score
        ats_score = (
            keyword_match['score'] * 0.4 +
            section_score * 0.3 +
            format_score * 0.3
        )
        
        return {
            'ats_score': ats_score,
            'keyword_match': keyword_match,
            'section_score': section_score,
            'format_score': format_score,
            'name': personal_info['name'],
            'email': personal_info['email'],
            'phone': personal_info['phone'],
            'linkedin': personal_info['linkedin'],
            'github': personal_info['github'],
            'education': education,
            'experience': experience,
            'projects': projects,
            'skills': skills,
            'summary': summary,
            'suggestions': suggestions
        }
    except Exception as e:
        return {'error': str(e)}
```

**Purpose:** Master analysis function that orchestrates everything

**Process:**
1. Extract raw text
2. Get personal info
3. Verify it's a resume
4. Calculate keyword match (40% weight)
5. Check sections (30% weight)
6. Check formatting (30% weight)
7. Extract all sections
8. Generate recommendations
9. Calculate final ATS score
10. Return comprehensive analysis

**ATS Score Calculation:**
```
ATS = (keyword_score × 0.4) + (section_score × 0.3) + (format_score × 0.3)

Example:
- Keyword match: 70 → 70 × 0.4 = 28
- Section score: 80 → 80 × 0.3 = 24
- Format score: 75 → 75 × 0.3 = 22.5
- Total ATS = 28 + 24 + 22.5 = 74.5 out of 100
```

---

## **SUMMARY TABLE: All Methods**

| Method | Purpose | Input | Output |
|--------|---------|-------|--------|
| `__init__` | Setup keywords | None | None |
| `detect_document_type` | Identify doc type | text | "resume"/"marksheet"/etc |
| `calculate_keyword_match` | Match skills | text, skills[] | {score, found[], missing[]} |
| `check_resume_sections` | Verify sections | text | score (0-100) |
| `check_formatting` | Check formatting | text | (score, deductions[]) |
| `extract_text_from_pdf` | Read PDF | file | text |
| `extract_text_from_docx` | Read DOCX | file | text |
| `extract_personal_info` | Get contact | text | {name, email, phone, ...} |
| `extract_education` | Get education | text | [edu1, edu2, ...] |
| `extract_experience` | Get jobs | text | [exp1, exp2, ...] |
| `extract_projects` | Get projects | text | [proj1, proj2, ...] |
| `extract_skills` | Get skills | text | [skill1, skill2, ...] |
| `extract_summary` | Get summary | text | "summary text" |
| `analyze_resume` | Full analysis | text, job_req | {ats_score, details, ...} |

---

This document explains every major section of both files with code examples and detailed breakdowns!
