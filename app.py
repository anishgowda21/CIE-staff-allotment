from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL
from wtforms import Form, StringField, SelectField, validators
# conn = pymysql.connect(host='localhost',user='root',password='mysql',database='DBS')
# cur = conn.cursor()

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'DBS'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)


def get_timetable(sem):
    cur = mysql.connection.cursor()
    q1 = f"SELECT * FROM {sem}"
    cur.execute(q1)
    return cur.fetchall()

def get_faculty():
    cur = mysql.connection.cursor()
    q1 = "SELECT * FROM faculty"
    cur.execute(q1)
    return cur.fetchall()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    articles = []

    return render_template("dashboard.html",articles=articles)

@app.route("/time_table/<sem>",methods = ["GET","POST"])
@app.route("/time_table",methods = ["GET","POST"])
def time_table(sem=None):
    sem_list = ['1st','2nd','3rd','4th','5th','6th','7th','8th']
    if request.method == "GET":
        if sem:
            sem = sem
            data = get_timetable(sem)
            sem_list.remove(sem)
            return render_template("time_table.html",data=data,sem=sem,list=sem_list)
        return render_template("time_table.html",list=sem_list)
    elif request.method == "POST":
        sem_list = ['1st','2nd','3rd','4th','5th','6th','7th','8th']
        sem = request.form["select-sem"]
        data = get_timetable(sem)
        sem_list.remove(sem)
        print(sem_list)
        return render_template("time_table.html",data=data,sem=sem,list=sem_list)



@app.route("/add_time_table",methods = ["GET","POST"])
def add_time_table():
    if request.method == "POST":
        sem = request.form["sem_no"]
        course_code = request.form["course-code"]
        course_name = request.form["course-name"]
        exam_start_time = request.form["exam-start-time"]
        exam_end_time = request.form["exam-end-time"]
        exam_date = request.form["exam-date"]
        fix_fac = request.form["fixed-faculties"]
        cur = mysql.connection.cursor()
        q1 = f"""INSERT INTO {sem} (course_code,course_name,exam_date,exam_start_time,exam_end_time,fixed_faculties) 
        values('{course_code}','{course_name}','{exam_date}','{exam_start_time}','{exam_end_time}','{fix_fac}')"""
        print(q1)
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Inserted to database', 'success')
        print("Inserted to db")
        return redirect(url_for("time_table",sem=sem))

        pass

@app.route("/delete_time_table",methods = ["POST"])
def delete_time_table():
    if request.method == "POST":
        rec_id = request.form["rec_id"]
        sem = request.form["sem"]
        cur = mysql.connection.cursor()
        q1 = f"DELETE FROM {sem} WHERE id = {rec_id}"
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Deleted from database', 'danger')
        print("Deleted from db")


        return redirect(url_for("time_table",sem=sem))

@app.route("/update_time_table",methods = ["POST"])
def update_time_table():
    if request.method == "POST":
        rec_id = request.form["rec_id"]
        sem = request.form["sem_no"]
        course_code = request.form["course-code"]
        course_name = request.form["course-name"]
        exam_start_time = request.form["exam-start-time"]
        exam_end_time = request.form["exam-end-time"]
        exam_date = request.form["exam-date"]
        fix_fac = request.form["fixed-faculties"]
        cur = mysql.connection.cursor()
        q1 = f"""UPDATE {sem} SET course_code = '{course_code}',course_name = '{course_name}'
        ,exam_date = '{exam_date}',exam_start_time = '{exam_start_time}',exam_end_time='{exam_end_time}',fixed_faculties='{fix_fac}' WHERE id = {rec_id}"""
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Updated the record', 'success')
        print("Updated to db")

        return redirect(url_for("time_table",sem=sem))
ch=[('1', '8am'), ('2', '10am')]

@app.route("/faculty",methods = ["GET","POST"])
def faculty():
    if request.method == "GET":
        data = get_faculty()
        return render_template("faculty.html",data=data)
    
    
    if request.method == "POST":
        fac_id = request.form["faculty-id"]
        name = request.form["faculty-name"]
        email = request.form["faculty-email"]
        phone = request.form["faculty-phone"]
        cur =   mysql.connection.cursor()
        q1 = f"INSERT INTO faculty (faculty_id,name,email,phone) values('{fac_id}','{name}','{email}','{phone}')"
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Inserted to database', 'success')
        print("Inserted to db")
        return redirect(url_for("faculty"))

@app.route("/delete_faculty",methods = ["POST"])
def delete_faculty():
    if request.method == "POST":
        fac_id = request.form["faculty-id"]
        cur = mysql.connection.cursor()
        q1 = f"DELETE FROM faculty WHERE id = '{fac_id}'"
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Deleted from database', 'danger')
        print("Deleted from db")

        return redirect(url_for("faculty"))
@app.route("/update_faculty",methods = ["POST"])
def update_faculty():
    if request.method == "POST":
        rec_id = request.form["rec_id"]
        fac_id = request.form["faculty-id"]
        name = request.form["faculty-name"]
        email = request.form["faculty-email"]
        phone = request.form["faculty-phone"]
        duties = request.form["duties-assigned"]
        q1 = f"UPDATE faculty SET faculty_id = '{fac_id}',name = '{name}',email = '{email}',phone = '{phone}',duties_assigned = {duties} WHERE id = {rec_id}"
        cur = mysql.connection.cursor()
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Updated the record', 'success')
        print("Updated to db")

        return redirect(url_for("faculty"))
if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)