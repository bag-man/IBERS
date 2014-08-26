import smtplib
from email.mime.text import MIMEText

def sendNotification(to, jobId):
  To = to
  From = "ClusterNotification@aber.ac.uk"

  s=smtplib.SMTP()
  s.connect('smtphost.aber.ac.uk', 587)
  s.ehlo()
  s.starttls()
  s.ehlo()
  s.login("username", "password")

  msg = MIMEText("""To view the details of your job, check the log file or run

          qacct -j """ + jobId + """ 
          
 on bert, to see more details. """)
  msg['Subject'] = "Job " + jobId + " finished"
  msg['From'] = From
  msg['To'] = To
  s.sendmail(From, To, msg.as_string())
