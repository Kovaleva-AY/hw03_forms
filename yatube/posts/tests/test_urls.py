from http import HTTPStatus
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='auth'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись',
            )
        cls.group = Group.objects.create(
            title=('Тестовый заголовок'),
            slug='test_slug',
            description='Тестовое описание'
        )


    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем авторизованый клиент
        self.user = User.objects.get(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_pages(self):
        postURLTests = PostURLTests()
        postid = postURLTests.post.pk
        
        """страницы группы и главная доступны всем"""
        url_names = [
            '/',
            '/group/test_slug/',
            '/profile/auth/',
            '/posts/' + str(postid) + '/',

        ]
        for adress in url_names:
            with self.subTest():
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_create_for_authorized(self):
        """Страница доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_post_edit_for_authorized(self):
        """Страница доступна авторизованному пользователю."""
        response = self.authorized_client.get('/posts/1/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    

    def test_urls_uses_correct_template(self):
        postURLTests = PostURLTests()
        postid = postURLTests.post.pk
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test_slug/',
            'posts/create_post.html': '/create/',
            'posts/profile.html': '/profile/auth/',
            'posts/post_detail.html': '/posts/' + str(postid) + '/',

        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template) 

    def test_page_404(self):
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    
