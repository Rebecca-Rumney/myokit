#!/usr/bin/env python3
#
# Tests the Fiber-tissue OpenCL simulation
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

from myokit.tests import OpenCL_FOUND, DIR_DATA, WarningCollector

# Unit testing in Python 2 and 3
try:
    unittest.TestCase.assertRaisesRegex
except AttributeError:
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp


# Show simulation output
debug = False


@unittest.skipIf(not OpenCL_FOUND, 'OpenCL not found on this system.')
class FiberTissueSimulationTest(unittest.TestCase):
    """
    Tests the fiber-tissue simulation.
    """

    @classmethod
    def setUpClass(cls):
        # Create objects for shared used in testing

        cls.mf = myokit.load_model(
            os.path.join(DIR_DATA, 'dn-1985-normalised.mmt'))
        cls.mt = myokit.load_model(os.path.join(DIR_DATA, 'lr-1991.mmt'))
        cls.p = myokit.pacing.blocktrain(1000, 2.0, offset=.01)

    def test_against_cvode(self):
        # Compare the fiber-tissue simulation output with CVODE output

        # Create simulation
        with WarningCollector():
            s1 = myokit.FiberTissueSimulation(
                self.mt,
                self.mt,
                self.p,
                ncells_fiber=(1, 1),
                ncells_tissue=(1, 1),
                nx_paced=1,
                g_fiber=(0, 0),
                g_tissue=(0, 0),
                g_fiber_tissue=0,
                precision=myokit.DOUBLE_PRECISION,
            )
        s1.set_step_size(0.01)

        # Set up logging
        logvars = ['engine.time', 'engine.pace', 'membrane.V', 'ica.ICa']
        logt = myokit.LOG_NONE

        # Run simulation
        tmax = 100
        dlog = 0.1
        with myokit.tools.capture():
            d1, logt = s1.run(tmax, logf=logvars, logt=logt, log_interval=dlog)
        del(logt)
        d1 = d1.npview()

        # Run CVODE simulation
        s2 = myokit.Simulation(self.mt, self.p)
        s2.set_tolerance(1e-8, 1e-8)
        d2 = s2.run(tmax, logvars, log_interval=dlog).npview()

        # Check implementation of logging point selection
        e0 = np.max(np.abs(d1.time() - d2.time()))

        # Check implementation of pacing
        r1 = d1['engine.pace'] - d2['engine.pace']
        e1 = np.sum(r1**2)

        # Check membrane potential (will have some error!)
        # Using MRMS from Marsh, Ziaratgahi, Spiteri 2012
        r2 = d1['membrane.V', 0, 0] - d2['membrane.V']
        r2 /= (1 + np.abs(d2['membrane.V']))
        e2 = np.sqrt(np.sum(r2**2) / len(r2))

        # Check logging of intermediary variables
        r3 = d1['ica.ICa', 0, 0] - d2['ica.ICa']
        r3 /= (1 + np.abs(d2['ica.ICa']))
        e3 = np.sqrt(np.sum(r3**2) / len(r3))

        if debug:
            import matplotlib.pyplot as plt
            print('Event at t=0')

            print(d1.time()[:7])
            print(d2.time()[:7])
            print(d1.time()[-7:])
            print(d2.time()[-7:])
            print(e0)

            plt.figure()
            plt.suptitle('Pacing signals')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['engine.pace'], '--', label='FiberTissue')
            plt.plot(d2.time(), d2['engine.pace'], '--', label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r1)
            print(e1)

            plt.figure()
            plt.suptitle('Membrane potential')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['membrane.V', 0, 0], label='FiberTissue')
            plt.plot(d2.time(), d2['membrane.V'], '--', label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e2)

            plt.figure()
            plt.suptitle('Calcium current')
            plt.subplot(2, 1, 1)
            plt.plot(d1.time(), d1['ica.ICa', 0, 0], label='FiberTissue')
            plt.plot(d2.time(), d2['ica.ICa'], '--', label='CVODE')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(d1.time(), r2)
            print(e3)

            plt.show()

        self.assertLess(e0, 1e-10)
        self.assertLess(e1, 1e-14)
        self.assertLess(e2, 0.05)
        self.assertLess(e3, 0.01)

    def test_basic(self):
        # Test basic functionality

        # Run times
        run = .1

        # Fiber/Tissue sizes
        nfx = 8
        nfy = 4
        ntx = 8
        nty = 6

        # Create simulation
        s = myokit.FiberTissueSimulation(
            self.mf,
            self.mt,
            self.p,
            ncells_fiber=(nfx, nfy),
            ncells_tissue=(ntx, nty),
            nx_paced=10,
            g_fiber=(235, 100),
            g_tissue=(9, 5),
            g_fiber_tissue=9
        )

        s.set_step_size(0.0012)
        # Set up logging
        logf = [
            'engine.time',
            'membrane.V',
            'isi.isiCa',
        ]
        logt = [
            'membrane.V',
            'ica.Ca_i',
            'ica.ICa',
        ]
        # Run simulation
        with myokit.tools.capture():
            logf, logt = s.run(run, logf=logf, logt=logt, log_interval=0.01)

        self.assertEqual(len(logf), 1 + 2 * nfx * nfy)
        self.assertIn('engine.time', logf)
        self.assertIn('0.0.membrane.V', logf)
        self.assertIn(str(nfx - 1) + '.' + str(nfy - 1) + '.membrane.V', logf)
        self.assertIn('0.0.isi.isiCa', logf)
        self.assertIn(str(nfx - 1) + '.' + str(nfy - 1) + '.isi.isiCa', logf)

        self.assertEqual(len(logt), 3 * ntx * nty)
        self.assertIn('0.0.membrane.V', logt)
        self.assertIn(str(ntx - 1) + '.' + str(nty - 1) + '.membrane.V', logt)
        self.assertIn('0.0.ica.Ca_i', logt)
        self.assertIn(str(ntx - 1) + '.' + str(nty - 1) + '.ica.Ca_i', logt)
        self.assertIn('0.0.ica.ICa', logt)
        self.assertIn(str(ntx - 1) + '.' + str(nty - 1) + '.ica.ICa', logt)

    def test_creation(self):
        # Tests fiber tisue simulation creation
        mf, mt, p = self.mf, self.mt, self.p
        FT = myokit.FiberTissueSimulation

        # Models must be valid
        m2 = mf.clone()
        m2.label('membrane_potential').set_rhs(None)
        self.assertFalse(m2.is_valid())
        self.assertRaises(myokit.MissingRhsError, FT, m2, mt)

        m2 = mt.clone()
        m2.label('membrane_potential').set_rhs(None)
        self.assertFalse(m2.is_valid())
        self.assertRaises(myokit.MissingRhsError, FT, mf, m2)

        # Models must have interdependent components
        m2 = mf.clone()
        x = m2.get('ik').add_variable('xx')
        x.set_rhs('membrane.i_ion')
        self.assertTrue(m2.has_interdependent_components())
        self.assertRaisesRegex(ValueError, 'interdependent', FT, m2, mt)

        m2 = mt.clone()
        x = m2.get('ina').add_variable('xx')
        x.set_rhs('membrane.i_ion')
        self.assertTrue(m2.has_interdependent_components())
        self.assertRaisesRegex(ValueError, 'interdependent', FT, mf, m2)

        # Dimensionalities must be 2d tuples
        s = FT(mf, mt, p, (5, 6), (7, 8))
        self.assertEqual(s.fiber_shape(), (6, 5))
        self.assertEqual(s.tissue_shape(), (8, 7))
        self.assertRaisesRegex(
            ValueError, r'fiber size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_fiber=None)
        self.assertRaisesRegex(
            ValueError, r'fiber size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_fiber=12)
        self.assertRaisesRegex(
            ValueError, r'fiber size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_fiber=(12, ))
        self.assertRaisesRegex(
            ValueError, r'fiber size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_fiber=(12, 12, 12))

        self.assertRaisesRegex(
            ValueError, r'tissue size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_tissue=None)
        self.assertRaisesRegex(
            ValueError, r'tissue size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_tissue=4)
        self.assertRaisesRegex(
            ValueError, r'tissue size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_tissue=(3, ))
        self.assertRaisesRegex(
            ValueError, r'tissue size must be a tuple \(nx, ny\)',
            FT, mf, mt, ncells_tissue=(6, 6, 6))

        # Number of cells must be at least 1
        self.assertRaisesRegex(
            ValueError, 'fiber size must be at least \(1, 1\)',
            FT, mf, mt, ncells_fiber=(0, 10))
        self.assertRaisesRegex(
            ValueError, 'fiber size must be at least \(1, 1\)',
            FT, mf, mt, ncells_fiber=(10, 0))
        self.assertRaisesRegex(
            ValueError, 'fiber size must be at least \(1, 1\)',
            FT, mf, mt, ncells_fiber=(-1, -1))
        self.assertRaisesRegex(
            ValueError, 'tissue size must be at least \(1, 1\)',
            FT, mf, mt, ncells_tissue=(0, 10))
        self.assertRaisesRegex(
            ValueError, 'tissue size must be at least \(1, 1\)',
            FT, mf, mt, ncells_tissue=(10, 0))
        self.assertRaisesRegex(
            ValueError, 'tissue size must be at least \(1, 1\)',
            FT, mf, mt, ncells_tissue=(-1, -1))
        self.assertRaisesRegex(
            ValueError, 'exceed that of the tissue',
            FT, mf, mt, p, (5, 6), (5, 5))

        # Number of paced cells must be >= 0
        FT(mf, mt, p, nx_paced=0)
        self.assertRaisesRegex(
            ValueError, 'width of the stimulus pulse must be non-negative',
            FT, mf, mt, p, nx_paced=-1)

        # Check conductivities are tuples
        self.assertRaisesRegex(
            ValueError, 'fiber conductivity must be a tuple \(gx, gy\)',
            FT, mf, mt, p, g_fiber=1)
        self.assertRaisesRegex(
            ValueError, 'fiber conductivity must be a tuple \(gx, gy\)',
            FT, mf, mt, p, g_fiber=(1, ))
        self.assertRaisesRegex(
            ValueError, 'fiber conductivity must be a tuple \(gx, gy\)',
            FT, mf, mt, p, g_fiber=(1, 1, 1))
        self.assertRaisesRegex(
            ValueError, 'tissue conductivity must be a tuple \(gx, gy\)',
            FT, mf, mt, p, g_tissue=1)
        self.assertRaisesRegex(
            ValueError, 'tissue conductivity must be a tuple \(gx, gy\)',
            FT, mf, mt, p, g_tissue=(1, ))
        self.assertRaisesRegex(
            ValueError, 'tissue conductivity must be a tuple \(gx, gy\)',
            FT, mf, mt, p, g_tissue=(1, 1, 1))

        # Check step size is > 0
        self.assertRaisesRegex(
            ValueError, 'step size must be greater', FT, mf, mt, p, dt=0)
        self.assertRaisesRegex(
            ValueError, 'step size must be greater', FT, mf, mt, p, dt=-1)

        # Precision must be single or double
        self.assertRaisesRegex(
            ValueError, 'Only single and double',
            FT, mf, mt,
            precision=myokit.SINGLE_PRECISION + myokit.DOUBLE_PRECISION)

        '''



        # Membrane potential must be given with label
        m2 = self.m.clone()
        m2.label('membrane_potential').set_label(None)
        self.assertRaisesRegex(
            ValueError, 'requires the membrane potential',
            FT, m2)

        # Membrane potential must be a state
        m2.get('ina.INa').set_label('membrane_potential')
        self.assertRaisesRegex(
            ValueError, 'must be a state variable',
            FT, m2)
    '''


if __name__ == '__main__':

    import sys
    if '-v' in sys.argv:
        print('Running in debug/verbose mode')
        debug = True
    else:
        print('Add -v for more debug output')

    import warnings
    warnings.simplefilter('always')

    unittest.main()
