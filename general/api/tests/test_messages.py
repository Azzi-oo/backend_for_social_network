from rest_framework.test import APITestCase
from general.factories import UserFactory, PostFactory, ChatFactory, MessageFactory
from rest_framework import status
import json
from django.contrib.auth.hashers import check_password
from general.models import User, Chat, Message


class MessageTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = "/api/messages/"

    def test_create_message(self):
        chat = ChatFactory(user_1=self.user)
        data = {
            "chat": chat.pk,
            "content": "Тестовое сообщение",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        message = Message.objects.last()
        self.assertEqual(message.author, self.user)
        self.assertEqual(message.chat, chat)
        self.assertEqual(message.content, data["content"])

    def test_try_to_create_message_for_other_chat(self):
        chat = ChatFactory()
        data = {
            "chat": chat.pk,
            "content": "Тестовое сообщение",
        }
        response = self.client.post(self.url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Message.objects.count(), 0)

    def test_delete_own_message(self):
        chat = ChatFactory(user_1=self.user)
        message = MessageFactory(author=self.user, chat=chat)

        response = self.client.delete(
            self.url + f"{message.pk}/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(chat.messages.count(), 0)
        self.assertEqual(self.user.messages.count(), 0)
        