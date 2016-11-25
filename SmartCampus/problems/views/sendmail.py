from django.http.response import HttpResponse
from django.core.mail.message import EmailMessage

def sendmail(request):
    
    
    subject ="test"
    message = "test message"
    from_mail = "noreply@smcamp.us"
    to_mail = ["noreply@smcamp.us"]
    
    email = EmailMessage(subject,message,from_mail,to_mail)
    email.send()
    return HttpResponse("mail sended")
