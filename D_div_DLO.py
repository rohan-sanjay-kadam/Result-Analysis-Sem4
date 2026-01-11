import pandas as pd
from flask import Blueprint, session
from analyze_DLO_grade import analyze_DLO_grade
from analyze_grade import analyze_grade

# routes_c_DLO = Blueprint("c_div_DLO", __name__)


# this MODULEE IS NOT USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def d_div_DLO_analysis(df,DLO1_df,DLO2_df,DLO3_df):
    new_df = pd.DataFrame(columns=['E-P', 'D', 'C-O', 'TOTAL PASS', 'FAILED', 'No.of students appeared', '% OF RESULT'])
    teachers_div2 = session.get('teachers_div2')
    teacher1_name = teachers_div2[0]['name']
    teacher1_subject = teachers_div2[0]['subject']
    teacher2_name = teachers_div2[1]['name']
    teacher2_subject = teachers_div2[1]['subject']
    teacher3_name = teachers_div2[2]['name']
    teacher3_subject = teachers_div2[2]['subject']
    teacher4_name = teachers_div2[3]['name']
    teacher4_subject = teachers_div2[3]['subject']
    # semester = session.get('semester')
    prn_start = session.get('div2_prn_start')
    prn_end = session.get('div2_prn_end')
    df.columns = df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    DLO1_df.columns = DLO1_df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    DLO2_df.columns = DLO2_df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    DLO3_df.columns = DLO3_df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)


    df = df[(df['ROLLNO'] >= prn_start) & (df['ROLLNO'] <= prn_end)]
    DLO1_df = DLO1_df[(DLO1_df['ROLLNO'] >= prn_start) & (DLO1_df['ROLLNO'] <= prn_end)] #PRN dynamic karna hai
    DLO2_df = DLO2_df[(DLO2_df['ROLLNO'] >= prn_start) & (DLO2_df['ROLLNO'] <= prn_end)]
    DLO3_df = DLO3_df[(DLO3_df['ROLLNO'] >= prn_start) & (DLO3_df['ROLLNO'] <= prn_end)]

    # if semester == 5 or semester == 6:  #IG we dont need this kyuki yeh function tabhi call hoga jab sem 5 or 6 hoga so blueprints bhi hata dena
    teacher1_DLO_name = teachers_div2[5]['name']
    teacher1_DLO_subject = teachers_div2[5]['subject']
    teacher2_DLO_name = teachers_div2[6]['name']
    teacher2_DLO_subject = teachers_div2[6]['subject']
    teacher3_DLO_name = teachers_div2[7]['name']
    teacher3_DLO_subject = teachers_div2[7]['subject']
    new_df.loc[teacher1_subject] = analyze_grade(df, 'GRADE1')
    new_df.loc[teacher2_subject] = analyze_grade(df, 'GRADE4')
    new_df.loc[teacher3_subject] = analyze_grade(df, 'GRADE7')
    new_df.loc[teacher4_subject] = analyze_grade(df, 'GRADE10')
    new_df.loc[teacher1_DLO_subject] = analyze_DLO_grade(df, DLO1_df,'GRADE13')
    new_df.loc[teacher2_DLO_subject] = analyze_DLO_grade(df, DLO2_df,'GRADE13')
    new_df.loc[teacher3_DLO_subject] = analyze_DLO_grade(df, DLO3_df,'GRADE13')
    new_df.index.name = "Subject"
    new_df.insert(0, 'Faculty',
                      [teacher1_name, teacher2_name, teacher3_name, teacher4_name, teacher1_DLO_name,
                       teacher2_DLO_name, teacher3_DLO_name])
    return new_df
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



