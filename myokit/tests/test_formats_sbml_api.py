#!/usr/bin/env python3
#
# Tests Myokit's SBML api.
#
# This file is part of Myokit.
# See http://myokit.org for copyright, sharing, and licensing details.
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

import unittest

import myokit
import myokit.formats
import myokit.formats.sbml as sbml
from myokit.formats.sbml import SBMLParser

# Unit testing in Python 2 and 3
try:
    unittest.TestCase.assertRaisesRegex
except AttributeError:  # pragma: no python 3 cover
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

# Strings in Python 2 and 3
try:
    basestring
except NameError:   # pragma: no python 2 cover
    basestring = str


class TestCompartment(unittest.TestCase):
    """
    Unit tests for :class:`Compartment`.
    """

    @classmethod
    def setUpClass(cls):
        cls.model = sbml.Model(name='model')
        cls.sid = 'compartment'
        cls.c = cls.model.add_compartment(sid=cls.sid)

    def test_initial_value(self):

        # Check default initial value
        self.assertIsNone(self.c.initial_value())

        # Check bad value
        expr = 2
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.c.set_initial_value, expr)

        # Check good value
        expr = myokit.Number(2)
        self.c.set_initial_value(expr)

        self.assertEqual(self.c.initial_value(), expr)

    def test_is_rate(self):

        # Check default
        self.assertFalse(self.c.is_rate())

        # Check setting rate to true
        expr = myokit.Number(2)
        self.c.set_value(value=expr, is_rate=True)

        self.assertTrue(self.c.is_rate())

    def test_sid(self):
        self.assertEqual(self.c.sid(), self.sid)

    def test_size_units(self):

        # Check default units
        unit = myokit.units.dimensionless
        self.assertEqual(self.c.size_units(), unit)

        # Check spatial dimensions = 1
        self.c.set_spatial_dimensions(dimensions=1)
        unit = myokit.units.meter
        self.model.set_length_units(unit)

        self.assertEqual(self.c.size_units(), unit)

        # Check spatial dimensions = 2
        self.c.set_spatial_dimensions(dimensions=2)
        unit = myokit.units.meter**2
        self.model.set_area_units(unit)

        self.assertEqual(self.c.size_units(), unit)

        # Check spatial dimensions = 3
        self.c.set_spatial_dimensions(dimensions=3)
        unit = myokit.units.L
        self.model.set_volume_units(unit)

        self.assertEqual(self.c.size_units(), unit)

        # Check bad size units
        unit = 'mL'
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.c.set_size_units, unit)

        # Check valid size units
        unit = myokit.units.L * 1E-3
        self.c.set_size_units(unit)

        self.assertEqual(self.c.size_units(), unit)

    def test_spatial_dimensions(self):

        # Test valid dimensions
        dim = 2.31
        self.c.set_spatial_dimensions(dim)

        self.assertEqual(self.c.spatial_dimensions(), dim)

    def test_value(self):

        # Check bad value
        expr = 2
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.c.set_value, expr)

        # Check good value
        expr = myokit.Number(2)
        self.c.set_value(expr)

        self.assertEqual(self.c.value(), expr)


