from zope.i18nmessageid import MessageFactory
from zope.component import getUtility
from zope.publisher.browser import BrowserView
from zope.exceptions.interfaces import UserError
from zope.security.proxy import removeSecurityProxy
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth.interfaces import IPluggableAuthentication
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from z3c.pagelet.browser import BrowserPagelet
from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from quotationtool.user.interfaces import ISignup


_ = MessageFactory('quotationtool')


class SignUpViewlet(ViewletBase):
    """ A viewlet for the provider used on the login form. """

    template = ViewPageTemplateFile('signup_viewlet.pt')

    def render(self):
        return self.template()


class SignUpForm(BrowserPagelet):
    """A form for signing up to the site."""


class SignUpHelper(object):

    def _signupfolder(self):
        pau = getUtility(IAuthentication)
        if not IPluggableAuthentication.providedBy(pau):
            raise LookupError("Signup requires a PAU instance.")

        for name, plugin in pau.getAuthenticatorPlugins():
            # TODO: remove old
            if ISignup.providedBy(plugin):# or ISignupOLD.providedBy(plugin):
                return plugin

        raise TypeError("Signup requires a sign-up capable authenticator "
                        "plugin.")


class SignUpView(SignUpHelper, BrowserView):

    def signUp(self, login, title, password, confirmation):
        if confirmation != password:
            raise UserError(_('password-confirmation-error',
                              u"Password and confirmation didn't match"))
        folder = self._signupfolder()
        if login in folder:
            raise UserError(_('duplicate-login-error',
                              u"This login has already been chosen."))
        principal_id = folder.signUp(login, password, title)

        role_manager = IPrincipalRoleManager(self.context)
        role_manager = removeSecurityProxy(role_manager)
        for role in folder.signup_roles:
            role_manager.assignRoleToPrincipal(role, principal_id)
        self.request.response.redirect("@@welcome.html")


class WelcomeView(BrowserPagelet):
    """A view that welcomes a user that has yust signed in."""


class PasswordForm(BrowserPagelet):
    """A view that lets a user change his password."""


class PasswordView(SignUpHelper, BrowserView):
    """Actually change the password."""

    def changePassword(self, title, password=None, confirmation=None):
        if confirmation != password:
            raise UserError(_('password-confirmation-error',
                              u"Password and confirmation didn't match"))

        folder = self._signupfolder()
        pau = getUtility(IAuthentication)
        info = folder.principalInfo(self.request.principal.id[len(pau.prefix):])
        if info is None:
            raise UserError(_('unkown-accoount-error',
                              u"Can only change the title and password of users who signed up."))

        folder.changePasswordTitle(info.login, password, title)
        self.request.response.redirect(".")
