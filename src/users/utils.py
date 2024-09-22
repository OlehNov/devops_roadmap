from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

# def send_confirmation_email(email, token_id, user_id):
#     data = {
#         'token_id': str(token_id),
#         'user_id': str(user_id),
#     }
#     message = get_template('users/confirmation_email.txt').render(data)
#     send_mail(subject='Please confirm email', message=message,
#               from_email='nehxbyaroslav.gmail.com', recipient_list=[email],
#               fail_silently=True)


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)


token_generator = TokenGenerator()
