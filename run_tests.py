#!/usr/bin/env python2

import sys
import unittest
from tests.not_create_topic_test import NoneCreateTopicTest
from tests.delete_topic_test import DeleteTopicTest
from  tests.auth_test import AuthTest


if __name__ == '__main__':
    
    suite = unittest.TestSuite((
        unittest.makeSuite(AuthTest),
        unittest.makeSuite(NoneCreateTopicTest),
        unittest.makeSuite(DeleteTopicTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
