import email, smtplib, ssl, getpass
import csv
import time
import art
import json
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from datetime import date
from email.mime.image import MIMEImage
from msvcrt import getch

f = (open("settings.txt", "r"))     #open and load settings in json format
x = json.loads(f.read())
f.close()

def attach_file(i):     #attach file function

    file_name_ = create_str(x["file_settings"]["file_name"][i]) #.replace("$jahr$", str(today.year)).replace("$monat$", monat[today.month - 1]).replace("$nummer$", nummer).replace("$nachname$", nachname).replace("$name$", name)
                
    file_path_ = create_str(x["file_settings"]["file_path"][i]).replace("$datei_name$", file_name_) #.replace("$jahr$", str(today.year)).replace("$monat$", monat[today.month - 1]).replace("$datei_name$", file_name_)

    with open(file_path_, "rb") as attachment:
        file = MIMEBase("application", "pdf")
        file.set_payload(attachment.read())

    encoders.encode_base64(file)

    file.add_header("Content-Disposition", "attachment", filename= f"{file_name_}")
    message.attach(file)

def attach_img(i):      #attach image function
    fp = open(x["img_settings"]["img_file_path"][i], "rb")
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header("Content-ID", x["img_settings"]["img_cid"][i])
    msgImage.add_header("Content-Disposition", "inline", filename=x["img_settings"]["img_file_name"][i])
    message.attach(msgImage)

def create_str(s):      #replace $monat$ $tag$ $jahr$ $name$ $nachname$ $datei_name$ in strings
    return s.replace("$jahr$", str(today.year)).replace("$monat$", monat[today.month - 1]).replace("$nummer$", nummer).replace("$nachname$", nachname).replace("$name$", name).replace("$tag$", str(today.day))

if x["setup_done"] == False:
    while x["setup_done"] == False:
        f = (open("settings.txt", "r"))     #reload settings to check if setup done
        x = json.loads(f.read())
        f.close()
        print("README.txt lesen und settings.txt richtig einstellen.")
        print("Wenn eingestellt mit beliebiger Taste fortfahren.")
        junk = getch()

print(art.text2art(x["name"], "random"))        # ascii art with random font

#smtp server setup from settings

smtp_server = x["smtp_settings"]["smtp"]
port = x["smtp_settings"]["smtp_port"]
sender_email = x["smtp_settings"]["sender_email"]

monat = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"] #months int>str
today = date.today()        # get current date
row_count = sum(1 for row in csv.reader(open(x["file_settings"]["csv_path"]))) - 1      # number of email recipients
mail_count = 0      # count number for mails
error_count = 0     # count number for errors

context = ssl.create_default_context()      #create ssl context

# Login try

while True:
    try:
        password = getpass.getpass(prompt="Passwort eingeben: ", stream=None)       # hidden password enter
        server = smtplib.SMTP(smtp_server, port)
        server.starttls(context=context)                                            # secure tls connection
        server.login(sender_email, password) 
    except Exception as e:
        print(e)        # print error code
        print("Versuche es in 2 Sekunden noch einmal.")
        time.sleep(2)
        continue
    break
print("Login erfolgreich, versende Emails\n\n")

with open(x["file_settings"]["csv_path"]) as file:       # open csv file
    reader = csv.reader(file)
    while True:
        next(reader)
        for name, nachname, email, nummer in reader:         # iterate through rows
            mail_count += 1
            try:
                message = MIMEMultipart("mixed")
                message["Subject"] = create_str(x["message_settings"]["subject"])   # create subject str
                message["From"] = x["message_settings"]["from"]                     # create from str
                message["To"] = email                                               # email recipient
                
                html = create_str(open(x["message_settings"]["html"], "r").read()) # html body from txt file
               
                part_html = MIMEText(html, "html") # create MIMEText html part
                
                message.attach(part_html) # attach html

                for i in range(len(x["img_settings"]["img_file_name"])):    # attach images from index in settings.txt list
                    attach_img(i)

                for i in range(len(x["file_settings"]["file_name"])):       # attach pdf files from index in settings.txt list
                    attach_file(i)

                print(f"Sende Email {mail_count}/{row_count} an {name} {nachname}")

                server.sendmail(sender_email, email, message.as_string())   # send composed emails

            except Exception as e:
                print(f"Fehler bei Email an {name} {nachname} mit Fehlermeldung: {e}") # print out errors and continue with next row in .csv
                error_count += 1
                continue
        break

if mail_count == row_count:
    print(f"\nEmail versand mit {error_count} Fehlern beendet.") # confirm sending of all emails with number of errors.
    print("\n\nDrücke eine beliebige Taste zum beenden.")
    junk = getch()
else: 
    print("Unerwarteter Fehler")
    print("\n\nDrücke eine beliebige Taste zum beenden.")
    junk = getch()
server.quit()

