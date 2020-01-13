"""
Django views for the Notifier.
"""


from django.contrib.auth.models import User
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions import permissions

from lms.djangoapps.discussion.notification_prefs import NOTIFICATION_PREF_KEY
from lms.djangoapps.discussion.notifier_api.serializers import NotifierUserSerializer


class NotifierPaginator(pagination.PageNumberPagination):
    """
    Paginator for the notifier API.
    """
    page_size = 10
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        """
        Construct a response with pagination information.
        """
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })


class NotifierUsersViewSet(ReadOnlyModelViewSet):
    """
    An endpoint that the notifier can use to retrieve users who have enabled
    daily forum digests, including all information that the notifier needs about
    such users.
    """
    authentication_classes = (JwtAuthentication, )
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NotifierUserSerializer
    pagination_class = NotifierPaginator

    # See NotifierUserSerializer for notes about related tables
    queryset = User.objects.filter(
        preferences__key=NOTIFICATION_PREF_KEY
    ).select_related(
        "profile"
    ).prefetch_related(
        "preferences",
        "courseenrollment_set",
        "course_groups",
        "roles__permissions"
    )
