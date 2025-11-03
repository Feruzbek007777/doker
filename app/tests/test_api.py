import json
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from app.models import Book, Like
from app.serializers import BookSerializer


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='123456')
        self.u2 = User.objects.create_user(username='u2', password='123456')

        self.b1 = Book.objects.create(title='Python Tricks', author='Alice', price='100.00')
        self.b2 = Book.objects.create(title='Django Mastery', author='Bob', price='80.00')
        self.b3 = Book.objects.create(title='Advanced Python', author='Alice', price='120.00')

        Like.objects.create(user=self.u1, book=self.b1, like=True)
        Like.objects.create(user=self.u2, book=self.b1, like=False)

    def test_get_all(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer = BookSerializer([self.b1, self.b2, self.b3], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'author': 'Alice'})
        serializer = BookSerializer([self.b1, self.b3], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Python'})
        serializer = BookSerializer([self.b1, self.b3], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ordering(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'ordering': 'price'})
        serializer = BookSerializer([self.b2, self.b1, self.b3], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        url = reverse('book-list')
        data = {'title': 'Clean Code', 'author': 'Uncle Bob', 'price': '90.00'}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data.get('title'), 'Clean Code')

    def test_update(self):
        url = reverse('book-detail', args=(self.b2.id,))
        data = {'title': 'Django Mastery 2', 'author': 'Bob', 'price': '85.00'}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.b2.refresh_from_db()
        self.assertEqual(self.b2.title, 'Django Mastery 2')

    def test_delete(self):
        url = reverse('book-detail', args=(self.b3.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    def test_like_counts_in_serializer(self):
        url = reverse('book-detail', args=(self.b1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 1)
        self.assertEqual(response.data['dislikes'], 1)
