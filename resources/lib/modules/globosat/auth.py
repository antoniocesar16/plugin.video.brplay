# -*- coding: UTF-8 -*-

from resources.lib.modules import control
import requests

try:
    import cPickle as pickle
except:
    import pickle


class auth:

    GLOBO_AUTH_URL = 'https://login.globo.com/api/authentication'
    GLOBOSAT_CREDENTIALS = 'globosat_credentials'

    GLOBOPLAY_TOKEN_ID = 'GLBID'

    def __init__(self):
        try:
            credentials = control.setting(self.GLOBOSAT_CREDENTIALS)
            self.credentials = pickle.loads(credentials)
        except:
            self.credentials = None

    def _save_credentials(self):
        control.setSetting(self.GLOBOSAT_CREDENTIALS, pickle.dumps(self.credentials))

    def is_authenticated(self):
        return self.credentials is not None

    def authenticate(self, username, password):

        if not self.is_authenticated() and (username and password):
            control.log('username/password set. trying to authenticate')
            self.credentials = self._authenticate(username, password)
            if self.is_authenticated():
                control.log('successfully authenticated')
                self._save_credentials()
            else:
                control.log('wrong username or password', control.LOGERROR)
                message = '[%s] %s' % (self.__class__.__name__, control.lang(32003))
                control.infoDialog(message, icon='ERROR')
                return None
        elif self.is_authenticated():
            control.log('[GLOBOSAT] - already authenticated')
        else:
            control.log('no username set to authenticate', control.LOGWARNING)
            message = 'Missing user credentials'
            control.infoDialog(message, icon='ERROR')
            control.openSettings()
            return None

        control.log(repr(self.credentials))

        return self.credentials

    def error(self, msg):
        control.infoDialog('[%s] %s' % (self.__class__.__name__, msg), 'ERROR')

    def _authenticate(self, username, password):
        payload = {
            'captcha': '',
            'payload': {
                'email': username,
                'password': password,
                'serviceId': 6248
            }
        }

        response = requests.post(self.GLOBO_AUTH_URL, json=payload, headers={'content-type': 'application/json; charset=UTF-8',
                                          'accept': 'application/json, text/javascript',
                                          'Accept-Encoding': 'gzip',
                                          'referer': 'https://login.globo.com/login/4654?url=https://globoplay.globo.com/&tam=WIDGET',
                                          'origin': 'https://login.globo.com'})

        response.raise_for_status()
        credentials = response.cookies.get(self.GLOBOPLAY_TOKEN_ID)

        control.log("GLOBOSAT CREDENTIALS: %s" % credentials)

        return {'GLBID': credentials}
