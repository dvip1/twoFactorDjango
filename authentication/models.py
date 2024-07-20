from django.contrib.auth.models import AbstractUser
from django_otp.plugins.otp_totp.models import TOTPDevice

class CustomUser(AbstractUser):
    @property
    def otp_device(self):
        devices = TOTPDevice.objects.filter(user=self, confirmed=True)
        return devices.first() if devices.exists() else None

    @otp_device.setter
    def otp_device(self, device):
        if device:
            device.user = self
            device.save()
        else:
            TOTPDevice.objects.filter(user=self).delete()