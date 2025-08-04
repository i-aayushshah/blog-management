from django.db.models import Q
from django.utils import timezone
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post, Category, Tag
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateSerializer, PostUpdateSerializer,
    MyPostSerializer, CategorySerializer, TagSerializer
)

class PostPagination(PageNumberPagination):
    """
    Custom pagination for posts.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(ModelViewSet):
    """
    ViewSet for blog posts with CRUD operations.
    """
    queryset = Post.objects.all()
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'author', 'category', 'tags', 'created_at']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'published_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Filter queryset based on action and user permissions.
        """
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')

        # For public actions, only show published posts
        if self.action in ['list', 'retrieve']:
            queryset = queryset.filter(status='published')

        return queryset

    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'create':
            return PostCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PostUpdateSerializer
        elif self.action == 'retrieve':
            return PostDetailSerializer
        elif self.action == 'my_posts':
            return MyPostSerializer
        else:
            return PostListSerializer

    def get_permissions(self):
        """
        Set permissions based on action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'my_posts', 'publish', 'unpublish']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Set author to current user and handle slug generation.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """
        Ensure user can only update their own posts.
        """
        post = self.get_object()
        if post.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only edit your own posts.')
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensure user can only delete their own posts.
        """
        if instance.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You can only delete your own posts.')
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_posts(self, request):
        """
        Get current user's posts (both draft and published).
        """
        posts = Post.objects.filter(author=request.user).select_related(
            'author', 'category'
        ).prefetch_related('tags').order_by('-created_at')

        # Apply search if provided
        search = request.query_params.get('search', None)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )

        # Apply filters
        status_filter = request.query_params.get('status', None)
        if status_filter:
            posts = posts.filter(status=status_filter)

        category_filter = request.query_params.get('category', None)
        if category_filter:
            posts = posts.filter(category_id=category_filter)

        # Paginate results
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured/popular posts.
        """
        posts = Post.objects.filter(
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')[:5]

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """
        Publish a draft post.
        """
        post = self.get_object()

        if post.author != request.user:
            return Response(
                {'error': 'You can only publish your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if post.status == 'published':
            return Response(
                {'error': 'Post is already published.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.status = 'published'
        post.published_at = timezone.now()
        post.save()

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        """
        Unpublish a published post (make it draft).
        """
        post = self.get_object()

        if post.author != request.user:
            return Response(
                {'error': 'You can only unpublish your own posts.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if post.status == 'draft':
            return Response(
                {'error': 'Post is already a draft.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.status = 'draft'
        post.published_at = None
        post.save()

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        """
        Get a post by slug.
        """
        try:
            post = Post.objects.select_related('author', 'category').prefetch_related('tags').get(slug=slug)

            # For public access, only show published posts
            if not request.user.is_authenticated or post.author != request.user:
                if post.status != 'published':
                    return Response(
                        {'error': 'Post not found.'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            serializer = PostDetailSerializer(post)
            return Response(serializer.data)

        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

class CategoryViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for categories (read-only).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """
        Get all posts in a specific category.
        """
        category = self.get_object()
        posts = Post.objects.filter(
            category=category,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')

        # Apply search if provided
        search = request.query_params.get('search', None)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )

        # Paginate results
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

class TagViewSet(ReadOnlyModelViewSet):
    """
    ViewSet for tags (read-only).
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """
        Get all posts with a specific tag.
        """
        tag = self.get_object()
        posts = Post.objects.filter(
            tags=tag,
            status='published'
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_at')

        # Apply search if provided
        search = request.query_params.get('search', None)
        if search:
            posts = posts.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(excerpt__icontains=search)
            )

        # Paginate results
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
