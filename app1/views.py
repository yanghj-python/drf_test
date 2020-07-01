from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework import generics
from rest_framework import viewsets

from api.models import Book
from api.serializers import BookDeModelSerializer
from utils.response import APIResponse
from .serializers import BookModelSerializer


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_list, many=True).data

        return APIResponse(results=data_ser)

class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(http_status=status.HTTP_204_NO_CONTENT)


class BookListAPIVIew(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"


class BookGenericViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    def user_login(self, request, *args, **kwargs):
        username = kwargs.get('name')
        password = kwargs.get('pwd')
        print(username,password)
        if username == 'yhj' and password == '123':
            return APIResponse(data_status=200,data_message="登录成功")
        else:
            return APIResponse(data_status=404, data_message="登录失败")

    def user_register(self, request, *args, **kwargs):
        request_data = request.data
        book_ser = BookDeModelSerializer(data=request_data)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return APIResponse(results=BookModelSerializer(book_obj).data,data_status=200,data_message="注册成功")
