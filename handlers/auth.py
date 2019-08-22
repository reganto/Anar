import uuid
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from tornado.escape import xhtml_escape
from mysql.connector import Error
from handlers.base import BaseHandler
from vendor.utils.captcha import check
from vendor.utils.email import validation
from vendor.utils.sendmail import send

ph = PasswordHasher()


class RegisterHandler(BaseHandler):
    def get(self):
        self.render(
            'auth/register.html',
            page_title='Register',
            error=None)

    async def post(self):
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        email = self.get_argument('email', '')

        self.cursor = self.settings.get('db').cursor()

        # check captcha
        user_ip = self.request.remote_ip
        g_recaptcha_response = self.get_argument('g-recaptcha-response', None)
        if not check.check_captcha(g_recaptcha_response, user_ip):
            error = "Captcha Error"
            self.render(
                'auth/register.html',
                page_title="Register",
                error=error
            )

        # check email
        if not validation.email_validation(email):
            error = "Please input a currect email"
            self.render(
                'auth/register.html',
                page_title="Register",
                error=error
            )

        # check username
        query = "SELECT username FROM users WHERE username=%s"
        username = xhtml_escape(username)
        self.cursor.execute(query, (username, ))
        result = self.cursor.fetchone()
        if result is not None:
            error = "Username already exist"
            self.render(
                'auth/register.html',
                page_title="Register",
                error=error
            )
        
        # check email
        query = "SELECT email FROM users WHERE email=%s"
        email = xhtml_escape(email)
        self.cursor.execute(query, (email, ))
        result = self.cursor.fetchone()
        if result is not None:
            error = "Email already exist"
            self.render(
                'auth/register.html',
                page_title="Register",
                error=error
            )

        # prepare values for insert to database

        # 1- encode password
        password = password.encode('utf-8')
        # 2-generate salt and encode it
        salt = uuid.uuid4().hex.encode('utf-8')
        # 3-hashed password+salt
        hashed_password = ph.hash(password+salt)
        
        # username = xhtml_escape(username) -> username already escaped
        # set status: -1 -> disable, 0 -> ban, 1 -> enable
        status = -1
        # generate token
        token = uuid.uuid4().hex
        # set created_at
        created_at = datetime.now()

        args = (
            username,
            hashed_password,
            salt,
            created_at,
            email,
            token,
            status
        )
        query = """INSERT INTO
        users (username,password,salt,created_at,email,token,status)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """

        try:
            self.cursor.execute(query, args)
            self.settings.get('db').commit()
        except Error as e:
            print(e)

        # send email
        if send.send_email(email, token):
            error = "Check your email inbox"
            self.render(
                'auth/register.html',
                page_title="Register",
                error=error
            )


class VerifyTokenHandler(BaseHandler):
    def get(self, token):
        self.cursor = self.settings.get('db').cursor()
        query = "SELECT id, status FROM users WHERE token = %s"
        self.cursor.execute(query, (token,))

        result = self.cursor.fetchone()
        if result is None:
            self.write({'status': 'error'})
            return
        if result[1] == 1:
            self.write({'status': 'Already enabled'})
            return
        # if token exists
        query = "UPDATE users SET status = %s WHERE id = %s"
        args = (1, result[0])

        try:
            self.cursor.execute(query, args)
            self.settings.get('db').commit()
        except Error as e:
            print(e)
        self.write({'status': 'ok'})


class AjaxHandler(BaseHandler):
    def post(self):
        username = self.get_body_argument('username')
        self.cursor = self.settings.get('db').cursor()
        query = "SELECT * FROM users WHERE username=%s"
        self.cursor.execute(query, (username, ))
        if self.cursor.fetchone() is not None:
            self.write('This username is not available')



class LoginHandler(BaseHandler):
    def get(self):
        self.render(
            'auth/login.html',
            page_title='Login',
            error=None
        )
    
    def post(self):
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        # g_recaptcha_response = self.get_argument('g-recaptcha-response', '')

        self.cursor = self.settings.get('db').cursor()
        query = "SELECT password, salt, status, token FROM users WHERE username=%s"
        args = (xhtml_escape(username), )
        self.cursor.execute(query, args)
        result = self.cursor.fetchone()

        # check user status
        if result[2] == -1:
            error = '''You MUST verify your account to continue.
            please check your email inbox!'''
            self.render(
                'auth/login.html',
                page_title='login',
                error=error,
            )
            return
        # elif result[2] == 0:
        #     error = 'Your account banned! please try 24 hours later'
        #     self.render(
        #         'auth/login.html',
        #         page_title='login',
        #         error=error,
        #     )
        try:
            # hashed_password = result[0].encode('utf-8')
            password = password.encode('utf-8')
            salt = result[1].encode('utf-8')
            ph.verify(result[0], password+salt)
        except VerifyMismatchError:
            error = '''Your password is incorrect'''
            self.render(
                'auth/login.html',
                page_title='login',
                error=error,
            )
        else:
            self.set_secure_cookie('user', xhtml_escape(result[3]))
            self.write({'login': 'True'})
        

class UserExistJaxHandler(BaseHandler):
    def get(self):
        username = self.get_query_argument('username')
        self.cursor = self.settings.get('db').cursor()
        query = "SELECT * FROM users WHERE username=%s"
        self.cursor.execute(query, (username, ))
        if self.cursor.fetchone() is None:
            self.write('This username does NOT exist')
