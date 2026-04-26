# Resume Analytics Analyzer.py - Complete Line-by-Line Explanation

## Overview
This analyzer uses **spaCy** (natural language processing library) to analyze resumes and extract metrics like word count, skills, experience years, and generate improvement suggestions.

---

## Import Statements (Lines 1-3)

### Line 1: `import spacy`
**Purpose:** Import spaCy NLP library
**Details:** 
- spaCy is a Python NLP library for advanced text processing
- Used for tokenization, sentence segmentation, linguistic features
- More sophisticated than regex-based approaches

```python
import spacy
```

**What spaCy does:**
- `spacy.load()`: Loads pre-trained language models
- Tokenization: Splits text into words/tokens
- Sentence segmentation: Identifies sentence boundaries
- POS tagging: Identifies parts of speech
- Entity recognition: Identifies named entities (people, organizations, dates)
- Token features: `token.like_num`, `token.text`, `token.i` provide linguistic info

---

### Line 2: `from collections import Counter`
**Purpose:** Import Counter for frequency analysis
**Details:**
- Not used in current code but imported for potential future use
- `Counter` counts frequency of items in a list
- Useful for skill frequency analysis

```python
from collections import Counter
```

**Example usage (not in current code):**
```python
skills_list = ["Python", "Python", "Java", "Python"]
Counter(skills_list)  # Returns: Counter({'Python': 3, 'Java': 1})
```

---

### Line 3: `from datetime import datetime`
**Purpose:** Import datetime for timestamps
**Details:**
- Used to create timestamp when analysis is performed
- `datetime.now()` gets current date/time
- `.isoformat()` converts to ISO 8601 format string

```python
from datetime import datetime
```

**Example:**
```python
datetime.now().isoformat()  # Returns: "2026-03-04T15:30:45.123456"
```

---

## Class Definition (Line 5)

```python
class ResumeAnalyzer:
```

**Purpose:** Main class for NLP-based resume analysis
**Scope:** Contains all methods for analyzing resume text
**Design:** Single-responsibility class focusing on text metrics and suggestions

---

## Constructor Method (Lines 6-7)

```python
def __init__(self):
    self.nlp = spacy.load("en_core_web_sm")
```

### Purpose
Initialize the analyzer with spaCy language model

### Line 6: `def __init__(self):`
- Constructor method runs when creating new ResumeAnalyzer instance
- `self` refers to the instance object

### Line 7: `self.nlp = spacy.load("en_core_web_sm")`
**Purpose:** Load spaCy's English language model
**Model: "en_core_web_sm"**
- `en`: English language
- `core`: Full pipeline (tokenization, POS tagging, dependency parsing)
- `web`: Trained on web text (general English)
- `sm`: Small model (efficient, smaller memory footprint)

**What the model includes:**
```
Tokenizer      → Splits text into words
Tagger         → Labels parts of speech (noun, verb, etc.)
Parser         → Analyzes sentence structure
NER            → Recognizes named entities
Vectors        → Word embeddings for semantic similarity
```

**Instance variable storage:**
- `self.nlp` stores the model for use in other methods
- Makes model available to entire class instance

**Usage in other methods:**
```python
doc = self.nlp(resume_text)  # Process text with loaded model
```

---

## Main Analysis Method (Lines 9-40)

```python
def analyze_resume(self, resume_text):
    """Analyze resume text and return metrics"""
```

### Purpose
Main entry point for resume analysis. Orchestrates all analysis methods.

### Line 9: Method Signature
```python
def analyze_resume(self, resume_text):
```
- **Parameters:**
  - `self`: Instance reference
  - `resume_text`: Raw resume text as string
- **Returns:** Dictionary with metrics, skills, and suggestions

### Line 11-12: Process text with spaCy
```python
doc = self.nlp(resume_text)

# Basic metrics
word_count = len(resume_text.split())
sentence_count = len(list(doc.sents))
```

**Line 11 Analysis:**
```python
doc = self.nlp(resume_text)
```
- Processes resume_text through spaCy pipeline
- `doc` is a spaCy `Doc` object (processed document)
- Contains tokenized text, sentences, linguistic features

