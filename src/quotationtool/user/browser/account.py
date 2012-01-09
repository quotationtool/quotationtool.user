from zope.interface import implements
import zope.component
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.location.interfaces import ILocation
from z3c.pagelet.browser import BrowserPagelet
from z3c.pagelet.interfaces import IPagelet

from quotationtool.user import interfaces
from quotationtool.user.interfaces import _


class AccountLabel(BrowserView):
    """ Label for account-controller."""

    def __call__(self):
        return _('account-label', u"Account")


class Account(BrowserView):
    """ Account is view that traverses to other views."""

    implements(interfaces.IAccountController)

    context = request = None
    __parent__ = None
    __name__ = u'account'

    viewInterface = interfaces.IAccountView

    def __init__(self, context, request):
        self.context = self.__parent__ = context
        self.request = request

    @property
    def views(self):
        for name, pagelet in zope.component.getAdapters(
            (self, self.request), IPagelet):
            if self.viewInterface.providedBy(pagelet):
                yield name, pagelet

    @property
    def viewMenu(self):
        # TODO
        raise NotImplemented

    view = None

    def publishTraverse(self, request, name):
        """ See IPublishTraverse"""
        if not name:
            raise Exception

        if '=' in name:
            view_name, content_name = name.split("=", 1)
            self.contentName = content_name

            if view_name.startswith('@@'):
                view_name = view_name[2:]
            self.view = zope.component.getMultiAdapter((self, request), name=view_name)
            return self.view

        if name.startswith('@@'):
            view_name = name[2:]
        else:
            view_name = name

        self.view = zope.component.queryMultiAdapter((self, request), name=view_name)
        return self.view

    browserDefault = u"index.html"
        

class AccountIndex(BrowserPagelet):
    """ Menu/Index page for account controller."""

    implements(interfaces.IAccountView)

    weight = 0

    title = description = u"Index"
    
    visible = False
