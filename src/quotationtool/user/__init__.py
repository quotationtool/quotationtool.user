import zope.component
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth.authentication import PluggableAuthentication
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
from signup import SignupPrincipalFolder


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createPAU(event):
    sm = event.object.getSiteManager()

    sm['default']['pau'] = pau = PluggableAuthentication()
    pau.prefix = 'pau.'

    pau['signup_principal_folder'] = folder = SignupPrincipalFolder()
    pau.authenticatorPlugins = [folder.__name__]
    folder.prefix = u"users."
    folder.signup_roles = [u'quotationtool.Member']

    pau['SessionCredentialsPlugin'] = session_creds = SessionCredentialsPlugin()
    pau.credentialsPlugins = [session_creds.__name__]
    session_creds.loginpagename = u"login.html"
    loginfield = u"login"
    passwordfield = u"password"

    sm.registerUtility(pau, IAuthentication)
    
    
