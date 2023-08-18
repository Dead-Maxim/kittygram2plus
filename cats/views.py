from rest_framework import viewsets
from .permissions import OwnerOrReadOnly
from rest_framework.throttling import ScopedRateThrottle
from .throttling import WorkingHoursRateThrottle
# from rest_framework.pagination import PageNumberPagination
from .models import Achievement, Cat, User
from .serializers import AchievementSerializer, CatSerializer, UserSerializer
from .pagination import CatsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (ScopedRateThrottle, WorkingHoursRateThrottle,)
    throttle_scope = 'low_request'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    pagination_class = CatsPagination
    filterset_fields = ('color', 'birth_year')
    search_fields = ('^name',)
    ordering_fields = ('name', 'birth_year') 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
