import smtplib
from email.mime.text import MIMEText

# Configuration
sender = "caissefildiwan@gmail.com"
app_password = "ofim wfsl fpdl hxlt"
recipients = ["hugo@ternet.fr"]  # ou plusieurs adresses

# Contenu du message
subject = "Sujet de l'email"
body = "Bonjour,\n\nVoici un message envoyé depuis un script Python."

# Construction du message
msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = ", ".join(recipients)

# Envoi via SMTP SSL
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(sender, app_password)
    smtp.sendmail(sender, recipients, msg.as_string())

print("Email envoyé !")
