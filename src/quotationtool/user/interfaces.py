from zope.interface import Interface
from zope.schema import List, Choice
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('quotationtool')



class ISignup(Interface):

  signup_roles = List(
      title=_(u"Roles for new principals"),
      description=_(u"These roles will be assigned to new principals."),
      value_type=Choice(vocabulary="Role Ids"),
      unique=True
      )

  def signUp(login, password, title):
      """Add a principal for yourself.  Returns the new principal's ID
      """

  def changePasswordTitle(login, password, title):
      """Change the principal's password and/or title.
      """

