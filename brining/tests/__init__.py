"""
    test package for brining module

See LICENSE.txt for Licensing details
Copyright (c) <2013> <Samuel M. Smith>
"""


__all__ = ['testBrine', 'testBrined', 'testDebrine']


def testAll():
    import testBrine
    import testBrined
    import testDebrine
    
    testBrine.testAll()
    testBrined.testAll()
    testDebrine.testAll()
    
    