**What happens internally:**
1. **Tokenization:** "Hello world" → ["Hello", "world"]
2. **POS Tagging:** Identifies word types (noun, verb, adjective)
3. **Sentence Segmentation:** Finds sentence boundaries
4. **Entity Recognition:** Identifies names, organizations, dates

**Line 13: Word Count**
```python
word_count = len(resume_text.split())
```
- `split()`: Splits text by whitespace (default separator)
- Default splits by spaces, tabs, newlines
- Returns list of words
- `len()`: Counts total words

**Example:**
```python
"Python Java SQL".split()  # ["Python", "Java", "SQL"]
len(["Python", "Java", "SQL"])  # 3
```

**Limitation:** Splits on whitespace, doesn't handle punctuation specially
- "Hello," and "Hello" counted separately by spaCy tokens

**Line 14: Sentence Count**
```python
sentence_count = len(list(doc.sents))
```

**Breakdown:**
- `doc.sents`: spaCy's sentence generator (iterator)
- `list()`: Converts iterator to list
- `len()`: Counts sentences

**How spaCy identifies sentences:**
- Trained on language patterns
- Recognizes sentence endings (periods, exclamation marks, question marks)
- Handles edge cases (abbreviations, decimals)

**Example:**
```python
resume_text = "I have 5 years experience. I know Python and Java."
doc = nlp(resume_text)
len(list(doc.sents))  # 2 (two sentences detected)
```

### Lines 16-17: Extract Skills
```python
# Skills extraction
skills = self._extract_skills(doc)
```
- Calls `_extract_skills()` method (defined later)
- Passes spaCy `doc` object
- Returns set of extracted skills
- `#` is a comment explaining the step

### Lines 19-20: Analyze Experience
```python
# Experience analysis
experience_years = self._analyze_experience(doc)
```
- Calls `_analyze_experience()` method
- Returns maximum years of experience found
- Returns 0 if no experience detected

### Lines 22-26: Calculate Score
```python
# Calculate profile score
profile_score = self._calculate_profile_score(
    word_count, sentence_count, len(skills), experience_years
)
```
- Calls `_calculate_profile_score()` method
- Passes all extracted metrics
- Returns score 0-100

**Parameters passed:**
- `word_count`: Total words in resume
- `sentence_count`: Number of sentences
- `len(skills)`: Number of unique skills found
- `experience_years`: Years of experience

### Lines 28-38: Return Results Dictionary
```python
return {
    "timestamp": datetime.now().isoformat(),
    "metrics": {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "skills_count": len(skills),
        "experience_years": experience_years,
        "profile_score": profile_score
    },
    "skills": list(skills),
    "suggestions": self._generate_suggestions(
        word_count, sentence_count, skills, experience_years
    )
}
```

**Return dictionary structure:**

```json
{
  "timestamp": "2026-03-04T15:30:45.123456",
  "metrics": {
    "word_count": 450,
    "sentence_count": 15,
    "skills_count": 8,
    "experience_years": 5,
    "profile_score": 85
  },
  "skills": ["Python", "Java", "AWS", ...],
  "suggestions": [
    {"icon": "fa-code", "text": "Add more skills..."},
    ...
  ]
}
```

**Line-by-line breakdown:**

**Line 29: Timestamp**
```python
"timestamp": datetime.now().isoformat()
```
- `datetime.now()`: Current date/time object
- `.isoformat()`: Converts to ISO 8601 string format
- Example: "2026-03-04T15:30:45.123456"
- Useful for tracking when analysis was performed

**Lines 30-37: Metrics Subdictionary**
```python
"metrics": {
    "word_count": word_count,
    "sentence_count": sentence_count,
    "skills_count": len(skills),
    "experience_years": experience_years,
    "profile_score": profile_score
}
```
- Organizes all quantitative metrics
- `skills_count`: Number of unique skills (len() of set)
- Provides summary statistics

**Line 38: Skills List**
```python
"skills": list(skills)
```
- Converts `skills` (which is a set) to a list
- Sets are unordered; list makes it serializable/printable
- Makes skills easily accessible to caller

**Lines 39-42: Suggestions**
```python
"suggestions": self._generate_suggestions(
    word_count, sentence_count, skills, experience_years
)
```
- Calls method to generate improvement suggestions
- Based on extracted metrics
- Returns list of suggestion dictionaries

