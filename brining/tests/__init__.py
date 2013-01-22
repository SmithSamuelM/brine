"""
    test package for brining module

"""


__all__ = ['testBrine', 'testBrined', 'testDebrine']


def testAll():
    import testBrine
    import testBrined
    import testDebrine
    
    testBrine.testAll()
    testBrined.testAll()
    testDebrine.testAll()
    
    