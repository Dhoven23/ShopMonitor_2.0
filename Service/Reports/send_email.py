import smtplib
from datetime import date
from email.message import EmailMessage


def main():
    EMAIL_ADDRESS = 'engineeringshop.gcu@gmail.com'
    EMAIL_PASSWORD = 'gcuengineering'

    msg = EmailMessage()
    msg['Subject'] = f'{date.today()} Weekly Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'Daniel.Hoven@gcu.edu'
    msg.set_content('Sent Attachment')
    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:Purple;">Weekly Report</h1>
        </body>
    </html>
    """, subtype='html')

    with open(f"Service/Reports/{date.today()}_report.docx", 'rb') as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype='application', subtype='msword', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        smtp.send_message(msg)


def send_weekly_report():
    main()

