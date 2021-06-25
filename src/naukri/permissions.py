from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model


User = get_user_model()


class UserTypePermission(BasePermission):

    user_type = None

    def has_permission(self, request, view):

        if request.user.is_authenticated and request.user.user_type == self.user_type:
            return True
        return False


class IsRecruiter(UserTypePermission):

    user_type = User.UserType.JOB_RECRUITER


class IsCandidate(UserTypePermission):

    user_type = User.UserType.JOB_SEEKER
