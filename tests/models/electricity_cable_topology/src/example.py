import casadi as ca

import numpy as np

from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.goal_programming_mixin_base import Goal
from rtctools.optimization.linearized_order_goal_programming_mixin import (
    LinearizedOrderGoalProgrammingMixin,
)
from rtctools.optimization.single_pass_goal_programming_mixin import SinglePassGoalProgrammingMixin
from rtctools.optimization.timeseries import Timeseries
from rtctools.util import run_optimization_problem

from rtctools_heat_network.esdl.esdl_mixin import ESDLMixin
from rtctools_heat_network.esdl.esdl_parser import ESDLFileParser
from rtctools_heat_network.esdl.profile_parser import ProfileReaderFromFile
from rtctools_heat_network.pipe_class import CableClass
from rtctools_heat_network.techno_economic_mixin import TechnoEconomicMixin


class TargetDemandGoal(Goal):
    """
    Goal class for matching a timeseries of values, we use it to match the time series of a demand
    profile. We use order 2 to match the profile at every time-step. We set the target in the
    constructor and function() method will return the state which should match the target.
    """

    priority = 1

    order = 2

    def __init__(self, state: str, target: Timeseries):
        """
        The constructor for the class where we pass the name of the state that should be matched to
        the target.

        Parameters
        ----------
        state : string for the name of the state.
        target : Timeseries to match with the state.
        """
        self.state = state

        self.target_min = target
        self.target_max = target
        self.function_range = (0.0, 2.0 * max(target.values))
        self.function_nominal = np.median(target.values)

    def function(
        self, optimization_problem: CollocatedIntegratedOptimizationProblem, ensemble_member: int
    ) -> ca.MX:
        """
        This function returns the state to which will be tried to match to the target.

        Parameters
        ----------
        optimization_problem : The optimization class containing the variables'
        ensemble_member : the ensemble member

        Returns
        -------
        The optimization problem state, the Heat_demand, which should be matched to the time-series
        """
        return optimization_problem.state(self.state)


class MinimizeElectricityCableInvestments(Goal):
    """
    A minimization goal for source heat production. We use order 1 here as we want to minimize heat
    over the full horizon and not per time-step.
    """

    priority = 3

    order = 1

    def __init__(self, cable: str):
        """
        The constructor of the goal.

        Parameters
        ----------
        source : string of the source name that is going to be minimized
        """
        self.target_max = 0.0
        self.function_range = (0.0, 1.0e3)
        self.cable = cable
        self.function_nominal = 1.0

    def function(
        self, optimization_problem: CollocatedIntegratedOptimizationProblem, ensemble_member: int
    ) -> ca.MX:
        """
        This function returns the state variable to which should to be matched to the target
        specified in the __init__.

        Parameters
        ----------
        optimization_problem : The optimization class containing the variables'.
        ensemble_member : the ensemble member.

        Returns
        -------
        The Heat_source state of the optimization problem.
        """
        return (
            optimization_problem.extra_variable(f"{self.cable}__investment_cost", ensemble_member)
            / 1e3
        )


class _GoalsAndOptions:
    """
    A goals class that we often use if we specify multiple problem classes.
    """

    def path_goals(self):
        """
        In this method we add the goals for matching the demand.

        Returns
        -------
        The appended goals list of goals
        """
        goals = super().path_goals().copy()

        for demand in self.heat_network_components.get("electricity_demand", []):
            target = self.get_timeseries(f"{demand}.target_electricity_demand")
            state = f"{demand}.Electricity_demand"

            goals.append(TargetDemandGoal(state, target))

        return goals


class HeatProblem(
    _GoalsAndOptions,
    TechnoEconomicMixin,
    LinearizedOrderGoalProgrammingMixin,
    SinglePassGoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    """
    This problem class is for the absolute heat tests. Meaning that this problem class
    is applied to an esdl where there is no dedicated supply or return line. For this test case
    we just match heating demand (_GoalsAndOptions) and minimize the energy production to have a
    representative result.
    """

    def goals(self):
        """
        This function adds the minimization goal for minimizing the heat production.

        Returns
        -------
        The appended list of goals
        """
        goals = super().goals().copy()

        for c in self.heat_network_components.get("electricity_cable", []):
            goals.append(MinimizeElectricityCableInvestments(c))

        return goals

    def solver_options(self):
        """
        This function does not add anything at the moment but during debugging we use this.

        Returns
        -------
        solver options dict
        """
        options = super().solver_options()
        options["solver"] = "highs"
        return options

    def heat_network_options(self):
        """
        This function does not add anything at the moment but during debugging we use this.

        Returns
        -------
        Options dict for the physics modelling
        """
        options = super().heat_network_options()
        options["minimum_velocity"] = 0.0
        options["heat_loss_disconnected_pipe"] = False
        options["include_electric_cable_power_loss"] = False
        return options

    def electricity_cable_classes(self, p):
        return [
            CableClass("None", 0.0, 0.0, 0.0),
            CableClass("DN40", 2.5, 1.5, 1.0),
            CableClass("DN50", 5.0, 1.7, 2.0),
            CableClass("DN65", 7.5, 1.9, 3.0),
            CableClass("DN80", 10.0, 2.2, 4.0),
            CableClass("DN100", 12.5, 2.4, 5.0),
            CableClass("DN125", 15.0, 2.6, 6.0),
            CableClass("DN150", 17.5, 2.8, 7.0),
            CableClass("DN200", 20.0, 3.0, 8.0),
            CableClass("DN250", 22.5, 3.0, 9.0),
            CableClass("DN300", 25.0, 3.0, 10.0),
            CableClass("DN400", 30.0, 3.0, 11.0),
            CableClass("DN450", 35.0, 3.0, 12.0),
        ]

    def bounds(self):
        bounds = super().bounds()
        for c in self.heat_network_components.get("electricity_cable", []):
            bounds.update({f"{c}__investment_cost": (0.0, np.inf)})

        return bounds


if __name__ == "__main__":
    elect = run_optimization_problem(
        HeatProblem,
        esdl_file_name="enettopology.esdl",
        esdl_parser=ESDLFileParser,
        profile_reader=ProfileReaderFromFile,
        input_timeseries_file="timeseries.csv",
    )
    results = elect.extract_results()
    a = 1
