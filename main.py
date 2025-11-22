import pandas as pd
import xlsxwriter

new_df=pd.DataFrame()
new2_df=pd.DataFrame()
def c_div():
    df = pd.read_excel('SEM-III.xlsx')
    # # df.loc[:,['ROLLNO']]
    # # print(df.iloc[:,7])
    # # df=df.sort_values('ROLLNO')
    df=df[(df['ROLLNO']<='122A1070') & (df['ROLLNO']> '122A1000')]
    # # df=df.iloc[1:74]
    # # print(df)

    # new_df['E-P'] = None
    # new_df['D'] = None
    # new_df['C-O'] = None
    # new_df['TOTAL PASS'] = None
    # new_df['FAILED'] = None
    # new_df['No.of students appeared'] = None
    # new_df['% OF RESULT'] = None

    new_df['E-P']=df.loc[(df['GRADE1'] == "E") | (df['GRADE1']=="P"),['GRADE1']].count()
    new_df['D']=df.loc[(df['GRADE1']=="D"),['GRADE1']].count()
    new_df['C-O']=df.loc[(df['GRADE1'] == "O") | (df['GRADE1']=="A") | (df['GRADE1']=="B") | (df['GRADE1']=="C"),['GRADE1']].count()
    new_df['TOTAL PASS']= new_df['E-P']+new_df['D']+new_df['C-O']
    new_df['FAILED']=df.loc[(df['GRADE1']=="F"),['GRADE1']].count()
    new_df['No.of students appeared']=new_df['TOTAL PASS']+new_df['FAILED']
    new_df['% OF RESULT']=(new_df['TOTAL PASS']/new_df['No.of students appeared']*100).round(2)




    #
    # E_P_GRADE4 = df.loc[(df['GRADE4'] == "E") | (df['GRADE4'] == "P"), ['GRADE4']].count()
    # D_GRADE4 = df.loc[df['GRADE4'] == "D", ['GRADE4']].count()
    # C_O_GRADE4 = df.loc[(df['GRADE4'] == "O") | (df['GRADE4'] == "A") | (df['GRADE4'] == "B") | (df['GRADE4'] == "C"), ['GRADE4']].count()
    # TOTAL_PASS_GRADE4 = E_P_GRADE4 + D_GRADE4 + C_O_GRADE4
    # FAILED_GRADE4 = df.loc[df['GRADE4'] == "F", ['GRADE4']].count()
    # No_of_students_in_GRADE4=TOTAL_PASS_GRADE4+FAILED_GRADE4
    # percent_result=(TOTAL_PASS_GRADE4/No_of_students_in_GRADE4*100).round(2)
    # new_df.loc['GRADE4']=[[E_P_GRADE4],[D_GRADE4],[C_O_GRADE4],[TOTAL_PASS_GRADE4],[FAILED_GRADE4],[No_of_students_in_GRADE4],[percent_result]]
    # print(new_df)





    def analyze_grade(df, grade_column):
        E_P = df.loc[(df[grade_column] == "E") | (df[grade_column] == "P"), [grade_column]].shape[0]
        D = df.loc[df[grade_column] == "D", [grade_column]].shape[0]
        C_O = df.loc[
            (df[grade_column] == "O") | (df[grade_column] == "A") | (df[grade_column] == "B") | (df[grade_column] == "C"), [
                grade_column]].shape[0]
        TOTAL_PASS = E_P + D + C_O
        FAILED = df.loc[df[grade_column] == "F", [grade_column]].shape[0]
        No_of_students = TOTAL_PASS + FAILED
        percent_result = (TOTAL_PASS / No_of_students * 100)
        # print(f"Grade Column: {grade_column}")
        # print(
        #     f"E_P: {E_P}, D: {D}, C_O: {C_O}, TOTAL_PASS: {TOTAL_PASS}, FAILED: {FAILED}, No_of_students: {No_of_students},percenr_result:{percent_result}")
        return {
            'E-P': E_P,
            'D': D,
            'C-O': C_O,
            'TOTAL PASS': TOTAL_PASS,
            'FAILED': FAILED,
            'No.of students appeared': No_of_students,
            '% OF RESULT': round(percent_result,2)
        }
    # new_df.loc['Maths'] = analyze_grade(df, 'GRADE1')

    new_df.loc['GRADE4'] = analyze_grade(df, 'GRADE4')
    new_df.loc['GRADE7'] = analyze_grade(df, 'GRADE7')
    new_df.loc['GRADE10'] = analyze_grade(df, 'GRADE10')
    new_df.loc['GRADE13'] = analyze_grade(df, 'GRADE13')


