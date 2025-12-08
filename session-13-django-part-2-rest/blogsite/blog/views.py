from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer, PostListSerializer, PostDetailsSerializer

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from .permissions import HasCreatePostPermission

# class PostViewSet(viewsets.ModelViewSet): # automatically generate all routes
class PostViewSet( # 和self.actions类似，表示支持的api type, 比如listmodelmaxin支持get/items这种
    mixins.ListModelMixin, # add allowed method routes
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    
    '''
    This class generates 5 apis automantically for us
    - GET /posts/ -> list all posts
    - GET /posts/1 -> list post details
    - POST /posts -> create post
    - PUT /posts/1 -> update
    - PATCH /posts/1 -> partial update
    - DELETE / posts/1 -> delete
    '''
    
    queryset = Post.objects.all() # data source is .models.Post's objects  
    serializer_class = PostSerializer  # used serializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        if self.action == 'list':
            # return Post.objects.filter(published=True).all()
            print(self.request.query_params)
            order_by = self.request.query_params.get('order_by' ,'')
            if order_by:
                return Post.objects.order_by(order_by).all()
            return Post.objects.all()
        elif self.action == 'retrieve':
             return Post.objects.all()
         
    def get_permissions(self):
        return super().get_permissions()
    

    def get_serializer_class(self):
        # self.action表示当前ViewSet正在执行的动作，值是由drf自动根据请求匹配的标准动作名或者自定义动作名
        """
        get/items -> list 
        get/items/1 -> retrieve
        post /items - create 
        put /items/id - update 
        patch /items/id - partial_update 
        delete /items/id - destroy 
        """
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'retrieve':
            return PostDetailsSerializer
        else:
            return PostSerializer
        
    
    # detail means -> /post/<id> 自定义api的return type 
    # detail = True 表示return的内容是针对单独id的， request api 应该是/items/1 
    @action(detail=True, methods=['POST'])    
    def publish(self, request, pk):
        print('pk', pk)
        post = Post.objects.get(pk=pk)
        post.published = True
        post.save()
        return Response({'status': 'Published'})
