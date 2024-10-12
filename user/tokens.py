from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return str(user.pk) + str(timestamp) + str(user.is_active)

class CustumPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp) -> str:
        return str(user.pk) + str(timestamp) + str(user.last_login)

account_activation_token = AccountActivationTokenGenerator()
password_reset_token = CustumPasswordResetTokenGenerator()
