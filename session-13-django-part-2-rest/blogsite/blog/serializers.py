from .models import Post
from rest_framework import serializers
# 这里的serializer 相当于 pydantic models
class PostSerializer(serializers.ModelSerializer):
    # 如下是一个复合field, 表示通过Post model的author field fk 拿到author对应的user's email，加入json return中表示author_email: xxx 
    # 这是一个只读属性
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post  # base model
        fields = '__all__' # 转换哪些的fields，__all__表示所有的都转换
        
class PostListSerializer(serializers.ModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published', 'author_email', 'created_at']
        
class PostDetailsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField() # 显示author本身related id, username, email 

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published', 'created_at', 'updated_at']
        
    def get_author(self, obj):# 当fetch author时自动call get_author, obj是此时的model
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'email': obj.author.email,
        }
        