def d_div():
    df = pd.read_excel('SEM-III.xlsx')
    df['exam2'] = df['exam2'].apply(str)
    df = df[(~df['exam2'].str.contains(r'\+', na=False)) & (df['ROLLNO'] > '122A1070')]
    new2_df['E-P'] = df.loc[(df['GRADE1'] == "E") | (df['GRADE1'] == "P"), ['GRADE1']].count()
    new2_df['D'] = df.loc[(df['GRADE1'] == "D"), ['GRADE1']].count()
    new2_df['C-O'] = df.loc[
        (df['GRADE1'] == "O") | (df['GRADE1'] == "A") | (df['GRADE1'] == "B") | (df['GRADE1'] == "C"), [
            'GRADE1']].count()
    new2_df['TOTAL PASS'] = new2_df['E-P'] + new2_df['D'] + new2_df['C-O']
    new2_df['FAILED'] = df.loc[(df['GRADE1'] == "F"), ['GRADE1']].count()
    new2_df['No.of students appeared'] = new2_df['TOTAL PASS'] + new2_df['FAILED']
    new2_df['% OF RESULT'] = (new2_df['TOTAL PASS'] / new2_df['No.of students appeared'] * 100).round(2)
    def analyze_grade(df, grade_column):
        E_P = df.loc[(df[grade_column] == "E") | (df[grade_column] == "P"), [grade_column]].shape[0]
        D = df.loc[df[grade_column] == "D", [grade_column]].shape[0]
        C_O = df.loc[
            (df[grade_column] == "O") | (df[grade_column] == "A") | (df[grade_column] == "B") | (df[grade_column] == "C"), [
                grade_column]].shape[0]
        TOTAL_PASS = E_P + D + C_O
        FAILED = df.loc[df[grade_column] == "F", [grade_column]].shape[0]
        No_of_students = TOTAL_PASS + FAILED
        percent_result = (TOTAL_PASS / No_of_students * 100)
        # print(f"Grade Column: {grade_column}")
        # print(
        #     f"E_P: {E_P}, D: {D}, C_O: {C_O}, TOTAL_PASS: {TOTAL_PASS}, FAILED: {FAILED}, No_of_students: {No_of_students},percenr_result:{percent_result}")
        return {
            'E-P': E_P,
            'D': D,
            'C-O': C_O,
            'TOTAL PASS': TOTAL_PASS,
            'FAILED': FAILED,
            'No.of students appeared': No_of_students,
            '% OF RESULT': round(percent_result,2)
        }
    # new_df.loc['Maths'] = analyze_grade(df, 'GRADE1')

    new2_df.loc['GRADE4'] = analyze_grade(df, 'GRADE4')
    new2_df.loc['GRADE7'] = analyze_grade(df, 'GRADE7')
    new2_df.loc['GRADE10'] = analyze_grade(df, 'GRADE10')
    new2_df.loc['GRADE13'] = analyze_grade(df, 'GRADE13')

c_div()
d_div()
excel_file='RESULT.xlsx'
with pd.ExcelWriter(excel_file,engine='xlsxwriter') as writer:
    new_df.to_excel(writer, index=True, sheet_name='SEM-3 SH2023')
    new2_df.to_excel(writer,index=True,sheet_name='SEM-3 SH2023',startrow=30)
# workbook=xlsxwriter.Workbook(new_df)
# first=workbook.add_worksheet('C-div')
# workbook.add_worksheet('D-div')
# print(workbook.sheetnames)
# print(new_df)
#
# print(new2_df)
# new_df.to_excel('Result_work2.xlsx')
