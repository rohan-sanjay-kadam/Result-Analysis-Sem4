# IG not needed
import pandas as pd
def kt_analysis_DLO__c(df,DLO_df):
    df = df[(df['ROLLNO'] <= '122A1070') & (df['ROLLNO'] > '122A1000')]

    No_of_students_appeared_div1=df[df['Remark'].notna()].shape[0]
    def count_kt(df, grade_columns):
        kt_counts = [df[df[grade_columns].eq("F").sum(axis=1) == i].shape[0] for i in range(1, 5)]
        return kt_counts
    def count_DLO_kt(df,DLO_df,grade_columns):
        filtered_df = df[df['ROLLNO'].isin(DLO_df['ROLLNO'])]

    kt_c_ext = count_kt(df, ["GRADE1", "GRADE4", "GRADE7", "GRADE10"])
    kt_c_int = count_kt(df, ["GRADE2", "GRADE5", "GRADE8", "GRADE11",])
    kt_c_DLO_ext = count_DLO_kt(df,DLO_df, "GRADE13")
    kt_c_DLO_int = count_DLO_kt(df, DLO_df,"GRADE14")


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
