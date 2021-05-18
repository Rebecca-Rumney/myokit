#!/usr/bin/env python3
#
# Tests the OpenCL simulation classes
#
# This file is part of Myokit.
# See http://myokit.org for copyright, sharing, and licensing details.
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

import os
import unittest
import numpy as np

import myokit

from shared import OpenCL_DOUBLE_PRECISION, DIR_DATA

# Unit testing in Python 2 and 3
try:
    unittest.TestCase.assertRaisesRegex
except AttributeError:
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp


# Show simulation output
debug = False


@unittest.skipIf(
    not OpenCL_DOUBLE_PRECISION,
    'OpenCL double precision extension not supported on selected device.')
class SimulationOpenCL0dTest(unittest.TestCase):
    """
    Tests the OpenCL simulation against CVODE, in 0d mode.
    """
    def test_event_at_t0(self):
        # Compare the SimulationOpenCL output with CVODE output

        # Load model and event with appropriate level/duration
        m, p, _ = myokit.load(os.path.join(DIR_DATA, 'lr-1991.mmt'))
        e = p.head()

        # Make protocol to compare t=0 event implementations
        dt = 0.1    # Note: this is too big to be very accurate
        tmax = 1300
        p = myokit.Protocol()
        p.schedule(level=e.level(), duration=e.duration(), period=600, start=0)
        logvars = ['engine.time', 'membrane.V', 'engine.pace', 'ica.ICa']

        s1 = myokit.SimulationOpenCL(
            m, p, ncells=1, rl=True, precision=myokit.DOUBLE_PRECISION)
        s1.set_step_size(dt)
        d1 = s1.run(tmax, logvars, log_interval=dt).npview()

        s2 = myokit.Simulation(m, p)
        s2.set_tolerance(1e-8, 1e-8)
        d2 = s2.run(tmax, logvars, log_interval=dt).npview()

        # Check implementation of logging point selection
        e0 = np.max(np.abs(d1.time() - d2.time()))

        # Check implementation of pacing
        r1 = d1['engine.pace'] - d2['engine.pace']
        e1 = np.sum(r1**2)

        # Check membrane potential (will have some error!)
        # Using MRMS from Marsh, Ziaratgahi, Spiteri 2012
        r2 = d1['membrane.V', 0] - d2['membrane.V']
        r2 /= (1 + np.abs(d2['membrane.V']))
        e2 = np.sqrt(np.sum(r2**2) / len(r2))

        # Check logging of intermediary variables
        r3 = d1['ica.ICa', 0] - d2['ica.ICa']
        r3 /= (1 + np.abs(d2['ica.ICa']))
        e3 = np.sqrt(np.sum(r3**2) / len(r3))

        if debug:
            import matplotlib.pyplot as plt
            print('Event at t=0')

            plt.figure()
            plt.suptitle('Time points')
            plt.plot(d1.time(), label='Euler')
            plt.plot(d1.time(), label='CVODE')
            plt.legend()
            print(d1.time()[:7])
            print(d2.time()[:7])
            print(d1.time()[-7:])
            print(d2.time()[-7:])
            print(e0)

            plt.figure()
            plt.suptitle('Pacing signals')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['engine.pace'], label='OpenCL')
            plt.plot(d2.time(), d2['engine.pace'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r1)
            print(e1)

            plt.figure()
            plt.suptitle('Membrane potential')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['membrane.V', 0], label='OpenCL')
            plt.plot(d2.time(), d2['membrane.V'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e2)

            plt.figure()
            plt.suptitle('Calcium current')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['ica.ICa', 0], label='OpenCL')
            plt.plot(d2.time(), d2['ica.ICa'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e3)

            plt.show()

        self.assertLess(e0, 1e-14)
        self.assertLess(e1, 1e-14)
        self.assertLess(e2, 0.1)   # Note: The step size is really too big here
        self.assertLess(e3, 0.05)

    def test_event_at_step_size_multiple(self):

        # Load model and event with appropriate level/duration
        m, p, _ = myokit.load(os.path.join(DIR_DATA, 'lr-1991.mmt'))
        e = p.head()

        # Make protocol to compare with event at step-size multiple
        dt = 0.1   # Note: this is too big to be very accurate
        tmax = 1300
        p = myokit.Protocol()
        p.schedule(
            level=e.level(),
            duration=e.duration(),
            period=600,
            start=10)
        logvars = ['engine.time', 'membrane.V', 'engine.pace', 'ica.ICa']

        s1 = myokit.SimulationOpenCL(
            m, p, ncells=1, rl=True, precision=myokit.DOUBLE_PRECISION)
        s1.set_step_size(dt)
        d1 = s1.run(tmax, logvars, log_interval=dt).npview()

        s2 = myokit.Simulation(m, p)
        s2.set_tolerance(1e-8, 1e-8)
        d2 = s2.run(tmax, logvars, log_interval=dt).npview()

        # Check implementation of logging point selection
        e0 = np.max(np.abs(d1.time() - d2.time()))

        # Check implementation of pacing
        r1 = d1['engine.pace'] - d2['engine.pace']
        e1 = np.sum(r1**2)

        # Check membrane potential (will have some error!)
        # Using MRMS from Marsh, Ziaratgahi, Spiteri 2012
        r2 = d1['membrane.V', 0] - d2['membrane.V']
        r2 /= (1 + np.abs(d2['membrane.V']))
        e2 = np.sqrt(np.sum(r2**2) / len(r2))

        # Check logging of intermediary variables
        r3 = d1['ica.ICa', 0] - d2['ica.ICa']
        r3 /= (1 + np.abs(d2['ica.ICa']))
        e3 = np.sqrt(np.sum(r3**2) / len(r3))

        if debug:
            import matplotlib.pyplot as plt
            print('Event at t=0')

            plt.figure()
            plt.suptitle('Time points')
            plt.plot(d1.time(), label='OpenCL')
            plt.plot(d1.time(), label='CVODE')
            plt.legend()
            print(d1.time()[:7])
            print(d2.time()[:7])
            print(d1.time()[-7:])
            print(d2.time()[-7:])
            print(e0)

            plt.figure()
            plt.suptitle('Pacing signals')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['engine.pace'], label='OpenCL')
            plt.plot(d2.time(), d2['engine.pace'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r1)
            print(e1)

            plt.figure()
            plt.suptitle('Membrane potential')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['membrane.V', 0], label='OpenCL')
            plt.plot(d2.time(), d2['membrane.V'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e2)

            plt.figure()
            plt.suptitle('Calcium current')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['ica.ICa', 0], label='OpenCL')
            plt.plot(d2.time(), d2['ica.ICa'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e3)

            plt.show()

        self.assertLess(e0, 1e-14)
        self.assertLess(e1, 1e-14)
        self.assertLess(e2, 0.1)   # Note: The step size is really too big here
        self.assertLess(e3, 0.05)

    def test_event_not_at_multiple(self):

        # Load model and event with appropriate level/duration
        m, p, _ = myokit.load(os.path.join(DIR_DATA, 'lr-1991.mmt'))
        e = p.head()

        # Make protocol to compare with event NOT at step-size multiple
        dt = 0.1   # Note: this is too big to be very accurate
        tmax = 1300
        p = myokit.Protocol()
        p.schedule(
            level=e.level(),
            duration=e.duration(),
            period=600,
            start=1.05)

        logvars = ['engine.time', 'membrane.V', 'engine.pace', 'ica.ICa']

        s1 = myokit.SimulationOpenCL(
            m, p, ncells=1, rl=True, precision=myokit.DOUBLE_PRECISION)

        s1.set_step_size(dt)
        d1 = s1.run(tmax, logvars, log_interval=dt).npview()

        s2 = myokit.Simulation(m, p)
        s2.set_tolerance(1e-8, 1e-8)
        d2 = s2.run(tmax, logvars, log_interval=dt).npview()

        # Check implementation of logging point selection
        e0 = np.max(np.abs(d1.time() - d2.time()))

        # Check implementation of pacing
        r1 = d1['engine.pace'] - d2['engine.pace']
        e1 = np.sum(r1**2)

        # Check membrane potential (will have some error!)
        # Using MRMS from Marsh, Ziaratgahi, Spiteri 2012
        r2 = d1['membrane.V', 0] - d2['membrane.V']
        r2 /= (1 + np.abs(d2['membrane.V']))
        e2 = np.sqrt(np.sum(r2**2) / len(r2))

        # Check logging of intermediary variables
        r3 = d1['ica.ICa', 0] - d2['ica.ICa']
        r3 /= (1 + np.abs(d2['ica.ICa']))
        e3 = np.sqrt(np.sum(r3**2) / len(r3))

        if debug:
            import matplotlib.pyplot as plt
            print('Event at t=0')

            plt.figure()
            plt.suptitle('Time points')
            plt.plot(d1.time(), label='Euler')
            plt.plot(d1.time(), label='CVODE')
            plt.legend()
            print(d1.time()[:7])
            print(d2.time()[:7])
            print(d1.time()[-7:])
            print(d2.time()[-7:])
            print(e0)

            plt.figure()
            plt.suptitle('Pacing signals')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['engine.pace'], label='Euler')
            plt.plot(d2.time(), d2['engine.pace'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r1)
            print(e1)

            plt.figure()
            plt.suptitle('Membrane potential')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['membrane.V', 0], label='Euler')
            plt.plot(d2.time(), d2['membrane.V'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e2)

            plt.figure()
            plt.suptitle('Calcium current')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['ica.ICa', 0], label='OpenCL')
            plt.plot(d2.time(), d2['ica.ICa'], label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e3)

            plt.show()

        self.assertLess(e0, 1e-14)
        self.assertLess(e1, 1e-14)
        self.assertLess(e2, 0.2)   # Note: The step size is really too big here
        self.assertLess(e3, 0.05)

    def test_event_at_step_size_multiple_no_rl(self):
        # Test again, with event at step multiple, but now without Rush-Larsen

        # Load model and event with appropriate level/duration
        m, p, _ = myokit.load(os.path.join(DIR_DATA, 'lr-1991.mmt'))
        e = p.head()

        dt = 0.01   # Note: this is too big to be very accurate
        tmax = 200
        p = myokit.Protocol()
        p.schedule(
            level=e.level(),
            duration=e.duration(),
            period=600,
            start=10)
        logvars = ['engine.time', 'membrane.V', 'engine.pace', 'ica.ICa']

        s1 = myokit.SimulationOpenCL(
            m, p, ncells=1, rl=False, precision=myokit.DOUBLE_PRECISION)
        s1.set_step_size(dt)
        d1 = s1.run(tmax, logvars, log_interval=dt).npview()

        s2 = myokit.Simulation(m, p)
        s2.set_tolerance(1e-8, 1e-8)
        d2 = s2.run(tmax, logvars, log_interval=dt).npview()

        # Check membrane potential (will have some error!)
        # Using MRMS from Marsh, Ziaratgahi, Spiteri 2012
        r2 = d1['membrane.V', 0] - d2['membrane.V']
        r2 /= (1 + np.abs(d2['membrane.V']))
        e2 = np.sqrt(np.sum(r2**2) / len(r2))
        self.assertLess(e2, 0.05)  # Note: The step size is really too big here

        # Check logging of intermediary variables
        r3 = d1['ica.ICa', 0] - d2['ica.ICa']
        r3 /= (1 + np.abs(d2['ica.ICa']))
        e3 = np.sqrt(np.sum(r3**2) / len(r3))
        self.assertLess(e3, 0.01)


if __name__ == '__main__':
    import sys
    if '-v' in sys.argv:
        print('Running in debug/verbose mode')
        debug = True
    else:
        print('Add -v for more debug output')
    unittest.main()
