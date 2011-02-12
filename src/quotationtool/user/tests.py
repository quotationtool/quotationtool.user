import unittest
import doctest
from zope.component.testing import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

import quotationtool.user


def setUpZCML(test):
    """
        >>> import quotationtool.user
        >>> from zope.configuration.xmlconfig import XMLConfig
        >>> XMLConfig('configure.zcml', quotationtool.user)()

    """
    setUp(test)
    XMLConfig('configure.zcml', quotationtool.user)()


def test_suite():
    return unittest.TestSuite((
            doctest.DocTestSuite(setUp = setUp,
                                 tearDown = tearDown,
                                 optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
                                 ),
            ))
