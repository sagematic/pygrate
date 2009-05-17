import pygration
import traceback


class PygrationSet(pygration.Pygration):
    """A collection of steps to change the database.
    
    The pygration includes steps to make the change prior to and
    subsequent to the application deployment.
    """

    def __init__( self, pygrations ):
        self._pygrations = pygrations
        self._function = \
                { "add": self.add
                , "drop": self.hide
                , "commit_drop": self.drop
                , 'rollback_add': self.rollback_add
                , 'rollback_drop': self.rollback_hide
                , 'pre_add_check': self.pre_add_check
                , 'post_add_check': self.post_add_check
                }

    def migrate( self, db, stage ):
        f = self._function[stage]
        try:
            f(db)
        except Exception:
            # typ, err, tb = sys.exc_info()
            tb_lines = traceback.format_exc().splitlines()
            print ''
            print "Pygration", tb_lines[-1]
            print tb_lines[-3]
            print tb_lines[-2]
            print ''

    def add( self, db ):
        """Add elements to the db"""
        self.pre_add_check( db )
        for p in self._pygrations:
            p.add( db )
            p.post_add_check( db )

    def hide( self, db ):
        """Hide elements in the db before dropping them"""
        for p in self._pygrations:
            p.hide( db )

    def drop( self, db ):
        """Permanently drop elements from the db"""
        for p in self._pygrations:
            p.drop( db )

    def rollback_add( self, db ):
        """Rollback any items that were added to the db"""
        for p in self._pygrations:
            p.rollback_add( db )

    def rollback_hide( self, db ):
        """Rollback any items that were hidden in the db"""
        for p in self._pygrations:
            p.rollback_hide( db )

    def pre_add_check( self, db ):
        """Check the state of the DB before running any migrations."""
        for p in self._pygrations:
            p.pre_add_check( db )

    def post_add_check( self, db ):
        """Check the state of the DB after all migrations were run."""
        for p in self._pygrations:
            p.post_add_check( db )
