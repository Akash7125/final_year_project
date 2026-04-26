# Smart AI Resume Analyzer - Code Flow Explanation

## 📋 Complete Flow: Input → Processing → Output

---

## **PART 1: APPLICATION INITIALIZATION (app.py Lines 1-125)**

### Step 1: Start Application
```python
# app.py - Lines 1-50
st.set_page_config(page_title="SkillMatch", page_icon="🚀", layout="wide")

class ResumeApp:
    def __init__(self):
        # Initialize session state variables
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {...}
```

**What happens:**
- Streamlit framework initializes the web application
- Session state is created to store user data across page refreshes
- Form data structure is set up with empty values for personal info, experience, etc.

---

## **PART 2: RESUME UPLOAD & TEXT EXTRACTION (app.py Lines 1189-1300)**

### Step 2: User Uploads Resume
```python
# app.py - Line 1214
uploaded_file = st.file_uploader("Upload your resume", type=['pdf', 'docx'])

if uploaded_file:
    analyze_standard = st.button("🔍 Analyze My Resume", type="primary")
    
    if analyze_standard:
        with st.spinner("Analyzing your document..."):
```

**What happens:**
- User selects PDF or DOCX file
- File is stored in `uploaded_file` variable
- User clicks "Analyze" button to trigger analysis

### Step 3: Extract Text from Resume
```python
# app.py - Lines 1240-1260
if uploaded_file.type == "application/pdf":
    text = self.analyzer.extract_text_from_pdf(uploaded_file)
    
elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
    text = self.analyzer.extract_text_from_docx(uploaded_file)
```

**Processing Details (ai_resume_analyzer.py Lines 17-85):**

```python
def extract_text_from_pdf(self, pdf_file):
    # Step 1: Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(pdf_file.getbuffer())
        temp_path = temp_file.name
    
    # Step 2: Try pdfplumber extraction first
    try:
        with pdfplumber.open(temp_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()  # Extract text per page
                if page_text:
                    text += page_text + "\n"
    
    # Step 3: If pdfplumber fails, use PyPDF2 as fallback
    if text.strip():
        return text.strip()
    
    # Step 4: If still no text, try OCR (Tesseract)
    try:
        images = convert_from_path(temp_path)
        for image in images:
            text += pytesseract.image_to_string(image)
    
    # Step 5: Clean up temporary file
    os.unlink(temp_path)
    return text
```

**Output:** Raw text string containing all resume content

---

## **PART 3: DOCUMENT TYPE DETECTION (resume_analyzer.py Lines 10-37)**

```python
# resume_analyzer.py - Lines 10-37
def detect_document_type(self, text):
    text = text.lower()
    scores = {}
    
    # Check against resume keywords
    resume_keywords = ['experience', 'education', 'skills', 'work', 'project', etc.]
    
    # Calculate score: (density * 0.7) + (frequency * 0.3)
    # density = matched_keywords / total_keywords
    # frequency = matched_keywords / total_words_in_text
    
    matches = sum(1 for keyword in resume_keywords if keyword in text)
    density = matches / len(resume_keywords)
    frequency = matches / (len(text.split()) + 1)
    scores['resume'] = (density * 0.7) + (frequency * 0.3)
    
    # Return highest scoring document type if score > 0.15
    best_match = max(scores.items(), key=lambda x: x[1])
    return best_match[0] if best_match[1] > 0.15 else 'unknown'
```

**Output:** Document type (e.g., "resume", "marksheet", "certificate")

---

## **PART 4: STANDARD RESUME ANALYSIS (resume_analyzer.py)**

### Step 4A: Check Resume Sections
```python
# resume_analyzer.py - Lines 55-75
def check_resume_sections(self, text):
    text = text.lower()
    
    essential_sections = {
        'contact': ['email', 'phone', 'address', 'linkedin'],
        'education': ['education', 'university', 'college', 'degree'],
        'experience': ['experience', 'work', 'employment', 'job'],
        'skills': ['skills', 'technologies', 'tools', 'proficiencies']
    }
    
    section_scores = {}
    for section, keywords in essential_sections.items():
        found = sum(1 for keyword in keywords if keyword in text)
        # Score = (found keywords / total keywords) * 25
        section_scores[section] = min(25, (found / len(keywords)) * 25)
    
    return sum(section_scores.values())  # Total out of 100
```

