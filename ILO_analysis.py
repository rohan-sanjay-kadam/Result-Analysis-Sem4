import pandas as pd
from flask import Blueprint, session
from analyze_DLO_grade import analyze_DLO_grade
from analyze_grade import analyze_grade

routes_ILO = Blueprint("ILO", __name__)


def ILO_analysis(df,n,DLO1_df,DLO2_df,DLO3_df,DLO4_df,DLO5_df,DLO6_df,ILO1_df,ILO2_df,ILO3_df,ILO4_df,prn_set):
    new_df = pd.DataFrame(columns=['E-P', 'D', 'C-O', 'TOTAL PASS', 'FAILED', 'No.of students appeared', '% OF RESULT'])
    teachers_div1 = session.get(f'teachers_div{n}')
    subjects = session.get('subjects')
    teacher1_name = teachers_div1[0]['name']
    teacher1_subject = subjects[0]['subject']
    teacher2_name = teachers_div1[1]['name']
    teacher2_subject = subjects[1]['subject']
    teacher3_name = teachers_div1[2]['name']
    teacher3_subject = subjects[2]['subject']
    teacher4_name = teachers_div1[3]['name']
    teacher4_subject = subjects[3]['subject']
    semester = session.get('semester')

    df.columns = df.columns.str.strip().str.upper()
    print(df.columns)
    df['EXAM2'] = df['EXAM2'].apply(str)

    def clean_columns(df):
        if df.empty:
            return df
        df.columns = [str(col).strip().upper() for col in df.columns] #columns ke whitespaces hata tah but sirf end ke bich ke nhi
        # like Roll No ka ROLL NO hi hoga so [No spaces allowed in column name]
        return df

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


    df = df[(~df['EXAM2'].str.contains(r'\+', na=False)) & (df['ROLLNO'].isin(prn_set))]
    print(f"DLO1df: {DLO1_df.columns}")
    if not DLO1_df.empty:
        DLO1_df = DLO1_df[(DLO1_df['ROLLNO'].isin(prn_set))] #PRN dynamic karna hai
    if not DLO2_df.empty:
        DLO2_df = DLO2_df[(DLO2_df['ROLLNO'].isin(prn_set))]
    if not DLO3_df.empty:
        DLO3_df = DLO3_df[(DLO3_df['ROLLNO'].isin(prn_set))]
    if not DLO4_df.empty:
        DLO4_df = DLO4_df[(DLO4_df['ROLLNO'].isin(prn_set))]
    if not DLO5_df.empty:
        DLO5_df = DLO5_df[(DLO5_df['ROLLNO'].isin(prn_set))]
    if not DLO6_df.empty:
        DLO6_df = DLO6_df[(DLO6_df['ROLLNO'].isin(prn_set))]

    if not ILO1_df.empty:
        ILO1_df = ILO1_df[(ILO1_df['ROLLNO'].isin(prn_set))]
    if not ILO2_df.empty:
        ILO2_df = ILO2_df[(ILO2_df['ROLLNO'].isin(prn_set))]
    if not ILO3_df.empty:
        ILO3_df = ILO3_df[(ILO3_df['ROLLNO'].isin(prn_set))]
    if not ILO4_df.empty:
        ILO4_df = ILO4_df[(ILO4_df['ROLLNO'].isin(prn_set))]

    # if semester == 5 or semester == 6:  #IG we dont need this kyuki yeh function tabhi call hoga jab sem 5 or 6 hoga so blueprints bhi hata dena
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
    teacher4_ILO_name = teachers_div1[14]['name']
    teacher4_ILO_subject = subjects[14]['subject']
    new_df.loc[teacher1_subject] = analyze_grade(df, 'GRADE1')
    new_df.loc[teacher2_subject] = analyze_grade(df, 'GRADE4')
    # new_df.loc[teacher3_subject] = analyze_grade(df, 'GRADE7')
    # new_df.loc[teacher4_subject] = analyze_grade(df, 'GRADE10') grades puure change honge 2 core 2-DLO-1_ILO
    new_df.loc[teacher1_DLO_subject] = analyze_DLO_grade(df, DLO1_df,'GRADE7') #13 ka 7 kiya
    new_df.loc[teacher2_DLO_subject] = analyze_DLO_grade(df, DLO2_df,'GRADE7')
    new_df.loc[teacher3_DLO_subject] = analyze_DLO_grade(df, DLO3_df,'GRADE7')

    new_df.loc[teacher4_DLO_subject] = analyze_DLO_grade(df, DLO4_df,'GRADE10')
    new_df.loc[teacher5_DLO_subject] = analyze_DLO_grade(df, DLO5_df,'GRADE10')
    new_df.loc[teacher6_DLO_subject] = analyze_DLO_grade(df, DLO6_df,'GRADE10')

    new_df.loc[teacher1_ILO_subject] = analyze_DLO_grade(df, ILO1_df,'GRADE13') #grade change hogaaaa assuming 16
    new_df.loc[teacher2_ILO_subject] = analyze_DLO_grade(df, ILO2_df, 'GRADE13')
    new_df.loc[teacher3_ILO_subject] = analyze_DLO_grade(df, ILO3_df, 'GRADE13')
    new_df.loc[teacher4_ILO_subject] = analyze_DLO_grade(df, ILO4_df, 'GRADE13')

    new_df.index.name = "Subject"
    new_df.insert(0, 'Faculty',
                      [teacher1_name, teacher2_name, teacher1_DLO_name,
                       teacher2_DLO_name, teacher3_DLO_name,teacher4_DLO_name,teacher5_DLO_name,teacher6_DLO_name, teacher1_ILO_name, teacher2_ILO_name, teacher3_ILO_name, teacher4_ILO_name])
    return new_df