from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from .models import Post, Category, Tag

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    post_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'created_at']
        read_only_fields = ['slug', 'created_at']

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """
    post_count = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count', 'created_at']
        read_only_fields = ['slug', 'created_at']

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for author information in posts.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing posts (public view).
    """
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.ReadOnlyField()
    reading_time = serializers.ReadOnlyField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category', 'tags',
            'status', 'featured_image', 'created_at', 'updated_at', 'published_at',
            'reading_time'
        ]

    def get_featured_image(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return f"http://localhost:8000{obj.featured_image.url}"
        return None

class PostDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed post view.
    """
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.ReadOnlyField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'author', 'category', 'tags',
            'status', 'featured_image', 'created_at', 'updated_at', 'published_at',
            'reading_time'
        ]

    def get_featured_image(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return f"http://localhost:8000{obj.featured_image.url}"
        return None

class PostCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating posts.
    """
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=list
    )
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'excerpt', 'category_id', 'tag_ids',
            'status', 'featured_image', 'author'
        ]
        read_only_fields = ['id', 'author']

    def validate_title(self, value):
        """
        Validate title length and uniqueness.
        """
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters.")
        return value

    def validate_content(self, value):
        """
        Validate content is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    def validate_status(self, value):
        """
        Validate status is valid.
        """
        valid_statuses = ['draft', 'published']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value

    def validate_category_id(self, value):
        """
        Validate category exists if provided.
        """
        if value is not None:
            try:
                Category.objects.get(id=value)
            except Category.DoesNotExist:
                raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_tag_ids(self, value):
        """
        Validate tags exist if provided.
        """
        if value:
            existing_tags = Tag.objects.filter(id__in=value)
            if len(existing_tags) != len(value):
                raise serializers.ValidationError("One or more tags do not exist.")
        return value

    def create(self, validated_data):
        """
        Create post with author and relationships.
        """
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', [])

        # Set author to current user
        validated_data['author'] = self.context['request'].user

        # Create post
        post = Post.objects.create(**validated_data)

        # Set category if provided
        if category_id:
            post.category = Category.objects.get(id=category_id)
            post.save()

        # Set tags if provided
        if tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids)
            post.tags.set(tags)

        return post

class PostUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating posts.
    """
    category_id = serializers.IntegerField(required=False, allow_null=True)
    tag_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category_id', 'tag_ids',
            'status', 'featured_image'
        ]

    def validate_title(self, value):
        """
        Validate title length.
        """
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters.")
        return value

    def validate_content(self, value):
        """
        Validate content is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value

    def validate_status(self, value):
        """
        Validate status is valid.
        """
        valid_statuses = ['draft', 'published']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value

    def validate_category_id(self, value):
        """
        Validate category exists if provided.
        """
        if value is not None:
            try:
                Category.objects.get(id=value)
            except Category.DoesNotExist:
                raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_tag_ids(self, value):
        """
        Validate tags exist if provided.
        """
        if value:
            existing_tags = Tag.objects.filter(id__in=value)
            if len(existing_tags) != len(value):
                raise serializers.ValidationError("One or more tags do not exist.")
        return value

    def update(self, instance, validated_data):
        """
        Update post with relationships.
        """
        category_id = validated_data.pop('category_id', None)
        tag_ids = validated_data.pop('tag_ids', None)

        # Update post fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update category if provided
        if category_id is not None:
            if category_id:
                instance.category = Category.objects.get(id=category_id)
            else:
                instance.category = None

        # Update tags if provided
        if tag_ids is not None:
            if tag_ids:
                tags = Tag.objects.filter(id__in=tag_ids)
                instance.tags.set(tags)
            else:
                instance.tags.clear()

        instance.save()
        return instance

class MyPostSerializer(serializers.ModelSerializer):
    """
    Serializer for user's own posts.
    """
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.ReadOnlyField()
    reading_time = serializers.ReadOnlyField()
    featured_image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author', 'category', 'tags',
            'status', 'featured_image', 'created_at', 'updated_at', 'published_at',
            'reading_time'
        ]

    def get_featured_image(self, obj):
        if obj.featured_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.featured_image.url)
            return f"http://localhost:8000{obj.featured_image.url}"
        return None
