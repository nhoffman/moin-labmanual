"""moinlm authentication methods

"""

import os

from MoinMoin import config, user
from MoinMoin.request import request_cli
from MoinMoin.auth import BaseAuth


class NeverAuth(BaseAuth):
    """ Always fail to authenticate, eg for a read-only site """

    name = 'never'

    def __init__(self, autocreate=False):
        self.autocreate = autocreate
        BaseAuth.__init__(self)

    def request(self, request, user_obj, **kw):
        return None, False


class PubcookieAuth(BaseAuth):
    """ authenticate using UWNetID authentication via pubcookie"""
    name = 'pubcookie'

    def __init__(self, autocreate=False):
        self.autocreate = autocreate
        BaseAuth.__init__(self)

    def request(self, request, user_obj, **kw):
        u = None
        _ = request.getText
        # always revalidate auth
        if user_obj and user_obj.auth_method == self.name:
            user_obj = None
        # something else authenticated before us
        if user_obj:
            return user_obj, True

        if isinstance(request, request_cli.Request):
            # may need to add commandline user to list of superusers
            username = os.environ['USER']
            u = user.User(request, auth_username=username,
                          auth_method='cli', auth_attribs=('name', 'password'))
        else:
            env = request.env
            auth_type = env.get('AUTH_TYPE', '')
            if auth_type in ['UWNetID']:
                username = env.get('REMOTE_USER', '').decode(config.charset)
                # when using http auth, we have external user name and password,
                # we don't use the moin user profile for those attributes.
                u = user.User(request, auth_username=username,
                              auth_method=self.name,
                              auth_attribs=('name', 'password'))

        if u and self.autocreate:
            u.create_or_update()
        if u and u.valid:
            return u, True  # True to get other methods called, too
        else:
            return user_obj, True
