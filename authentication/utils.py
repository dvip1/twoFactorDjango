from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core import serializers
import pyotp
import base64

User = get_user_model()

def hex_to_base32(hex_string):
    # Convert hex to bytes
    bytes_data = bytes.fromhex(hex_string)
    # Convert bytes to base32
    base32_string = base64.b32encode(bytes_data).decode('utf-8')
    # Remove padding
    return base32_string.rstrip('=')

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def generate_otp(user):
    try:
        device, created = TOTPDevice.objects.get_or_create(user=user, confirmed=True)
        print(f"Device: {device}, Created: {created}")
        print(f"Device details: {device.__dict__}")
        
        # Try to serialize the device to see all its fields
        serialized_device = serializers.serialize('json', [device])
        print(f"Serialized device: {serialized_device}")
        
        if not device.key:
            device.key = pyotp.random_base32()
            device.save()
        elif is_hex(device.key):
            # Convert the existing hex key to base32 only if it's in hex format
            device.key = hex_to_base32(device.key)
            device.save()
            
        # Use the device key to create the TOTP object
        totp = pyotp.TOTP(device.key)
        otp = totp.now()
        print(f"Generated OTP: {otp}")
        
        print(f"OTP for {user.email}: {otp}")
        return otp
    except Exception as e:
        print(f"Error generating OTP: {str(e)}")
        return None
    


def verify_otp(user, otp):
    device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
    print(device)
    if device is None: 
        return False
    # Check if the key is in hexadecimal format before converting
    if is_hex(device.key):
        device.key = hex_to_base32(device.key)
        device.save()
    totp = pyotp.TOTP(device.key)
    print(totp.verify(otp))
    return totp.verify(otp)