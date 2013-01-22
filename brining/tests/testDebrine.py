""" Unit Tests """
import sys
import os
import logging
import unittest

if sys.version_info[1] < 7: #python 2.6 or earlier
    from  ordereddict import OrderedDict
else:
    from collections import OrderedDict

import simplejson as json

#from libs import brining
from brining import Brine, debrines,  debrine

class DebrineTestCase(unittest.TestCase):
    """ Test mixin"""
    
    def setUp(self):
        class B(object):
            X = 0 #class attribute
            Y = -1 #class attribute
            def __init__(self):
                self.x =  1
                self.y =  2
                self.z =  3
                self._u = 4
                self._v = 5                      
                self._p = 0
                
            def getp(self):
                return self._p
            def setp(self, value):
                self._p = value
            def delp(self):
                del self._p
            p = property(getp, setp, delp, "Property p of T")
    
            @staticmethod
            def pest():
                pass
        
        self.B = B
        
    
    def tearDown(self):
        pass    

    def testDebrinesBasic(self):
        """ Debrine """
        logger.debug("\nBasic Debrine\n")

        brinee = self.B()
          
        s = \
"""{
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""        
        
        debrinee = debrines(s, [self.B])
        logger.debug("debrinee dir = \n%s\n debrinee __dict__ = \n%s" %\
                                    (dir(debrinee), debrinee.__dict__))        
        logger.debug( "Dumpable:\n%s" % (debrinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (debrinee._dumps()))        
        self.assertEqual(debrinee._dumps(), s)
        
        logger.debug("\nWith Properties\n")
        #with properties
        self.B._Propertied = True
        logger.debug( "Dumpable:\n%s" % (brinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (brinee._dumps()))
   
        self.assertDictEqual(brinee._dumpable(),
                OrderedDict([('p', 0), ('x', 1), ('y', 2), ('z', 3), ('@class', 'B')]))
        s = \
"""{
  "p": 0,
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""        
        self.assertEqual(brinee._dumps(), s)
        
        debrinee = debrines(s, [self.B])
        logger.debug("debrinee dir = \n%s\n debrinee __dict__ = \n%s" %\
                                    (dir(debrinee), debrinee.__dict__))        
        logger.debug( "Dumpable:\n%s" % (debrinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (debrinee._dumps()))        
        self.assertEqual(debrinee._dumps(), s)
        

        self.B._Keys = ['z', 'x', 'y']
        logger.debug("Debrine With Keys: %s \n", self.B._Keys)
        
        logger.debug("Dumpable:\n%s." % (brinee._dumpable()))
        logger.debug("Dumps:\n%s" % (brinee._dumps()))
                                     
        self.assertDictEqual(brinee._dumpable(),
                OrderedDict([('z', 3), ('x', 1), ('y', 2), ('@class', 'B')]))
        s = \
"""{
  "z": 3,
  "x": 1,
  "y": 2,
  "@class": "B"
}"""        
        self.assertEqual(brinee._dumps(), s)
        debrinee = debrines(s, [self.B])
        logger.debug("debrinee dir = \n%s\n debrinee __dict__ = \n%s" %\
                                    (dir(debrinee), debrinee.__dict__))        
        logger.debug( "Dumpable:\n%s" % (debrinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (debrinee._dumps()))        
        self.assertEqual(debrinee._dumps(), s)        
        
        

    def testDebrinesRecursive(self):
        """ Debrine recursive"""
        class B(object):
            def __init__(self):
                self.a = 0
                self.x =  1
                self.y =  2
                self.z =  3
                self.under = None
                self.name = "Over"
                
            def getp(self):
                return self._p
            def setp(self, value):
                self._p = value
            def delp(self):
                del self._p
            p = property(getp, setp, delp, "Property p of T")
    
            @staticmethod
            def pest():
                pass
        
        class C(object):
            def __init__(self):
                self.a = 2
                self.under = None
                self.name = "Other"
                
            def getp(self):
                return self._p
            def setp(self, value):
                self._p = value
            def delp(self):
                del self._p
            p = property(getp, setp, delp, "Property p of T")
    
            @staticmethod
            def pest():
                pass             
        
        over = B()
        over.name = "Over"
        over.under = B()
        over.a = 2
        over.under.name = "Under"
        over.under.a =  3
        over.under.under = C()
        over.under.under.name = "Bottom"
        
        logger.debug("\Debrine Recursive.")             
                        
        s = \
"""{
  "a": 2,
  "name": "Over",
  "under": {
    "a": 3,
    "name": "Under",
    "under": {
      "a": 2,
      "name": "Bottom",
      "under": null,
      "@class": "C"
    },
    "x": 1,
    "y": 2,
    "z": 3,
    "@class": "B"
  },
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""

        debrinee = debrines(s, [B, C])
        logger.debug("debrinee dir = \n%s\n debrinee __dict__ = \n%s" %\
                                    (dir(debrinee), debrinee.__dict__))        
        logger.debug( "Dumpable:\n%s" % (debrinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (debrinee._dumps()))        
        self.assertEqual(debrinee._dumps(), s)        
        

    def testDebrinesExtendable(self):
        """ Debrine """
        logger.debug("\nExtendable Debrine\n")

        brinee = self.B()
       
        s = \
"""{
  "w": 0,
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""        
        
        debrinee = debrines(s, [self.B], extendable=True)
        logger.debug("debrinee dir = \n%s\n debrinee __dict__ = \n%s" %\
                                    (dir(debrinee), debrinee.__dict__))        
        logger.debug( "Dumpable:\n%s" % (debrinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (debrinee._dumps()))        
        self.assertEqual(debrinee._dumps(), s)        
        
        

          
    def testDebrine(self):
        """ Debrine from dump to File"""
        
        filename = ".testdumpfile"        
        logger.debug("\nDebrine from file")
        w = \
"""{
  "x": 10,
  "y": 20,
  "z": 30,
  "@class": "B"
}"""
        with open(filename, "w") as f:
            f.write(w)
        logger.debug("File contents\n%s" % w)
        
        debrinee = debrine(filename,  [self.B])
        
        logger.debug("debrinee dir = \n%s\n debrinee __dict__ = \n%s" %\
                                    (dir(debrinee), debrinee.__dict__))        
        logger.debug( "Dumpable:\n%s" % (debrinee._dumpable()))
        logger.debug( "Dumps:\n%s" % (debrinee._dumps()))        
        self.assertEqual(debrinee._dumps(), w)          
        
def setupLogging():
    """ Setup loggin for tests"""
    global logger
    
    logger = logging.getLogger(__name__) #name logger after module
    logger.setLevel(logging.DEBUG)
    
    basicConsoleHandler = logging.StreamHandler() #sys.stderr
    basicformatter = logging.Formatter('%(message)s') #standard format
    basicConsoleHandler.setFormatter(basicformatter)
    logger.addHandler(basicConsoleHandler)
    logger.propagate = False    
                
        
def testSome():
    """ Unittest runner """
    setupLogging()
    
    tests = []
    tests.append('testDebrinesBasic')
    tests.append('testDebrinesRecursive')
    tests.append('testDebrinesExtendable')
    tests.append('testDebrine')
    
    
    suite = unittest.TestSuite(map(DebrineTestCase, tests))    
    unittest.TextTestRunner(verbosity=2).run(suite) 
        
def testAll():
    """ Unittest runner """
    setupLogging()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(DebrineTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)    

if __name__ == '__main__' and __package__ is None:
    
    logger = logging.getLogger(__name__) #name logger after module
    logger.setLevel(logging.DEBUG)
    
    basicConsoleHandler = logging.StreamHandler() #sys.stderr
    basicformatter = logging.Formatter('%(message)s') #standard format
    basicConsoleHandler.setFormatter(basicformatter)
    logger.addHandler(basicConsoleHandler)
    logger.propagate = False
    

    testAll() #run all unittests
    
    #testSome()#only run some

