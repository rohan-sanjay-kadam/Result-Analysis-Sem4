import pandas as pd
from flask import Blueprint, session
from analyze_DLO_grade import analyze_DLO_grade
from analyze_grade import analyze_grade

routes_c_DLO = Blueprint("c_div_DLO", __name__)


def c_div_DLO_analysis(df, n, DLO1_df, DLO2_df, DLO3_df, prn_set):

    # ------------------------------------------------------------
    # Helper: clean columns
    # ------------------------------------------------------------
    def clean_columns(df):
        if df.empty:
            return df
        df = df.copy()
        df.columns = [
            str(col).strip().upper().replace(" ", "").replace("_", "")
            for col in df.columns
        ]
        df['ROLLNO'] = df['ROLLNO'].astype(str).str.strip()
        return df

    # ------------------------------------------------------------
    # Session data
    # ------------------------------------------------------------
    teachers_div1 = session.get(f'teachers_div{n}')
    subjects = session.get('subjects')
    semester = session.get('semester')  # kept (even if unused)

    teacher1_name = teachers_div1[0]['name']
    teacher1_subject = subjects[0]['subject']

    teacher2_name = teachers_div1[1]['name']
    teacher2_subject = subjects[1]['subject']

    teacher3_name = teachers_div1[2]['name']
    teacher3_subject = subjects[2]['subject']

    teacher4_name = teachers_div1[3]['name']
    teacher4_subject = subjects[3]['subject']

    # ------------------------------------------------------------
    # Clean main df
    # ------------------------------------------------------------
    df = df.copy()
    df.columns = df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    df['EXAM2'] = df['EXAM2'].astype(str)

    # ------------------------------------------------------------
    # Clean DLO dfs
    # ------------------------------------------------------------
    DLO1_df = clean_columns(DLO1_df)
    DLO2_df = clean_columns(DLO2_df)
    DLO3_df = clean_columns(DLO3_df)

    # ------------------------------------------------------------
    # Filter main df
    # ------------------------------------------------------------
    df = df[(~df['EXAM2'].str.contains(r'\+', na=False)) & (df['ROLLNO'].isin(prn_set))]

    # ------------------------------------------------------------
    # Filter DLO dfs by PRN
    # ------------------------------------------------------------
    for d in [DLO1_df, DLO2_df, DLO3_df]:
        if not d.empty:
            d.drop(d[~d['ROLLNO'].isin(prn_set)].index, inplace=True)

    # ------------------------------------------------------------
    # DLO teacher mapping
    # ------------------------------------------------------------
    teacher1_DLO_name = teachers_div1[5]['name']
    teacher1_DLO_subject = subjects[5]['subject']

    teacher2_DLO_name = teachers_div1[6]['name']
    teacher2_DLO_subject = subjects[6]['subject']

    teacher3_DLO_name = teachers_div1[7]['name']
    teacher3_DLO_subject = subjects[7]['subject']

    # ------------------------------------------------------------
    # BUILD ROWS FIRST (NO ROW-WISE .loc ASSIGNMENT)
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

    rows[teacher1_DLO_subject] = analyze_DLO_grade(df, DLO1_df, 'GRADE13')
    faculty.append(teacher1_DLO_name)

    rows[teacher2_DLO_subject] = analyze_DLO_grade(df, DLO2_df, 'GRADE13')
    faculty.append(teacher2_DLO_name)

    rows[teacher3_DLO_subject] = analyze_DLO_grade(df, DLO3_df, 'GRADE13')
    faculty.append(teacher3_DLO_name)

    # ------------------------------------------------------------
    # CREATE DATAFRAME ONCE (NO WARNINGS)
    # ------------------------------------------------------------
    new_df = pd.DataFrame.from_dict(rows, orient='index')
    new_df.index.name = "Subject"

    # ------------------------------------------------------------
    # Enforce dtypes (safe with NA)
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
