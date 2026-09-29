import streamlit as st
import sqlite3

# ---------------- DATABASE ----------------

conn = sqlite3.connect("skillgap.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_skills TEXT,
    job_description TEXT,
    match_percentage REAL,
    missing_skills TEXT
)
""")

conn.commit()


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="SkillGap AI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 SkillGap AI")
st.subheader("Job Skill Gap Analyzer")

st.write(
    "Analyze your skills against a job description and find "
    "your missing skills and learning roadmap."
)


# ---------------- USER INPUT ----------------

your_skills = st.text_input(
    "💻 Enter your skills",
    placeholder="Example: Python, HTML, Git"
)

job_description = st.text_area(
    "📄 Enter the Job Description",
    placeholder="Paste the job description here..."
)


# ---------------- SKILL LIST ----------------

skills = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "git",
    "github",
    "rest api",
    "machine learning",
    "pandas",
    "numpy"
]


# ---------------- ROADMAP ----------------

roadmap = {
    "python": "Learn Python basics, functions, OOP and projects",
    "java": "Learn Java basics, OOP and exception handling",
    "sql": "Learn SELECT, WHERE, JOIN, GROUP BY and databases",
    "html": "Learn HTML tags, forms and semantic elements",
    "css": "Learn CSS selectors, Flexbox and responsive design",
    "javascript": "Learn JavaScript, DOM and events",
    "git": "Learn commits, branches and GitHub",
    "github": "Learn repositories and collaboration",
    "rest api": "Learn HTTP, GET, POST, JSON and APIs",
    "machine learning": "Learn NumPy, Pandas and ML algorithms",
    "pandas": "Learn DataFrames and data analysis",
    "numpy": "Learn arrays and numerical operations"
}


# ---------------- ANALYZE ----------------

if st.button("🔍 Analyze Skills"):

    if not your_skills or not job_description:
        st.warning("⚠️ Please enter both your skills and the job description.")

    else:

        # Convert user skills into a list
        your_skill_list = [
            skill.strip().lower()
            for skill in your_skills.split(",")
        ]

        # Find required skills in job description
        job_text = job_description.lower()

        required_skills = []

        for skill in skills:
            if skill in job_text:
                required_skills.append(skill)

        # Find missing skills
        missing_skills = []

        for skill in required_skills:
            if skill not in your_skill_list:
                missing_skills.append(skill)

        # Calculate match percentage
        if len(required_skills) > 0:
            match_percentage = (
                (len(required_skills) - len(missing_skills))
                / len(required_skills)
            ) * 100
        else:
            match_percentage = 0

        # ---------------- SAVE TO DATABASE ----------------

        cursor.execute(
            """
            INSERT INTO analysis
            (user_skills, job_description, match_percentage, missing_skills)
            VALUES (?, ?, ?, ?)
            """,
            (
                your_skills,
                job_description,
                match_percentage,
                ", ".join(missing_skills)
            )
        )

        conn.commit()

        # ---------------- RESULTS ----------------

        st.success("✅ Analysis completed and saved!")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🎯 Skill Match",
                f"{match_percentage:.0f}%"
            )

        with col2:
            st.metric(
                "📋 Required Skills",
                len(required_skills)
            )

        with col3:
            st.metric(
                "❌ Missing Skills",
                len(missing_skills)
            )

        st.divider()

        # Required skills
        st.subheader("📋 Required Skills")

        if required_skills:
            st.write(", ".join(required_skills))
        else:
            st.info("No recognized skills found in the job description.")

        # Current skills
        st.subheader("💻 Your Skills")

        st.write(", ".join(your_skill_list))

        # Missing skills
        st.subheader("❌ Missing Skills")

        if missing_skills:
            for skill in missing_skills:
                st.write("•", skill)
        else:
            st.success("🎉 You have all the recognized required skills!")

        # Roadmap
        st.subheader("🗺️ Learning Roadmap")

        if missing_skills:

            for skill in missing_skills:
                st.write(
                    f"**{skill.title()}** → {roadmap.get(skill, 'Learn this skill through projects and practice.')}"
                )

        else:
            st.success("No learning gaps found!")


# ---------------- ANALYSIS HISTORY ----------------

st.divider()

st.header("📜 Analysis History")

history = cursor.execute("""
    SELECT id, match_percentage, missing_skills
    FROM analysis
    ORDER BY id DESC
""").fetchall()

if history:

    for record in history:

        analysis_id = record[0]
        match = record[1]
        missing = record[2]

        st.write(
            f"**Analysis #{analysis_id}** — "
            f"Match: {match:.0f}% — "
            f"Missing: {missing if missing else 'None'}"
        )

else:

    st.info("No analysis history yet.")


# ---------------- SKILL DASHBOARD ----------------

st.divider()

st.header("📊 Skill Dashboard")

if history:

    latest = history[0]

    latest_match = latest[1]
    latest_missing = latest[2]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎯 Latest Skill Match",
            f"{latest_match:.0f}%"
        )

    with col2:

        if latest_missing:
            missing_count = len(
                [x for x in latest_missing.split(",") if x.strip()]
            )
        else:
            missing_count = 0

        st.metric(
            "❌ Missing Skills",
            missing_count
        )

    st.subheader("🎯 Skill Match Progress")

    st.progress(
        int(latest_match) / 100
    )

    st.subheader("📈 Previous Analysis Scores")

    scores = [
        record[1]
        for record in history
    ]

    chart_data = {
        "Analysis": [
            f"Analysis {i + 1}"
            for i in range(len(scores))
        ],
        "Match %": scores
    }

    st.bar_chart(
        chart_data,
        x="Analysis",
        y="Match %"
    )

else:

    st.info("Analyze a job to see your Skill Dashboard.")