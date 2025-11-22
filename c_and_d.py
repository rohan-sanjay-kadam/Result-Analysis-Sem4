import pandas as pd
from flask import session,Blueprint

routes_cd = Blueprint("c_and_d", __name__)

def c_d_analysis(df):
    cd_df=pd.DataFrame(columns=["40%-49%", "50%-59%", "Above 60%", "Total"])
    # cd_df=pd.DataFrame(columns = pd.MultiIndex.from_tuples([("23 - 24  BATCH PERCENTAGE OF STUDENTS SCORING IN THE RANGE OF (NO. OF STUDENTS = 133)", "40%-49%"),
    #                                  ("23 - 24  BATCH PERCENTAGE OF STUDENTS SCORING IN THE RANGE OF (NO. OF STUDENTS = 133)", "50%-59%"),
    #                                  ("23 - 24  BATCH PERCENTAGE OF STUDENTS SCORING IN THE RANGE OF (NO. OF STUDENTS = 133)", "Above 60%"),
    #                                  ("23 - 24  BATCH PERCENTAGE OF STUDENTS SCORING IN THE RANGE OF (NO. OF STUDENTS = 133)", "Total")])
    #                    )
    # cd_df=pd.DataFrame()
    teachers_div1 = session.get('teachers_div1', [])
    teacher1_name = teachers_div1[0]['name']
    teacher1_subject = teachers_div1[0]['subject']
    teacher2_name = teachers_div1[1]['name']
    teacher2_subject = teachers_div1[1]['subject']
    teacher3_name = teachers_div1[2]['name']
    teacher3_subject = teachers_div1[2]['subject']
    teacher4_name = teachers_div1[3]['name']
    teacher4_subject = teachers_div1[3]['subject']
    teacher5_name = teachers_div1[4]['name']
    teacher5_subject = teachers_div1[4]['subject']
    df['exam2'] = df['exam2'].apply(str)
    df = df[(~df['exam2'].str.contains(r'\+', na=False)) & (df['ROLLNO'] > '122A1000')]
    # E_P = df.loc[(df['GRADE1'] == "E") | (df['GRADE1'] == "P"), ['GRADE1']].count()
    # D = df.loc[(df['GRADE1'] == "D"), ['GRADE1']].count()
    # A_B_C_O = df.loc[
    #     (df['GRADE1'] == "O") | (df['GRADE1'] == "A") | (df['GRADE1'] == "B") | (df['GRADE1'] == "C"), [
    #         'GRADE1']].count()
    # TOTAL_PASS= E_P+D+A_B_C_O
    # FAILED= df.loc[(df['GRADE1'] == "F"), ['GRADE1']].count()
    # No_of_students_appeared= TOTAL_PASS + FAILED
    # cd_df['40%-49%']= (E_P/No_of_students_appeared*100).round(2)
    # cd_df['50%-59%']=(D/No_of_students_appeared*100).round(2)
    # cd_df['Above 60%']=(A_B_C_O/No_of_students_appeared*100).round(2)
    # cd_df['Total'] = (TOTAL_PASS / No_of_students_appeared * 100).round(2)


    def analyze_grade(df, grade_column):
        E_P = df.loc[(df[grade_column] == "E") | (df[grade_column] == "P"), [grade_column]].shape[0]
        D = df.loc[df[grade_column] == "D", [grade_column]].shape[0]
        C_O = df.loc[
            (df[grade_column] == "O") | (df[grade_column] == "A") | (df[grade_column] == "B") | (
                    df[grade_column] == "C"), [
                grade_column]].shape[0]
        TOTAL_PASS = E_P + D + C_O
        FAILED = df.loc[df[grade_column] == "F", [grade_column]].shape[0]
        No_of_students = TOTAL_PASS + FAILED
        e=(E_P/No_of_students*100)
        d = (D / No_of_students * 100)
        c = (C_O / No_of_students * 100)
        percent_result = (TOTAL_PASS / No_of_students * 100)
        return {
            '40%-49%': round(e,2),
            '50%-59%': round(d,2),
            'Above 60%': round(c,2),
            # 'TOTAL PASS': TOTAL_PASS,
            # 'FAILED': FAILED,
            # 'No.of students appeared': No_of_students,
            'Total': round(percent_result, 2)
        }
    cd_df.loc[teacher1_subject] = analyze_grade(df, 'GRADE1')
    cd_df.loc[teacher2_subject] = analyze_grade(df, 'GRADE4')
    cd_df.loc[teacher3_subject] = analyze_grade(df, 'GRADE7')
    cd_df.loc[teacher4_subject] = analyze_grade(df, 'GRADE10')
    cd_df.loc[teacher5_subject] = analyze_grade(df, 'GRADE13')
    cd_df.index.name = "Name of the Subjects"

    return cd_df