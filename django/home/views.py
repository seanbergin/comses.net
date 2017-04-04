import logging

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView
from django.http import QueryDict

from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from taggit.models import Tag
from wagtail.wagtailsearch.backends import get_search_backend

from core.view_helpers import get_search_queryset, retrieve_with_perms
from .models import Event, Job, FeaturedContentItem
from .serializers import EventSerializer, JobSerializer, TagSerializer, FeaturedContentItemSerializer, UserSerializer

logger = logging.getLogger(__name__)

search = get_search_backend()


class SmallResultSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data, **kwargs):
        query_params = QueryDict('', mutable=True)

        query = self.request.query_params.get('query')
        if query:
            query_params['query'] = query
        tags = self.request.query_params.getlist('tags')
        if tags:
            query_params['tags'] = tags
        order_by = self.request.query_params.getlist('order_by')
        if order_by:
            query_params['order_by'] = order_by

        count = self.page.paginator.count
        n_pages = count // self.page_size + 1
        page = int(self.request.query_params.get('page', 1))
        logger.debug("Request page")
        return Response({
            'current_page': page,
            'count': count,
            'query': self.request.query_params.get('query'),
            'query_params': query_params.urlencode(),
            'range': list(range(max(1, page - 4), min(n_pages + 1, page + 5))),
            'n_pages': n_pages,
            'results': data
        }, **kwargs)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.order_by('-date_created')
    pagination_class = SmallResultSetPagination

    def get_queryset(self):
        return get_search_queryset(self)

    @property
    def template_name(self):
        return 'home/events/{}.jinja'.format(self.action)

    def retrieve(self, request, *args, **kwargs):
        return retrieve_with_perms(self, request, *args, **kwargs)


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    pagination_class = SmallResultSetPagination
    queryset = Job.objects.all()

    @property
    def template_name(self):
        return 'home/jobs/{}.jinja'.format(self.action)

    def get_queryset(self):
        return get_search_queryset(self)

    def retrieve(self, request, *args, **kwargs):
        return retrieve_with_perms(self, request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = SmallResultSetPagination

    @property
    def template_name(self):
        return 'home/tags/{}.jinja'.format(self.action)

    def get_queryset(self):
        query = self.request.query_params.get('query')
        if query:
            queryset = Tag.objects.filter(name__icontains=query).order_by('name')
        else:
            queryset = Tag.objects.order_by('name')
        return queryset


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = SmallResultSetPagination

    @property
    def template_name(self):
        return 'home/profles/{}.jinja'.format(self.action)

    def get_queryset(self):
        return get_search_queryset(self)

    def retrieve(self, request, *args, **kwargs):
        return retrieve_with_perms(self, request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = 'home/profiles/retrieve.jinja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        serializer = UserSerializer(user)
        data = serializer.data
        for key in data:
            context[key] = data[key]

        return context


class FeaturedContentListAPIView(generics.ListAPIView):
    serializer_class = FeaturedContentItemSerializer
    queryset = FeaturedContentItem.objects.all()
    pagination_class = SmallResultSetPagination
