import pygrate.pygrate
import pygrate.pygration
import unittest
import os.path
import sys


class TestPygration(pygrate.pygration.Pygration):
    def add( self ):
        pass


class PygrateTestCase(unittest.TestCase):
    def testListMigrations( self ):
        path, file = os.path.split( __file__ )
        p = pygrate.pygrate.Pygrator( path, 'r1' )
        m = p._list_migrations()

        self.assertEqual( [ 'employee' ], m )

    def testImportMigrations( self ):
        path, file = os.path.split( __file__ )
        p = pygrate.pygrate.Pygrator( path, 'r1' )
        p._import_migrations()
        print dir(p._modules)

    def testPygrationSubclass( self ):
        p = pygrate.pygrate.Pygrator( '.', 'r1' )
        tp = TestPygration
        bp = pygrate.pygration.Pygration

        self.assertEqual( True, p._pygration_subclass( tp ) )
        self.assertEqual( False, p._pygration_subclass( bp ) )