class TestModel(unittest.TestCase):
    """
    Unit tests for :class:`Model`.
    """

    def test_area_units(self):

        model = sbml.Model(name='model')

        area_units = myokit.units.meter ** 2
        model.set_area_units(area_units)

        self.assertEqual(model.area_units(), area_units)

    def test_assignable(self):

        model = sbml.Model(name='model')

        # Add assignables to model
        c_sid = 'compartment'
        model.add_compartment(c_sid)

        p_sid = 'parameters'
        model.add_parameter(p_sid)

        s_sid = 'species'
        comp = sbml.Compartment(model=model, sid=c_sid)
        model.add_species(compartment=comp, sid=s_sid)

        # Check that all assignables are accessible
        self.assertIsNotNone(model.assignable(c_sid))
        self.assertIsNotNone(model.assignable(p_sid))
        self.assertIsNotNone(model.assignable(s_sid))

    def test_base_unit(self):

        model = sbml.Model(name='model')

        # Check all base units
        self.assertEqual(
            model.base_unit('ampere'), myokit.units.A)
        self.assertEqual(
            model.base_unit('avogadro'),
            myokit.parse_unit('1 (6.02214179e23)'))
        self.assertEqual(model.base_unit('becquerel'), myokit.units.Bq)
        self.assertEqual(model.base_unit('candela'), myokit.units.cd)
        self.assertEqual(model.base_unit('coulomb'), myokit.units.C)
        self.assertEqual(
            model.base_unit('dimensionless'), myokit.units.dimensionless)
        self.assertEqual(model.base_unit('farad'), myokit.units.F)
        self.assertEqual(model.base_unit('gram'), myokit.units.g)
        self.assertEqual(model.base_unit('gray'), myokit.units.Gy)
        self.assertEqual(model.base_unit('henry'), myokit.units.H)
        self.assertEqual(model.base_unit('hertz'), myokit.units.Hz)
        self.assertEqual(model.base_unit('item'), myokit.units.dimensionless)
        self.assertEqual(model.base_unit('joule'), myokit.units.J)
        self.assertEqual(model.base_unit('katal'), myokit.units.kat)
        self.assertEqual(model.base_unit('kelvin'), myokit.units.K)
        self.assertEqual(model.base_unit('kilogram'), myokit.units.kg)
        self.assertEqual(model.base_unit('liter'), myokit.units.L)
        self.assertEqual(model.base_unit('litre'), myokit.units.L)
        self.assertEqual(model.base_unit('lumen'), myokit.units.lm)
        self.assertEqual(model.base_unit('lux'), myokit.units.lux)
        self.assertEqual(model.base_unit('meter'), myokit.units.m)
        self.assertEqual(model.base_unit('metre'), myokit.units.m)
        self.assertEqual(model.base_unit('mole'), myokit.units.mol)
        self.assertEqual(model.base_unit('newton'), myokit.units.N)
        self.assertEqual(model.base_unit('ohm'), myokit.units.ohm)
        self.assertEqual(model.base_unit('pascal'), myokit.units.Pa)
        self.assertEqual(model.base_unit('radian'), myokit.units.rad)
        self.assertEqual(model.base_unit('second'), myokit.units.s)
        self.assertEqual(model.base_unit('siemens'), myokit.units.S)
        self.assertEqual(model.base_unit('sievert'), myokit.units.Sv)
        self.assertEqual(model.base_unit('steradian'), myokit.units.sr)
        self.assertEqual(model.base_unit('tesla'), myokit.units.T)
        self.assertEqual(model.base_unit('volt'), myokit.units.V)
        self.assertEqual(model.base_unit('watt'), myokit.units.W)
        self.assertEqual(model.base_unit('weber'), myokit.units.Wb)

        # Check celsius (not supported)
        self.assertRaisesRegex(
            sbml.SBMLError,
            'The units "celsius" are not supported.',
            model.base_unit,
            'celsius')

        # Check bad base unit
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.base_unit, 'some unit')

    def test_compartment(self):

        model = sbml.Model(name='model')

        # Test bad sid
        sid = ';'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid SId "', model.add_compartment, sid)

        # Test good sid
        sid = 'compartment'
        model.add_compartment(sid)

        self.assertIsInstance(model.compartment(sid), sbml.Compartment)

        # Test duplicate sid
        sid = 'compartment'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Duplicate SId "', model.add_compartment, sid)

    def test_conversion_factor(self):

        model = sbml.Model(name='model')

        # Test default value
        self.assertIsNone(model.conversion_factor())

        # Bad conversion factor
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.set_conversion_factor, 10)

        # Good conversion factor
        factor = sbml.Parameter(model, 'parameter')
        model.set_conversion_factor(factor)

        self.assertIsInstance(
            model.conversion_factor(), sbml.Parameter)

    def test_extent_units(self):

        model = sbml.Model(name='model')

        # Test default
        self.assertEqual(model.extent_units(), myokit.units.dimensionless)

        # Test bad extent units
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.set_extent_units, 'mg')

        # Test good extent units
        model.set_extent_units(myokit.units.g)

        self.assertEqual(model.extent_units(), myokit.units.g)

    def test_length_units(self):

        model = sbml.Model(name='model')

        # Test default
        self.assertEqual(model.length_units(), myokit.units.dimensionless)

        # Test bad length units
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.set_length_units, 'm')

        # Test good length units
        model.set_length_units(myokit.units.meter)

        self.assertEqual(model.length_units(), myokit.units.meter)

    def test_name(self):

        name = 'model'
        model = sbml.Model(name=name)

        self.assertEqual(model.name(), name)

    def test_notes(self):

        model = sbml.Model(name='model')

        notes = 'Here are some notes.'
        model.set_notes(notes)

        self.assertEqual(model.notes(), notes)

    def test_parameter(self):

        model = sbml.Model(name='model')

        # Test bad sid
        sid = ';'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid SId "', model.add_parameter, sid)

        # Test good sid
        sid = 'parameter'
        model.add_parameter(sid)

        self.assertIsInstance(model.parameter(sid), sbml.Parameter)

        # Test duplicate sid
        sid = 'parameter'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Duplicate SId "', model.add_parameter, sid)

    def test_reaction(self):

        model = sbml.Model(name='model')

        # Test bad sid
        sid = ';'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid SId "', model.add_reaction, sid)

        # Test good sid
        sid = 'reaction'
        model.add_reaction(sid)

        self.assertIsInstance(model.reaction(sid), sbml.Reaction)

        # Test duplicate sid
        sid = 'reaction'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Duplicate SId "', model.add_reaction, sid)

    def test_species(self):

        model = sbml.Model(name='model')

        # Test bad compartment
        comp = 'some compartment'
        sid = 'species'
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.add_species, comp, sid)

        # Test bad sid
        c_sid = 'compartment'
        comp = sbml.Compartment(model=model, sid=c_sid)
        sid = ';'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid SId "', model.add_species, comp, sid)

        # Test good sid
        c_sid = 'compartment'
        comp = sbml.Compartment(model=model, sid=c_sid)
        sid = 'species'

        model.add_species(compartment=comp, sid=sid)

        self.assertIsInstance(model.species(sid), sbml.Species)

        # Test duplicate sid
        sid = 'species'
        self.assertRaisesRegex(
            sbml.SBMLError, 'Duplicate SId "', model.add_species, comp, sid)

    def test_substance_units(self):

        model = sbml.Model(name='model')

        # Test default
        self.assertEqual(model.substance_units(), myokit.units.dimensionless)

        # Test bad substance units
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.set_substance_units, 'mg')

        # Test good substance units
        model.set_substance_units(myokit.units.g)

        self.assertEqual(model.substance_units(), myokit.units.g)

    def test_time_units(self):

        model = sbml.Model(name='model')

        # Test default
        self.assertEqual(model.time_units(), myokit.units.dimensionless)

        # Test bad time units
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.set_time_units, 's')

        # Test good time units
        model.set_time_units(myokit.units.s)

        self.assertEqual(model.time_units(), myokit.units.s)

    def test_unit(self):

        model = sbml.Model(name='model')

        # Check bad units
        unitsid = 'some_unit'
        self.assertRaisesRegex(
            sbml.SBMLError, 'The unit SID <', model.unit, unitsid)

        # Check base unit
        unitsid = 'ampere'
        self.assertEqual(model.unit(unitsid), myokit.units.A)

        # Check invalid unitsid for user-defined unit
        unitsid = ';'
        unit = myokit.units.dimensionless
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid UnitSId "', model.add_unit, unitsid, unit)

        # Check unitsid for user-defined unit that coincides with base unit
        unitsid = 'ampere'
        unit = myokit.units.dimensionless
        self.assertRaisesRegex(
            sbml.SBMLError,
            'User unit overrides built-in unit: "',
            model.add_unit,
            unitsid,
            unit)

        # Check invalid user-defined unit
        unitsid = 'some_unit'
        unit = 'ampere'
        self.assertRaisesRegex(
            sbml.SBMLError,
            'Unit "',
            model.add_unit,
            unitsid,
            unit)

        # Check good user-defined unit
        unitsid = 'some_unit'
        unit = myokit.units.A
        model.add_unit(unitsid, unit)

        self.assertEqual(model.unit(unitsid), unit)

    def test_volume_units(self):

        model = sbml.Model(name='model')

        # Test default
        self.assertEqual(model.volume_units(), myokit.units.dimensionless)

        # Test bad volume units
        self.assertRaisesRegex(
            sbml.SBMLError, '<', model.set_volume_units, 'L')

        # Test good volume units
        model.set_volume_units(myokit.units.L)

        self.assertEqual(model.volume_units(), myokit.units.L)


