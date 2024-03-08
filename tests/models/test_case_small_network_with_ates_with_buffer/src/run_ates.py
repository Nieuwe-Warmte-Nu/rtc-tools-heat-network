import esdl

import numpy as np

from rtctools.data.storage import DataStore
from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.goal_programming_mixin import Goal, GoalProgrammingMixin
from rtctools.optimization.linearized_order_goal_programming_mixin import (
    LinearizedOrderGoalProgrammingMixin,
)
from rtctools.util import run_optimization_problem

from rtctools_heat_network.esdl.esdl_mixin import ESDLMixin
from rtctools_heat_network.esdl.esdl_parser import ESDLFileParser
from rtctools_heat_network.esdl.profile_parser import ProfileReaderFromFile
from rtctools_heat_network.techno_economic_mixin import TechnoEconomicMixin


class TargetDemandGoal(Goal):
    priority = 1

    order = 2

    def __init__(self, state, target):
        self.state = state

        self.target_min = target
        self.target_max = target
        self.function_range = (-1.0, 2.0 * max(target.values))
        self.function_nominal = np.median(target.values)

    def function(self, optimization_problem, ensemble_member):
        return optimization_problem.state(self.state)


class MinimizeSourcesHeatCostGoal(Goal):
    priority = 2

    order = 1

    def __init__(self, source):
        self.target_max = 0.0
        self.function_range = (0.0, 1.0e8)
        self.source = source
        self.function_nominal = 1.0e7

    def function(self, optimization_problem, ensemble_member):
        return (
            optimization_problem.extra_variable(
                optimization_problem._asset_installation_cost_map[self.source], ensemble_member
            )
            + optimization_problem.extra_variable(
                optimization_problem._asset_investment_cost_map[self.source], ensemble_member
            )
            + optimization_problem.extra_variable(
                optimization_problem._asset_variable_operational_cost_map[self.source],
                ensemble_member,
            )
        )


class _GoalsAndOptions:
    def path_goals(self):
        goals = super().path_goals().copy()

        for demand in self.energy_system_components["heat_demand"]:
            target = self.get_timeseries(f"{demand}.target_heat_demand")
            state = f"{demand}.Heat_demand"

            goals.append(TargetDemandGoal(state, target))

        return goals

    def goals(self):
        goals = super().goals().copy()
        for s in [
            *self.energy_system_components.get("heat_source", []),
            *self.energy_system_components.get("ates", []),
            *self.energy_system_components.get("buffer", []),
        ]:
            goals.append(MinimizeSourcesHeatCostGoal(s))

        return goals


class HeatProblem(
    _GoalsAndOptions,
    TechnoEconomicMixin,
    LinearizedOrderGoalProgrammingMixin,
    GoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def path_goals(self):
        goals = super().path_goals().copy()

        return goals

    def energy_system_options(self):
        options = super().energy_system_options()
        self.heat_network_settings["minimum_velocity"] = 0.0001
        options["neglect_pipe_heat_losses"] = True
        options["heat_loss_disconnected_pipe"] = True
        return options

    def constraints(self, ensemble_member):
        constraints = super().constraints(ensemble_member)

        # By default we do not add any constraints on the cyclic behaviour of the ates, as we
        # might want to do optimization over shorter periods of time where this would lead to
        # infeasibility. In this case we do want the cyclic behaviour, therefore we add it to the
        # problem.
        for a in self.energy_system_components.get("ates", []):
            stored_heat = self.state_vector(f"{a}.Stored_heat")
            constraints.append(((stored_heat[0] - stored_heat[-1]), 0.0, 0.0))

        return constraints

    def solver_options(self):
        options = super().solver_options()
        options["solver"] = "highs"
        # options["solver"] = "gurobi"

        return options

    @property
    def esdl_assets(self):
        assets = super().esdl_assets

        asset = next(a for a in assets.values() if a.name == "Pipe_8125")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
        asset = next(a for a in assets.values() if a.name == "Pipe_8125_ret")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
        asset = next(a for a in assets.values() if a.name == "Pipe_9768")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL
        asset = next(a for a in assets.values() if a.name == "Pipe_9768_ret")
        asset.attributes["state"] = esdl.AssetStateEnum.OPTIONAL

        return assets

    def pipe_classes(self, p):
        return self._override_pipe_classes.get(p, [])

    def read(self):
        """
        Reads the yearly profile with hourly time steps and adapt to a daily averaged profile
        """
        super().read()

        demands = self.energy_system_components.get("heat_demand", [])
        new_datastore = DataStore(self)
        new_datastore.reference_datetime = self.io.datetimes[0]

        for ensemble_member in range(self.ensemble_size):
            nr_of_days = 10
            new_date_times = list()
            for day in range(nr_of_days):
                new_date_times.append(self.io.datetimes[day * 24])
            new_date_times = np.asarray(new_date_times)

            for demand in demands:
                var_name = f"{demand}.target_heat_demand"
                data = self.get_timeseries(
                    variable=var_name, ensemble_member=ensemble_member
                ).values
                new_data = list()
                for day in range(nr_of_days):
                    data_for_day = data[day * 24 : (day + 1) * 24]
                    new_data.append(np.mean(data_for_day))
                new_datastore.set_timeseries(
                    variable=var_name,
                    datetimes=new_date_times,
                    values=np.asarray(new_data),
                    ensemble_member=ensemble_member,
                    check_duplicates=True,
                )

            self.io = new_datastore


if __name__ == "__main__":
    from pathlib import Path

    base_folder = Path(__file__).resolve().parent.parent
    solution = run_optimization_problem(
        HeatProblem,
        base_folder=base_folder,
        esdl_file_name="test_case_small_network_with_ates_with_buffer.esdl",
        esdl_parser=ESDLFileParser,
        profile_reader=ProfileReaderFromFile,
        input_timeseries_file="Warmte_test.csv",
    )
    results = solution.extract_results()
