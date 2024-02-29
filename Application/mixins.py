from Transport import settings
from twilio.rest import Client



class MessagseHandler:
    
    phone = None
    otp = None
    
    def __init__(self, phone,otp) -> None:
        self.phone = phone
        self.otp = otp
        
    def send_otp(self,phone, otp):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = client.messages.create(
            body=f'Your OTP is: {self.otp}',
            from_='+17407911029',
            to=self.phone
        )
