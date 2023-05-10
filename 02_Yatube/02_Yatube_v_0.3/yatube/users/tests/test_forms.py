# from http import HTTPStatus

# from django.contrib.auth import authenticate, get_user_model
# from django.test import Client, TestCase
# from django.urls import reverse

# User = get_user_model()


# class TaskCreateFormTests(TestCase):
#     fixtures = [
#         'posts.xml',
#         'groups.xml',
#         'users.xml'
#     ]

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.user = User.objects.create(
#             username='test_user',
#             email='test_email@gmail.com',
#             password='Testpassword1'
#         )

#     def setUp(self):
#         self.guest_client = Client()
#         self.authorized_client = Client()
#         self.data_create = {
#             'first_name': "Тест",
#             'last_name': 'Тестович',
#             'username': 'user_test',
#             'email': 'dkushlevich@yandex.ru',
#             'password1': 'Gulyaeva2109',
#             'password2': 'Gulyaeva2109'
#         }

#     def test_user_post(self):
#         """Проверка: Валидная форма создает пользователя в User"""
#         users_count = User.objects.count()
#         response = self.guest_client.post(
#             (reverse('users:signup')), self.data_create, follow=True
#         )

#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(User.objects.count(), users_count + 1)
#         self.assertTrue(
#             User.objects.filter(
#                 first_name="Тест",
#                 last_name='Тестович',
#                 username='user_test',
#                 email='dkushlevich@yandex.ru',
#             ).exists()
#         )
#         self.assertRedirects(response, reverse('posts:index'))

#         response = self.guest_client.post(
#             reverse('users:login'),
#             {'username': self.data_create['username'],
#              'password': self.data_create['password1']
#              }
#         )
#         self.assertRedirects(response, reverse('posts:index'))

#         user = User.objects.last()
#         # Отправляем письмо на почту
#         response = self.guest_client.post(
#             (reverse('users:password_reset_form')),
#             {'email': user.email}
#         )
#         # Цепляем из контекста токен и uid
#         token = response.context[0]['token']
#         uid = response.context[0]['uid']

#         # Отправляем GET-запрос
#         response = self.guest_client.get(
#             reverse('users:password_reset_confirm', kwargs={
#                 'uidb64': uid,
#                 'token': token
#             }),
#             follow=True
#         )
#         # Происходит редирект на "set-password"
#         self.assertRedirects(response, reverse(
#             'users:password_reset_confirm',
#             kwargs={
#                 'uidb64': uid,
#                 'token': 'set-password'
#             }
#         ))
#         # Отправляем POST-запрос смены пароля
#         response = self.guest_client.post(
#             reverse(
#                 'users:password_reset_confirm',
#                 kwargs={
#                     'uidb64': uid,
#                     'token': 'set-password'
#                 }
#             ),
#             {"new_password1": "Newpassword1",
#              "new_password2": "Newpassword1"},
#             follow=True
#         )
#         # Пароль остаётся прежним :(
#         self.assertIsNone(authenticate(
#             username='user_test', password='randompassword1'
#         ))