import pandas as pd
def kt_analysis_c(df,prn_start,prn_end):
    df = df[(df['ROLLNO'] <= prn_end) & (df['ROLLNO'] >= prn_start)] #yeh sem5 ke liye PRN
    df.columns = df.columns.str.strip().str.upper()
    print(df.columns.tolist())
    No_of_students_appeared_div1=df[df['REMARK'].notna()].shape[0]
    print(No_of_students_appeared_div1)
    def count_kt(df, grade_columns):
        kt_counts = [df[df[grade_columns].eq("F").sum(axis=1) == i].shape[0] for i in range(1, 6)]
        return kt_counts

    kt_c_ext = count_kt(df, ["GRADE1", "GRADE4", "GRADE7", "GRADE10", "GRADE13"])
    kt_c_int = count_kt(df, ["GRADE2", "GRADE5", "GRADE8", "GRADE11", "GRADE14"])

    FAILED= kt_c_ext[0]+kt_c_ext[1]+kt_c_ext[2]+kt_c_ext[3]+kt_c_ext[4]
    TOTAL_PASS=No_of_students_appeared_div1-FAILED
    result_div1=round(TOTAL_PASS/No_of_students_appeared_div1*100,2)
    # Create KT DataFrame
    df_kt_c = pd.DataFrame({
        "Appeared": [No_of_students_appeared_div1, None],
        "Failed": [FAILED, None],
        "Pass": [TOTAL_PASS, None],
        "1KT": [kt_c_ext[0], kt_c_int[0]],
        "2KT": [kt_c_ext[1], kt_c_int[1]],
        "3KT": [kt_c_ext[2], kt_c_int[2]],
        "4KT": [kt_c_ext[3], kt_c_int[3]],
        "5KT": [kt_c_ext[4], kt_c_int[4]],
        "": ["External", "Internal"]
    })

    return df_kt_c,No_of_students_appeared_div1,TOTAL_PASS
