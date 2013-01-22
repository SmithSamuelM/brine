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
from brining import Brine, brined

class BrineTestCase(unittest.TestCase):
    """ Test decorator """
    def setUp(self):
        @brined()
        class B(object):
            X = 0 #class attribute
            Y = -1 #class attribute
            def __init__(self):
                
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
        
        self.B = B #save reference to class
        self.brined = B()
        self.brined.x =  1
        self.brined.y =  2
        self.brined.z =  3
        self.brined._u = 4
        self.brined._v = 5
        #logger.debug("\nself.brined dir = \n%s\nself.brined __dict__ = \n%s" %\
                    #(dir(self.brined), self.brined.__dict__))
    
    def tearDown(self):
        pass    

    def testDumpsBasic(self):
        """ Dumps """
        logger.debug("\nBasic Dumps\n")
        logger.debug("\nself.brined dir = \n%s\nself.brined __dict__ = \n%s" %\
                            (dir(self.brined), self.brined.__dict__))        
        logger.debug( "Dumpable:\n%s" % (self.brined._dumpable()))
        logger.debug( "Dumps:\n%s" % (self.brined._dumps()))
   
        self.assertDictEqual(self.brined._dumpable(),
                OrderedDict([('x', 1), ('y', 2), ('z', 3), ('@class', 'B')]))
        s = \
