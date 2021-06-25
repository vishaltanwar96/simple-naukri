from django.urls import path, include
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from core.views import UserRegistrationView, JobCreateAPIView, ListCandidatesForJobView, JobListView, JobApplyView


user_urls = [
    path('signup/', UserRegistrationView.as_view(), name='user-signup'),
    path('login/', token_obtain_pair, name='login'),
    path('token-refresh/', token_refresh, name='token-refresh'),
]

job_urls = [
    path('', JobListView.as_view(), name='list-jobs'),
    path('', JobCreateAPIView.as_view(), name='create-job'),
    path('<int:job_id>/applicants/', ListCandidatesForJobView.as_view(), name='list-applicants-for-job'),
    path('apply/', JobApplyView.as_view(), name='apply-to-jobs'),
]

urlpatterns = [
    path('users/', include(user_urls)),
    path('jobs/', include(job_urls)),
]
