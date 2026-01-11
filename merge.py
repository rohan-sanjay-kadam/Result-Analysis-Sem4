from pandas import *
from Models import GradeReport,KtReport,db
import pandas as pd
from flask import Blueprint,session
import logging

# Basic configuration
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
routes_merging = Blueprint("merge", __name__)
def merg(df):
    sub = session.get('subjects', [])
    subjects=[sub[n]['subject'] for n in range(0,5)]
    grades = ["GRADE1", "GRADE4", "GRADE7", "GRADE10", "GRADE13"]
    internal_grades = ["GRADE2", "GRADE5", "GRADE8", "GRADE11", "GRADE14"]
    pairs = [
        ('GRADE1', 'GRADE2'),
        ('GRADE4', 'GRADE5'),
        ('GRADE7', 'GRADE8'),
        ('GRADE10', 'GRADE11'),
        ('GRADE13', 'GRADE14')
    ]
    year=session.get("year")
    prev_year=f'{int(year.split("-")[0])-1}-{year.split("-")[0]}'
    branch=session.get('branch').upper()
    sem=session.get('semester')

    print("Merge wala")
    df.columns = df.columns.str.upper().str.replace(" ", "", regex=False).str.replace("_", "", regex=False)
    print(df.columns.tolist())
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
    analysis=[analyze_subject(df,grade) for grade in grades]
    curr_data_df = DataFrame({
        "subject": subjects,
        "40%-49%": [x[0] for x in analysis],
        "50%-59%": [x[1] for x in analysis],
        "Above 60%": [x[2] for x in analysis],
        "Total": [x[3] for x in analysis]

    })

    def count_kt(df, pairs):
        kt_count = 0
        for ext, inte in pairs:
            kt_count += (df[ext].eq("F") | df[inte].eq("F"))

        return [(kt_count == i).sum() for i in range(1, 6)]

    curr_failed=df[(df["REMARK"]=="F")].shape[0]
    curr_allclear=total_students-curr_failed
    kt_analysis=count_kt(df,pairs)
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

            existing = GradeReport.query.filter_by(
                academic_year=year,
                semester=sem,
                subject=subject,
                branch=branch
            ).first()

            if existing:
                # Compare all values
                if (
                        existing._40_49 != row["40%-49%"] or
                        existing._50_59 != row["50%-59%"] or
                        existing.above_60 != row["Above 60%"] or
                        existing.total != row["Total"]
                ):
                    # Only update if something changed
                    existing._40_49 = row["40%-49%"]
                    existing._50_59 = row["50%-59%"]
                    existing.above_60 = row["Above 60%"]
                    existing.total = row["Total"]
                    print(f"Updated: {subject}")
                else:
                    print(f"No change for: {subject}")
            else:
                # Insert new row
                new_row = GradeReport(
                    academic_year=year,
                    semester=sem,
                    subject=subject,
                    branch=branch,
                    _40_49=row["40%-49%"],
                    _50_59=row["50%-59%"],
                    above_60=row["Above 60%"],
                    total=row["Total"]
                )
                db.session.add(new_row)
                db.session.commit()
                print(f"Inserted: {subject}")
                print(new_row)

        for index, rows in curr_kt_df.iterrows():
            existing = KtReport.query.filter_by(
                academic_year=year,
                semester=sem,
                branch=branch
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
                    print("Updated the kt database:")
                else:
                    print("No change for kt database")
            else:
                kt_row = KtReport(academic_year=year, semester=sem,branch=branch, appeared=int(rows["Appeared"]),
                                  failed=int(rows["Failed"]), all_clear=int(rows["All Clear"]), kt1=int(rows["1KT"]),
                                  kt2=int(rows["2KT"]), kt3=int(rows["3KT"]), kt4=int(rows["4KT"]),
                                  kt5=int(rows["5KT"]))
                # db.session.add_all(grade_rows)
                db.session.add(kt_row)
                db.session.commit()


    #previous database se data lera
    prev_data = GradeReport.query.filter_by(academic_year=prev_year,semester=sem,branch=branch).order_by(GradeReport.id).all()
    # prev_data = GradeReport.query.filter_by(academic_year=prev_year,semester=sem).all()

    prev_kt = KtReport.query.filter_by(academic_year=prev_year,semester=sem,branch=branch).first()
    previous_data = []
    for row in prev_data:
        previous_data.append({
            # "id":row.id,
            "subject":row.subject,
            "40%-49%":row._40_49,
            "50%-59%":row._50_59,
            "Above 60%":row.above_60,
            "Total":row.total
        })
        # I was dumb that's why i added this spent 2 weeks debugging this a error found out i was debugging the wrong module:)
    # "Merge_ILO" edit karna tha mai "merge" karra the:))
    prev_data_df = pd.DataFrame(previous_data)
    # prev_data_df["id"] = prev_data_df["id"].astype(int)
    # prev_data_df = prev_data_df.sort_values(by="id",kind="stable")
    # baadmai drop karna id column
    # prev_data_df = prev_data_df.drop(columns=["id"])

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
    prev_total_students = int(prev_kt_df["Appeared"].iloc[0] ) #int mai covert kiya cus NUMPY:INT64 MAI THA VALUE used
    prev_perc_result = int(round((prev_kt_df["All Clear"].iloc[0]/prev_total_students)*100,2)) #iloc[0] to select first row only even though it has only one row warning ara tha isiliye.
    difference = curr_data_df.iloc[:,1:] - prev_data_df.iloc[:,1:]


    curr_perc_result=round((curr_allclear/total_students)*100,2)

    return curr_data_df,prev_data_df,difference,curr_kt_df,prev_kt_df,total_students,prev_total_students,curr_perc_result,prev_perc_result,prev_year
