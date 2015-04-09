#testing
import psycopg2

print "Hello World!"

conn = psycopg2.connect("dbname=tournament")

print conn

cur = conn.cursor()

print cur

cur.execute("SELECT * FROM tbl_players;")

print cur.fetchone()

cur.close()
conn.close()