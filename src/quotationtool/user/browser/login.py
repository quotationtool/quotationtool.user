from z3c.pagelet.browser import BrowserPagelet
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.exceptions.interfaces import UserError
from zope.viewlet import viewlet
from zope.traversing.browser import absoluteURL
from zope.app.component import hooks
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class LoginViewlet(viewlet.ViewletBase):
    """A login viewlet for the tool box."""

    template = ViewPageTemplateFile('login_viewlet.pt')

    def render(self):
        return self.template()

    def quotationtoolURL(self):
        # use hooks because component lookup error if error is context
        return absoluteURL(hooks.getSite(), self.request)


#BBB:
class LoginForm(BrowserPagelet):
    """A login form"""

    def update(self):
        if (not IUnauthenticatedPrincipal.providedBy(self.request.principal)
            and 'quotationtool.Login' in self.request
            ):
            camefrom = self.request.get('camefrom', '.')
            self.request.response.redirect(camefrom)
            
        

