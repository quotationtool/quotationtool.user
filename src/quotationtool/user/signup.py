import zope.interface
from zope.app.authentication.principalfolder import PrincipalFolder
from zope.app.authentication.principalfolder import InternalPrincipal

import interfaces



class SignupPrincipalFolder(PrincipalFolder):
    """Principal folder that allows users to sign up.
    """
    zope.interface.implements(interfaces.ISignup)

    signup_roles = []

    def signUp(self, login, password, title):
        self[login] = InternalPrincipal(login, password, title)
        return self.__parent__.prefix + self.prefix + login

    def changePasswordTitle(self, login, password, title):
        if login not in self:
            raise ValueError("Principal is not managed by this "
                             "principal source.")
        principal = self[login]
        principal.password = password and password or principal.password
        principal.title = title and title or principal.title