---

## Skills Extraction Method (Lines 44-61)

```python
def _extract_skills(self, doc):
    """Extract skills from resume"""
    # Common technical skills keywords
    tech_skills = {
        "python", "java", "javascript", "react", "node.js", "sql",
        "html", "css", "aws", "docker", "kubernetes", "git",
        "machine learning", "ai", "data science", "analytics"
    }
```

### Purpose
Extract technical skills from resume text using keyword matching

### Line 44: Method Definition
```python
def _extract_skills(self, doc):
```
- `_extract_skills`: Underscore prefix indicates "private" method (convention)
- Takes spaCy `doc` object as parameter
- Returns set of skills found

### Lines 46-52: Tech Skills Set
```python
tech_skills = {
    "python", "java", "javascript", "react", "node.js", "sql",
    "html", "css", "aws", "docker", "kubernetes", "git",
    "machine learning", "ai", "data science", "analytics"
}
```

**Data Structure:** Python set `{}`
- Unordered collection of unique values
- Fast lookup: O(1) time complexity
- Prevents duplicate skills

**Skills Included:**
- **Programming Languages:** python, java, javascript
- **Frontend:** react, html, css
- **Backend:** node.js, sql
- **DevOps:** aws, docker, kubernetes, git
- **Data/AI:** machine learning, ai, data science, analytics

**Limitation:** 
- Hard-coded keywords only
- Won't detect "R", "Go", "Rust", or other languages
- Won't match misspellings ("Pyton" instead of "Python")
- Won't match variant names ("scikit-learn" vs "machine learning")

### Lines 54-55: Initialize Skills Set
```python
skills = set()
for token in doc:
```

**Line 54:** Create empty set to store found skills
**Line 55:** Loop through each token (word) in processed document

**How iteration works:**
```python
resume_text = "I know Python and Java"
doc = nlp(resume_text)

for token in doc:
    print(token.text)  # Prints: I, know, Python, and, Java
    print(token.i)     # Index: 0, 1, 2, 3, 4
```

### Lines 56-57: Single Word Skill Matching
```python
if token.text.lower() in tech_skills:
    skills.add(token.text)
```

**Line 56 Analysis:**
```python
if token.text.lower() in tech_skills:
```
- `token.text`: The actual text of the token
- `.lower()`: Converts to lowercase for case-insensitive matching
- `in tech_skills`: Checks if token exists in skills set
- Set membership check is very fast O(1)

**Example:**
```python
token.text = "Python"
token.text.lower() = "python"
"python" in tech_skills  # True → skill found
```

