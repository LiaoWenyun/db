# create_courses.py
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
		if len(row) < 4:
			print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
		code, name, term, instructor, capacity = row[0:5]
		prerequisites = row[5:] #List of zero or more items

		 
		try:
			insert_statement =cursor.mogrify("insert into offerings values( %s,%s,%s, %s,%s );",(code, name,term,instructor,capacity))
			cursor.execute(insert_statement)
			conn.commit()
	
			for item in prerequisites:
				insert_statement=cursor.mogrify("insert into prerequisites values( %s,%s, %s );",(code,term,item))
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


		#Do something with the data here
		#Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
	
conn.commit() #Remember to always commit before the program exits, since otherwise no modifications will occur
cursor.close()
conn.close()

