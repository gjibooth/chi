#
# This file is part of the erlotinib repository
# (https://github.com/DavAug/erlotinib/) which is released under the
# BSD 3-clause license. See accompanying LICENSE.md for copyright notice and
# full license details.
#

import copy

import pandas as pd
import plotly.colors
import plotly.graph_objects as go

import erlotinib.plots as eplt


class ParameterEstimatePlot(eplt.MultiFigure):
    """
    A figure class that visualises parameter maximum a posteriori probability
    estimates across multiple optimisation runs.

    One figure is generated for each parameter, which contain a box plot of the
    parameter estimates across multiple optmisation runs. The estimates for
    each indiviudal are plotted next to each other.

    This figure can be used to assess the stability of the optimisation
    results, as well as the variation of parameter estimates across
    individuals.

    Extends :class:`MultiFigure`.
    """

    def __init__(self):
        super(ParameterEstimatePlot, self).__init__()

    def _add_box_plots(self, fig_id, parameter, data, colors):
        """
        Adds box plots of the parameter estimates for each individual across
        runs to the figure.

        One figure will only contain the estimates of one parameter.
        """
        # Get figure
        fig = self._figs[fig_id]

        # Set y label to parameter name
        fig.update_layout(
            yaxis_title=parameter)

        # Add trace for each individual
        ids = data[self._id_key].unique()
        for index, individual in enumerate(ids):
            # Get individual data
            mask = data[self._id_key] == individual
            estimates = data[self._est_key][mask]
            scores = data[self._score_key][mask].to_numpy()
            runs = data[self._run_key][mask].to_numpy()
            color = colors[index]

            self._add_trace(
                fig_id, individual, estimates, scores, runs, color)

    def _add_trace(
            self, fig_id, individual, estimates, scores, runs, color):
        """
        Adds a box plot of an individuals estimates across multiple
        optimisation runs to a figure.
        """
        # Get number of runs
        n_runs = len(runs)

        # Get figure
        fig = self._figs[fig_id]
        fig.add_trace(
            go.Box(
                y=estimates,
                name='ID: %d' % individual,
                hovertemplate=(
                    'Estimate: %{y:.2f}<br>'
                    '%{text}'),
                text=[
                    'Run: %d <br>Log-posterior score: %.2f' % (
                        runs[i], scores[i]) for i in range(n_runs)],
                boxpoints='all',
                jitter=0.2,
                pointpos=-1.5,
                visible=True,
                marker=dict(
                    symbol='circle',
                    opacity=0.7,
                    line=dict(color='black', width=1)),
                marker_color=color,
                line_color=color))

    def add_data(
            self, data, id_key='ID', param_key='Parameter', est_key='Estimate',
            score_key='Score', run_key='Run'):
        """
        Adds box plots of the estimates across runs to the figure. The
        estimates are grouped by the individual ID.

        Parameters
        ----------
        data
            A :class:`pandas.DataFrame` with the parameter estimates in form of
            an ID, parameter, estimate, score, and run column.
        id_key
            Key label of the :class:`DataFrame` which specifies the ID column.
            The ID refers to the identity of an individual. Defaults to
            ``'ID'``.
        param_key
            Key label of the :class:`DataFrame` which specifies the parameter
            name column. Defaults to ``'Parameter'``.
        est_key
            Key label of the :class:`DataFrame` which specifies the parameter
            estimate column. Defaults to ``'Estimate'``.
        score_key
            Key label of the :class:`DataFrame` which specifies the score
            estimate column. The score refers to the maximum a posteriori
            probability associated with the estimate. Defaults to ``'Score'``.
        run_key
            Key label of the :class:`DataFrame` which specifies the
            optimisation run column. Defaults to ``'Run'``.
        """
        # Check input format
        if not isinstance(data, pd.DataFrame):
            raise ValueError(
                'Data has to be pandas.DataFrame.')

        keys = [param_key, id_key, est_key, score_key, run_key]
        for key in [id_key, param_key, est_key, score_key, run_key]:
            if key not in data.keys():
                raise ValueError(
                    'Data does not have the key <' + str(key) + '>.')
        self._id_key, self._est_key, self._score_key, self._run_key = keys[1:]

        # Get a unique colour for each individual
        ids = data[id_key].unique()
        n_ids = len(ids)
        colors = plotly.colors.qualitative.Plotly[:n_ids]

        # Create one figure for each parameter
        parameters = data[param_key].unique()
        self._figs = [copy.copy(self._fig) for _ in parameters]

        # Add estimates to parameter figures
        for index, parameter in enumerate(parameters):
            # Get estimates for this parameter
            mask = data[param_key] == parameter
            estimates = data[mask][[id_key, est_key, score_key, run_key]]

            # Add box plots for all individuals
            self._add_box_plots(index, parameter, estimates, colors)

    def show(self):
        """
        Displays the figures.
        """
        for fig in self._figs:
            fig.show()
