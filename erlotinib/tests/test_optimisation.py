#
# This file is part of the erlotinib repository
# (https://github.com/DavAug/erlotinib/) which is released under the
# BSD 3-clause license. See accompanying LICENSE.md for copyright notice and
# full license details.
#

import unittest

import pints

import erlotinib as erlo


class TestOptimisationController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Get test data and model
        data = erlo.DataLibrary().lung_cancer_control_group()
        mask = data['#ID'] == 40  # Arbitrary test id
        times = data[mask]['TIME in day'].to_numpy()
        observed_volumes = data[mask]['TUMOUR VOLUME in cm^3'].to_numpy()

        path = erlo.ModelLibrary().tumour_growth_inhibition_pd_model()
        model = erlo.PharmacodynamicModel(path)

        # Create inverse problem
        problem = erlo.InverseProblem(model, times, observed_volumes)
        log_likelihood = pints.GaussianLogLikelihood(problem)
        log_prior_tumour_volume = pints.UniformLogPrior(1E-3, 1E1)
        log_prior_drug_conc = pints.UniformLogPrior(-1E-3, 1E-3)
        log_prior_kappa = pints.UniformLogPrior(-1E-3, 1E-3)
        log_prior_lambda_0 = pints.UniformLogPrior(1E-3, 1E1)
        log_prior_lambda_1 = pints.UniformLogPrior(1E-3, 1E1)
        log_prior_sigma = pints.HalfCauchyLogPrior(location=0, scale=3)
        log_prior = pints.ComposedLogPrior(
            log_prior_tumour_volume,
            log_prior_drug_conc,
            log_prior_kappa,
            log_prior_lambda_0,
            log_prior_lambda_1,
            log_prior_sigma)
        log_posterior = pints.LogPosterior(log_likelihood, log_prior)

        # Set up optmisation controller
        cls.optimiser = erlo.OptimisationController(
            log_posterior=log_posterior,
            optimiser=pints.CMAES)

    def test_fix_parameters_bad_mask(self):
        # Mask length doesn't match number of parameters
        mask = [False, True, True]
        value = [1, 1]

        with self.assertRaisesRegex(ValueError, 'Length of mask'):
            self.optimiser.fix_parameters(mask, value)

        # Mask is not boolean
        mask = ['False', 'True', 'True', 'False', 'True', 'True']
        value = [1, 1, 1, 1]

        with self.assertRaisesRegex(ValueError, 'Mask has to be'):
            self.optimiser.fix_parameters(mask, value)

    def test_fix_parameters_bad_values(self):
        # Number of values doesn't match the number of parameters to fix
        mask = [False, True, True, False, True, True]
        value = [1, 1, 1, 1, 1, 1]

        with self.assertRaisesRegex(ValueError, 'Values has to have the same'):
            self.optimiser.fix_parameters(mask, value)

    def test_fix_parameters(self):
        # Fix all but parameter 1 and 4
        mask = [False, True, True, False, True, True]
        value = [1, 1, 1, 1]

        self.optimiser.fix_parameters(mask, value)

        parameters = self.optimiser._parameters
        self.assertEqual(len(parameters), 2)
        self.assertEqual(parameters[0], 'myokit.tumour_volume')
        self.assertEqual(parameters[1], 'myokit.lambda_0')

        # Fix a different set of parameters
        mask = [False, True, False, True, True, False]
        value = [1, 1, 1]

        self.optimiser.fix_parameters(mask, value)

        parameters = self.optimiser._parameters
        self.assertEqual(len(parameters), 3)
        self.assertEqual(parameters[0], 'myokit.tumour_volume')
        self.assertEqual(parameters[1], 'myokit.kappa')
        self.assertEqual(parameters[2], 'noise 1')

    def test_run(self):
        # Unfix all parameters (just to reset possibly fixed parameters)
        mask = [False, False, False, False, False, False]
        value = []
        self.optimiser.fix_parameters(mask, value)

        self.optimiser.set_n_runs(3)
        result = self.optimiser.run(n_max_iterations=1)

        keys = result.keys()
        self.assertEqual(len(keys), 4)
        self.assertEqual(keys[0], 'Parameter')
        self.assertEqual(keys[1], 'Estimate')
        self.assertEqual(keys[2], 'Score')
        self.assertEqual(keys[3], 'Run')

        parameters = result['Parameter'].unique()
        self.assertEqual(len(parameters), 6)
        self.assertEqual(parameters[0], 'myokit.tumour_volume')
        self.assertEqual(parameters[1], 'myokit.drug_concentration')
        self.assertEqual(parameters[2], 'myokit.kappa')
        self.assertEqual(parameters[3], 'myokit.lambda_0')
        self.assertEqual(parameters[4], 'myokit.lambda_1')
        self.assertEqual(parameters[5], 'noise 1')

        runs = result['Run'].unique()
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0], 1)
        self.assertEqual(runs[1], 2)
        self.assertEqual(runs[2], 3)

        # Check failure of optimisation doesn't interrupt all runs
        # (CMAES returns NAN for 1-dim problems)
        mask = [True, True, True, True, True, False]
        value = [1, 0, 0, 1, 1]
        self.optimiser.fix_parameters(mask, value)

        self.optimiser.set_n_runs(3)
        result = self.optimiser.run(n_max_iterations=10)

        keys = result.keys()
        self.assertEqual(len(keys), 4)
        self.assertEqual(keys[0], 'Parameter')
        self.assertEqual(keys[1], 'Estimate')
        self.assertEqual(keys[2], 'Score')
        self.assertEqual(keys[3], 'Run')

        parameters = result['Parameter'].unique()
        self.assertEqual(len(parameters), 1)
        self.assertEqual(parameters[0], 'noise 1')

        runs = result['Run'].unique()
        self.assertEqual(len(runs), 3)
        self.assertEqual(runs[0], 1)
        self.assertEqual(runs[1], 2)
        self.assertEqual(runs[2], 3)

    def test_set_n_runs(self):
        # Unfix all parameters (just to reset possibly fixed parameters)
        mask = [False, False, False, False, False, False]
        value = []
        self.optimiser.fix_parameters(mask, value)

        self.optimiser.set_n_runs(5)

        self.assertEqual(self.optimiser._n_runs, 5)
        self.assertEqual(self.optimiser._initial_params.shape, (5, 6))

        # Fix parameters
        mask = [True, True, True, False, False, False]
        value = [1, 1, 1]
        self.optimiser.fix_parameters(mask, value)

        self.optimiser.set_n_runs(20)

        self.assertEqual(self.optimiser._n_runs, 20)
        self.assertEqual(self.optimiser._initial_params.shape, (20, 3))

    def test_set_optmiser(self):
        self.optimiser.set_optimiser(pints.PSO)
        self.assertEqual(self.optimiser._optimiser, pints.PSO)

        self.optimiser.set_optimiser(pints.CMAES)
        self.assertEqual(self.optimiser._optimiser, pints.CMAES)

    def test_set_optimiser_bad_input(self):
        with self.assertRaisesRegex(ValueError, 'Optimiser has to be'):
            self.optimiser.set_optimiser(str)

    def test_set_transform_bad_transform(self):
        # Try to set transformation that is not a `pints.Transformation`
        transform = 'bad transform'

        with self.assertRaisesRegex(ValueError, 'Transform has to be an'):
            self.optimiser.set_transform(transform)

        # Try to set transformation with the wrong dimension
        transform = pints.LogTransformation(n_parameters=10)

        with self.assertRaisesRegex(ValueError, 'The dimensionality of the'):
            self.optimiser.set_transform(transform)

    def test_set_transform(self):
        # Unfix all parameters (just to reset possibly fixed parameters)
        mask = [False, False, False, False, False, False]
        value = []
        self.optimiser.fix_parameters(mask, value)

        # Apply transform
        transform = pints.LogTransformation(n_parameters=6)
        self.optimiser.set_transform(transform)

        self.assertEqual(self.optimiser._transform, transform)

        # Fix parameters and apply transform again
        mask = [False, True, True, True, True, True]
        value = [1, 1, 1, 1, 1]
        self.optimiser.fix_parameters(mask, value)

        self.assertIsNone(self.optimiser._transform)

        transform = pints.LogTransformation(n_parameters=1)
        self.optimiser.set_transform(transform)

        self.assertEqual(self.optimiser._transform, transform)


if __name__ == '__main__':
    unittest.main()
