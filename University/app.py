from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="university1"
)

@app.route('/')
def index():
    return render_template('index.html')
   

# Add Classroom Data
@app.route('/classroom_submit', methods=['POST'])
def classroom_submit():
    if request.method == 'POST':
        building = request.form['building']
        room_number = request.form['room_number']
        capacity = request.form['capacity']
        
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM classroom WHERE building = %s AND room_number = %s", (building, room_number))
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO classroom (building, room_number, capacity) VALUES (%s, %s, %s)", (building, room_number, capacity))
            db.commit()
            return redirect('/?success=true')
        else:
            print("Duplicate entry already exists.")
            cursor.close()


        return redirect('/')

# Add Department Data
@app.route('/department_submit', methods=['POST'])
def department_submit():
    if request.method == 'POST':
        dept_name = request.form['dept_name']
        dept_building = request.form['building']  # Corrected variable name
        budget = request.form['budget']
        cursor = db.cursor()
        cursor.execute("INSERT INTO department (dept_name, building, budget) VALUES (%s, %s, %s)", (dept_name, dept_building, budget))  # Corrected variable name
        db.commit()
        cursor.close()
        return redirect('/')


# Add Course Data
@app.route('/course_submit', methods=['POST'])
def course_submit():
    if request.method == 'POST':
        course_id = request.form['course_id']
        title = request.form['title']
        dept_name = request.form['dept_name']
        credits = request.form['credits']
        
        # Check if the department exists
        cursor = db.cursor()
        cursor.execute("SELECT * FROM department WHERE dept_name = %s", (dept_name,))
        department = cursor.fetchone()
        cursor.close()
        
        if department:
            # Department exists, proceed with insertion
            cursor = db.cursor()
            cursor.execute("INSERT INTO course (course_id, title, dept_name, credits) VALUES (%s, %s, %s, %s)", (course_id, title, dept_name, credits))
            db.commit()
            cursor.close()
            return redirect('/')
        else:
            # Department does not exist, handle the error (you can redirect to an error page or show a message)
            return "Error: Department does not exist"


# Add Instructor Data
@app.route('/instructor_submit', methods=['POST'])
def instructor_submit():
    if request.method == 'POST':
        instructor_id = request.form['ID']
        name = request.form['name']
        dept_name = request.form['dept_name']
        salary = request.form['salary']
        cursor = db.cursor()
        cursor.execute("INSERT INTO instructor (ID, name, dept_name, salary) VALUES (%s, %s, %s, %s)", (instructor_id, name, dept_name, salary))
        db.commit()
        cursor.close()
        return redirect('/')

# Add Section Data
@app.route('/section_submit', methods=['POST'])
def section_submit():
    if request.method == 'POST':
        course_id = request.form['course_id']
        sec_id = request.form['sec_id']
        semester = request.form['semester']
        year = request.form['year']
        building = request.form['building']
        room_number = request.form['room_number']
        time_slot_id = request.form['time_slot_id']

        # Check if the combination of building and room_number exists in the classroom table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM classroom WHERE building = %s AND room_number = %s", (building, room_number))
        result = cursor.fetchone()
        cursor.close()

        if result:
            # The combination of building and room_number exists, proceed with insertion
            cursor = db.cursor()
            cursor.execute("INSERT INTO section (course_id, sec_id, semester, year, building, room_number, time_slot_id) VALUES (%s, %s, %s, %s, %s, %s, %s)", (course_id, sec_id, semester, year, building, room_number, time_slot_id))
            db.commit()
            cursor.close()
            return redirect('/')
        else:
            # The combination of building and room_number does not exist, handle this scenario
            return "Error: Building and room number combination does not exist in the classroom table."


# Add Teaches Data
@app.route('/teaches_submit', methods=['POST'])
def teaches_submit():
    if request.method == 'POST':
        instructor_id = request.form['ID']
        course_id = request.form['course_id']
        sec_id = request.form['sec_id']
        semester = request.form['semester']
        year = request.form['year']
        cursor = db.cursor()
        cursor.execute("INSERT INTO teaches (ID, course_id, sec_id, semester, year) VALUES (%s, %s, %s, %s, %s)", (instructor_id, course_id, sec_id, semester, year))
        db.commit()
        cursor.close()
        return redirect('/')

