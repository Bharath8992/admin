import requests

def send_whatsapp_message(phone_number, message, media_url=None):
    """
    Replace this with Twilio / Meta API call.
    """
    print(f"📤 Sending WhatsApp to {phone_number}: {message}")
    if media_url:
        print(f"🖼️ With media: {media_url}")
    # Example Twilio or Meta API request can go here later
