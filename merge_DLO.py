from pandas import *
from Models import GradeReport,KtReport,db
from analyze_DLO_grade import analyze_DLO_grade
import pandas as pd
from flask import Blueprint,session
routes_merging_DLO = Blueprint("merge_DLO", __name__)
def merg_DLO(df,DLO1_df,DLO2_df,DLO3_df):
    sub = session.get('subjects', [])
    # subjects=[sub[n]['subject'] for n in range(0,8)] subject 5 bhi ara tha jo ki empty hai
    #DATABASE CLEAN KARNA HAI EK WITHOUT SUBJECT VALUE HAI!!!

    subjects=[
        sub[0]['subject'],
        sub[1]['subject'],
        sub[2]['subject'],
        sub[3]['subject'],
        sub[5]['subject'],
        sub[6]['subject'],
        sub[7]['subject']
    ]
    grades = ["GRADE1", "GRADE4", "GRADE7", "GRADE10"] #for calculating percentage DLO ka alag lagega isiliye no GRADE13
    all_grades = ["GRADE1", "GRADE4", "GRADE7", "GRADE10","GRADE13"] #for calculating kt's
    internal_grades = ["GRADE2", "GRADE5", "GRADE8", "GRADE11", "GRADE14"]


    year=session.get("year")
    prev_year=f'{int(year.split("-")[0])-1}-{year.split("-")[0]}'
    branch=session.get('branch').lower()
    sem=session.get('semester')


    df=df[~(df['EXAM2'].str.contains(r'\+',na=False))&~(df['EXAMTOTAL'].isnull())]
    total_students=df.shape[0]
    def analyze_subject(df, grade_column):
        df.loc[:,grade_column] = df[grade_column].astype(str).str.strip().str.upper() #used .loc cus pandas dont understand whether its a slice or copy
        total_students = df[df[grade_column].notna()].shape[0]
        ep =round (((df[df[grade_column].isin(["E", "P"])].shape[0])/total_students)*100,2)
        d = round(((df[df[grade_column] == "D"].shape[0])/total_students)*100,2)
        co = round(((df[df[grade_column].isin(["C", "B", "A", "O"])].shape[0])/total_students)*100,2)
        total = round(ep+d+co,2)
        return ep, d, co, total
    def analyze_DLO_subject(DLO_df):
        first_DLO_row = analyze_DLO_grade(df,DLO_df,"GRADE13")
        total_number_of_DLO_students = first_DLO_row["No.of students appeared"]
        ep = round((first_DLO_row["E-P"]/total_number_of_DLO_students)*100,2)
        d = round((first_DLO_row["D"] / total_number_of_DLO_students) * 100, 2)
        co = round((first_DLO_row["C-O"] / total_number_of_DLO_students) * 100, 2)
        total = round(ep+d+co,2)
        return ep,d,co,total
    analysis=[analyze_subject(df,grade) for grade in grades]

    # CreateD a helper to handle empty dataframes like if DLO2_df is empty sheet so it will return none
    def safe_analyze(DLO_df):
        return analyze_DLO_subject(DLO_df) if not DLO_df.empty else (None, None, None, None)
    analysis.append(safe_analyze(DLO1_df))
    analysis.append(safe_analyze(DLO2_df))
    analysis.append(safe_analyze(DLO3_df))
    curr_data_df = DataFrame({
        "subject": subjects,
        "40%-49%": [x[0] for x in analysis],
        "50%-59%": [x[1] for x in analysis],
        "Above 60%": [x[2] for x in analysis],
        "Total": [x[3] for x in analysis]

    })
    def count_kt(df, grade_columns,internal_grades):
        # kt_counts = [df[df[grade_columns].eq("F").sum(axis=1) == i].shape[0] for i in range(1, 6)]
        kt_counts = [df[(((df[grade_columns]).eq("F"))|((df[internal_grades]).eq("F"))).sum(axis=1) == i].shape[0] for i in range(1, 6)]
        return kt_counts

    curr_failed=df[(df["REMARK"]=="F")].shape[0]
    curr_allclear=total_students-curr_failed
    kt_analysis=count_kt(df,all_grades,internal_grades)
    curr_kt_df= DataFrame({
        "Appeared": [total_students],
        "Failed": [curr_failed],
        "All Clear": [curr_allclear],
        "1KT": [kt_analysis[0]],
        "2KT": [kt_analysis[1]],
        "3KT": [kt_analysis[2]],
        "4KT": [kt_analysis[3]],
        "5KT": [kt_analysis[4]],
        # "6KT": [kt_analysis[5]]
    })
    grade_rows = []
    #There has to be better way timebeing ke liye aise kiya
    from app import app
    with app.app_context():

        # for index,rows in curr_data_df.iterrows():
        #     grade_rows.append(GradeReport(academic_year=year, semester=sem,subject=rows["subject"], _40_49=rows["40%-49%"], _50_59=rows["50%-59%"], above_60=rows["Above 60%"], total=rows["Total"]))
        for _, row in curr_data_df.iterrows():
            subject = row["subject"]
            val_40_49 = None if pd.isna(row["40%-49%"]) else row["40%-49%"] #did this to give/make the values null
            val_50_59 = None if pd.isna(row["50%-59%"]) else row["50%-59%"]
            val_above_60 = None if pd.isna(row["Above 60%"]) else row["Above 60%"]
            val_total = None if pd.isna(row["Total"]) else row["Total"]

            existing = GradeReport.query.filter_by(
                academic_year=year,
                semester=sem,
                subject=subject
            ).first()

            if existing:
                # Compare all values
                if (
                        existing._40_49 != val_40_49 or
                        existing._50_59 != val_50_59 or
                        existing.above_60 != val_above_60 or
                        existing.total != val_total
                ):
                    # Only update if something changed
                    existing._40_49 = val_40_49
                    existing._50_59 = val_50_59
                    existing.above_60 = val_above_60
                    existing.total = val_total
                    db.session.commit()
                    print(f"Updated: {subject}")
                else:
                    print(f"No change for: {subject}")
            else:
                # Insert new row
                new_row = GradeReport(
                    academic_year=year,
                    semester=sem,
                    subject=subject,
                    _40_49=val_40_49,
                    _50_59=val_50_59,
                    above_60=val_above_60,
                    total=val_total
                )
                db.session.add(new_row)
                db.session.commit()
                print(f"Inserted: {subject}")
                print(new_row)

        for index, rows in curr_kt_df.iterrows():
            existing = KtReport.query.filter_by(
                academic_year=year,
                semester=sem
            ).first()
            if existing:
                if (
                        existing.appeared != int(rows["Appeared"]) or
                        existing.failed != int(rows["Failed"]) or
                        existing.all_clear != int(rows["All Clear"]) or
                        existing.kt1 != int(rows["1KT"]) or
                        existing.kt2 != int(rows["2KT"]) or
                        existing.kt3 != int(rows["3KT"]) or
                        existing.kt4 != int(rows["4KT"]) or
                        existing.kt5 != int(rows["5KT"])

                ):
                    # Only update if something changed
                    existing.appeared = int(rows["Appeared"])
                    existing.failed = int(rows["Failed"])
                    existing.all_clear = int(rows["All Clear"])
                    existing.kt1 = int(rows["1KT"])
                    existing.kt2 = int(rows["2KT"])
                    existing.kt3 = int(rows["3KT"])
                    existing.kt4 = int(rows["4KT"])
                    existing.kt5 = int(rows["5KT"])
                    db.session.commit()
                    print("Updated the kt database:")
                else:
                    print("No change for kt database")
            else:
                kt_row = KtReport(academic_year=year, semester=sem, appeared=int(rows["Appeared"]),
                                  failed=int(rows["Failed"]), all_clear=int(rows["All Clear"]), kt1=int(rows["1KT"]),
                                  kt2=int(rows["2KT"]), kt3=int(rows["3KT"]), kt4=int(rows["4KT"]),
                                  kt5=int(rows["5KT"]))
                # db.session.add_all(grade_rows)
                db.session.add(kt_row)
                db.session.commit()


    #previous database se data lera
    prev_data = GradeReport.query.filter_by(academic_year=prev_year,semester=sem).order_by(GradeReport.id).all()
    prev_kt = KtReport.query.filter_by(academic_year=prev_year,semester=sem).first()
    previous_data = []
    for row in prev_data:
        previous_data.append({
            "subject":row.subject,
            "40%-49%":row._40_49,
            "50%-59%":row._50_59,
            "Above 60%":row.above_60,
            "Total":row.total
        })
    prev_data_df = pd.DataFrame(previous_data)

    prev_kt_df = DataFrame({
        "Appeared": [prev_kt.appeared],
        "Failed": [prev_kt.failed],
        "All Clear": [prev_kt.all_clear],
        "1KT": [prev_kt.kt1],
        "2KT": [prev_kt.kt2],
         "3KT": [prev_kt.kt3],
        "4KT": [prev_kt.kt4],
        "5KT": [prev_kt.kt5]
    })
    prev_total_students = int(prev_kt_df["Appeared"].iloc[0])
    prev_perc_result = int(round((prev_kt_df["All Clear"].iloc[0]/prev_total_students)*100,2))

    difference = curr_data_df.iloc[:,1:] - prev_data_df.iloc[:,1:]


    curr_perc_result=round((curr_allclear/total_students)*100,2)

    return curr_data_df,prev_data_df,difference,curr_kt_df,prev_kt_df,total_students,prev_total_students,curr_perc_result,prev_perc_result,prev_year
