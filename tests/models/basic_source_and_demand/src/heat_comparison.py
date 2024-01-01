from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.csv_mixin import CSVMixin
from rtctools.optimization.goal_programming_mixin import Goal, GoalProgrammingMixin
from rtctools.optimization.modelica_mixin import ModelicaMixin
from rtctools.util import run_optimization_problem

from rtctools_heat_network.esdl.esdl_mixin import ESDLMixin
from rtctools_heat_network.heat_mixin import HeatMixin
from rtctools_heat_network.component_type_mixin import ModelicaComponentTypeMixin
from rtctools_heat_network.physics_mixin import PhysicsMixin
from rtctools_heat_network.pycml.pycml_mixin import PyCMLMixin

if __name__ == "__main__":
    from model_heat import Model
else:
    from .model_heat import Model


class TargetDemandGoal(Goal):
    priority = 1

    order = 1

    def __init__(self, optimization_problem):
        self.target_min = optimization_problem.get_timeseries("demand.target_heat_demand")
        self.target_max = optimization_problem.get_timeseries("demand.target_heat_demand")
        self.function_range = (0.0, 2e5)
        self.function_nominal = 1e5

    def function(self, optimization_problem, ensemble_member):
        return optimization_problem.state("demand.Heat_demand")


class _GoalsAndOptions:
    def path_goals(self):
        goals = super().path_goals().copy()
        goals.append(TargetDemandGoal(self))
        return goals


class HeatModelica(
    _GoalsAndOptions,
    HeatMixin,
    ModelicaComponentTypeMixin,
    GoalProgrammingMixin,
    CSVMixin,
    ModelicaMixin,
    CollocatedIntegratedOptimizationProblem,
):
    pass


class HeatPython(
    _GoalsAndOptions,
    PhysicsMixin,
    ModelicaComponentTypeMixin,
    GoalProgrammingMixin,
    CSVMixin,
    PyCMLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def __init__(self, *args, **kwargs):
        self.__model = Model()
        super().__init__(*args, **kwargs)

    def pycml_model(self):
        return self.__model


class HeatESDL(
    _GoalsAndOptions,
    HeatMixin,
    GoalProgrammingMixin,
    ESDLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def bounds(self):
        bounds = super().bounds()
        bounds["source.Heat_source"] = (75_000.0, 125_000.0)
        return bounds


if __name__ == "__main__":
    a = run_optimization_problem(HeatModelica)
    b = run_optimization_problem(HeatPython)
    c = run_optimization_problem(HeatESDL)
