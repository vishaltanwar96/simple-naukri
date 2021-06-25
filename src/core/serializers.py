from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from core.models import Job


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(required=True, write_only=True, label=_('Confirm Password'))

    def validate(self, attrs):

        if attrs['password'] != attrs.pop('confirm_password'):
            raise ValidationError(detail={'password': 'Must match confirm password'})
        return attrs

    class Meta:
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password', 'user_type']
        model = User
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'user_type': {
                'write_only': True
            }
        }


class JobSerializer(serializers.ModelSerializer):

    posted_by = UserSerializer(read_only=True)

    class Meta:
        exclude = ['applicants']
        model = Job
        extra_kwargs = {
            'posted_on': {'read_only': True},
            'updated_on': {'read_only': True},
        }


class JobIDSerializer(serializers.Serializer):

    job_ids = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(),
        many=True,
        required=True,
        allow_empty=False
    )