**Output:** Section score (0-100)

### Step 4B: Keyword Matching
```python
# resume_analyzer.py - Lines 38-54
def calculate_keyword_match(self, resume_text, required_skills):
    found_skills = []
    missing_skills = []
    
    for skill in required_skills:
        # Exact match
        if skill.lower() in resume_text.lower():
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    # Score = (found skills / total required skills) * 100
    match_score = (len(found_skills) / len(required_skills)) * 100
    
    return {
        'score': match_score,
        'found_skills': found_skills,
        'missing_skills': missing_skills
    }
```

**Output:** 
- Skill match score (0-100)
- List of found skills
- List of missing skills

### Step 4C: Full Resume Analysis
```python
# app.py - Line 1270
analysis = self.analyzer.analyze_resume({'raw_text': text}, role_info)
```

**Returns:**
```python
{
    'ats_score': 75,
    'keyword_match': {
        'score': 60,
        'found_skills': ['Python', 'SQL'],
        'missing_skills': ['Kubernetes', 'AWS']
    },
    'format_score': 85,
    'section_coverage': {'contact': 25, 'education': 25, ...},
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890',
    'education': [...],
    'experience': [...],
    'projects': [...],
    'skills': [...]
}
```

---

## **PART 5: DATABASE STORAGE (app.py Lines 1283-1310)**

```python
# app.py - Lines 1283-1310
resume_data = {
    'personal_info': {
        'name': analysis.get('name', ''),
        'email': analysis.get('email', ''),
        'phone': analysis.get('phone', ''),
        'linkedin': analysis.get('linkedin', ''),
    },
    'target_role': selected_role,
    'skills': analysis.get('skills', []),
    # ... more data
}

# Save to SQLite database
resume_id = save_resume_data(resume_data)

# Save analysis results
analysis_data = {
    'resume_id': resume_id,
    'ats_score': analysis['ats_score'],
    'keyword_match_score': analysis['keyword_match']['score'],
    'format_score': analysis['format_score'],
}
save_analysis_data(analysis_data)
```

**Database Tables:**
- `resumes`: Stores resume content
- `analysis_results`: Stores analysis scores
- Indexed by resume_id for fast lookups

---

## **PART 6: OUTPUT DISPLAY (app.py Lines 1320+)**

### Step 6A: Display ATS Score
```python
# Score visualization
st.metric("ATS Compatibility Score", "75/100", delta="Good")

# Score breakdown
col1, col2, col3 = st.columns(3)
col1.metric("Keyword Match", "60%")
col2.metric("Format Score", "85%")
col3.metric("Section Coverage", "80%")
```

### Step 6B: Display Missing Skills
```python
st.subheader("🔴 Skills Gap Analysis")
missing = analysis['keyword_match']['missing_skills']

for skill in missing:
    st.warning(f"❌ Missing: {skill}")
    
# Interactive visualization
st.plotly_chart(
    px.bar(
        x=missing,
        y=[1]*len(missing),
        title="Missing Technical Skills"
    )
)
```

### Step 6C: Display Recommendations
```python
st.subheader("💡 AI-Generated Recommendations")
recommendations = generate_recommendations(analysis)

for i, rec in enumerate(recommendations, 1):
    st.info(f"{i}. {rec}")
    # Example: "Add 'Docker' to your project descriptions"
    # Example: "Improve ATS formatting by using standard section headers"
```

### Step 6D: Export Options
```python
# Generate PDF report
pdf_bytes = generate_pdf_report(analysis)

st.download_button(
    label="📥 Download PDF Report",
    data=pdf_bytes,
    file_name="resume_analysis_report.pdf",
    mime="application/pdf"
)
```

---

## **PART 7: AI ANALYZER FLOW (Optional Tab)**

### Step 7A: Custom Job Description Input
```python
# app.py - AI Analyzer Tab
job_description = st.text_area(
    "Enter Job Description",
    height=200
)

if st.button("🤖 Analyze with AI"):
```