# Add Student Data
@app.route('/student_submit', methods=['POST'])
def student_submit():
    if request.method == 'POST':
        student_id = request.form['ID']
        name = request.form['name']
        dept_name = request.form['dept_name']
        tot_cred = request.form['tot_cred']
        cursor = db.cursor()
        cursor.execute("INSERT INTO student (ID, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)", (student_id, name, dept_name, tot_cred))
        db.commit()
        cursor.close()
        return redirect('/')

# Add Takes Data
@app.route('/takes_submit', methods=['POST'])
def takes_submit():
    if request.method == 'POST':
        # Extract form data
        student_id = request.form['ID']
        course_id = request.form['course_id']
        sec_id = request.form['sec_id']
        semester = request.form['semester']
        year = request.form['year']
        grade = request.form['grade']
        
        # Check if the student ID exists in the student table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student WHERE ID = %s", (student_id,))
        existing_student = cursor.fetchone()
        cursor.close()

        if existing_student:
            # Student ID exists, proceed with insertion
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO takes (ID, course_id, sec_id, semester, year, grade) VALUES (%s, %s, %s, %s, %s, %s)", (student_id, course_id, sec_id, semester, year, grade))
                db.commit()
                cursor.close()
                return redirect('/')
            except mysql.connector.IntegrityError as e:
                # Catch integrity error (foreign key constraint failure)
                error_message = str(e)
                return f"Error: {error_message}"
        else:
            # Student ID does not exist, handle this scenario
            return "Error: Student ID does not exist in the student table."


# Add Advisor Data
@app.route('/advisor_submit', methods=['POST'])
def advisor_submit():
    if request.method == 'POST':
        student_id = request.form['s_ID']
        instructor_id = request.form['i_ID']
        cursor = db.cursor()
        cursor.execute("INSERT INTO advisor (s_ID, i_ID) VALUES (%s, %s)", (student_id, instructor_id))
        db.commit()
        cursor.close()
        return redirect('/')

# Add Time Slot Data
@app.route('/time_slot_submit', methods=['POST'])
def time_slot_submit():
    if request.method == 'POST':
        time_slot_id = request.form['time_slot_id']
        day = request.form['day']
        start_hr = request.form['start_hr']
        start_min = request.form['start_min']
        end_hr = request.form['end_hr']
        end_min = request.form['end_min']
        cursor = db.cursor()
        cursor.execute("INSERT INTO time_slot (time_slot_id, day, start_hr, start_min, end_hr, end_min) VALUES (%s, %s, %s, %s, %s, %s)", (time_slot_id, day, start_hr, start_min, end_hr, end_min))
        db.commit()
        cursor.close()
        return redirect('/')

# Add Prerequisite Data
@app.route('/prereq_submit', methods=['POST'])
def prereq_submit():
    if request.method == 'POST':
        course_id = request.form['course_id']
        prereq_id = request.form['prereq_id']
        
        # Check if the prereq_id exists in the course_id column of the course table
        cursor = db.cursor()
        cursor.execute("SELECT * FROM course WHERE course_id = %s", (prereq_id,))
        existing_prereq = cursor.fetchone()
        cursor.close()

        if existing_prereq:
            # Prerequisite course_id exists, proceed with insertion
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO prereq (course_id, prereq_id) VALUES (%s, %s)", (course_id, prereq_id))
                db.commit()
                cursor.close()
                return redirect('/')
            except mysql.connector.IntegrityError as e:
                # Catch integrity error (foreign key constraint failure)
                error_message = str(e)
                return f"Error: {error_message}"
        else:
            # Prerequisite course_id does not exist, handle this scenario
            return "Error: Prerequisite course_id does not exist in the course table."


if __name__ == '__main__':
    app.run(debug=True)

