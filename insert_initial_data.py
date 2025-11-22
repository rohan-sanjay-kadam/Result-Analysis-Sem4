from Models import db, GradeReport, KtReport
from flask import Flask
import urllib.parse

app = Flask(__name__)
# githup pr save nhi karna password hai isme
password = urllib.parse.quote_plus("Sujirohan@7")

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost/sem4_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()  # creates tables if not present

    grade_rows = [
        GradeReport(academic_year="22-23", semester=5,subject="TCS", _40_49=14.60, _50_59=20.44, above_60=62.77, total=97.81),
        GradeReport(academic_year="22-23", semester=5,subject="SE", _40_49=5.84, _50_59=10.22, above_60=83.94, total=100.00),
        GradeReport(academic_year="22-23", semester=5,subject="CN", _40_49=21.90, _50_59=23.36, above_60=54.01, total=99.27),
        GradeReport(academic_year="22-23", semester=5,subject="DWM", _40_49=7.30, _50_59=13.87, above_60=78.83, total=100.00),
        GradeReport(academic_year="22-23", semester=5,subject="PGM", _40_49=37.50, _50_59=17.50, above_60=45.00, total=100.00),
        GradeReport(academic_year="22-23", semester=5,subject="IP", _40_49=61.64, _50_59=20.55, above_60=13.70, total=95.89),
        GradeReport(academic_year="22-23", semester=5,subject="ADBMS", _40_49=75.00, _50_59=12.5, above_60=12.50, total=100.00)
    ]
    kt_row = KtReport(appeared=137, failed=7, all_clear=130, kt1=3, kt2=2, kt3=0, kt4=0, kt5=0)

    db.session.add_all(grade_rows)
    db.session.add(kt_row)
    db.session.commit()

    print("✅ Data inserted.")
