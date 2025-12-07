import pandas as pd
def kt_analysis_d(df,prn_set):
    df.columns = df.columns.str.strip().str.upper()
    # print(df.columns.tolist())
    df['EXAM2'] = df['EXAM2'].apply(str)
    df['ROLLNO'] = df['ROLLNO'].astype(str).str.strip()
    # df = df[(~df['EXAM2'].str.contains(r'\+', na=False)) & (df['ROLLNO'] > '122A1070')] #for sem3 dyanamic karna hai PRN
    df = df[(~df['EXAM2'].str.contains(r'\+', na=False)) & (df['ROLLNO'].isin(prn_set))]

    # No_of_students_appeared_div2=df[(df['Remark'] != 'NULL') & (df['Remark'] != 'ABS') ].shape[0]
    No_of_students_appeared_div2=df[df['REMARK'].notna()].shape[0]
    def count_kt(df, grade_columns):
        df[grade_columns] = df[grade_columns].astype(str).applymap(str.strip) #applymap helps in applying function(like strip) to every single cell in dataframe
        df[grade_columns] = df[grade_columns].applymap(str.upper)
        kt_counts = [df[df[grade_columns].eq("F").sum(axis=1) == i].shape[0] for i in range(1, 6)]
        return kt_counts

    kt_d_ext = count_kt(df, ["GRADE1", "GRADE4", "GRADE7", "GRADE10", "GRADE13"])
    kt_d_int = count_kt(df, ["GRADE2", "GRADE5", "GRADE8", "GRADE11", "GRADE14"])

    # FAILED= kt_d_ext[0] + kt_d_ext[1] + kt_d_ext[2] + kt_d_ext[3] + kt_d_ext[4]
    # FAILED = sum(kt_d_ext) + sum(kt_d_int) #int nhi aayega ig sem 3,5 mai nhi tha
    FAILED = df[(df["REMARK"]=="F")].shape[0]
    TOTAL_PASS=No_of_students_appeared_div2-FAILED
    result_div2 = round(TOTAL_PASS/No_of_students_appeared_div2*100,2)
    # Create KT DataFrame
    df_kt_d = pd.DataFrame({
        "Appeared": [No_of_students_appeared_div2, None],
        "Failed": [FAILED, None],
        "Pass": [TOTAL_PASS, None],
        "1KT": [kt_d_ext[0], kt_d_int[0]],
        "2KT": [kt_d_ext[1], kt_d_int[1]],
        "3KT": [kt_d_ext[2], kt_d_int[2]],
        "4KT": [kt_d_ext[3], kt_d_int[3]],
        "5KT": [kt_d_ext[4], kt_d_int[4]],
        "": ["External", "Internal"]
    })

    return df_kt_d,No_of_students_appeared_div2,TOTAL_PASS
