from zope.interface import Interface, Attribute
import zope.schema
#from zope.schema import List, Choice, Bool, Int, Object
from zope.i18nmessageid import MessageFactory
from z3c.pagelet.interfaces import IPagelet
from zope.location.interfaces import ILocation
from zope.publisher.interfaces import IPublishTraverse

_ = MessageFactory('quotationtool')


class ISignup(Interface):

    signup_roles = zope.schema.List(
        title=_(u"Roles for new principals"),
        description=_(u"These roles will be assigned to new principals."),
        value_type=zope.schema.Choice(vocabulary="Role Ids"),
        unique=True
        )

    def signUp(login, password, title):
        """Add a principal for yourself.  Returns the new principal's ID
        """

    def changePasswordTitle(login, password, title):
        """Change the principal's password and/or title.
        """


class IAccountView(IPagelet):
    """ A page for a use account."""

    weight = zope.schema.Int(
        title=u"Weight",
        description=u"Determines the order in menu.",
        required=True,
        )

    title = zope.schema.Text(
        title=u"Title",
        description=u"Title in menu.",
        required=True,
        )

    description = zope.schema.Text(
        title=u"Description",
        description=u"Description in menu.",
        )

    visible = zope.schema.Bool(
        title=u"Visible",
        description=u"Occurs in menu or not.",
        )


class IAccountController(ILocation, IPublishTraverse):
    """ The view-controller for the account."""

    viewInterface = zope.schema.InterfaceField(
        title=u"View Interface",
        description=u"View lookup interface.",
        required=True,
        default=IAccountView,
        )

    views = Attribute("List of views")

    viewMenu = Attribute("View menu information")

    view = Attribute(""" Current view""")

    def publishTraverse(request, name):
        """Traverse to view by it's name."""
 
