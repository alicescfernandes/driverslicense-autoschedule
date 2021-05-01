import modules.database
from modules.emails import send_email
import schedule

#config = dotenv_values(".env")
"""
Fetch the file
Check for headers update
Update the DB to the same header file
"""
send_email()
"""
If the file has changed, 
get the first 3 classes by 19h
send email
add them to the db 

"""
