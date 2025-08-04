import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.authentication.models import User
from apps.blog.models import Post, Category, Tag
from apps.authentication.jwt_utils import generate_token

User = get_user_model()

class BlogTestCase(APITestCase):
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            is_email_verified=True
        )

        # Create another user
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123',
            first_name='Other',
            last_name='User',
            is_email_verified=True
        )

        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test category description'
        )

        # Create test tags
        self.tag1 = Tag.objects.create(
            name='Test Tag 1',
            slug='test-tag-1'
        )
        self.tag2 = Tag.objects.create(
            name='Test Tag 2',
            slug='test-tag-2'
        )

        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post content.',
            excerpt='Test post excerpt',
            author=self.user,
            category=self.category,
            status='published'
        )
        self.post.tags.add(self.tag1, self.tag2)

        # URLs
        self.posts_url = reverse('blog:post-list')
        self.post_detail_url = reverse('blog:post-detail', kwargs={'pk': self.post.id})
        self.post_by_slug_url = reverse('blog:post-by-slug', kwargs={'slug': self.post.slug})
        self.categories_url = reverse('blog:category-list')
        self.tags_url = reverse('blog:tag-list')
        self.my_posts_url = reverse('blog:my-posts')

        # Authenticate user
        token = generate_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_posts_list(self):
        """Test getting list of posts"""
        response = self.client.get(self.posts_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post')

    def test_get_post_detail(self):
        """Test getting a specific post by ID"""
        response = self.client.get(self.post_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.data['content'], 'This is a test post content.')
        self.assertEqual(response.data['author']['id'], self.user.id)

    def test_get_post_by_slug(self):
        """Test getting a post by slug"""
        response = self.client.get(self.post_by_slug_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.data['slug'], 'test-post')

    def test_get_post_by_slug_not_found(self):
        """Test getting a post by non-existent slug"""
        response = self.client.get(reverse('blog:post-by-slug', kwargs={'slug': 'non-existent'}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_success(self):
        """Test creating a new post"""
        post_data = {
            'title': 'New Test Post',
            'content': 'This is a new test post content.',
            'excerpt': 'New test post excerpt',
            'category': self.category.id,
            'tags': [self.tag1.id, self.tag2.id],
            'status': 'draft'
        }

        response = self.client.post(self.posts_url, post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Test Post')
        self.assertEqual(response.data['author']['id'], self.user.id)

        # Check if post was created in database
        post = Post.objects.get(title='New Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.status, 'draft')

    def test_create_post_invalid_data(self):
        """Test creating a post with invalid data"""
        post_data = {
            'title': '',  # Empty title
            'content': 'Test content'
        }

        response = self.client.post(self.posts_url, post_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_update_post_success(self):
        """Test updating a post"""
        update_data = {
            'title': 'Updated Test Post',
            'content': 'Updated content',
            'excerpt': 'Updated excerpt'
        }

        response = self.client.patch(self.post_detail_url, update_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Test Post')
        self.assertEqual(response.data['content'], 'Updated content')

    def test_update_post_unauthorized(self):
        """Test updating a post by non-author"""
        # Create post by other user
        other_post = Post.objects.create(
            title='Other User Post',
            slug='other-user-post',
            content='Other user content',
            author=self.other_user,
            status='published'
        )

        update_data = {'title': 'Unauthorized Update'}
        response = self.client.patch(
            reverse('blog:post-detail', kwargs={'pk': other_post.id}),
            update_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_success(self):
        """Test deleting a post"""
        response = self.client.delete(self.post_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check if post was deleted
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_unauthorized(self):
        """Test deleting a post by non-author"""
        # Create post by other user
        other_post = Post.objects.create(
            title='Other User Post',
            slug='other-user-post',
            content='Other user content',
            author=self.other_user,
            status='published'
        )

        response = self.client.delete(
            reverse('blog:post-detail', kwargs={'pk': other_post.id})
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_publish_post(self):
        """Test publishing a draft post"""
        # Create draft post
        draft_post = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            content='Draft content',
            author=self.user,
            status='draft'
        )

        response = self.client.post(
            reverse('blog:post-publish', kwargs={'pk': draft_post.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if post was published
        draft_post.refresh_from_db()
        self.assertEqual(draft_post.status, 'published')

    def test_unpublish_post(self):
        """Test unpublishing a published post"""
        response = self.client.post(
            reverse('blog:post-unpublish', kwargs={'pk': self.post.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if post was unpublished
        self.post.refresh_from_db()
        self.assertEqual(self.post.status, 'draft')

    def test_get_my_posts(self):
        """Test getting current user's posts"""
        response = self.client.get(self.my_posts_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Post')

    def test_get_categories(self):
        """Test getting list of categories"""
        response = self.client.get(self.categories_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Category')

    def test_get_tags(self):
        """Test getting list of tags"""
        response = self.client.get(self.tags_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_posts_by_category(self):
        """Test filtering posts by category"""
        response = self.client.get(f'{self.posts_url}?category={self.category.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_posts_by_status(self):
        """Test filtering posts by status"""
        response = self.client.get(f'{self.posts_url}?status=published')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_posts(self):
        """Test searching posts"""
        response = self.client.get(f'{self.posts_url}?search=Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_post_model_str(self):
        """Test Post model string representation"""
        self.assertEqual(str(self.post), 'Test Post')

    def test_category_model_str(self):
        """Test Category model string representation"""
        self.assertEqual(str(self.category), 'Test Category')

    def test_tag_model_str(self):
        """Test Tag model string representation"""
        self.assertEqual(str(self.tag1), 'Test Tag 1')

    def test_post_slug_generation(self):
        """Test automatic slug generation for posts"""
        post = Post.objects.create(
            title='Test Post With Slug',
            content='Test content',
            author=self.user,
            status='published'
        )

        self.assertEqual(post.slug, 'test-post-with-slug')

    def test_category_slug_generation(self):
        """Test automatic slug generation for categories"""
        category = Category.objects.create(
            name='Test Category With Slug',
            description='Test description'
        )

        self.assertEqual(category.slug, 'test-category-with-slug')

    def test_tag_slug_generation(self):
        """Test automatic slug generation for tags"""
        tag = Tag.objects.create(name='Test Tag With Slug')

        self.assertEqual(tag.slug, 'test-tag-with-slug')

    def test_post_reading_time_calculation(self):
        """Test reading time calculation"""
        # Create post with specific content length
        post = Post.objects.create(
            title='Reading Time Test',
            content='This is a test content. ' * 50,  # ~300 words
            author=self.user,
            status='published'
        )

        # Reading time should be calculated (approximately 1-2 minutes for 300 words)
        self.assertGreater(post.reading_time, 0)

    def test_post_excerpt_generation(self):
        """Test automatic excerpt generation"""
        post = Post.objects.create(
            title='Excerpt Test',
            content='This is a very long content that should be truncated for the excerpt. ' * 10,
            author=self.user,
            status='published'
        )

        # Excerpt should be generated and shorter than content
        self.assertIsNotNone(post.excerpt)
        self.assertLess(len(post.excerpt), len(post.content))

    def test_unauthorized_access(self):
        """Test accessing endpoints without authentication"""
        self.client.credentials()  # Remove authentication

        response = self.client.get(self.posts_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Public endpoint

        response = self.client.get(self.my_posts_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Private endpoint

        response = self.client.post(self.posts_url, {'title': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Private endpoint
