from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.serializers import UserSerializer
from users.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
    filter_backends = (SearchFilter,)
    http_method_names = ('get', 'patch', 'delete', 'post')
    search_fields = ('username',)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        else:
            self.permission_classes = [IsAuthenticated,]
        return super(UserViewSet, self).get_permissions()

    @action(
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path='me',
    )
    def edit_self_user(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=self.request.user)
        serializer = UserSerializer(user)
        if self.request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
