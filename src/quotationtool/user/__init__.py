import zope.component
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth.authentication import PluggableAuthentication
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin
from zope.security.proxy import removeSecurityProxy
from zope.securitypolicy.interfaces import IPrincipalRoleManager

from quotationtool.site.interfaces import INewQuotationtoolSiteEvent
from signup import SignupPrincipalFolder


@zope.component.adapter(INewQuotationtoolSiteEvent)
def createPAU(event):
    """ Create a pau (pluggable authentication utility, a signup
    principal folder in it and a manger user (!)."""
    sm = event.object.getSiteManager()

    sm['default']['pau'] = pau = PluggableAuthentication()
    pau.prefix = 'pau.'

    pau['signup_principal_folder'] = folder = SignupPrincipalFolder()
    pau.authenticatorPlugins = [folder.__name__]
    folder.prefix = u"users."
    folder.signup_roles = [u'quotationtool.Member']

    principal_id = folder.signUp('admin', 'Op3n', 'Quotationtool Manager')
    role_manager = IPrincipalRoleManager(event.object)
    role_manager = removeSecurityProxy(role_manager)
    role_manager.assignRoleToPrincipal('quotationtool.Manager', principal_id)

    pau['SessionCredentialsPlugin'] = session_creds = SessionCredentialsPlugin()
    pau.credentialsPlugins = [session_creds.__name__]
    session_creds.loginpagename = u"loginForm.html"
    loginfield = u"login"
    passwordfield = u"password"

    sm.registerUtility(pau, IAuthentication)
    
    
