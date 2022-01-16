from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mysqldb import MySQL
from allot import get_allot_list,clear_tables_formate
from functools import wraps
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


def get_allotment_table():
    cur = mysql.connection.cursor()
    q1 = "SELECT * FROM fin order by fac_id"
    cur.execute(q1)
    return cur.fetchall()

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

def get_sem_info(sem_type):
    cur = mysql.connection.cursor()
    q1 = f"SELECT * FROM {sem_type}_sem_info"
    cur.execute(q1)
    return cur.fetchall()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/allot_list_pub")
def allot_list_pub():
    return render_template("allot_list_pub.html",data=get_allotment_table())


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        passwd = request.form['password']
        if username == "admin" and passwd == "admin":
            session['username'] = username
            session['logged_in'] = True
            flash("Login Successful","success") 
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Credentials"
            return render_template('login.html', error=error)
    return render_template("login.html")

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("Please Login",'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route("/dashboard")
@is_logged_in
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
        print("Inside time table post")
        print(request.args.get("sem"))
        sem_list = ['1st','2nd','3rd','4th','5th','6th','7th','8th']
        sem = request.form["select-sem"]
        data = get_timetable(sem)
        sem_list.remove(sem)
        return render_template("time_table.html",data=data,sem=sem,list=sem_list)



@app.route("/add_time_table",methods = ["POST"])
@is_logged_in
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
@is_logged_in
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
@is_logged_in
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

@app.route("/faculty",methods = ["GET","POST"])
@is_logged_in
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
@is_logged_in
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
@is_logged_in
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

@app.route("/sem_info",methods=["GET","POST"])
@is_logged_in
def sem_info():
    if request.method == "GET":
        return render_template("sem_info.html")
    if request.method == "POST":
        sem_type = request.form["sem-type"]
        data = get_sem_info(sem_type.lower())
        print("outside if",sem_type)
        return render_template("sem_info.html",data=data,sem_type=sem_type)


@app.route("/update_sem_info",methods=["POST"])
@is_logged_in
def update_sem_info():
    if request.method == "POST":
        sem_type = request.form["sem-type"]
        semester = request.form["semester"]
        no_of_courses = request.form["sub"]
        ava_rooms = request.form["ava-rooms"]
        rooms = request.form["rooms"]
        print(rooms)
        duties = request.form["total-duties"]
        cur = mysql.connection.cursor()
        q1 = f"UPDATE {sem_type.lower()}_sem_info SET sub_no = {no_of_courses},ava_rooms = {ava_rooms},rooms='{rooms}',total_duties = {duties} WHERE semester = '{semester}';"
        print(q1)
        cur.execute(q1)
        mysql.connection.commit()
        cur.close()
        flash('Updated the record', 'success')
        print("Updated to db")
        print(q1)
        return redirect(url_for("sem_info"),code=307)

@app.route("/allot_list",methods=["GET","POST"])
@is_logged_in
def allot_list():
    if request.method == "GET":
        data = get_allotment_table()
        return render_template("allot_list.html",data=data,sem_type="odd")

@app.route("/create_allot_list",methods=["POST"])
@is_logged_in
def create_allot_list():
    if request.method == "POST":
        sem_type = request.form["sem-type"]
        data = get_allot_list(sem_type.lower())
        if data:
            flash(message=data,category="danger")
            return render_template("allot_list.html")
        data = get_allotment_table()
        return redirect(url_for("allot_list"))

@app.route("/delete_allot",methods=["POST"])
@is_logged_in
def delete_allot():
    if request.method == "POST":
        clear_tables_formate()
        return redirect(url_for("allot_list"))

if __name__ == "__main__":
    app.secret_key = "secret123"
    app.run(debug=True)