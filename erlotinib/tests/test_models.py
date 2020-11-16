#
# This file is part of the erlotinib repository
# (https://github.com/DavAug/erlotinib/) which is released under the
# BSD 3-clause license. See accompanying LICENSE.md for copyright notice and
# full license details.
#

import unittest

import numpy as np

import erlotinib as erlo


class TestPharmacodynamicModel(unittest.TestCase):
    """
    Tests `pkpd.PharmacodynamicModel`.
    """
    @classmethod
    def setUpClass(cls):
        path = erlo.ModelLibrary().tumour_growth_inhibition_model_koch()
        cls.model = erlo.PharmacodynamicModel(path)

    def test_n_outputs(self):
        self.assertEqual(self.model.n_outputs(), 1)

    def test_n_parameters(self):
        self.assertEqual(self.model.n_parameters(), 5)

    def test_outputs(self):
        outputs = self.model.outputs()

        self.assertEqual(outputs, ['myokit.tumour_volume'])

    def test_parameters(self):
        parameters = self.model.parameters()

        self.assertEqual(parameters[0], 'myokit.tumour_volume')
        self.assertEqual(parameters[1], 'myokit.drug_concentration')
        self.assertEqual(parameters[2], 'myokit.kappa')
        self.assertEqual(parameters[3], 'myokit.lambda_0')
        self.assertEqual(parameters[4], 'myokit.lambda_1')

    def test_pk_input(self):
        pk_input = self.model.pk_input()

        self.assertEqual(pk_input, 'myokit.drug_concentration')

    def test_set_outputs(self):

        # Set bad output
        self.assertRaisesRegex(
            KeyError, 'The variable <', self.model.set_outputs, ['some.thing'])

        # Set twice the same output
        outputs = ['myokit.tumour_volume', 'myokit.tumour_volume']
        self.model.set_outputs(outputs)
        self.assertEqual(self.model.outputs(), outputs)
        self.assertEqual(self.model.n_outputs(), 2)
        output = self.model.simulate([0.1, 2, 1, 1, 1], [0, 1])
        self.assertEqual(output.shape, (2, 2))

        # Set to default again
        outputs = ['myokit.tumour_volume']
        self.model.set_outputs(outputs)
        self.assertEqual(self.model.outputs(), outputs)
        self.assertEqual(self.model.n_outputs(), 1)
        output = self.model.simulate([0.1, 2, 1, 1, 1], [0, 1])
        self.assertEqual(output.shape, (1, 2))

    def test_set_parameter_names(self):
        # Set some parameter names
        names = {
            'myokit.tumour_volume': 'TV',
            'myokit.lambda_0': 'Expon. growth rate'}
        self.model.set_parameter_names(names)
        parameters = self.model.parameters()

        self.assertEqual(parameters[0], 'TV')
        self.assertEqual(parameters[1], 'myokit.drug_concentration')
        self.assertEqual(parameters[2], 'myokit.kappa')
        self.assertEqual(parameters[3], 'Expon. growth rate')
        self.assertEqual(parameters[4], 'myokit.lambda_1')

        # Reverse parameter names
        names = {
            'TV': 'myokit.tumour_volume',
            'Expon. growth rate': 'myokit.lambda_0'}
        self.model.set_parameter_names(names)
        parameters = self.model.parameters()

        self.assertEqual(parameters[0], 'myokit.tumour_volume')
        self.assertEqual(parameters[1], 'myokit.drug_concentration')
        self.assertEqual(parameters[2], 'myokit.kappa')
        self.assertEqual(parameters[3], 'myokit.lambda_0')
        self.assertEqual(parameters[4], 'myokit.lambda_1')

    def test_set_parameter_names_bad_input(self):
        # List input is not ok!
        names = ['TV', 'some name']

        with self.assertRaisesRegex(TypeError, 'Names has to be a dictionary'):
            self.model.set_parameter_names(names)

    def test_set_pk_input(self):
        # Set pk input variable
        pk_input = 'myokit.kappa'
        self.model.set_pk_input(pk_input)

        self.assertEqual(self.model.pk_input(), pk_input)

        # Reset pk input
        pk_input = 'myokit.drug_concentration'
        self.model.set_pk_input(pk_input)

        self.assertEqual(self.model.pk_input(), pk_input)

    def test_set_pk_input_bad_input(self):
        # Set pk input variable
        pk_input = 'SOME NON-EXISTENT VARIABLE'

        with self.assertRaisesRegex(ValueError, 'The name does not'):
            self.model.set_pk_input(pk_input)

    def test_simulate(self):

        times = [0, 1, 2, 3]

        # Test model with bare parameters
        parameters = [0.1, 1, 1, 1, 1]
        output = self.model.simulate(parameters, times)
        self.assertIsInstance(output, np.ndarray)
        self.assertEqual(output.shape, (1, 4))


if __name__ == '__main__':
    unittest.main()