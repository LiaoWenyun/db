# add_drop.py
# CSC 370 - Spring 2018 - Starter code for Assignment 4
#
#
# B. Bird - 02/26/2018

import sys, csv, psycopg2



if len(sys.argv) < 2:
	print("Usage: %s <input file>",file=sys.stderr)
	sys.exit(0)
	
input_filename = sys.argv[1]

# Open your DB connection here

psql_user = 'wenyun' #Change this to your username
psql_db = 'wenyun' #Change this to your personal DB name
psql_password = 'msdj23-1' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

with open(input_filename) as f:
	for row in csv.reader(f):
		if len(row) == 0:
			continue #Ignore blank rows
		if len(row) != 5:
			print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
		add_or_drop,student_id,student_name,course_code,term = row
		try:
		
			
			insert_statement = cursor.mogrify("insert into student values( %s, %s );", (student_id, student_name))
			cursor.execute(insert_statement)
			conn.commit() 
			
		except psycopg2.ProgrammingError as err:
			print("Caught a ProgrammingError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.IntegrityError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		except psycopg2.InternalError as err:
			print("Caught an IntegrityError:",file=sys.stderr)
			print(err,file=sys.stderr)
			conn.rollback()
		finally:
			try:
				if row[0]=="ADD":
					cursor.execute("insert into grades values( %s, %s, %s );",(student_id, course_code,int(term)))
					conn.commit() 
				elif row[0]=="DROP":
					drop_class=cursor.mogrify("delete from grades WHERE student_id=%s and course_code=%s and term_code=%s and grade is null;",(student_id, course_code,term))
					cursor.execute(drop_class)			
					conn.commit()	
	
			except psycopg2.ProgrammingError as err: 
				print("Caught a ProgrammingError:",file=sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()	
			except psycopg2.IntegrityError as err: 
				print("Caught an IntegrityError:",file=sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()
			except psycopg2.InternalError as err:
				print("Caught an IntegrityError:",file=sys.stderr)
				print(err,file=sys.stderr)
				conn.rollback()

		#Do something with the data here
		#Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
	
conn.commit() #Remember to always commit before the program exits, since otherwise no modifications will occur
cursor.close()
conn.close()

