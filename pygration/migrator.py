
def step_name(step):
    """Get the name of a step.  It's just the name of the class."""
    return step.__name__


class StepMigrator(object):
    def __init__(self, version, step, state):
        self._version = version
        self._step = step
        self._state = state

    def version(self):
        return self._version

    def step_name(self):
        return step_name(self._step)

    def phase_complete(self, phase):
        print "phase=%s, state: add=%s, drop=%s, commit=%s" % (  phase
                                                               , self._state.add_state
                                                               , self._state.drop_state
                                                               , self._state.commit_state)
        if (not hasattr(self._step, phase)):
            return True
        state_flag = "%s_state" % phase
        state = getattr(self._state, state_flag)
        return state == 'pass'

    def migrate(self, db, phase):
        """The step wrapper that joins the db, step, history and phase."""
        step_instance = self._step()
        step_phase = getattr(step_instance, phase)
        result = step_phase(db)
        return 'pass'

    def rollback(self, db, phase):
        step_instance = self._step()
        func = "rollback_%s" % phase
        step_phase = getattr(step_instance, func)
        result = step_phase(db)

    def store_state(self, session, phase, state):
        state_flag = "%s_state" % phase
        if hasattr(self._state, state_flag):
            setattr(self._state, state_flag, state)
            self._state = session.merge(self._state)

    def __str__(self):
        return "%s.%s" % (self._version, step_name(self._step))

    def __repr__(self):
        return "<StepMigrator(%s, %s)>" % (self._version, self._step)


class LiveDB(object):
    def __init__(self, session):
        self._session = session

    def sql(self, sql):
        print "  Execute: '%s'" % sql
        self._session.execute(sql)

class NoopDB(object):
    def sql(self, sql):
        print "  Noop Execute: '%s'" % sql


class Migrator(object):
    """The object that handles the history and available version sets."""

    def __init__(self, session, database, migration_set, history):
        self._session = session
        self._database = database
        self._migration_set = migration_set
        self._history = history
        self._steps = []
        for m in self._migration_set.migrations():
            print "loading steps for migration(%s)" % m
            for s in m.steps():
                v = m.version()
                state = self._history.state(v, step_name(s))
                self._steps.append(StepMigrator(v, s, state))

    def migrate(self, phase, migration):
        print "Migrate(%s)" % phase
        migrate_steps = []
        complete_steps = []
        for m in self._steps:
            #print "\tcheck step(%s)" % m
            if m.version() != migration:
                continue
            if not m.phase_complete(phase):
                migrate_steps.append(m)
            else:
                complete_steps.append(m)

        if len(complete_steps) > 0:
            print "These steps are already complete:"
            for m in complete_steps:
                print "\t%s.%s()" % (str(m), phase)

        if len(migrate_steps) > 0:
            print "Begin migration:"
            for m in migrate_steps:
                print "\n%s.%s()" % (str(m), phase)
                result = m.migrate(self._database, phase)
                m.store_state(self._session, phase, result)
                self._session.commit()
        else:
            print "Nothing left to migrate."

    def rollback(self, phase, migration):
        print "Migrate(%s)" % phase
        rollback_steps = []
        for m in self._steps:
            if m.version() != migration:
                continue
            #print "\tcheck step(%s)" % m
            if m.phase_complete(phase):
                rollback_steps.insert(0, m)

        for m in rollback_steps:
            print "\n%s.%s()" % (str(m), phase)
            result = m.rollback(self._database, phase)
            m.store_state(self._session, phase, result)

    def find_next_phase(self):
        phase = None
        next_version, last_version = self.find_next_last()
        return version, phase

    def find_next_last(self):
        last = None
        provisional_next = None
        final_next = None
        for v in self._migration_set.versions():
            provisional_next = v
            if self._history.committed(v):
                last = v
            else:
                final_next = provisional_next
                break
        return final_next, last

    def show(self, what):
        print "Migrator.show(%s)" % what
        if what == 'next?':
            self.show_next()
        elif what == 'last?':
            self.show_last()
        elif len(what) == 0:
            self.show_all()
        else:
            raise "Unknown object to show."

    def show_all(self):
        print "All Migrations:"
        for m in self._join:
            print "\t%s" % m

    def show_next(self):
        print "Next Migration:"
        next, last = self.find_next_last()
        print "\t%s" % next

    def show_last(self):
        print "Last Migration:"
        next, last = self.find_next_last()
        print "\t%s" % last

