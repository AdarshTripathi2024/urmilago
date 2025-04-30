from django.contrib.auth.backends import BaseBackend
from .models import MyAdmin

class AdminAuthBackend(BaseBackend):
    def authenticate(self,request, username=None, password=None,**Kwargs):
        try:
            admin=MyAdmin.objects.get(username=username)
        except MyAdmin.DoesNotExist:
            return None

        if admin.check_password(password):
            return admin
        return None

    def get_user(self, user_id):
        try:
            return MyAdmin.objects.get(pk=user_id)
        except MyAdmin.DoesNotExist:
            return None