### Step 7B: Call Gemini API (ai_resume_analyzer.py)
```python
def analyze_with_ai(self, resume_text, job_description):
    # Configure Google Gemini
    genai.configure(api_key=self.google_api_key)
    
    # Create detailed prompt
    prompt = f"""
    Analyze this resume against the job description:
    
    RESUME:
    {resume_text}
    
    JOB DESCRIPTION:
    {job_description}
    
    Provide:
    1. Overall match score (0-100)
    2. Matching skills
    3. Missing skills
    4. Improvement suggestions
    """
    
    # Call Gemini API
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    # Parse response (JSON format from API)
    analysis = json.loads(response.text)
    
    return analysis
```

### Step 7C: Process AI Response
```python
analysis = {
    'match_score': 78,
    'matching_skills': ['Python', 'SQL', 'Git'],
    'missing_skills': ['Kubernetes', 'Docker', 'AWS'],
    'strengths': [
        'Strong Python background',
        'Good database design skills'
    ],
    'weaknesses': [
        'Limited cloud platform experience',
        'No containerization experience'
    ],
    'improvement_suggestions': [
        'Take an AWS certification course',
        'Build 1-2 projects using Docker',
        'Learn Kubernetes basics'
    ]
}
```

### Step 7D: Display AI Results
```python
st.metric("AI Match Score", f"{analysis['match_score']}/100")

col1, col2 = st.columns(2)
with col1:
    st.subheader("✅ Strengths")
    for strength in analysis['strengths']:
        st.success(strength)

with col2:
    st.subheader("⚠️ Gaps")
    for gap in analysis['missing_skills']:
        st.warning(gap)

st.subheader("📚 Recommendations")
for i, rec in enumerate(analysis['improvement_suggestions'], 1):
    st.info(f"{i}. {rec}")
```

---

## **PART 8: DASHBOARD & ANALYTICS (app.py - render_dashboard)**

```python
# Track statistics across all analyses
analytics_data = {
    'total_analyses': 150,
    'average_ats_score': 72,
    'score_distribution': {
        '90-100': 25,
        '80-89': 45,
        '70-79': 55,
        '60-69': 20,
        '< 60': 5
    }
}

# Display as pie chart
st.plotly_chart(
    px.pie(
        labels=list(analytics_data['score_distribution'].keys()),
        values=list(analytics_data['score_distribution'].values()),
        title="Resume Score Distribution"
    )
)
```

---

## **COMPLETE DATA FLOW DIAGRAM**

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INPUT PHASE                            │
├─────────────────────────────────────────────────────────────────┤
│ 1. User uploads PDF/DOCX resume file                            │
│ 2. User selects job role (category + specific role)             │
│ 3. (Optional) User enters custom job description                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   TEXT EXTRACTION PHASE                         │
├─────────────────────────────────────────────────────────────────┤
│ extract_text_from_pdf() OR extract_text_from_docx()            │
│   → pdfplumber / python-docx                                   │
│   → If fails: PyPDF2 (fallback)                                │
│   → If fails: Tesseract OCR                                    │
│ Output: Plain text string                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  DOCUMENT TYPE CHECK                            │
├─────────────────────────────────────────────────────────────────┤
│ detect_document_type(text)                                      │
│   → Check if it's actually a resume or other document          │
│ Output: Document type (resume/marksheet/certificate/id)        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                 STANDARD ANALYZER PATH                          │
├─────────────────────────────────────────────────────────────────┤
│ analyze_resume(text, role_info)                                │
│   ├─ check_resume_sections() → Score 0-100                    │
│   │   └─ Check for: contact, education, experience, skills    │
│   ├─ calculate_keyword_match() → Score 0-100                  │
│   │   └─ Match required_skills against resume text            │
│   ├─ calculate_ats_score() → Score 0-100                      │
│   │   └─ Check formatting, keywords, layout                   │
│   └─ extract_sections() → Parse structured data               │
│       └─ name, email, phone, education[], experience[]        │
│ Output: Complete analysis object                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓ (Optional)
┌─────────────────────────────────────────────────────────────────┐
│                   AI ANALYZER PATH                              │
├─────────────────────────────────────────────────────────────────┤
│ analyze_with_ai(resume_text, job_description)                  │
│   ├─ Configure Gemini API                                      │
│   ├─ Create detailed prompt with resume + JD                  │
│   ├─ Call genai.GenerativeModel('gemini-pro')                 │
│   └─ Parse JSON response                                       │
│ Output: AI-enhanced analysis with insights                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  DATABASE STORAGE PHASE                         │
├─────────────────────────────────────────────────────────────────┤
│ save_resume_data() → SQLite 'resumes' table                    │
│ save_analysis_data() → SQLite 'analysis_results' table         │
│ Log timestamps and user information                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   OUTPUT DISPLAY PHASE                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. ATS Score Cards (metric display)                             │
│ 2. Skill Analysis (found vs missing)                            │
│ 3. Section Coverage (pie/bar charts)                            │
│ 4. Recommendations (AI-generated text)                          │
│ 5. PDF Report Download                                         │
│ 6. Course Recommendations (Udemy/YouTube links)                │
│ 7. Job Openings (LinkedIn search results)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  DASHBOARD ANALYTICS                            │
├─────────────────────────────────────────────────────────────────┤
│ Display aggregate statistics from all analyses:                │
│   • Total resumes analyzed                                      │
│   • Average ATS score                                           │
│   • Score distribution (pie chart)                              │
│   • Most common missing skills                                  │
│   • Top recommended courses                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## **KEY PROCESSING FUNCTIONS & LINE NUMBERS**

