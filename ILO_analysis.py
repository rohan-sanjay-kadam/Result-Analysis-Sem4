import pandas as pd
from flask import Blueprint, session
from analyze_DLO_grade import analyze_DLO_grade
from analyze_grade import analyze_grade

routes_ILO = Blueprint("ILO", __name__)


def ILO_analysis(
    df, n,
    DLO1_df, DLO2_df, DLO3_df, DLO4_df, DLO5_df, DLO6_df,
    ILO1_df, ILO2_df, ILO3_df, ILO4_df,
    prn_set
):
    # ------------------------------------------------------------------
    # Helper to clean columns
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Session data
    # ------------------------------------------------------------------
    teachers_div1 = session.get(f'teachers_div{n}')
    subjects = session.get('subjects')
    semester = session.get('semester')

    teacher1_name = teachers_div1[0]['name']
    teacher1_subject = subjects[0]['subject']

    teacher2_name = teachers_div1[1]['name']
    teacher2_subject = subjects[1]['subject']

    # ------------------------------------------------------------------
    # Clean main df
    # ------------------------------------------------------------------
    df = df.copy()
    df.columns = df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    df['EXAM2'] = df['EXAM2'].astype(str)

    # ------------------------------------------------------------------
    # Clean all DLO / ILO dataframes
    # ------------------------------------------------------------------
    DLO1_df = clean_columns(DLO1_df)
    DLO2_df = clean_columns(DLO2_df)
    DLO3_df = clean_columns(DLO3_df)
    DLO4_df = clean_columns(DLO4_df)
    DLO5_df = clean_columns(DLO5_df)
    DLO6_df = clean_columns(DLO6_df)

    ILO1_df = clean_columns(ILO1_df)
    ILO2_df = clean_columns(ILO2_df)
    ILO3_df = clean_columns(ILO3_df)
    ILO4_df = clean_columns(ILO4_df)

    # ------------------------------------------------------------------
    # Filter main df
    # ------------------------------------------------------------------
    df = df[(~df['EXAM2'].str.contains(r'\+', na=False)) & (df['ROLLNO'].isin(prn_set))]

    # ------------------------------------------------------------------
    # Filter DLO / ILO dfs by PRN
    # ------------------------------------------------------------------
    for d in [DLO1_df, DLO2_df, DLO3_df, DLO4_df, DLO5_df, DLO6_df,
              ILO1_df, ILO2_df, ILO3_df, ILO4_df]:
        if not d.empty:
            d.drop(d[~d['ROLLNO'].isin(prn_set)].index, inplace=True)

    # ------------------------------------------------------------------
    # Teacher & subject mapping
    # ------------------------------------------------------------------
    teacher1_DLO_name = teachers_div1[5]['name']
    teacher1_DLO_subject = subjects[5]['subject']

    teacher2_DLO_name = teachers_div1[6]['name']
    teacher2_DLO_subject = subjects[6]['subject']

    teacher3_DLO_name = teachers_div1[7]['name']
    teacher3_DLO_subject = subjects[7]['subject']

    teacher4_DLO_name = teachers_div1[8]['name']
    teacher4_DLO_subject = subjects[8]['subject']

    teacher5_DLO_name = teachers_div1[9]['name']
    teacher5_DLO_subject = subjects[9]['subject']

    teacher6_DLO_name = teachers_div1[10]['name']
    teacher6_DLO_subject = subjects[10]['subject']

    teacher1_ILO_name = teachers_div1[11]['name']
    teacher1_ILO_subject = subjects[11]['subject']

    teacher2_ILO_name = teachers_div1[12]['name']
    teacher2_ILO_subject = subjects[12]['subject']

    teacher3_ILO_name = teachers_div1[13]['name']
    teacher3_ILO_subject = subjects[13]['subject']

    if semester == 7:
        teacher4_ILO_name = teachers_div1[14]['name']
        teacher4_ILO_subject = subjects[14]['subject']

    # ------------------------------------------------------------------
    # BUILD ROWS (NO .loc ROW INSERTION → NO WARNINGS)
    # ------------------------------------------------------------------
    rows = {}
    faculty = []

    if semester == 7:
        rows[teacher1_subject] = analyze_grade(df, 'GRADE1')
        faculty.append(teacher1_name)

        rows[teacher2_subject] = analyze_grade(df, 'GRADE4')
        faculty.append(teacher2_name)

        rows[teacher1_DLO_subject] = analyze_DLO_grade(df, DLO1_df, 'GRADE7')
        faculty.append(teacher1_DLO_name)

        rows[teacher2_DLO_subject] = analyze_DLO_grade(df, DLO2_df, 'GRADE7')
        faculty.append(teacher2_DLO_name)

        rows[teacher3_DLO_subject] = analyze_DLO_grade(df, DLO3_df, 'GRADE7')
        faculty.append(teacher3_DLO_name)

        rows[teacher4_DLO_subject] = analyze_DLO_grade(df, DLO4_df, 'GRADE10')
        faculty.append(teacher4_DLO_name)

        rows[teacher5_DLO_subject] = analyze_DLO_grade(df, DLO5_df, 'GRADE10')
        faculty.append(teacher5_DLO_name)

        rows[teacher6_DLO_subject] = analyze_DLO_grade(df, DLO6_df, 'GRADE10')
        faculty.append(teacher6_DLO_name)

        rows[teacher1_ILO_subject] = analyze_DLO_grade(df, ILO1_df, 'GRADE13')
        faculty.append(teacher1_ILO_name)

        rows[teacher2_ILO_subject] = analyze_DLO_grade(df, ILO2_df, 'GRADE13')
        faculty.append(teacher2_ILO_name)

        rows[teacher3_ILO_subject] = analyze_DLO_grade(df, ILO3_df, 'GRADE13')
        faculty.append(teacher3_ILO_name)

        rows[teacher4_ILO_subject] = analyze_DLO_grade(df, ILO4_df, 'GRADE13')
        faculty.append(teacher4_ILO_name)

    elif semester == 8:
        rows[teacher1_subject] = analyze_grade(df, 'GRADE1')
        faculty.append(teacher1_name)

        rows[teacher1_DLO_subject] = analyze_DLO_grade(df, DLO1_df, 'GRADE4')
        faculty.append(teacher1_DLO_name)

        rows[teacher2_DLO_subject] = analyze_DLO_grade(df, DLO2_df, 'GRADE4')
        faculty.append(teacher2_DLO_name)

        rows[teacher3_DLO_subject] = analyze_DLO_grade(df, DLO3_df, 'GRADE4')
        faculty.append(teacher3_DLO_name)

        rows[teacher4_DLO_subject] = analyze_DLO_grade(df, DLO4_df, 'GRADE7')
        faculty.append(teacher4_DLO_name)

        rows[teacher5_DLO_subject] = analyze_DLO_grade(df, DLO5_df, 'GRADE7')
        faculty.append(teacher5_DLO_name)

        rows[teacher6_DLO_subject] = analyze_DLO_grade(df, DLO6_df, 'GRADE7')
        faculty.append(teacher6_DLO_name)

        rows[teacher1_ILO_subject] = analyze_DLO_grade(df, ILO1_df, 'GRADE10')
        faculty.append(teacher1_ILO_name)

        rows[teacher2_ILO_subject] = analyze_DLO_grade(df, ILO2_df, 'GRADE10')
        faculty.append(teacher2_ILO_name)

        rows[teacher3_ILO_subject] = analyze_DLO_grade(df, ILO3_df, 'GRADE10')
        faculty.append(teacher3_ILO_name)

    # ------------------------------------------------------------------
    # CREATE DATAFRAME ONCE (SAFE & FUTURE-PROOF)
    # ------------------------------------------------------------------
    new_df = pd.DataFrame.from_dict(rows, orient='index')
    new_df.index.name = "Subject"

    # Enforce dtypes
    new_df = new_df.astype({
        'E-P': 'Int64',
        'D': 'Int64',
        'C-O': 'Int64',
        'TOTAL PASS': 'Int64',
        'FAILED': 'Int64',
        'No.of students appeared': 'Int64',
        '% OF RESULT': 'float'
    })

    # Insert Faculty column
    new_df.insert(0, 'Faculty', faculty)

    return new_df
