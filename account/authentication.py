from django.contrib.auth.models import User

from .models import Profile


class EmailAuthBackend:

    """Authenticate using an e-mail addresse"""

    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(str(password)) and self.user_can_authenticate(user):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, response, *args, **kwargs):
    """Create user profile for social authentication."""
    try:
        user.email = response["email"]
        user.save()
    except KeyError:
        pass

    Profile.objects.get_or_create(user=user)
