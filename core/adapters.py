from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class ForceAutoSignupSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Skip the "complete the following form" third-party signup page.
    User is created directly from provider data (GitHub/Google supply email).
    """

    def is_auto_signup_allowed(self, request, sociallogin):
        return True
