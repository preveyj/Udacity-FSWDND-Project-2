#testing
import psycopg2

print "Hello World!"

conn = psycopg2.connect("dbname=tournament")

if conn != None :
	print "Connection is established"
	print conn

cur = conn.cursor()

print cur

cur.execute("SELECT * FROM tbl_players;")

print cur.fetchone()

cur.close()
conn.close()