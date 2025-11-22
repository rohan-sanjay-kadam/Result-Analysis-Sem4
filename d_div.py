import pandas as pd
from flask import Blueprint,session
import pandas
from analyze_grade import analyze_grade

routes_d = Blueprint("d_div", __name__)

def d_div_analysis(df):
    new2_df = pd.DataFrame(columns=['E-P','D','C-O','TOTAL PASS','FAILED','No.of students appeared','% OF RESULT'])
    teachers_div2 = session.get('teachers_div2', [])
    teacher1_name = teachers_div2[0]['name']
    teacher1_subject = teachers_div2[0]['subject']
    teacher2_name = teachers_div2[1]['name']
    teacher2_subject = teachers_div2[1]['subject']
    teacher3_name = teachers_div2[2]['name']
    teacher3_subject = teachers_div2[2]['subject']
    teacher4_name = teachers_div2[3]['name']
    teacher4_subject = teachers_div2[3]['subject']
    teacher5_name = teachers_div2[4]['name']
    teacher5_subject = teachers_div2[4]['subject']
    prn_start = session.get('div2_prn_start')
    df['exam2'] = df['exam2'].apply(str)
    # df = df[(~df['exam2'].str.contains(r'\+', na=False)) & (df['ROLLNO'] > '122A1070')]
    df = df[(~df['exam2'].str.contains(r'\+', na=False)) & (df['ROLLNO'] >= prn_start)]

    # new2_df['E-P'] = df.loc[(df['GRADE1'] == "E") | (df['GRADE1'] == "P"), ['GRADE1']].count()
    # new2_df['D'] = df.loc[(df['GRADE1'] == "D"), ['GRADE1']].count()
    # new2_df['C-O'] = df.loc[
    #     (df['GRADE1'] == "O") | (df['GRADE1'] == "A") | (df['GRADE1'] == "B") | (df['GRADE1'] == "C"), [
    #         'GRADE1']].count()
    # new2_df['TOTAL PASS'] = new2_df['E-P'] + new2_df['D'] + new2_df['C-O']
    # new2_df['FAILED'] = df.loc[(df['GRADE1'] == "F"), ['GRADE1']].count()
    # new2_df['No.of students appeared'] = new2_df['TOTAL PASS'] + new2_df['FAILED']
    # new2_df['% OF RESULT'] = (new2_df['TOTAL PASS'] / new2_df['No.of students appeared'] * 100).round(2)


    new2_df.loc[teacher1_subject] = analyze_grade(df, 'GRADE1')
    new2_df.loc[teacher2_subject] = analyze_grade(df, 'GRADE4')
    new2_df.loc[teacher3_subject] = analyze_grade(df, 'GRADE7')
    new2_df.loc[teacher4_subject] = analyze_grade(df, 'GRADE10')
    new2_df.loc[teacher5_subject] = analyze_grade(df, 'GRADE13')
    new2_df.index.name = "Subject"
    new2_df.insert(0,'Faculty' ,[teacher1_name, teacher2_name, teacher3_name, teacher4_name, teacher5_name])

    return new2_df
