import pandas as pd
from flask import Blueprint,session
from analyze_grade import analyze_grade
from analyze_DLO_grade import analyze_DLO_grade


routes_c = Blueprint("c_div", __name__)

def c_div_analysis(df,n,prn_set):
    new_df = pd.DataFrame(columns=['E-P','D','C-O','TOTAL PASS','FAILED','No.of students appeared','% OF RESULT'])
    teachers_div1 = session.get(f'teachers_div{n}') #change teachers_div1 to teachers if working
    subjects = session.get('subjects')
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
    semester = session.get('semester')
    df.columns = df.columns.str.strip().str.upper()
    df['EXAM2'] = df['EXAM2'].apply(str)
    df['ROLLNO'] = df['ROLLNO'].astype(str).str.strip()

    df = df[(~df['EXAM2'].str.contains(r'\+', na=False)) & (df['ROLLNO'].isin(prn_set))]

    # D division condition
    # df['exam2'] = df['exam2'].apply(str)
    # df = df[(~df['exam2'].str.contains(r'\+', na=False)) & (df['ROLLNO'] > '122A1070')]

    # new_df['E-P'] = df.loc[(df['GRADE1'] == "E") | (df['GRADE1'] == "P"), ['GRADE1']].count()
    # new_df['D'] = df.loc[(df['GRADE1'] == "D"), ['GRADE1']].count()
    # new_df['C-O'] = df.loc[
    #     (df['GRADE1'] == "O") | (df['GRADE1'] == "A") | (df['GRADE1'] == "B") | (df['GRADE1'] == "C"), [
    #         'GRADE1']].count()
    # new_df['TOTAL PASS'] = new_df['E-P'] + new_df['D'] + new_df['C-O']
    # new_df['FAILED'] = df.loc[(df['GRADE1'] == "F"), ['GRADE1']].count()
    # new_df['No.of students appeared'] = new_df['TOTAL PASS'] + new_df['FAILED']
    # new_df['% OF RESULT'] = (new_df['TOTAL PASS'] / new_df['No.of students appeared'] * 100).round(2)

    # This wont work
    # new_df['E-P']=np.nan
    # new_df['D']=np.nan
    # new_df['C-O'] = np.nan
    # new_df['TOTAL PASS'] = np.nan
    # new_df['FAILED'] = np.nan
    # new_df['No.of students appeared'] = np.nan
    # new_df['% OF RESULT'] = np.nan


    new_df.loc[teacher1_subject] = analyze_grade(df, 'GRADE1')
    new_df.loc[teacher2_subject] = analyze_grade(df, 'GRADE4')
    new_df.loc[teacher3_subject] = analyze_grade(df, 'GRADE7')
    new_df.loc[teacher4_subject] = analyze_grade(df, 'GRADE10')
    new_df.loc[teacher5_subject] = analyze_grade(df, 'GRADE13')
    new_df.index.name = "Subject"
    new_df.insert(0,'Faculty' ,[teacher1_name, teacher2_name, teacher3_name, teacher4_name, teacher5_name])


    return new_df