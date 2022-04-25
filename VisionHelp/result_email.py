from unicodedata import name
import pymysql
import datetime 
import smtplib
from dotenv import load_dotenv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import collections
import os
# connect to aws
load_dotenv()
conn = pymysql.connect(
        host = os.environ['HOST_NAME'],
        port = int(os.environ['PORT_NO']),
        user = os.environ['USER_NAME'],    
        password = os.environ['PASSWORD'],
        db = os.environ['DB'],
        )

# test_type: 1- hypermetropia, 2- myopia 
def get_data_for_email(email, test_type=1):
    output = []
    with conn.cursor() as curr:
        if test_type ==1:
            curr.execute("SELECT email, first_name, last_name, hypermetropia_level, hypermetropia_diopter FROM UserInfo WHERE email = %s", (email))
        else:
            curr.execute("SELECT email, first_name, last_name, myopia_blur_idx FROM UserInfo WHERE email = %s", (email))
        user_details = curr.fetchone()
        output.extend(user_details())    
    print(output)
    print(output[0])
    return output

def email(data, test_type=1):

    email_id = data[0]
    fname = data[1]
    lname = data[2]
    test_type_name = "Hypermetropia" if test_type == 1 else "Myopia"
    full_name = fname + " " + lname if fname and lname else "User"
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(os.environ['EMAIL'],os.environ['SENDER_PASS'])
    
    msg = MIMEMultipart()
    html=""

    if test_type ==1:
        html = """\
            <html>
                <body style="background-color:#D4D6CF;">
                    <span style="opacity: 0"> {{ randomness }} </span>
                    <h1 style="color:#DBA40E;"> """ + str(test_type_name) + """ Vision Test Results</h1>
                    <h2 style="color:#013A20;">Hello """ + str(full_name) + """</h2>
                    <p><h3 style="color:#3F4122;">Please find your hypermetropia vision test results as follows: <br>
                        Hypermetropia Level: """+str(data[3]) + """ <br>
                        Hypermetropia Diopter: """+str(data[4]) + """ <br>
                    </h3></p>
                    <span style="opacity: 0"> {{ randomness }} </span>
                </body>
            </html>
            """
    else:
        html = """\
            <html>
                <body style="background-color:#D4D6CF;">
                    <span style="opacity: 0"> {{ randomness }} </span>
                    <h1 style="color:#DBA40E;">""" + str(test_type_name) + """ Vision Test Results</h1>
                    <h2 style="color:#013A20;">Hello """ + str(full_name) + """</h2>
                    <p><h3 style="color:#3F4122;">Please find your myopia vision test results as follows: <br>
                        Myopia Range: """+str(data[3]) + """ <br>
                    </h3></p>
                    <span style="opacity: 0"> {{ randomness }} </span>
                </body>
            </html>
            """
    temp = MIMEText(html, 'html')

    msg['From']='sai.shreyashi@gmail.com'
    msg['To']= email_id
    msg['Subject'] ="Vision Test Results"

    msg.attach(temp)
    s.send_message(msg)

    #del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def flatten(x):
    try:
        collectionsAbc = collections.abc
    except AttributeError:
        collectionsAbc = collections

    if isinstance(x, dict) :
        return [x]
    elif isinstance(x, collectionsAbc.Iterable) :
        return [a for i in x for a in flatten(i)]
    else:
        return [x]

def execute():
    #get data from database
    ans = get_data_for_email()
    
    #checks which emails to send today by comparing date and frequency
    #temp = give_emailing_rows(ans)
    
    email(ans)

if __name__ == '__main__':
    execute()