import zope.interface
from z3c.menu.ready2go.item import SiteMenuItem
from zope.viewlet.manager import ViewletManager
from z3c.menu.ready2go import ISiteMenu, IContextMenu
from z3c.menu.ready2go.manager import MenuManager
from z3c.menu.ready2go.interfaces import IMenuManager

from quotationtool.skin.interfaces import IMainNav, ISubNavManager
from quotationtool.skin.browser.nav import MainNavItem


class IAccountMainNavItem(zope.interface.Interface):
    pass


class AccountMainNavItem(MainNavItem):
    zope.interface.implements(IAccountMainNavItem)


class IAccountSubNav(ISubNavManager):
    pass


AccountSubNav = ViewletManager(
    'accountsubnav', 
    ISiteMenu,
    bases = (MenuManager,))


IAccountSubNav.implementedBy(AccountSubNav)
