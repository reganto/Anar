from handlers.base import BaseHandler
from vendor.keys.secret import CAPTCHA_SITE_KEY


class RegisterHandler(BaseHandler):
    def get(self):
        self.render(
            'auth/register.html',
            page_title='Register',
            sk=CAPTCHA_SITE_KEY
        )