"""{
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""        
        self.assertEqual(self.brined._dumps(), s)
        
        logger.debug("\nWith Properties\n")
        #with properties
        self.B._Propertied = True
        logger.debug( "Dumpable:\n%s" % (self.brined._dumpable()))
        logger.debug( "Dumps:\n%s" % (self.brined._dumps()))
   
        self.assertDictEqual(self.brined._dumpable(),
                OrderedDict([('p', 0), ('x', 1), ('y', 2), ('z', 3), ('@class', 'B')]))
        s = \
"""{
  "p": 0,
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""        
        self.assertEqual(self.brined._dumps(), s)
        

    def testDumpsKeys(self):
        """ Dumps with reordered keys list """
        
        self.B._Keys = ['z', 'x', 'y']
        logger.debug("\nDump With Keys: %s \n", self.B._Keys)
        
        logger.debug("Dumpable:\n%s." % (self.brined._dumpable()))
        logger.debug("Dumps:\n%s" % (self.brined._dumps()))
                                     
        self.assertDictEqual(self.brined._dumpable(),
                OrderedDict([('z', 3), ('x', 1), ('y', 2), ('@class', 'B')]))
        s = \
"""{
  "z": 3,
  "x": 1,
  "y": 2,
  "@class": "B"
}"""        
        self.assertEqual(self.brined._dumps(), s)
        
        logger.debug("\nWith Properties\n")
        #with properties
        self.B._Propertied = True
        
        logger.debug("Dumpable:\n%s." % (self.brined._dumpable()))
        logger.debug("Dumps:\n%s" % (self.brined._dumps()))
                                     
        self.assertDictEqual(self.brined._dumpable(),
                OrderedDict([('z', 3), ('x', 1), ('y', 2), ('@class', 'B')]))
        s = \
"""{
  "z": 3,
  "x": 1,
  "y": 2,
  "@class": "B"
}"""        
        self.assertEqual(self.brined._dumps(), s)
        
        self.B._Keys = ['z', 'x', 'y', 'p']
        logger.debug("\nDump With Properties and Keys: %s \n", self.B._Keys)        
        logger.debug( "Dumpable:\n%s" % (self.brined._dumpable()))
        logger.debug( "Dumps:\n%s" % (self.brined._dumps()))
   
        self.assertDictEqual(self.brined._dumpable(),
                 OrderedDict([('z', 3), ('x', 1), ('y', 2), ('p', 0), ('@class', 'B')]))
        s = \
"""{
  "z": 3,
  "x": 1,
  "y": 2,
  "p": 0,
  "@class": "B"
}"""        
        self.assertEqual(self.brined._dumps(), s)


        self.B._Keys = ['x', 'w', 'y', '_t', '_u']
        logger.debug("With missing and extra keys: %s." % (self.B._Keys))
        logger.debug("Dumpable: %s." % (self.brined._dumpable()))
        logger.debug("Dumps: %s" % (self.brined._dumps()))        
        self.assertDictEqual(self.brined._dumpable(),
                             OrderedDict([('x', 1), ('y', 2), ('@class', 'B')]))                
        s = \
"""{
  "x": 1,
  "y": 2,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)

    def testDumpsRecursive(self):
        """ Dumps recursive"""
        over = self.B()
        over.name = "Over"
        over.under = self.B()
        over.a = 2
        over.under.name = "Under"
        over.under.a =  3
        logger.debug("\nDumps Recursive.")        
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))        
                        
        s = \
"""{
  "a": 2,
  "name": "Over",
  "under": {
    "a": 3,
    "name": "Under",
    "@class": "B"
  },
  "@class": "B"
}"""
        self.assertEqual(over._dumps(), s)
        
        self.B._Keys = [ 'name', 'under']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))         
        s = \
"""{
  "name": "Over",
  "under": {
    "name": "Under",
    "@class": "B"
  },
  "@class": "B"
}"""
        self.assertEqual(over._dumps(), s)
        
        self.B._Keys = [ 'name']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))        
        s = \
"""{
  "name": "Over",
  "@class": "B"
}"""
        self.assertEqual(over._dumps(), s)        
    
    def testDumpsSafely(self):
        """ Dumps with unserializible attributes"""
        class A(object):
            pass
        a = A()
        a.name = "Not Serializable"
        self.brined.name = "unserattr"
        self.brined.nsa = a
        logger.debug("\nTest Dumps Unserializable Attribute." )
        
        logger.debug("Dumpable unsafely:\n%s" % self.brined._dumpable())
        self.assertEqual(self.brined._dumpable().keys(),
                         ['name','nsa','x', 'y','z', '@class', ])
            
        with self.assertRaises(TypeError):
            logger.debug("Dumps unsafely:" )
            logger.debug("%s" % self.brined._dumps())
            
        
        self.B._Safed = True
        logger.debug("Dumpable safely:\n%s" % self.brined._dumpable())
        self.assertDictEqual(self.brined._dumpable(),
                             OrderedDict([('name', 'unserattr'),
                                          ('x', 1),
                                          ('y', 2),
                                          ('z', 3),
                                          ('@class', 'B')]))
        logger.debug("Dumps unsafely:\n%s" % self.brined._dumps())        
        s = \
"""{
  "name": "unserattr",
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)
                
    def testLoadsBasic(self):
        """ Loads tests"""
        logger.debug("\nTest Loads Basic." )
        logger.debug("Before Loads:\n%s" % self.brined._dumps())
        s = \
"""{
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)
        
        s = \
"""{
  "x": 4,
  "y": 5,
  "z": 6,
  "@class": "B"
}"""                        
        self.brined._loads(s)
        logger.debug("After Loads:\n%s" % self.brined._dumps())
        self.assertEqual(self.brined._dumps(), s)
        
        logger.debug("With Properly:")
        self.B._Propertied = True
        logger.debug("Before Loads:\n%s" % self.brined._dumps())
        s = \
"""{
  "p": 0,
  "x": 4,
  "y": 5,
  "z": 6,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)
        
        s = \
"""{
  "p": 7,
  "x": 8,
  "y": 9,
  "z": 10,
  "@class": "B"
}"""                        
        self.brined._loads(s)
        logger.debug("After Loads:\n%s" % self.brined._dumps())
        self.assertEqual(self.brined._dumps(), s)        
        
        self.B._Keys = ['x', 'y', 'p']
        logger.debug("With Keys: %s" % self.B._Keys)
        logger.debug("Before Loads:\n%s" % self.brined._dumps())
        s = \
"""{
  "x": 8,
  "y": 9,
  "p": 7,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)
        
        s = \
"""{
  "p": 11,
  "x": 12,
  "y": 13,
  "z": 14,
  "@class": "B"
}"""                        
        self.brined._loads(s)
        logger.debug("After Loads:\n%s" % self.brined._dumps())
        s = \
"""{
  "x": 12,
  "y": 13,
  "p": 11,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)         
        
    def testLoadsSafely(self):
        """ Loads into unserializible attributes"""
        class A(object):
            pass
        a = A()
        a.name = "Not Serializable"
        self.brined.name = "unserattr"
        self.brined.nsa = a
        logger.debug("\nTest Loads into Unserializable Attribute." )
        self.B._Safed = True
        logger.debug("Before Loads Safely:\n%s" % self.brined._dumps())
        s = \
"""{
  "name": "unserattr",
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""
        self.assertEqual(self.brined._dumps(), s)        
        
        logger.debug("Loads safely:" ) 
        s = \
"""{
  "name": "nsa ignored",
  "nsa": "WhoMe",
  "x": 2,
  "y": 2,
  "z": 3,
  "a": 4,
  "@class": "B"
}"""
        self.brined._loads(s)     
        logger.debug("After Loads:\n%s" % self.brined._dumps())
        s = \
"""{
  "name": "nsa ignored",
  "x": 2,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""        
        self.assertEqual(self.brined._dumps(), s)
        
        self.B._Safed = False
        s = \
"""{
  "name": "nsa not ignored",
  "nsa": "Woops",
  "x": 3,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""
        self.brined._loads(s)
        logger.debug("After Loads:\n%s" % self.brined._dumps())
        self.assertEqual(self.brined._dumps(), s)
        
    def testLoadsRecursive(self):
        """ Loads recursive"""
        over = self.B()
        over.name = "Over"
        over.under = self.B()
        over.a = 2
        over.under.name = "Under"
        over.under.a =  3
        logger.debug("\nLoads Recursive.")        
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Before Loads: \n%s" % (over._dumps()))        
                        
        s = \
"""{
  "a": 2,
  "name": "Over",
  "under": {
    "a": 3,
    "name": "Under",
    "@class": "B"
  },
  "@class": "B"
}"""
        self.assertEqual(over._dumps(), s)
        s = \
"""{
  "a": 20,
  "name": "Over",
  "under": {
    "a": 30,
    "name": "Under",
    "@class": "B"
  },
  "@class": "B"
}"""        
        over._loads(s)
        logger.debug("After Loads:\n%s" %  over._dumps())
        self.assertEqual( over._dumps(), s)        
        
        self.B._Keys = [ 'name', 'under']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))         
        s = \
"""{
  "name": "Over",
  "under": {
    "name": "Under",
    "@class": "B"
  },
  "@class": "B"
}"""
        self.assertEqual(over._dumps(), s)
        s = \
"""{
  "name": "Over More",
  "under": {
    "name": "Under Less",
    "@class": "B"
  },
  "@class": "B"
}"""        
        over._loads(s)
        logger.debug("After Loads:\n%s" %   over._dumps())
        self.assertEqual(  over._dumps(), s)
        
        self.B._Keys = [ 'name']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))        
        s = \
"""{
  "name": "Over More",
  "@class": "B"
}"""
        self.assertEqual(over._dumps(), s)
        s = \
"""{
  "name": "Over Less",
  "under": {
    "name": "Under More",
    "@class": "B"
  },
  "@class": "B"
}"""        
        over._loads(s)
        logger.debug("After Loads:\n%s" %   over._dumps())
        s = \
"""{
  "name": "Over Less",
  "@class": "B"
}"""        
        self.assertEqual(over._dumps(), s)
        
          
    def testDumpLoad(self):
        """ Dump to File, Load from File tests"""
        brinee = self.B()
        brinee.x =  1
        brinee.y =  2
        brinee.z =  3
        logger.debug("Brined: \n%s" % brinee._dumps())
        s = \
"""{
  "x": 1,
  "y": 2,
  "z": 3,
  "@class": "B"
}"""
        self.assertEqual(brinee._dumps(), s)
        
        filename = ".testdumpfile"
        logger.debug("\nDump to filename %s" % filename)
        brinee._dump(filename)
        
        with open(filename, "r") as f:
            r = f.read()

        logger.debug("File contents: \n%s" % r)
        self.assertEqual(brinee._dumps(), r)
        
        logger.debug("\nLoad from filename %s" % filename)
        w = \
"""{
  "x": 10,
  "y": 20,
  "z": 30,
  "@class": "B"
}"""
        with open(filename, "w") as f:
            f.write(w)
        
        brinee._load(filename)
        logger.debug("After Load: \n%s" % brinee._dumps())
        self.assertEqual(brinee._dumps(), w)
        
    def testDumpsUnhintedlyRecursive(self):
        """ Dumps unhintely recursive"""
        self.B._Hinted = False
        over = self.B()
        over.name = "Over"
        over.under = self.B()
        over.a = 2
        over.under.name = "Under"
        over.under.a =  3
        logger.debug("\nDumps Recursive.")        
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))        
                        
        s = \
"""{
  "a": 2,
  "name": "Over",
  "under": {
    "a": 3,
    "name": "Under"
  }
}"""
        self.assertEqual(over._dumps(), s)
        
        self.B._Keys = [ 'name', 'under']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))         
        s = \
"""{
  "name": "Over",
  "under": {
    "name": "Under"
  }
}"""
        self.assertEqual(over._dumps(), s)
        
        self.B._Keys = [ 'name']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))        
        s = \
"""{
  "name": "Over"
}"""
        self.assertEqual(over._dumps(), s)                       

    def testLoadsUnhintedlyRecursive(self):
        """ Loads recursive"""
        self.B._Hinted = False
        over = self.B()
        over.name = "Over"
        over.under = self.B()
        over.a = 2
        over.under.name = "Under"
        over.under.a =  3
        logger.debug("\nLoads Recursive.")        
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Before Loads: \n%s" % (over._dumps()))        
                        
        s = \
"""{
  "a": 2,
  "name": "Over",
  "under": {
    "a": 3,
    "name": "Under"
  }
}"""
        self.assertEqual(over._dumps(), s)
        s = \
"""{
  "a": 20,
  "name": "Over",
  "under": {
    "a": 30,
    "name": "Under"
  }
}"""        
        over._loads(s)
        logger.debug("After Loads:\n%s" %  over._dumps())
        self.assertEqual( over._dumps(), s)        
        
        self.B._Keys = [ 'name', 'under']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))         
        s = \
"""{
  "name": "Over",
  "under": {
    "name": "Under"
  }
}"""
        self.assertEqual(over._dumps(), s)
        s = \
"""{
  "name": "Over More",
  "under": {
    "name": "Under Less"
  }
}"""        
        over._loads(s)
        logger.debug("After Loads:\n%s" %   over._dumps())
        self.assertEqual(  over._dumps(), s)
        
        self.B._Keys = [ 'name']
        logger.debug("Recursive with keys: \n%s" % (self.B._Keys))
        logger.debug("Over: \n%s" % (over._dumpable()))
        logger.debug("Under: \n%s" % (over.under._dumpable()))        
        logger.debug("Over Dumps: \n%s" % (over._dumps()))        
        s = \
"""{
  "name": "Over More"
}"""
        self.assertEqual(over._dumps(), s)
        s = \
"""{
  "name": "Over Less",
  "under": {
    "name": "Under More"
  }
}"""        
        over._loads(s)
        logger.debug("After Loads:\n%s" %   over._dumps())
        s = \
"""{
  "name": "Over Less"
}"""        
        self.assertEqual(over._dumps(), s)
        
        
def testSome():
    """ Unittest runner """
    tests = []
    tests.append('testDumpsBasic')
    tests.append('testDumpsKeys')
    tests.append('testDumpsRecursive')
    tests.append('testDumpsSafely')
    tests.append('testLoadsBasic')
    tests.append('testLoadsSafely')
    tests.append('testLoadsRecursive')
    tests.append('testDumpLoad')
    tests.append('testDumpsUnhintedlyRecursive')
    tests.append('testLoadsUnhintedlyRecursive')
    
    
    suite = unittest.TestSuite(map(BrineTestCase, tests))    
    unittest.TextTestRunner(verbosity=2).run(suite) 
        
def testAll():
    """ Unittest runner """
    suite = unittest.TestLoader().loadTestsFromTestCase(BrineTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)    

if __name__ == '__main__' and __package__ is None:
    
    logger = logging.getLogger(__name__) #name logger after module
    logger.setLevel(logging.DEBUG)
    
    basicConsoleHandler = logging.StreamHandler() #sys.stderr
    basicformatter = logging.Formatter('%(message)s') #standard format
    basicConsoleHandler.setFormatter(basicformatter)
    logger.addHandler(basicConsoleHandler)
    logger.propagate = False
    

    #testAll() #run all unittests
    
    testSome()#only run some

