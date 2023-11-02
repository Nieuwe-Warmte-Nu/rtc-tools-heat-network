import numpy as np

import esdl

from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.goal_programming_mixin import Goal, GoalProgrammingMixin
from rtctools.optimization.linearized_order_goal_programming_mixin import (
    LinearizedOrderGoalProgrammingMixin,
)
from rtctools.util import run_optimization_problem

from rtctools_heat_network.esdl.esdl_mixin import ESDLMixin
from rtctools_heat_network.heat_mixin import HeatMixin


# TODO: check if this run script is still valid as test case for electric heatpump and update with
# functions
class TargetDemandGoal(Goal):
    priority = 1

    order = 2

    def __init__(self, state, target):
        self.state = state

        self.target_min = target
        self.target_max = target
        self.function_range = (0.0, 2.0 * max(target.values))
        self.function_nominal = np.median(target.values)

    def function(self, optimization_problem, ensemble_member):
        return optimization_problem.state(self.state)


class _GoalsAndOptions:
    def path_goals(self):
        goals = super().path_goals().copy()

        for demand in self.heat_network_components["demand"]:
            target = self.get_timeseries(f"{demand}.target_heat_demand")
            state = f"{demand}.Heat_demand"

            goals.append(TargetDemandGoal(state, target))

        return goals

    def heat_network_options(self):
        options = super().heat_network_options()
        # options["heat_loss_disconnected_pipe"] = False
        options["minimum_velocity"] = 0.0001

        return options

    def solver_options(self):
        options = super().solver_options()
        # options["solver"] = "gurobi"
        return options


# this goal will result in the sources at the primary side of the heatpump to be utilised as much
# as possible as this requires less heat_source because it is upgraded with electricity, heat_source
# is a variable that heatpumps don't have
class MinimizeSourcesHeatGoal(Goal):
    priority = 2

    order = 1

    def __init__(self, sources):
        self.target_max = 0.0
        self.function_range = (0.0, 10e6)
        self.sources = sources
        self.function_nominal = 1e6

    def function(self, optimization_problem, ensemble_member):
        sum_heat_prod = 0
        for source in self.sources:
            sum_heat_prod += optimization_problem.state(f"{source}.Heat_source")
        return sum_heat_prod


# this goal will minimise the electricty use and thus minimise the use of the heatpump, should use
# the heatsource at the secondary side of the heatpump as much as possible to provide heat for
# that heating demand.
class MinimizeElectricityGoal(Goal):
    priority = 2

    order = 1

    def __init__(self, source):
        self.target_max = 0.0
        self.function_range = (0.0, 10e6)
        self.source = source
        self.function_nominal = 1e6

    def function(self, optimization_problem, ensemble_member):
        return optimization_problem.state(f"{self.source}.Power_elec")


class HeatProblem(
    _GoalsAndOptions,
    HeatMixin,
    LinearizedOrderGoalProgrammingMixin,
    GoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def path_goals(self):
        goals = super().path_goals().copy()

        s = self.heat_network_components["source"]
        goals.append(MinimizeSourcesHeatGoal(s))

        return goals

    def heat_network_options(self):
        options = super().heat_network_options()
        options["minimum_velocity"] = 0.0001
        options["heat_loss_disconnected_pipe"] = True

        return options

    @property
    def esdl_assets(self):
        assets = super().esdl_assets

        asset = next(a for a in assets.values() if a.name == "Pipe3")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
        asset = next(a for a in assets.values() if a.name == "Pipe3_ret")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL

        return assets

    def parameters(self, ensemble_member):
        parameters = super().parameters(ensemble_member)
        parameters["GenericConversion_3d3f.min_voltage"] = 230.0

        return parameters

    def pipe_classes(self, p):
        return self._override_pipe_classes.get(p, [])


class HeatProblem2(
    _GoalsAndOptions,
    HeatMixin,
    LinearizedOrderGoalProgrammingMixin,
    GoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def read(self):
        super().read()

        for d in self.heat_network_components["demand"]:
            new_timeseries = self.get_timeseries(f"{d}.target_heat_demand").values * 0.01
            self.set_timeseries(f"{d}.target_heat_demand", new_timeseries)

    def path_goals(self):
        goals = super().path_goals().copy()

        s = self.heat_network_components["source"]
        goals.append(MinimizeSourcesHeatGoal(s))

        return goals

    def heat_network_options(self):
        options = super().heat_network_options()
        options["minimum_velocity"] = 0.0001
        options["heat_loss_disconnected_pipe"] = True

        return options

    @property
    def esdl_assets(self):
        assets = super().esdl_assets

        asset = next(a for a in assets.values() if a.name == "Pipe3")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
        asset = next(a for a in assets.values() if a.name == "Pipe3_ret")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL

        return assets

    def pipe_classes(self, p):
        return self._override_pipe_classes.get(p, [])


class ElectricityProblem(
    _GoalsAndOptions,
    HeatMixin,
    LinearizedOrderGoalProgrammingMixin,
    GoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def read(self):
        super().read()

        for d in self.heat_network_components["demand"]:
            new_timeseries = self.get_timeseries(f"{d}.target_heat_demand").values * 0.01
            self.set_timeseries(f"{d}.target_heat_demand", new_timeseries)

    def path_goals(self):
        goals = super().path_goals().copy()

        for s in self.heat_network_components["heat_pump_elec"]:
            goals.append(MinimizeElectricityGoal(s))

        return goals

    # @property
    # def esdl_assets(self):
    #     assets = super().esdl_assets
    #
    #     # asset = next(a for a in assets.values() if a.name == "GenericConversion_3d3f")
    #     # asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
    #     asset = next(a for a in assets.values() if a.name == "Pipe_408e")
    #     asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
    #     asset = next(a for a in assets.values() if a.name == "Pipe_408e_ret")
    #     asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
    #     asset = next(a for a in assets.values() if a.name == "Pipe_ce68")
    #     asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
    #     asset = next(a for a in assets.values() if a.name == "Pipe_ce68_ret")
    #     asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
    #
    #     return assets
    #
    # def pipe_classes(self, p):
    #     return self._override_pipe_classes.get(p, [])

    def heat_network_options(self):
        options = super().heat_network_options()
        options["minimum_velocity"] = 0.0001
        options["heat_loss_disconnected_pipe"] = False

        return options


if __name__ == "__main__":
    sol = run_optimization_problem(HeatProblem)
    results = sol.extract_results()
    print(results["GenericConversion_3d3f.Power_elec"])
    print(results["ResidualHeatSource_aec9.Heat_source"])
    # print(results["Pipe3__hn_diameter"])
    # print(sol.bounds()["Pipe3__hn_diameter"])
    # run_optimization_problem(ElectricityProblem)
