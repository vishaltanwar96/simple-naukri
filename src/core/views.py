from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm, get_objects_for_user
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView

from core.models import Job
from core.filters import JobFilterSet
from naukri.permissions import IsRecruiter, IsCandidate
from core.serializers import UserSerializer, JobSerializer, JobIDSerializer


User = get_user_model()


class UserRegistrationView(CreateAPIView):
    """
    Candidate/Recruiter Signup
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class JobCreateAPIView(CreateAPIView):
    """
    Recruiter can post jobs using this API
    """

    serializer_class = JobSerializer
    queryset = Job.objects.all()
    permission_classes = [IsRecruiter]

    def perform_create(self, serializer):

        job = serializer.save(posted_by=self.request.user)
        assign_perm('view_job', self.request.user, job)


class ListCandidatesForJobView(APIView):
    """
    Lists all the candidates who have applied to a previously posted job by the current recuiter
    """

    permission_classes = [IsRecruiter]

    @extend_schema(responses={status.HTTP_200_OK: UserSerializer})
    def get(self, request, job_id):

        try:
            Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise NotFound(detail='Invalid job_id, not found')

        try:
            job = get_objects_for_user(request.user, 'view_job', klass=Job).get(id=job_id)
        except Job.DoesNotExist:
            raise PermissionDenied(detail='You do not have permission to perform this action')
        return Response(UserSerializer(job.applicants, many=True).data, status.HTTP_200_OK)


class JobListView(ListAPIView):
    """
    Lists all the jobs if a Candidate is requesting and Lists the created jobs
    by the recruiter if recruiter is requesting.
    Also acts as a search view for the candidate and can search jobs using recruiter_fname, recruiter_lname
    description(of job) and title(of job).
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filterset_class = JobFilterSet
    permission_classes = [IsCandidate | IsRecruiter]

    def get_queryset(self):

        if self.request.user.user_type == User.UserType.JOB_RECRUITER:
            queryset = get_objects_for_user(self.request.user, 'view_job', Job)
        else:
            queryset = Job.objects.all()
        return queryset


class JobApplyView(GenericAPIView):
    """
    A Candidate can apply to one or more jobs by passing in a list of Job IDs.
    """

    permission_classes = [IsCandidate]
    serializer_class = JobIDSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        jobs = serializer.validated_data['job_ids']
        for job in jobs:
            job.applicants.add(self.request.user)
        return Response({'msg': 'Applied to jobs successfully'}, status.HTTP_200_OK)
