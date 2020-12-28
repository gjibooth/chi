#
# This file is part of the erlotinib repository
# (https://github.com/DavAug/erlotinib/) which is released under the
# BSD 3-clause license. See accompanying LICENSE.md for copyright notice and
# full license details.
#

import unittest

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import erlotinib as erlo


class TestPDPredictivePlot(unittest.TestCase):
    """
    Tests the erlotinib.plots.PDPredictivePlot class.
    """

    @classmethod
    def setUpClass(cls):
        # Create test dataset
        ids = [0, 0, 0, 1, 1, 1, 2, 2]
        times = [0, 1, 2, 2, np.nan, 4, 1, 3]
        volumes = [np.nan, 0.3, 0.2, 0.5, 0.1, 0.2, 0.234, 0]
        cls.data = pd.DataFrame({
            'ID': ids,
            'Time': times,
            'Biomarker': volumes})

        cls.prediction = pd.DataFrame({
            'Time': times,
            'Biomarker': 'TUMOUR VOLUME',
            'Sample': volumes})

        # Create test figure
        cls.fig = erlo.plots.PDPredictivePlot()

    def test_add_data_wrong_data_type(self):
        # Create data of wrong type
        data = np.ones(shape=(10, 4))

        self.assertRaisesRegex(
            TypeError, 'Data has to be pandas.DataFrame.',
            self.fig.add_data, data)

    def test_add_data_wrong_id_key(self):
        # Rename ID key
        data = self.data.rename(columns={'ID': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <ID>.',
            self.fig.add_data, data)

    def test_add_data_wrong_time_key(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Time>.',
            self.fig.add_data, data)

    def test_add_data_wrong_biom_key(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Biomarker>.',
            self.fig.add_data, data)

    def test_add_data_id_key_mapping(self):
        # Rename ID key
        data = self.data.rename(columns={'ID': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, id_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, id_key='SOME WRONG KEY')

    def test_add_data_time_key_mapping(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, time_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, time_key='SOME WRONG KEY')

    def test_add_data_biom_key_mapping(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, biom_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, biom_key='SOME WRONG KEY')

    def test_add_prediction_wrong_data_type(self):
        # Create data of wrong type
        data = np.ones(shape=(10, 4))

        self.assertRaisesRegex(
            TypeError, 'Data has to be pandas.DataFrame.',
            self.fig.add_prediction, data)

    def test_add_prediction_wrong_biomarker(self):
        # Specify biomarker that is not in the dataset
        biomarker = 'Does not exist'

        with self.assertRaisesRegex(ValueError, 'The biomarker could not be'):
            self.fig.add_prediction(self.prediction, biomarker)

    def test_add_prediction_bad_bulk_probs(self):
        # A maximum of 7 bulk probs are allowed
        bulk_probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

        with self.assertRaisesRegex(ValueError, 'At most 7 different bulk'):
            self.fig.add_prediction(self.prediction, bulk_probs=bulk_probs)

        # Negative probability
        bulk_probs = [-0.1]

        with self.assertRaisesRegex(ValueError, 'The provided bulk prob'):
            self.fig.add_prediction(self.prediction, bulk_probs=bulk_probs)

        # Probability greater 1
        bulk_probs = [1.1]

        with self.assertRaisesRegex(ValueError, 'The provided bulk prob'):
            self.fig.add_prediction(self.prediction, bulk_probs=bulk_probs)

    def test_add_prediction_wrong_time_key(self):
        # Rename time key
        data = self.prediction.rename(
            columns={'Time': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Time>.',
            self.fig.add_prediction, data)

    def test_add_prediction_wrong_biom_key(self):
        # Rename biomarker key
        data = self.prediction.rename(
            columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Biomarker>.',
            self.fig.add_prediction, data)

    def test_add_prediction_wrong_sample_key(self):
        # Rename sample key
        data = self.prediction.rename(
            columns={'Sample': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Sample>.',
            self.fig.add_prediction, data)

    def test_add_prediction_biom_mapping(self):
        # Rename rename biomarker
        data = self.prediction.copy()
        data['Biomarker'] = 'SOME NON-STANDARD BIOMARKER'

        # Test that it works with correct mapping
        self.fig.add_prediction(data=data, biom='SOME NON-STANDARD BIOMARKER')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'The biomarker could not be found'):
            self.fig.add_prediction(data=data, biom='SOME WRONG BIOMARKER')

    def test_add_prediction_no_provided_bulk_prob(self):
        # Test that it works with correct mapping
        self.fig.add_prediction(data=self.prediction, bulk_probs=None)

        trace = self.fig._fig.data[-1]
        self.assertIsInstance(trace, go.Scatter)

    def test_add_prediction_time_key_mapping(self):
        # Rename time key
        data = self.prediction.rename(
            columns={'Time': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_prediction(data=data, time_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_prediction(data=data, time_key='SOME WRONG KEY')

    def test_add_prediction_biom_key_mapping(self):
        # Rename biomarker key
        data = self.prediction.rename(
            columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_prediction(data=data, biom_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_prediction(data=data, biom_key='SOME WRONG KEY')

    def test_add_prediction_sample_key_mapping(self):
        # Rename sample key
        data = self.prediction.rename(
            columns={'Sample': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_prediction(data=data, sample_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_prediction(data=data, sample_key='SOME WRONG KEY')


class TestPDTimeSeriesPlot(unittest.TestCase):
    """
    Tests the erlotinib.plots.PDTimeSeriesPlot class.
    """

    @classmethod
    def setUpClass(cls):
        # Create test dataset
        ids = [0, 0, 0, 1, 1, 1, 2, 2]
        times = [0, 1, 2, 2, np.nan, 4, 1, 3]
        volumes = [np.nan, 0.3, 0.2, 0.5, 0.1, 0.2, 0.234, 0]
        cls.data = pd.DataFrame({
            'ID': ids,
            'Time': times,
            'Biomarker': volumes})

        # Create test figure
        cls.fig = erlo.plots.PDTimeSeriesPlot()

    def test_add_data_wrong_data_type(self):
        # Create data of wrong type
        data = np.ones(shape=(10, 4))

        self.assertRaisesRegex(
            TypeError, 'Data has to be pandas.DataFrame.',
            self.fig.add_data, data)

    def test_add_data_wrong_id_key(self):
        # Rename ID key
        data = self.data.rename(columns={'ID': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <ID>.',
            self.fig.add_data, data)

    def test_add_data_wrong_time_key(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Time>.',
            self.fig.add_data, data)

    def test_add_data_wrong_biom_key(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Biomarker>.',
            self.fig.add_data, data)

    def test_add_data_id_key_mapping(self):
        # Rename ID key
        data = self.data.rename(columns={'ID': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, id_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, id_key='SOME WRONG KEY')

    def test_add_data_time_key_mapping(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, time_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, time_key='SOME WRONG KEY')

    def test_add_data_biom_key_mapping(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, biom_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, biom_key='SOME WRONG KEY')

    def test_add_simulation_wrong_data_type(self):
        # Create data of wrong type
        data = np.ones(shape=(10, 4))

        self.assertRaisesRegex(
            TypeError, 'Data has to be pandas.DataFrame.',
            self.fig.add_simulation, data)

    def test_add_simulation_wrong_time_key(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Time>.',
            self.fig.add_simulation, data)

    def test_add_simulation_wrong_biom_key(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Biomarker>.',
            self.fig.add_simulation, data)

    def test_add_simulation_time_key_mapping(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_simulation(data=data, time_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_simulation(data=data, time_key='SOME WRONG KEY')

    def test_add_simulation_biom_key_mapping(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_simulation(data=data, biom_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_simulation(data=data, biom_key='SOME WRONG KEY')


class TestPKTimeSeriesPlot(unittest.TestCase):
    """
    Tests the erlotinib.plots.PKTimeSeriesPlot class.
    """

    @classmethod
    def setUpClass(cls):
        # Create test dataset
        ids = [0, 0, 0, 1, 1, 1, 2, 2]
        times = [0, 1, 2, 2, np.nan, 4, 1, 3]
        dose = [1, np.nan, np.nan, 1, np.nan, np.nan, 1, np.nan]
        conc = [np.nan, 0.3, 0.2, 0.5, 0.1, 0.2, 0.234, 0]
        cls.data = pd.DataFrame({
            'ID': ids,
            'Time': times,
            'Dose': dose,
            'Biomarker': conc})

        # Create test figure
        cls.fig = erlo.plots.PKTimeSeriesPlot()

    def test_add_data_wrong_data_type(self):
        # Create data of wrong type
        data = np.ones(shape=(10, 4))

        self.assertRaisesRegex(
            TypeError, 'Data has to be pandas.DataFrame.',
            self.fig.add_data, data)

    def test_add_data_wrong_id_key(self):
        # Rename ID key
        data = self.data.rename(columns={'ID': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <ID>.',
            self.fig.add_data, data)

    def test_add_data_wrong_time_key(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Time>.',
            self.fig.add_data, data)

    def test_add_data_wrong_biom_key(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Biomarker>.',
            self.fig.add_data, data)

    def test_add_data_wrong_dose_key(self):
        # Rename dose key
        data = self.data.rename(columns={'Dose': 'SOME NON-STANDARD KEY'})

        self.assertRaisesRegex(
            ValueError, 'Data does not have the key <Dose>.',
            self.fig.add_data, data)

    def test_add_data_id_key_mapping(self):
        # Rename ID key
        data = self.data.rename(columns={'ID': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, id_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, id_key='SOME WRONG KEY')

    def test_add_data_time_key_mapping(self):
        # Rename time key
        data = self.data.rename(columns={'Time': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, time_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, time_key='SOME WRONG KEY')

    def test_add_data_biom_key_mapping(self):
        # Rename biomarker key
        data = self.data.rename(columns={'Biomarker': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, biom_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, biom_key='SOME WRONG KEY')

    def test_add_data_dose_key_mapping(self):
        # Rename dose key
        data = self.data.rename(columns={'Dose': 'SOME NON-STANDARD KEY'})

        # Test that it works with correct mapping
        self.fig.add_data(data=data, dose_key='SOME NON-STANDARD KEY')

        # Test that it fails with wrong mapping
        with self.assertRaisesRegex(
                ValueError, 'Data does not have the key <SOME WRONG KEY>.'):
            self.fig.add_data(data=data, dose_key='SOME WRONG KEY')

    def test_add_simulation(self):
        with self.assertRaisesRegex(NotImplementedError, ''):
            self.fig.add_simulation(self.data)


if __name__ == '__main__':
    unittest.main()