class SBMLTestMyokitModel(unittest.TestCase):
    """
    Unit tests for Model.myokit_model method.
    """

    @classmethod
    def setUpClass(cls):
        cls.p = SBMLParser()

    def parse(self, xml, lvl=3, v=2):
        """
        Inserts the given ``xml`` into an <sbml> element, parses it, and
        returns the result.
        """
        return self.p.parse_string(self.wrap(xml, lvl, v))

    def wrap(self, xml_content, level=3, version=2):
        """
        Wraps ``xml_content`` into an SBML document of the specified ``level``
        and ``version``.
        """
        lv = 'level' + str(level) + '/version' + str(version)
        return (
            '<sbml xmlns="http://www.sbml.org/sbml/' + lv + '/core"'
            ' level="' + str(level) + '"'
            ' version="' + str(version) + '">'
            + xml_content +
            '</sbml>'
        )

    def test_compartments_exist(self):
        # Tests compartment conversion from SBML to myokit model.

        a = '<model><listOfCompartments>'
        b = '</listOfCompartments></model>'

        # Test simple compartment
        x = '<compartment id="a" />'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check whether component 'a' exists
        self.assertTrue(m.has_component('a'))

        # Check whether component 'myokit' exists
        self.assertTrue(m.has_component('myokit'))

        # Check that number of components is as expected
        # (component 'a' and 'myokit')
        self.assertEqual(m.count_components(), 2)

    def test_compartment_size_exists(self):
        # Tests whether compartment size variable is created.

        a = '<model><listOfCompartments>'
        b = '</listOfCompartments></model>'

        # Test simple compartment
        x = '<compartment id="c" />'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that size variable exists
        self.assertTrue(m.has_variable('c.size'))

    def test_compartment_size_unit(self):
        # Tests whether compartment size variable units are set correctly.

        a = '<model><listOfCompartments>'
        b = '</listOfCompartments></model>'

        # Test simple compartment
        x = '<compartment id="c" units="meter"/>'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that units are set correctly
        var = m.get('c.size')
        self.assertEqual(var.unit(), myokit.units.meter)

    def test_compartment_size_initial_value(self):
        # Tests whether setting the intial value of size variable works.

        a = '<model><listOfCompartments>' \
            + '<compartment id="c" size="10"/>' \
            + '</listOfCompartments>'

        b = '</model>'

        # Test 1: Initial value assigned from compartment
        m = self.parse(a + b)
        m = m.myokit_model()

        # Check initial value of size
        var = m.get('c.size')
        self.assertEqual(var.eval(), 10)

        # Test 2: Initial value assigned by initialAssignment
        x = '<listOfInitialAssignments>' + \
            '  <initialAssignment symbol="c">' + \
            '    <math xmlns="http://www.w3.org/1998/Math/MathML">' + \
            '      <cn>5</cn>' + \
            '    </math>' + \
            '  </initialAssignment>' + \
            '</listOfInitialAssignments>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check initial value of size
        var = m.get('c.size')
        self.assertEqual(var.eval(), 5)

    def test_compartment_size_values(self):
        # Tests whether setting the value of the size variable works.

        a = '<model><listOfCompartments>' + \
            '  <compartment id="c" size="10"/>' + \
            '</listOfCompartments>' + \
            '<listOfParameters>' + \
            '  <parameter id="V" value="1.2">' + \
            '  </parameter>' + \
            '</listOfParameters>'

        b = '</model>'

        # Test I: Set by assignmentRule
        x = '<listOfRules>' + \
            '  <assignmentRule variable="c"> ' + \
            '    <math xmlns="http://www.w3.org/1998/Math/MathML">' + \
            '      <apply>' + \
            '        <plus/>' + \
            '        <ci> V </ci>' + \
            '        <cn> 5 </cn>' + \
            '      </apply>' + \
            '    </math>' + \
            '  </assignmentRule>' + \
            '</listOfRules>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check initial value of size
        var = m.get('c.size')
        self.assertEqual(var.eval(), 6.2)

        # Test II: Set by rateRule
        x = '<listOfRules>' + \
            '  <rateRule variable="c"> ' + \
            '    <math xmlns="http://www.w3.org/1998/Math/MathML">' + \
            '      <apply>' + \
            '        <plus/>' + \
            '        <ci> V </ci>' + \
            '        <cn> 5 </cn>' + \
            '      </apply>' + \
            '    </math>' + \
            '  </rateRule>' + \
            '</listOfRules>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that size is state variable
        var = m.get('c.size')
        self.assertTrue(var.is_state())

        # Check that value is set correctly
        self.assertEqual(var.eval(), 6.2)

    def test_existing_myokit_compartment(self):
        # Tests whether renaming of 'myokit' compartment works.

        a = '<model><listOfCompartments>'
        b = '</listOfCompartments></model>'

        # Test simple compartment
        x = '<compartment id="myokit" />'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check whether component 'a' exists
        self.assertTrue(m.has_component('myokit'))

        # Check whether component 'myokit' exists
        self.assertTrue(m.has_component('myokit_1'))

        # Check that number of components is as expected
        # (component 'a' and 'myokit')
        self.assertEqual(m.count_components(), 2)

    def test_species_exist(self):
        # Tests whether species initialisation in amount and concentration
        # works.
        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>')
        b = (' </listOfSpecies>'
             '</model>')

        # Species in amount
        x = '<species compartment="c" id="spec" hasOnlySubstanceUnits="true"/>'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check whether species exists in amount
        self.assertTrue(m.has_variable('c.spec_amount'))

        # Check that component has 2 variables
        # [size, spec_amount]
        component = m.get('c')
        self.assertEqual(component.count_variables(), 2)

        # Species in concentration
        x = '<species compartment="c" id="spec" />'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check whether species exists in amount and concentration
        self.assertTrue(m.has_variable('c.spec_amount'))
        self.assertTrue(m.has_variable('c.spec_concentration'))

        # Check that component has 3 variables
        # [size, spec_amount, spec_concentration]
        component = m.get('c')
        self.assertEqual(component.count_variables(), 3)

    def test_species_units(self):
        # Tests whether species units are set properly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>')
        b = (' </listOfSpecies>'
             '</model>')

        # Test I: No substance nor size units provided
        x = '<species compartment="c" id="spec" />'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that units are set properly
        amount = m.get('c.spec_amount')
        conc = m.get('c.spec_concentration')

        self.assertEqual(amount.unit(), myokit.units.dimensionless)
        self.assertEqual(conc.unit(), myokit.units.dimensionless)

        # Test II: Substance and size units provided
        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" units="meter"/>'
             ' </listOfCompartments>'
             ' <listOfSpecies>')
        b = (' </listOfSpecies>'
             '</model>')

        x = '<species compartment="c" id="spec" substanceUnits="kilogram"/>'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that units are set properly
        amount = m.get('c.spec_amount')
        conc = m.get('c.spec_concentration')

        self.assertEqual(amount.unit(), myokit.units.kg)
        self.assertEqual(conc.unit(), myokit.units.kg / myokit.units.meter)

    def test_species_initial_values(self):
        # Tests whether initial values of species is set properly.
        a = ('<model>'
             '  <listOfCompartments>'
             '    <compartment id="c" size="10"/>'
             '  </listOfCompartments>'
             '  <listOfSpecies>'
             '    <species compartment="c" id="spec"'
             '      initialConcentration="2.1"/>'
             '  </listOfSpecies>')
        b = ('</model>')

        # Test I: Set by species
        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that intial values are set
        amount = m.get('c.spec_amount')
        conc = m.get('c.spec_concentration')

        self.assertEqual(amount.eval(), 21)
        self.assertEqual(conc.eval(), 2.1)

        # Test II: Set by initialAssignment
        x = ('<listOfInitialAssignments>'
             '  <initialAssignment symbol="spec">'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <cn>5</cn>'
             '    </math>'
             '  </initialAssignment>'
             '</listOfInitialAssignments>')

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that intial values are set
        amount = m.get('c.spec_amount')
        conc = m.get('c.spec_concentration')

        self.assertEqual(amount.eval(), 50)
        self.assertEqual(conc.eval(), 5)

    def test_species_values(self):
        # Tests whether values of species is set properly. This does not
        # include rate expressions from reactions.

        a = ('<model>'
             '  <listOfCompartments>'
             '    <compartment id="c" size="10"/>'
             '  </listOfCompartments>'
             '  <listOfSpecies>'
             '    <species compartment="c" id="spec"'
             '      initialConcentration="2.1" boundaryCondition="true"/>'
             '  </listOfSpecies>')
        b = ('</model>')

        # Test I: Set by assignmentRule
        x = ('<listOfRules>'
             '  <assignmentRule variable="spec"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <apply>'
             '        <plus/>'
             '        <ci> c </ci>'
             '        <cn> 5 </cn>'
             '      </apply>'
             '    </math>'
             '  </assignmentRule>'
             '</listOfRules>')

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that values are set
        amount = m.get('c.spec_amount')
        conc = m.get('c.spec_concentration')

        self.assertEqual(amount.eval(), 150)
        self.assertEqual(conc.eval(), 15)

        # Test II: Set by rateRule
        x = ('<listOfRules>'
             '  <rateRule variable="spec"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <apply>'
             '        <plus/>'
             '        <ci> c </ci>'
             '        <cn> 5 </cn>'
             '      </apply>'
             '    </math>'
             '  </rateRule>'
             '</listOfRules>')

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that intial values are set
        damount = m.get('c.spec_amount')
        conc = m.get('c.spec_concentration')

        self.assertEqual(damount.eval(), 150)
        self.assertEqual(conc.eval(), 2.1)

    def test_parameter_exist(self):
        # Tests whether initialisation of parameters works properly.

        a = '<model><listOfParameters>'
        b = '</listOfParameters></model>'

        x = '<parameter id="a" /><parameter id="b" />'
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that model created parameters in 'myokit' component
        self.assertTrue(m.has_variable('myokit.a'))
        self.assertTrue(m.has_variable('myokit.b'))

        # Check that total number of parameters is 3
        # [a, b, time]
        self.assertEqual(m.count_variables(), 3)

    def test_parameter_units(self):
        # Tests whether parameter units are set properly.

        a = '<model><listOfParameters>'
        b = '</listOfParameters></model>'

        x = ('<parameter id="c" value="2" />'
             '<parameter id="d" units="volt" />'
             '<parameter id="e" units="ampere" value="-1.2e-3" />')
        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Get parameters
        c = m.get('myokit.c')
        d = m.get('myokit.d')
        e = m.get('myokit.e')

        # Check that units are set properly
        self.assertIsNone(c.unit())
        self.assertEqual(d.unit(), myokit.units.volt)
        self.assertEqual(e.unit(), myokit.units.ampere)

    def test_parameter_initial_values(self):
        # Tests whether initial values of parameters are set correctly.

        a = '<model>'
        b = '</model>'

        # Test I: Initial value set by parameter
        x = '<listOfParameters>' + \
            '  <parameter id="V" value="1.2">' + \
            '  </parameter>' + \
            '</listOfParameters>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check initial value of parameter
        var = m.get('myokit.V')
        self.assertEqual(var.eval(), 1.2)

        # Test II: Initial value set by initialAssignment
        x = '<listOfParameters>' + \
            '  <parameter id="V" value="1.2">' + \
            '  </parameter>' + \
            '</listOfParameters>' + \
            '<listOfInitialAssignments>' + \
            '  <initialAssignment symbol="V">' + \
            '    <math xmlns="http://www.w3.org/1998/Math/MathML">' + \
            '      <cn>5</cn>' + \
            '    </math>' + \
            '  </initialAssignment>' + \
            '</listOfInitialAssignments>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check initial value of parameter
        var = m.get('myokit.V')
        self.assertEqual(var.eval(), 5)

    def test_parameter_values(self):
        # Tests whether values of parameters are set correctly.

        a = '<model>' + \
            '  <listOfParameters>' + \
            '    <parameter id="V" value="1.2">' + \
            '    </parameter>' + \
            '    <parameter id="K" value="3">' + \
            '    </parameter>' + \
            '  </listOfParameters>'
        b = '</model>'

        # Test I: Set by assignmentRule
        x = '<listOfRules>' + \
            '  <assignmentRule variable="V"> ' + \
            '    <math xmlns="http://www.w3.org/1998/Math/MathML">' + \
            '      <apply>' + \
            '        <plus/>' + \
            '        <ci> K </ci>' + \
            '        <cn> 5 </cn>' + \
            '      </apply>' + \
            '    </math>' + \
            '  </assignmentRule>' + \
            '</listOfRules>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check value of parameter
        var = m.get('myokit.V')
        self.assertEqual(var.eval(), 8)

        # Test II: Set by rateRule
        x = '<listOfRules>' + \
            '  <rateRule variable="V"> ' + \
            '    <math xmlns="http://www.w3.org/1998/Math/MathML">' + \
            '      <apply>' + \
            '        <plus/>' + \
            '        <ci> V </ci>' + \
            '        <cn> 5 </cn>' + \
            '      </apply>' + \
            '    </math>' + \
            '  </rateRule>' + \
            '</listOfRules>'

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that parameter is state variable
        var = m.get('myokit.V')
        self.assertTrue(var.is_state())

        # Check value of parameter
        self.assertEqual(var.eval(), 6.2)

    def test_stoichiometries_exist(self):
        # Tests whether stoichiometries are created properly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" />'
             '  <species id="s2" compartment="c" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1" id="sr" />'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2" id="sp" />'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that stoichiometry variables exists
        self.assertTrue(m.has_variable('c.sr'))
        self.assertTrue(m.has_variable('c.sp'))

    def test_stoichiometries_initial_value(self):
        # Tests whether initial values of stoichiometries are set properly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" />'
             '  <species id="s2" compartment="c" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1" id="sr" stoichiometry="2.1"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2" id="sp" stoichiometry="3.5"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        # Test I: Set by speciesReference
        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that initial values are set properly
        stoich_reactant = m.get('c.sr')
        stoich_product = m.get('c.sp')

        self.assertEqual(stoich_reactant.eval(), 2.1)
        self.assertEqual(stoich_product.eval(), 3.5)

        # Test I: Set by initialAssignment
        x = (' <listOfInitialAssignments>'
             '  <initialAssignment symbol="sr">'
             '   <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <cn>4.51</cn>'
             '   </math>'
             '  </initialAssignment>'
             '  <initialAssignment symbol="sp">'
             '   <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <cn>6</cn>'
             '   </math>'
             '  </initialAssignment>'
             ' </listOfInitialAssignments>')

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that initial values are set properly
        stoich_reactant = m.get('c.sr')
        stoich_product = m.get('c.sp')

        self.assertEqual(stoich_reactant.eval(), 4.51)
        self.assertEqual(stoich_product.eval(), 6)

    def test_stoichiometry_values(self):
        # Tests whether values of parameters are set correctly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfParameters>'
             '  <parameter id="V" value="10.23">'
             '  </parameter>'
             ' </listOfParameters>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" />'
             '  <species id="s2" compartment="c" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1" id="sr" stoichiometry="2.1"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2" id="sp" stoichiometry="3.5"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        # Test I: Set by assignmentRule
        x = ('<listOfRules>'
             '  <assignmentRule variable="sr"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <apply>'
             '        <plus/>'
             '        <ci> V </ci>'
             '        <cn> 5 </cn>'
             '      </apply>'
             '    </math>'
             '  </assignmentRule>'
             '  <assignmentRule variable="sp"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <apply>'
             '        <plus/>'
             '        <ci> V </ci>'
             '        <cn> 3.81 </cn>'
             '      </apply>'
             '    </math>'
             '  </assignmentRule>'
             '</listOfRules>')

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check value of stoichiometries
        var = m.get('c.sr')
        self.assertEqual(var.eval(), 15.23)

        var = m.get('c.sp')
        self.assertAlmostEqual(var.eval(), 14.04)

        # Test II: Set by rateRule
        x = ('<listOfRules>'
             '  <rateRule variable="sr"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <apply>'
             '        <plus/>'
             '        <ci> V </ci>'
             '        <cn> 3 </cn>'
             '      </apply>'
             '    </math>'
             '  </rateRule>'
             '  <rateRule variable="sp"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <apply>'
             '        <minus/>'
             '        <ci> V </ci>'
             '        <cn> 1 </cn>'
             '      </apply>'
             '    </math>'
             '  </rateRule>'
             '</listOfRules>')

        m = self.parse(a + x + b)
        m = m.myokit_model()

        # Check that stoichiometries are state variables
        var = m.get('c.sr')
        self.assertTrue(var.is_state())

        var = m.get('c.sp')
        self.assertTrue(var.is_state())

        # Check value of stoichiometries
        var = m.get('c.sr')
        self.assertEqual(var.eval(), 13.23)

        var = m.get('c.sp')
        self.assertEqual(var.eval(), 9.23)

    def test_reaction_expression(self):
        # Tests whether species reaction rate expressions are set correctly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" initialAmount="2" />'
             '  <species id="s2" compartment="c" initialConcentration="1.5" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that species are state variables
        var = m.get('c.s1_amount')
        self.assertTrue(var.is_state())

        var = m.get('c.s2_amount')
        self.assertTrue(var.is_state())

        # Check rates
        var = m.get('c.s1_amount')
        self.assertEqual(var.eval(), -(2 / 1.2 + 1.5))

        var = m.get('c.s2_amount')
        self.assertEqual(var.eval(), 2 / 1.2 + 1.5)

    def test_reaction_no_kinteic_law(self):
        # Tests whether missing kinetic law is handled correctly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" initialAmount="2" />'
             '  <species id="s2" compartment="c" initialConcentration="1.5" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2"/>'
             '   </listOfProducts>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that species are state variables
        var = m.get('c.s1_amount')
        self.assertFalse(var.is_state())

        var = m.get('c.s2_amount')
        self.assertFalse(var.is_state())

        # Check rates
        var = m.get('c.s1_amount')
        self.assertEqual(var.eval(), 2)

        var = m.get('c.s2_amount')
        self.assertEqual(var.eval(), 1.2 * 1.5)

    def test_reaction_boundary_species(self):
        # Tests whether rate of boundary species remains unaltered.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" initialAmount="2" />'
             '  <species id="s2" compartment="c" initialAmount="2"'
             '    boundaryCondition="true"/>'
             '  <species id="s3" compartment="c" initialConcentration="1.5"'
             '    boundaryCondition="true"/>'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1"/>'
             '    <speciesReference species="s2"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s3"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s3</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that species are state variables
        var = m.get('c.s1_amount')
        self.assertTrue(var.is_state())

        var = m.get('c.s2_amount')
        self.assertFalse(var.is_state())

        var = m.get('c.s3_amount')
        self.assertFalse(var.is_state())

        # Check rates
        var = m.get('c.s1_amount')
        self.assertEqual(var.eval(), -(2 / 1.2 + 1.5))

        var = m.get('c.s2_amount')
        self.assertEqual(var.eval(), 2)

        var = m.get('c.s3_amount')
        self.assertEqual(var.eval(), 1.2 * 1.5)

    def test_reaction_stoichiometry(self):
        # Tests whether stoichiometry is used in reactions correctly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" initialAmount="2" />'
             '  <species id="s2" compartment="c" initialConcentration="1.5" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1" stoichiometry="3"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2" stoichiometry="2"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that species are state variables
        var = m.get('c.s1_amount')
        self.assertTrue(var.is_state())

        var = m.get('c.s2_amount')
        self.assertTrue(var.is_state())

        # Check rates
        var = m.get('c.s1_amount')
        self.assertEqual(var.eval(), -3 * (2 / 1.2 + 1.5))

        var = m.get('c.s2_amount')
        self.assertEqual(var.eval(), 2 * (2 / 1.2 + 1.5))

    def test_reaction_stoichiometry_parameter(self):
        # Tests whether stoichiometry is used in reactions correctly,
        # when it's set by a parameter.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" initialAmount="2" />'
             '  <species id="s2" compartment="c" initialConcentration="1.5" />'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference id="s1ref" species="s1"'
             '      stoichiometry="3"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference id="s2ref" species="s2"'
             '      stoichiometry="2"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        x = ('<listOfRules>'
             '  <assignmentRule variable="s1ref"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <cn> 5 </cn>'
             '    </math>'
             '  </assignmentRule>'
             '  <rateRule variable="s2ref"> '
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '      <cn> 3.81 </cn>'
             '    </math>'
             '  </rateRule>'
             '</listOfRules>')

        m = self.parse(a + x + b)

        m = m.myokit_model()

        # Check that species are state variables
        var = m.get('c.s1_amount')
        self.assertTrue(var.is_state())

        var = m.get('c.s2_amount')
        self.assertTrue(var.is_state())

        # Check rates
        var = m.get('c.s1_amount')
        self.assertEqual(var.eval(), -5 * (2 / 1.2 + 1.5))

        var = m.get('c.s2_amount')
        self.assertEqual(var.eval(), 2 * (2 / 1.2 + 1.5))

    def test_reaction_conversion_factor(self):
        # Tests whether rate contributions are converted correctly.

        a = ('<model>'
             ' <listOfCompartments>'
             '  <compartment id="c" size="1.2" />'
             ' </listOfCompartments>'
             ' <listOfParameters>'
             '  <parameter id="x" value="1.2">'
             '  </parameter>'
             '  <parameter id="y" value="3">'
             '  </parameter>'
             ' </listOfParameters>'
             ' <listOfSpecies>'
             '  <species id="s1" compartment="c" initialAmount="2"'
             '    conversionFactor="x"/>'
             '  <species id="s2" compartment="c" initialConcentration="1.5"'
             '    conversionFactor="y"/>'
             ' </listOfSpecies>'
             ' <listOfReactions>'
             '  <reaction id="r">'
             '   <listOfReactants>'
             '    <speciesReference species="s1"/>'
             '   </listOfReactants>'
             '   <listOfProducts>'
             '    <speciesReference species="s2"/>'
             '   </listOfProducts>'
             '   <kineticLaw>'
             '    <math xmlns="http://www.w3.org/1998/Math/MathML">'
             '     <apply>'
             '      <plus/>'
             '      <ci>s1</ci>'
             '      <ci>s2</ci>'
             '     </apply>'
             '    </math>'
             '   </kineticLaw>'
             '  </reaction>'
             ' </listOfReactions>')
        b = ('</model>')

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that species are state variables
        var = m.get('c.s1_amount')
        self.assertTrue(var.is_state())

        var = m.get('c.s2_amount')
        self.assertTrue(var.is_state())

        # Check rates
        var = m.get('c.s1_amount')
        self.assertEqual(var.eval(), -1.2 * (2 / 1.2 + 1.5))

        var = m.get('c.s2_amount')
        self.assertEqual(var.eval(), 3 * (2 / 1.2 + 1.5))

    def test_time(self):
        # Tests whether time variable is created properly.

        a = '<model timeUnits="second"><listOfParameters>'
        b = '</listOfParameters></model>'

        m = self.parse(a + b)
        m = m.myokit_model()

        # Check that time variable exists
        self.assertTrue(m.has_variable('myokit.time'))

        # Check that unit is set
        var = m.get('myokit.time')
        self.assertEqual(var.unit(), myokit.units.second)

        # Check that initial value is set
        self.assertEqual(var.eval(), 0)

        # Chet that variable is time bound
        self.assertTrue(var.binding(), 'time')


