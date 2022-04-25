"""
Using pymysql to access the db on AWS RDS
"""

import pymysql
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

# connect to aws
conn = pymysql.connect(
        host = os.environ['HOST_NAME'],
        port = int(os.environ['PORT_NO']),
        user = os.environ['USER_NAME'],    
        password = os.environ['PASSWORD'],
        db = os.environ['DB'],
        )

# create table if not already existing (no encryption)
#cursor = conn.cursor()
#create_table = """CREATE TABLE IF NOT EXISTS UserInfo (user_id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, email VARCHAR(255) DEFAULT NULL, first_name VARCHAR(255), last_name VARCHAR(255), age FLOAT(24), gender VARCHAR(10), ochistory VARCHAR(255), medhistory VARCHAR(255), hypermetropia_level VARCHAR(10), hypermetropia_diopter float(24))"""
#cursor.execute(create_table)

# insert new user info or update existing info
# exceptions:
# return: user id if successful
def insert_user_info(email, fname, lname, gender, age, ochistory, medhistory):
    # check if username already exists or insert new user account
    with conn.cursor() as curr:
        # check if username already exists
        email = email.lower()
        #update existing record
        curr.execute("SELECT * FROM UserInfo WHERE email = %s", (email))
        user_details = curr.fetchone()
        if user_details: # if username already in use
            curr.execute("UPDATE UserInfo SET first_name = %s, last_name = %s, age = %s, gender = %s, ochistory=%s, medhistory=%s WHERE email=%s",  (fname, lname, age, gender, ochistory, medhistory, email))
            conn.commit()
            return user_details[0]
        
        # otherwise, add new user
        curr.execute("INSERT INTO UserInfo (email, first_name, last_name, age, gender, ochistory, medhistory) VALUES (%s, %s, %s, %s, %s, %s, %s)",  (email, fname, lname, age, gender, ochistory, medhistory))
        conn.commit()
        # now get user ID to return
        curr.execute("SELECT email FROM UserInfo WHERE email = %s", (email))
        new_user = curr.fetchone()
        return new_user[0]
    # if connection failed return false
    # return False

def update_user_info_hyper(email, hypermet_level, hypermet_diop):
    with conn.cursor() as curr:
        email = email.lower()
        curr.execute("SELECT * FROM UserInfo WHERE email = %s", (email))
        user_details = curr.fetchone()
        if not user_details: 
            curr.execute("INSERT INTO UserInfo (email) VALUES (%s)", (email))
            conn.commit()
        curr.execute("UPDATE UserInfo SET hypermetropia_level=%s, hypermetropia_diopter=%s WHERE email=%s",  (hypermet_level, hypermet_diop, email))
        conn.commit()
        # now get user email to return
        curr.execute("SELECT email FROM UserInfo WHERE email = %s", (email))
        new_user = curr.fetchone()
        return new_user[0]

def update_user_info_myop(email, myop_blur_idx):
    with conn.cursor() as curr:
        email = email.lower()
        curr.execute("SELECT * FROM UserInfo WHERE email = %s", (email))
        user_details = curr.fetchone()
        if not user_details: 
            curr.execute("INSERT INTO UserInfo (email) VALUES (%s)", (email))
            conn.commit()
        curr.execute("UPDATE UserInfo SET myopia_blur_idx=%s WHERE email=%s",  (myop_blur_idx, email))
        conn.commit()
        # now get user email to return
        curr.execute("SELECT email FROM UserInfo WHERE email = %s", (email))
        new_user = curr.fetchone()
        return new_user[0]

# verify record given email id
# exceptions: user does not exist
# return: email if valid
def get_user(email):
    with conn.cursor() as curr:
        # run query and get results
        curr.execute("SELECT * FROM UserInfo WHERE email = %s", (email))
        user_details = curr.fetchone()
        # details is now a map of schema names to values
        # check if row exists or password doesn't match what's in mySQL
        if not user_details:
            raise Exception('Username does not exist')
        else:
            return user_details[0]

def get_user_list():
    with conn.cursor() as curr:
        curr.execute("SELECT * FROM UserInfo")
        user_list = curr.fetchall()

        return user_list


"""
Helper Functions
"""

# get DB
def get_db():
    with conn.cursor() as curr:
        curr.execute("SELECT * database")
        table_contents = curr.fetchall()
        print(table_contents)
        
if __name__=="__main__":
    get_db()