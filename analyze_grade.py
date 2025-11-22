def analyze_grade(df, grade_column):
    df = df.copy()
    df[grade_column] = df[grade_column].astype(str).str.strip().str.upper() #strips whitespaces and makes it uppercase
    df = df[df[grade_column].isin(['E', 'P', 'D', 'C', 'B', 'A', 'O', 'F'])]
    E_P = df.loc[(df[grade_column] == "E") | (df[grade_column] == "P"), [grade_column]].shape[0]
    D = df.loc[df[grade_column] == "D", [grade_column]].shape[0]
    C_O = df.loc[
        (df[grade_column] == "O") | (df[grade_column] == "A") | (df[grade_column] == "B") | (
                df[grade_column] == "C"), [
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
        '% OF RESULT': round(percent_result, 2)
    }