# report_classlist.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_classlist.py
# as specified in the assignment. You can copy and paste the functions in this
# program into your solution to ensure the correct formatting.
#
# B. Bird - 02/26/2018

import psycopg2, sys

psql_user = 'wenyun' #Change this to your username
psql_db = 'wenyun' #Change this to your personal DB name
psql_password = 'msdj23-1' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)) )
	print("  Term %s"%(str(term), ) )
	print("  Instructor: %s"%(str(instructor_name), ) )
	
def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)) )
	else:
		print("%10s %-25s"%(str(student_id), str(student_name),) )

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity)) )

if len(sys.argv) < 3:
        print('Usage: %s <course code> <term>'%sys.argv[0], file=sys.stderr)
        sys.exit(0)
        
course_code, term_code = sys.argv[1:3]

cursor.execute("""with
			table1 as(select course_code, term_code from grades), 
			table2 as(select course_code, term_code, count(*) from table1 group by (course_code,term_code)) ,
			table3 as(select course_code,term_code,course_name,instructor, count,max_cap from offerings natural join table2 where course_code=%s and term_code=%s),
			table4 as(select course_code,term_code,course_name,student_id,grade, instructor, count, max_cap from table3 natural join grades)
			select course_code,term_code,course_name, student_id, student_name,grade, instructor, count, max_cap from table4 natural join student;

			   """, (course_code,term_code) )

rows_found = 0
count =0
while True:
	count =count+1
	row = cursor.fetchone()
	if row is None:
		break
	rows_found += 1
	course_code=row[0]
	term=row[1]
	course_name = row[2]
	student_id = row[3]
	student_name = row[4]
	grade = row[5]
	instructor=row[6]
	total_enrolled=row[7]
	max_cap=row[8]
	if count==1:	
		print_header(course_code, course_name, term, instructor)
	print_row(student_id, student_name, grade)
	
print_footer(total_enrolled, max_cap)

"""
# Mockup: Print a class list for CSC 370
course_code = 'CSC 370'
course_name = 'Database Systems'
course_term = 201801
instructor_name = 'Bill Bird'
print_header(course_code, course_name, course_term, instructor_name)

#Print records for a few students
print_row('V00123456', 'Rebecca Raspberry', 81)
print_row('V00123457', 'Alissa Aubergine', 90)
print_row('V00123458', 'Neal Naranja', 83)

#Print the last line (enrollment/max_capacity)
print_footer(3,150)
"""


cursor.close()
conn.close()
