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
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_public_pages(self):
        post_id = PostURLTests.id
        """страницы группы и главная доступны всем"""
        url_names = [
            '/',
            '/group/test_slug/',
            '/profile/auth/',
            '/posts/' + str(post_id) + '/',

        ]
        for adress in url_names:
            with self.subTest():
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    
