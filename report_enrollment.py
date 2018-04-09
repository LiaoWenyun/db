# report_enrollment.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
# The code below generates a mockup of the output of report_enrollment.py
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


def print_row(term_code, course_code, course_name, instructor, total_enrollment, max_cap):
        print("%6s %10s %-35s %-25s %s/%s"%(str(term_code), str(course_code), str(course_name), str(instructor), str(total_enrollment), str(max_cap)) )

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

cursor.execute("""with 
		table1 as(select course_code, term_code from grades), 
		table2 as(select course_code, term_code, count(*) from table1 group by (course_code,term_code)) 
		select term_code, course_code,course_name,instructor, count,max_cap from offerings natural join table2;""" )

rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
		break
	rows_found += 1
	term_code = row[0]
	course_code = row[1]
	course_name = row[2]
	instructor = row[3]
	total_enrollment= row[4]
	max_cap=row[5]
	print_row(term_code, course_code, course_name, instructor, total_enrollment, max_cap)



# Mockup: Print some data for a few made up classes
"""
print_row(201709, 'CSC 106', 'The Practice of Computer Science', 'Bill Bird', 203, 215)
print_row(201709, 'CSC 110', 'Fundamentals of Programming: I', 'Jens Weber', 166, 200)
print_row(201801, 'CSC 370', 'Database Systems', 'Bill Bird', 146, 150)
"""






cursor.close()
conn.close()