| Function | File | Lines | Purpose |
|----------|------|-------|---------|
| `__init__` | app.py | 41-125 | Initialize app, session state |
| `extract_text_from_pdf` | ai_resume_analyzer.py | 17-85 | Extract text from PDF |
| `extract_text_from_docx` | ai_resume_analyzer.py | 130-160 | Extract text from DOCX |
| `detect_document_type` | resume_analyzer.py | 10-37 | Verify it's a resume |
| `check_resume_sections` | resume_analyzer.py | 55-75 | Check required sections |
| `calculate_keyword_match` | resume_analyzer.py | 38-54 | Match skills |
| `analyze_resume` | resume_analyzer.py | 76-150+ | Full analysis logic |
| `analyze_with_ai` | ai_resume_analyzer.py | 200-500+ | AI analysis via Gemini |
| `save_resume_data` | config/database.py | ? | Save to SQLite |
| `render_analyzer` | app.py | 1189-1350 | Display analyzer UI |

---

## **EXAMPLE: Complete Single Analysis (Start to End)**

```
INPUT: User uploads "my_resume.pdf" and selects "Python Developer" role

STEP 1: Extract Text
  → pdfplumber opens my_resume.pdf
  → Reads 2 pages
  → Extracts raw text: "John Doe\nPython Developer\nEmail: john@...\"

STEP 2: Detect Type
  → Find keywords: 'experience' (10x), 'skills' (8x), 'education' (5x)
  → Score: 0.65 → Document type = 'resume' ✓

STEP 3: Standard Analysis
  → Sections found: contact ✓, education ✓, experience ✓, skills ✓
  → Section score: 100/100
  
  → Required skills: [Python, Flask, PostgreSQL, Git, Docker, AWS]
  → Found: [Python, Flask, PostgreSQL, Git]
  → Missing: [Docker, AWS]
  → Keyword match: 66.7%
  
  → Format check: Good ATS formatting
  → Format score: 85/100
  
  → Final ATS: 83/100 ✓

STEP 4: Save to DB
  → INSERT into resumes table
  → INSERT into analysis_results table
  → resume_id = 42 (returned)

STEP 5: Display Results
  ┌─ ATS Score: 83/100
  │
  ├─ Found Skills: Python, Flask, PostgreSQL, Git
  │
  ├─ Missing Skills: Docker, AWS
  │
  ├─ Recommendations:
  │  1. Add Docker projects to demonstrate containerization
  │  2. Include AWS certification or project experience
  │  3. Mention Flask production deployment experience
  │
  ├─ Suggested Courses:
  │  • Docker Mastery (Udemy) - 4.8★
  │  • AWS for Developers (YouTube) - 9K views
  │
  └─ Download PDF Report

OUTPUT: Complete analysis displayed in Streamlit UI + PDF downloadable
```

---

This comprehensive flow ensures that from the moment a user uploads their resume to seeing detailed analysis and recommendations, every step is tracked, processed, and displayed efficiently.
