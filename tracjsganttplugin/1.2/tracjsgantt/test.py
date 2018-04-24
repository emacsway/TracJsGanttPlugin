# -*- coding: utf-8 -*-
#
# Copyright (C) 2010-2014 Chris Nelson <Chris.Nelson@SIXNET.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import os
import tempfile
import shutil
import unittest
import filecmp
import copy

from trac.env import Environment

from tracpm import *


class TracPMTestCase(unittest.TestCase):

    index = [0]

    def _setup(self, configuration=None):
        configuration = configuration or \
            '[TracPM]\nfields.estimate = estimatedhours\n' + \
            'date_format = %Y-%m-%d\n' + \
            '[components]\ntracpm.* = enabled\n'
        instancedir = os.path.join(
            tempfile.gettempdir(), 'test-PM%d' % self.index[0])
        self.index[0] += 1
        if os.path.exists(instancedir):
            shutil.rmtree(instancedir, False)
        open(os.path.join(os.path.join(instancedir, 'conf'), 'trac.ini'),
             'a').write('\n' + configuration + '\n')
        return Environment(instancedir)

    def _get_data(self, env, options, tickets):
        pm = TracPM(env)
        pm.recomputeSchedule(options, tickets)
        result = ''
        for t in tickets:
            result += format_date(t['_calc_start'][0],
                                  '%Y-%m-%d %H:%M:%S') + '\n'
            result += format_date(t['_calc_finish'][0],
                                  '%Y-%m-%d %H:%M:%S') + '\n'
        return result

    def _do_test(self, env, options, tickets, testfun, testname):
        from os.path import join, dirname
        testdir = join(dirname(dirname(dirname(testfolder))), 'test')
        outfilename = join(testdir, testname + '.out')
        ctlfilename = join(testdir, testname + '.ctl')
        open(outfilename, 'w').write(testfun(env, options, tickets))
        return filecmp.cmp(outfilename, ctlfilename)

    def _do_test_diffs(self, env, options, tickets, testfun, testname):
        self._do_test(env, options, tickets, testfun, testname)
        from os.path import join, dirname
        testdir = join(dirname(dirname(dirname(testfolder))), 'test')
        from difflib import Differ
        d = Differ()

        def readall(ext):
            return open(join(testdir, testname + ext), 'rb').readlines()
        result = d.compare(readall('.ctl'),
                           readall('.out'))
        lines = [line for line in result if line[0] != ' ']
        self.assertEquals(0, len(lines))

    def test_resource_leveling_0_ASAP(self):
        env = self._setup()

        options = {
            'doResourceLeveling': '0',
            'hoursPerDay': 8,
            'useActuals': False,
            'schedule': 'asap',
            'force': True,
            'start': '2007-01-01'
        }

        tickets = []
        ticket = {'id': 1, 'estimatedhours': 6, 'children': [],
                  'priority': None, 'type': None, 'owner': 'Monty',
                  'status': 'new'}
        tickets.append(copy.copy(ticket))
        ticket['id'] = 2
        ticket['estimatedhours'] = 9
        tickets.append(copy.copy(ticket))

        self._do_test_diffs(env, options, tickets,
                            self._get_data, 'test_resource_leveling_0_ASAP')

    def test_resource_leveling_1_ASAP(self):
        env = self._setup()

        options = {
            'doResourceLeveling': '1',
            'hoursPerDay': 8,
            'useActuals': False,
            'schedule': 'asap',
            'force': True,
            'start': '2007-01-01'
        }

        tickets = []
        ticket = {
            'id': 1,
            'estimatedhours': 6,
            'children': [],
            'priority': None,
            'type': None,
            'owner': 'Monty',
            'status': 'new'
        }
        tickets.append(copy.copy(ticket))
        ticket['id'] = 2
        ticket['estimatedhours'] = 9
        tickets.append(copy.copy(ticket))

        self._do_test_diffs(env, options, tickets,
                            self._get_data, 'test_resource_leveling_1_ASAP')


def suite():
    return unittest.makeSuite(TracPMTestCase, 'test')


if __name__ == '__main__':
    testfolder = __file__
    unittest.main(defaultTest='suite')