class TestParameter(unittest.TestCase):
    """
    Unit tests for :class:`Parameter`.
    """

    @classmethod
    def setUpClass(cls):
        cls.model = sbml.Model(name='model')
        cls.sid = 'parameter'
        cls.p = cls.model.add_parameter(sid=cls.sid)

    def test_initial_value(self):

        # Check default initial value
        self.assertIsNone(self.p.initial_value())

        # Check bad value
        expr = 2
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.p.set_initial_value, expr)

        # Check good value
        expr = myokit.Number(2)
        self.p.set_initial_value(expr)

        self.assertEqual(self.p.initial_value(), expr)

    def test_is_rate(self):

        # Check default
        self.assertFalse(self.p.is_rate())

        # Check setting rate to true
        expr = myokit.Number(2)
        self.p.set_value(value=expr, is_rate=True)

        self.assertTrue(self.p.is_rate())

    def test_sid(self):
        self.assertEqual(self.p.sid(), self.sid)

    def test_units(self):

        # Check default units
        self.assertIsNone(self.p.units())

        # Check bad size units
        unit = 'mL'
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.p.set_units, unit)

        # Check valid size units
        unit = myokit.units.L * 1E-3
        self.p.set_units(unit)

        self.assertEqual(self.p.units(), unit)

    def test_value(self):

        # Check bad value
        expr = 2
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.p.set_value, expr)

        # Check good value
        expr = myokit.Number(2)
        self.p.set_value(expr)

        self.assertEqual(self.p.value(), expr)


