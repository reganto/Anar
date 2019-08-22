from tornado.web import url
from handlers.home import HomeHandler
from handlers.auth import RegisterHandler, LoginHandler, \
    VerifyTokenHandler, AjaxHandler, UserExistJaxHandler

url_patterns = [
    url(r"/", HomeHandler, name='home'),
    url(r"/auth/register", RegisterHandler, name='register'),
    url(r"/v/(\w+)", VerifyTokenHandler, name='vtoken'),
    url(r"/auth/login", LoginHandler, name='login'),
    url(r"/userjax", AjaxHandler, name='ajax'),
    url(r"/usrexist", UserExistJaxHandler, name='usrjaxexit'),
]
