import numpy as np

from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.goal_programming_mixin import GoalProgrammingMixin
from rtctools.optimization.goal_programming_mixin_base import Goal
from rtctools.optimization.linearized_order_goal_programming_mixin import (
    LinearizedOrderGoalProgrammingMixin,
)
from rtctools.optimization.timeseries import Timeseries
from rtctools.util import run_optimization_problem

from rtctools_heat_network.esdl.esdl_mixin import ESDLMixin
from rtctools_heat_network.esdl.esdl_parser import ESDLFileParser
from rtctools_heat_network.esdl.profile_parser import ProfileReaderFromFile
from rtctools_heat_network.techno_economic_mixin import TechnoEconomicMixin


class TargetDemandGoal(Goal):
    priority = 1

    order = 2

    def __init__(self, state: str, target: Timeseries):
        self.state = state

        self.target_min = target
        self.target_max = target
        self.function_range = (0.0, 2.0 * max(target.values))
        self.function_nominal = np.median(target.values)

    def function(
        self, optimization_problem: CollocatedIntegratedOptimizationProblem, ensemble_member: int
    ):
        return optimization_problem.state(self.state)


class _GoalsAndOptions:
    def path_goals(self):
        """
        Add a goal to meet specified gas consumption.

        Returns
        -------
        list of goals.
        """
        goals = super().path_goals().copy()

        for demand in self.heat_network_components["gas_demand"]:
            target = self.get_timeseries(f"{demand}.target_gas_demand")
            state = f"{demand}.Gas_demand_mass_flow"

            goals.append(TargetDemandGoal(state, target))

        return goals


class GasProblem(
    _GoalsAndOptions,
    TechnoEconomicMixin,
    LinearizedOrderGoalProgrammingMixin,
    GoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    """
    This is a problem to check the behaviour of a gas network with a node.
    """

    def times(self, variable=None) -> np.ndarray:
        """
        Shorten the horizon here to have a faster test.

        Parameters
        ----------
        variable : string with name of the variable

        Returns
        -------
        The timeseries.
        """
        return super().times(variable)[:10]


if __name__ == "__main__":
    elect = run_optimization_problem(
        GasProblem,
        esdl_file_name="test.esdl",
        esdl_parser=ESDLFileParser,
        profile_reader=ProfileReaderFromFile,
        input_timeseries_file="timeseries.csv",
    )
    r = elect.extract_results()
    a = 1
