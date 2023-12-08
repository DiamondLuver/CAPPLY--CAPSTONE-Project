import sqlite3

# conn = sqlite3.connect('src/db.sqlite3')
# c = conn.cursor()
# c.execute('''INSERT INTO category_country VALUES(?,?,?) SELECT country FROM category_scholarship GROUP BY country;''',(None, name, None))
            
# conn.commit()
# print('complete.')

# #close connection
# conn.close()
# import pymysql

# Connect to the database
conn = sqlite3.connect('src/db.sqlite3')

# Create a cursor
cursor = conn.cursor()

# Execute the SQL query
# cursor.execute("INSERT INTO category_country (name)  SELECT country FROM category_scholarship GROUP BY country ;")

cursor.execute("INSERT INTO category_level (name)  SELECT level FROM category_scholarship GROUP BY level ;")


# cursor.execute("ALTER TABLE category_scholarship ADD COLUMN country_id int;")

# Commit the changes to the database
conn.commit()

# Close the connection
conn.close()