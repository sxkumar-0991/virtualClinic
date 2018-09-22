from .models import CustomUser


class MyCustomUserBackend:
    def authenticate(self, email=None, password=None):
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None

        except CustomUser.DoesNotExist:
            return None


    def get_user(self, id):
        try:
            user = CustomUser.objects.get(pk=id)
            if user.is_active:
                return user
            else:
                return None
        except CustomUser.DoesNotExist:
            return None