class TestReaction(unittest.TestCase):
    """
    Unit tests for :class:`Reaction`.
    """

    @classmethod
    def setUpClass(cls):
        cls.model = sbml.Model(name='model')
        cls.sid = 'reaction'
        cls.r = cls.model.add_reaction(sid=cls.sid)

    def test_kinetic_law(self):

        # Check default
        self.assertIsNone(self.r.kinetic_law())

        # Check bad kinetic law
        expr = '2 * s'
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.r.set_kinetic_law, expr)

        # Check good kinetic law
        expr = myokit.Multiply(myokit.Number(2), myokit.Name('s'))
        self.r.set_kinetic_law(expr)

        self.assertEqual(self.r.kinetic_law(), expr)

    def test_modifiers(self):

        # Check bad species
        sid = 'modifier'
        species = 'species'
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.r.add_modifier, species, sid)

        # Check invalid sid
        sid = ';'
        compartment = sbml.Compartment(self.model, sid='compartment')
        species = sbml.Species(
            compartment=compartment,
            sid='species',
            is_amount=False,
            is_constant=False,
            is_boundary=False)
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid SId "', self.r.add_modifier, species, sid)

        # Check good sid
        sid = 'modifier'
        compartment = sbml.Compartment(self.model, sid='compartment')
        species = sbml.Species(
            compartment=compartment,
            sid='species',
            is_amount=False,
            is_constant=False,
            is_boundary=False)
        self.r.add_modifier(species, sid)

        self.assertEqual(len(self.r.modifiers()), 1)
        self.assertIsInstance(
            self.r.modifiers()[0], sbml.ModifierSpeciesReference)

        # Check duplicate sid
        sid = 'modifier'
        compartment = sbml.Compartment(self.model, sid='compartment')
        species = sbml.Species(
            compartment=compartment,
            sid='species',
            is_amount=False,
            is_constant=False,
            is_boundary=False)
        self.assertRaisesRegex(
            sbml.SBMLError, 'Duplicate SId "', self.r.add_modifier, species,
            sid)

    def test_products(self):

        # Check bad species
        sid = 'product'
        species = 'species'
        self.assertRaisesRegex(
            sbml.SBMLError, '<', self.r.add_product, species, sid)

        # Check invalid sid
        sid = ';'
        compartment = sbml.Compartment(self.model, sid='compartment')
        species = sbml.Species(
            compartment=compartment,
            sid='species',
            is_amount=False,
            is_constant=False,
            is_boundary=False)
        self.assertRaisesRegex(
            sbml.SBMLError, 'Invalid SId "', self.r.add_product, species, sid)

        # Check good sid
        sid = 'product'
        compartment = sbml.Compartment(self.model, sid='compartment')
        species = sbml.Species(
            compartment=compartment,
            sid='species',
            is_amount=False,
            is_constant=False,
            is_boundary=False)
        self.r.add_product(species, sid)

        self.assertEqual(len(self.r.products()), 1)
        self.assertIsInstance(
            self.r.products()[0], sbml.SpeciesReference)

        # Check duplicate sid
        sid = 'product'
        compartment = sbml.Compartment(self.model, sid='compartment')
        species = sbml.Species(
            compartment=compartment,
            sid='species',
            is_amount=False,
            is_constant=False,
            is_boundary=False)
        self.assertRaisesRegex(
            sbml.SBMLError, 'Duplicate SId "', self.r.add_product, species,
            sid)


if __name__ == '__main__':
    import warnings
    warnings.simplefilter('always')
    unittest.main()