**Line 57:**
```python
skills.add(token.text)
```
- Adds the original-case token text to skills set
- Using original case preserves user's capitalization
- Set automatically handles duplicates (won't add "Python" twice)

### Lines 58-63: Compound Skill Matching (Bigrams)
```python
# Check for compound skills (e.g., "machine learning")
if token.i < len(doc) - 1:
    bigram = (token.text + " " + doc[token.i + 1].text).lower()
    if bigram in tech_skills:
        skills.add(bigram)
```

**Purpose:** Match multi-word skills like "machine learning", "data science"

**Line 58: Comment**
```python
# Check for compound skills (e.g., "machine learning")
```
- Explains the purpose of the following code block

**Line 59: Boundary Check**
```python
if token.i < len(doc) - 1:
```
- `token.i`: Index of current token
- `len(doc) - 1`: Index of last token
- Ensures we don't go past the end of document
- Prevents IndexError when accessing next token

**Example:**
```python
doc = nlp("machine learning is great")
# doc has 4 tokens: [0: machine, 1: learning, 2: is, 3: great]
# len(doc) = 4, len(doc) - 1 = 3

# When token.i = 2 (word "is"):
# 2 < 3 is True → check next token
# When token.i = 3 (word "great"):
# 3 < 3 is False → don't check (no next token)
```

**Line 60: Create Bigram**
```python
bigram = (token.text + " " + doc[token.i + 1].text).lower()
```
- `token.text`: Current word
- `doc[token.i + 1].text`: Next word
- String concatenation with space in between
- `.lower()`: Convert to lowercase for matching

**Example:**
```python
token.text = "machine"
token.i = 0
doc[1].text = "learning"
bigram = ("machine" + " " + "learning").lower()  # "machine learning"
```

**Line 61-62: Bigram Matching**
```python
if bigram in tech_skills:
    skills.add(bigram)
```
- Checks if 2-word phrase is in tech_skills set
- If found, adds to skills (not individual words)
- Example: "machine learning" added as one skill, not separately

**Advantage:** Captures meaning of compound terms
**Limitation:** Only detects adjacent words (won't find "machine... learning" with words between)

### Lines 64-65: Return Skills
```python
return skills
```

**Returns:** Python set of extracted skills
- Unordered, unique skills
- Converted to list later if needed
- Example: {"Python", "AWS", "Docker", "machine learning"}

---

## Experience Analysis Method (Lines 67-80)

```python
def _analyze_experience(self, doc):
    """Analyze years of experience"""
    # Simple heuristic - look for number + "years"
    experience_years = 0
```

### Purpose
Extract years of experience from resume text

### Line 67: Method Definition
```python
def _analyze_experience(self, doc):
```
- Takes spaCy `doc` object
- Returns integer of years found (0 if none detected)

### Lines 69-70: Heuristic and Initialization
```python
# Simple heuristic - look for number + "years"
experience_years = 0
```

**Comment:** Explains the approach
**Initialization:** Starts at 0, will update if experience found

**How it works:**
- Looks for pattern: number + "years" word
- Examples that would match:
  - "5 years of experience"
  - "10 years as a developer"
  - "3 years with Python"
- Takes maximum if multiple experience entries

### Lines 71-79: Token Loop
```python
for token in doc:
    if token.like_num and token.i < len(doc) - 1:
        next_token = doc[token.i + 1]
        if "year" in next_token.text.lower():
            try:
                experience_years = max(experience_years, int(token.text))
            except ValueError:
                continue
```

**Line 71: Loop Setup**
```python
for token in doc:
```
- Iterates through every token in resume

**Line 72: Check for Number**
```python
if token.like_num and token.i < len(doc) - 1:
```
- `token.like_num`: spaCy feature that checks if token looks like a number
  - Returns True for "5", "10", "3.5"
  - Returns False for "five", "ten"
- `token.i < len(doc) - 1`: Ensures next token exists
- Both conditions must be true (AND logic)

**Example:**
```python
token.text = "5"
token.like_num  # True

token.text = "five"
token.like_num  # False

token.text = "3.5"
token.like_num  # True
```

**Line 73: Get Next Token**
```python
next_token = doc[token.i + 1]
```
- Accesses token immediately after current one
- By index: `doc[token.i + 1]`

**Line 74: Check if Next is "Years"**
```python
if "year" in next_token.text.lower():
```
- `next_token.text`: The next word as string
- `.lower()`: Case-insensitive comparison
- `"year" in ...`: Substring check (partial match)
- Matches "years", "year", "YEARS", "Year"

**Examples:**
```python
"years" in "years".lower()  # True
"year" in "years".lower()   # True (substring match)
"year" in "experienced".lower()  # True (but not desired)
```

**Line 75-78: Convert and Store**
```python
try:
    experience_years = max(experience_years, int(token.text))
except ValueError:
    continue
```

**Purpose:** Safely convert text to integer and store

**Line 75: Error Handling Start**
```python
try:
```
- Begins try-except block
- Handles conversion errors

**Line 76: Parse and Store**
```python
experience_years = max(experience_years, int(token.text))
```
- `int(token.text)`: Converts "5" to integer 5
- `max(experience_years, int(token.text))`: Keeps the larger value
- Updates only if new value is higher

**Example:**
```python
experience_years = 0
int("5")  # 5
max(0, 5)  # 5
experience_years = 5

# Later in resume:
int("3")  # 3
max(5, 3)  # 5 (keeps higher value)
experience_years = 5 (unchanged)
```

**Line 77-78: Error Handling**
```python
except ValueError:
    continue
```
- `ValueError`: Raised if `int()` conversion fails
- Example: `int("five")` raises ValueError
- `continue`: Skip to next iteration if error
- Gracefully handles non-numeric "numbers"

### Line 79: Return Experience
```python
return experience_years
```
- Returns maximum years of experience found
- 0 if no "number + years" pattern detected

**Limitations:**
- Only matches adjacent "number years" pattern
- Misses "I have 5+ years" (+ sign)
- Misses "more than 10 years"
- Won't catch "senior" or "junior" level inference
- Returns single max value, not range

---

## Profile Score Calculation (Lines 81-102)

```python
def _calculate_profile_score(self, word_count, sentence_count, skills_count, experience_years):
    """Calculate profile score based on various metrics"""
    score = 0
```

### Purpose
Calculate composite score (0-100) from multiple metrics using weighted formula

### Line 81: Method Definition
```python
def _calculate_profile_score(self, word_count, sentence_count, skills_count, experience_years):
```
- Takes 4 metric parameters
- Returns integer score 0-100

### Line 83: Initialize Score
```python
score = 0
```
- Starts at 0, accumulates points from each metric

### Lines 85-91: Word Count Scoring (0-25 points)
```python
# Word count scoring (0-25 points)
if word_count >= 300:
    score += 25
else:
    score += (word_count / 300) * 25
```

**Goal:** Encourage detailed resumes (target 300+ words)

**Line 87: Full Points**
```python
if word_count >= 300:
    score += 25
```
- If resume has 300+ words: add full 25 points
- Binary: get all or none of these points

**Line 89: Partial Points**
```python
score += (word_count / 300) * 25
```
- If less than 300 words: proportional credit
- Formula: `(actual / target) * max_points`

**Examples:**
```python
word_count = 300:  score += (300/300) * 25 = 25 points
word_count = 150:  score += (150/300) * 25 = 12.5 points
word_count = 75:   score += (75/300) * 25 = 6.25 points
word_count = 0:    score += (0/300) * 25 = 0 points
```

### Lines 93-99: Skills Scoring (0-35 points)
```python
# Skills scoring (0-35 points)
if skills_count >= 8:
    score += 35
else:
    score += (skills_count / 8) * 35
```

**Goal:** Encourage listing multiple relevant skills (target 8)

**Same pattern as word count:**
- 8+ skills: Full 35 points
- Less than 8: Proportional credit

**Examples:**
```python
skills_count = 8:  score += 35 points
skills_count = 4:  score += (4/8) * 35 = 17.5 points
skills_count = 0:  score += 0 points
```

### Lines 101-107: Experience Scoring (0-40 points)
```python
# Experience scoring (0-40 points)
if experience_years >= 5:
    score += 40
else:
    score += (experience_years / 5) * 40
```

**Goal:** Value experience (target 5 years)

**Same proportional formula:**
- 5+ years: Full 40 points
- Less: Proportional credit

**Examples:**
```python
experience_years = 5:   score += 40 points
experience_years = 2.5: score += (2.5/5) * 40 = 20 points
experience_years = 0:   score += 0 points
```

### Scoring Summary
```
Maximum Possible Score: 25 + 35 + 40 = 100 points

Distribution:
- Word Count (Details):      25% (0-25 points)
- Skills (Breadth):          35% (0-35 points)
- Experience (Maturity):     40% (0-40 points)
```

**Weighting Rationale:**
- Experience weighted highest (40%) → values seniority
- Skills weighted second (35%) → values versatility
- Word count weighted lowest (25%) → values detail but less critical

### Line 109: Return Clamped Score
```python
return min(round(score), 100)
```

**Purpose:** Ensure score never exceeds 100

**Line-by-line:**
- `round(score)`: Rounds to nearest integer (e.g., 87.5 → 88)
- `min(..., 100)`: Takes minimum of (calculated score, 100)
- Prevents scores > 100 from floating-point arithmetic

**Examples:**
```python
score = 85.7:  round(85.7) = 86, min(86, 100) = 86
score = 100.2: round(100.2) = 100, min(100, 100) = 100
score = 102:   round(102) = 102, min(102, 100) = 100 (clamped)
```

---

## Suggestions Generation (Lines 111-146)

```python
def _generate_suggestions(self, word_count, sentence_count, skills, experience_years):
    """Generate improvement suggestions based on analysis"""
    suggestions = []
```

### Purpose
Generate actionable improvement recommendations based on detected weaknesses

### Line 111: Method Definition
```python
def _generate_suggestions(self, word_count, sentence_count, skills, experience_years):
```
- Takes metrics and skills data
- Returns list of suggestion dictionaries
- Note: Takes `skills` (set) not `skills_count` (int)

### Line 113: Initialize List
```python
suggestions = []
```
- Empty list to accumulate suggestions
- Will be populated conditionally

### Lines 115-119: Word Count Suggestion
```python
if word_count < 300:
    suggestions.append({
        "icon": "fa-file-text",
        "text": "Add more detail to your resume - aim for at least 300 words"
    })
```

**Condition:** If resume is less than 300 words
- `word_count < 300`: Checks if too short

**Suggestion Dictionary:**
```python
{
    "icon": "fa-file-text",      # Font Awesome icon name
    "text": "Add more detail..."  # Actionable suggestion text
}
```

**Icon Reference:**
- `fa-file-text`: Document icon from Font Awesome
- Used to visually represent the suggestion type
- Displayed in UI alongside text

**Suggestion Text:**
- Specific and actionable: "aim for at least 300 words"
- Provides target rather than vague "add more"

### Lines 121-125: Skills Suggestion
```python
if len(skills) < 8:
    suggestions.append({
        "icon": "fa-code",
        "text": "Include more relevant technical skills and technologies"
    })
```

**Condition:** If fewer than 8 skills found
- `len(skills)`: Number of skills (converts set to count)
- Suggests expanding skill list if under 8

**Icon:** `fa-code` represents programming/technical skills

### Lines 127-131: Sentence Count Suggestion
```python
if sentence_count < 10:
    suggestions.append({
        "icon": "fa-list",
        "text": "Add more achievements and responsibilities from your experience"
    })
```

**Condition:** If fewer than 10 sentences
- Proxy for detailed descriptions of experience
- Encourages bullet-point achievements

**Icon:** `fa-list` represents lists/details

### Lines 133-137: Experience Suggestion
```python
if experience_years < 2:
    suggestions.append({
        "icon": "fa-briefcase",
        "text": "Highlight any internships, projects, or relevant coursework"
    })
```

**Condition:** If less than 2 years detected
- Helpful for entry-level resumes
- Suggests alternative experience forms

**Icon:** `fa-briefcase` represents work/career

### Lines 139-143: Fallback Positive Suggestion
```python
if not suggestions:
    suggestions.append({
        "icon": "fa-star",
        "text": "Your resume looks great! Consider adding more quantifiable achievements"
    })
```

**Purpose:** If no improvements suggested, provide positive feedback
- `if not suggestions`: Empty list evaluates to False
- True if all metrics above thresholds

**Encouragement:** 
- Positive reinforcement even when metrics are good
- Still offers aspirational improvement (quantifiable achievements)

**Icon:** `fa-star` represents excellence/achievement

### Line 145: Return Suggestions
```python
return suggestions
```
- Returns list of 0+ suggestion dictionaries
- Can be 0 if resume is excellent
- Can be 1-4 if specific areas need improvement
- Displayed in UI with icons and text

---

## Data Flow Diagram

```
Input: Resume Text String
    ↓
ResumeAnalyzer.analyze_resume(text)
    ↓
1. Parse with spaCy: doc = self.nlp(text)
    ↓
2. Extract Metrics:
    - word_count = len(text.split())
    - sentence_count = len(list(doc.sents))
    - skills = _extract_skills(doc)           [set of 0+ skills]
    - experience_years = _analyze_experience(doc)  [int 0+]
    ↓
3. Calculate Score:
    - profile_score = _calculate_profile_score(...)  [0-100]
    ↓
4. Generate Suggestions:
    - suggestions = _generate_suggestions(...)  [list of dicts]
    ↓
Output: Dictionary with timestamp, metrics, skills, suggestions
```

---

## Complete Example

**Input Resume:**
```
Software Engineer with 5 years of experience.

I'm skilled in Python, Java, and JavaScript. 
I've worked with React, AWS, and Docker.
I have strong experience in machine learning.

Recent Projects:
- Built web app with React and Node.js
- Deployed to AWS using Docker and Kubernetes

Education: B.S. Computer Science
```

**Analysis Process:**

**Step 1: Text Metrics**
```python
text = "Software Engineer with 5 years of experience...[full text]"
word_count = 60  # Approximately 60 words
sentence_count = 6  # 6 sentences detected
```

**Step 2: Skills Extraction**
```python
Token-by-token search:
- "Software" → not in tech_skills
- "Engineer" → not in tech_skills
- "5" → not a skill, but next token is "years"
- "Python" → ✓ in tech_skills, added to skills set
- "Java" → ✓ added
- "JavaScript" → ✓ added
- "React" → ✓ added
- "AWS" → ✓ added
- "Docker" → ✓ added
- "machine" + "learning" → ✓ bigram found, added

Result: skills = {"Python", "Java", "JavaScript", "React", "AWS", "Docker", "machine learning"}
skills_count = 7
```

**Step 3: Experience Extraction**
```python
Searching for "number years" pattern:
- Token "5", next token "years" → Found!
- int("5") = 5
- experience_years = max(0, 5) = 5

Result: experience_years = 5
```

**Step 4: Score Calculation**
```python
word_count = 60 < 300:
  score += (60/300) * 25 = 5 points

skills_count = 7 < 8:
  score += (7/8) * 35 = 30.625 points

experience_years = 5 >= 5:
  score += 40 points

Total: 5 + 30.625 + 40 = 75.625
Rounded: 76
Clamped: min(76, 100) = 76

profile_score = 76
```

**Step 5: Suggestions**
```python
word_count = 60 < 300:
  ✓ Add more detail suggestion (60 words is too short)

len(skills) = 7 < 8:
  ✓ Add more skills suggestion (close but not at target)

sentence_count = 6 < 10:
  ✓ Add achievements suggestion (not enough detail)

experience_years = 5 >= 2:
  ✗ No experience suggestion (5 years is good)

Result: 3 suggestions generated
```

**Final Output:**
```python
{
  "timestamp": "2026-03-04T15:30:45.123456",
  "metrics": {
    "word_count": 60,
    "sentence_count": 6,
    "skills_count": 7,
    "experience_years": 5,
    "profile_score": 76
  },
  "skills": ["Python", "Java", "JavaScript", "React", "AWS", "Docker", "machine learning"],
  "suggestions": [
    {
      "icon": "fa-file-text",
      "text": "Add more detail to your resume - aim for at least 300 words"
    },
    {
      "icon": "fa-code",
      "text": "Include more relevant technical skills and technologies"
    },
    {
      "icon": "fa-list",
      "text": "Add more achievements and responsibilities from your experience"
    }
  ]
}
```

---

## Key Characteristics

### Strengths
✅ **Simple & Fast:** Uses basic heuristics, processes quickly
✅ **No API Calls:** Runs locally without external services
✅ **Interpretable:** Easy to understand what it's checking
✅ **Extensible:** Easy to add more tech skills to the set

### Limitations
❌ **Hard-coded Skills:** Only detects predefined list
❌ **Pattern-based Experience:** Misses "5+ years", "senior level"
❌ **No Semantic Understanding:** Can't detect "backend" unless explicitly listed
❌ **English Only:** Model trained for English text
❌ **No Context:** Doesn't distinguish skills section from casual mentions
❌ **Sentence count:** Counts sentences, not necessarily quality

### Differences from utils/resume_analyzer.py
| Aspect | resume_analytics/analyzer.py | utils/resume_analyzer.py |
|--------|------------------------------|--------------------------|
| **Approach** | NLP-based (spaCy) | Regex-based keyword matching |
| **Text Extraction** | None (assumes raw text) | Extracts from PDF/DOCX |
| **Focus** | Metrics and suggestions | ATS scoring and formatting |
| **Speed** | Moderate | Fast |
| **Accuracy** | Better for unstructured text | Better for formatted resumes |

---

## Usage in Application

This analyzer appears to be for **analytics/dashboard** purposes rather than the main resume analysis. Used for:

1. **Profile Analytics Dashboard:** Shows user's resume metrics
2. **Skill Tracking:** Monitors skill growth over time
3. **Improvement Suggestions:** Recommends resume enhancements
4. **Resume Quality Assessment:** Simple scoring system

It complements the main `utils/resume_analyzer.py` which focuses on ATS optimization.

