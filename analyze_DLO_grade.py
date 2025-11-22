def analyze_DLO_grade(df,DLO_df, grade_column):
        df = df.copy()
        if DLO_df.empty:
            return {
                'E-P': None,
                'D': None,
                'C-O': None,
                'TOTAL PASS': None,
                'FAILED': None,
                'No.of students appeared': None,
                '% OF RESULT': None
            }
        print("Unique grades before filtering:", df[grade_column].unique())
        df[grade_column] = df[grade_column].astype(str).str.strip().str.upper()
        df['ROLLNO'] = df['ROLLNO'].astype(str).str.strip() #Converts the rollno column to string and strips whitespaces
        DLO_df['ROLLNO'] = DLO_df['ROLLNO'].astype(str).str.strip()
        df = df[df[grade_column].isin(['E', 'P', 'D', 'C', 'B', 'A', 'O', 'F'])]
        df = df[df['ROLLNO'].isin(DLO_df['ROLLNO'])] # This only keeps the row where rollno matches
        print("Unique grades after filtering:", df[grade_column].unique())


        # if DLO_df['ROLLNO'] == df['ROLLNO']:
        # filtered_df = df.loc[df[grade_column].isin(["E", "P"]), ["ROLLNO", "NAME", grade_column]]
        # print("E_P ke rows")
        filtered_df = df.loc[df[grade_column].isin(["O","A","B","C"]), ["ROLLNO", "NAME", grade_column]]
        print(filtered_df)

        # E_P = df.loc[(df[grade_column] == "E") | (df[grade_column] == "P"), [grade_column]].shape[0]
        # .loc gives the data not just count means it will also give rows and columns ex below
        #       GRADE
        # 0     E
        # 3     P
        # 7     P
        E_P = df[df[grade_column].isin(["E","P"])].shape[0] #This gives the actual count like 3 4 instead of the data like above
        D = df.loc[df[grade_column] == "D", [grade_column]].shape[0]
        # C_O = df.loc[
        #     (df[grade_column] == "O") | (df[grade_column] == "A") | (df[grade_column] == "B") | (
        #             df[grade_column] == "C"), [
        #         grade_column]].shape[0]
        C_O = df[df[grade_column].isin(["O","A","B","C"])].shape[0]
        TOTAL_PASS = E_P + D + C_O
        FAILED = df.loc[df[grade_column] == "F", [grade_column]].shape[0]
        No_of_students = TOTAL_PASS + FAILED
        print("Failed",FAILED)
        print("Total Pass",TOTAL_PASS)
        print("No of students",No_of_students)
        missing_rollno = "121A1058"

        # Filter rows with that rollno
        filtered = df[df['ROLLNO'] == missing_rollno]

        if not filtered.empty and grade_column in filtered.columns:
            grade_value = filtered[grade_column].values[0]
            print("Raw grade value:", repr(grade_value))
        else:
            print(f"ROLLNO {missing_rollno} not found in DataFrame or grade column missing.")
        percent_result = (TOTAL_PASS / No_of_students * 100)

        return {
            'E-P': E_P,
            'D': D,
            'C-O': C_O,
            'TOTAL PASS': TOTAL_PASS,
            'FAILED': FAILED,
            'No.of students appeared': No_of_students,
            '% OF RESULT': round(percent_result, 2)
        }