import pandas as pd
from flask import Blueprint, session
from analyze_grade import analyze_grade
from analyze_DLO_grade import analyze_DLO_grade

routes_c = Blueprint("c_div", __name__)


def c_div_analysis(df, n, prn_set):

    # ------------------------------------------------------------
    # Session data
    # ------------------------------------------------------------
    teachers_div1 = session.get(f'teachers_div{n}')
    subjects = session.get('subjects')
    semester = session.get('semester')  # kept intentionally

    teacher1_name = teachers_div1[0]['name']
    teacher1_subject = subjects[0]['subject']

    teacher2_name = teachers_div1[1]['name']
    teacher2_subject = subjects[1]['subject']

    teacher3_name = teachers_div1[2]['name']
    teacher3_subject = subjects[2]['subject']

    teacher4_name = teachers_div1[3]['name']
    teacher4_subject = subjects[3]['subject']

    teacher5_name = teachers_div1[4]['name']
    teacher5_subject = subjects[4]['subject']

    # ------------------------------------------------------------
    # Clean main dataframe
    # ------------------------------------------------------------
    df = df.copy()
    df.columns = (
        df.columns
          .str.upper()
          .str.replace(" ", "", regex=False)
          .str.replace("_", "", regex=False)
    )

    df['EXAM2'] = df['EXAM2'].astype(str)
    df['ROLLNO'] = df['ROLLNO'].astype(str).str.strip()

    # ------------------------------------------------------------
    # Apply filters (same logic)
    # ------------------------------------------------------------
    df = df[
        (~df['EXAM2'].str.contains(r'\+', na=False)) &
        (df['ROLLNO'].isin(prn_set))
    ]

    # ------------------------------------------------------------
    # BUILD ROWS FIRST (NO .loc ASSIGNMENT)
    # ------------------------------------------------------------
    rows = {}
    faculty = []

    rows[teacher1_subject] = analyze_grade(df, 'GRADE1')
    faculty.append(teacher1_name)

    rows[teacher2_subject] = analyze_grade(df, 'GRADE4')
    faculty.append(teacher2_name)

    rows[teacher3_subject] = analyze_grade(df, 'GRADE7')
    faculty.append(teacher3_name)

    rows[teacher4_subject] = analyze_grade(df, 'GRADE10')
    faculty.append(teacher4_name)

    rows[teacher5_subject] = analyze_grade(df, 'GRADE13')
    faculty.append(teacher5_name)

    # ------------------------------------------------------------
    # CREATE DATAFRAME ONCE (NO WARNINGS)
    # ------------------------------------------------------------
    new_df = pd.DataFrame.from_dict(rows, orient='index')
    new_df.index.name = "Subject"

    # ------------------------------------------------------------
    # Enforce dtypes (NA-safe, future-proof)
    # ------------------------------------------------------------
    new_df = new_df.astype({
        'E-P': 'Int64',
        'D': 'Int64',
        'C-O': 'Int64',
        'TOTAL PASS': 'Int64',
        'FAILED': 'Int64',
        'No.of students appeared': 'Int64',
        '% OF RESULT': 'float'
    })

    # ------------------------------------------------------------
    # Insert Faculty column
    # ------------------------------------------------------------
    new_df.insert(0, 'Faculty', faculty)

    return new_df
