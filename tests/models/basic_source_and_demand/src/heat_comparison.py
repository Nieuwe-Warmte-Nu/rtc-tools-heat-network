from rtctools.optimization.collocated_integrated_optimization_problem import (
    CollocatedIntegratedOptimizationProblem,
)
from rtctools.optimization.csv_mixin import CSVMixin
from rtctools.optimization.goal_programming_mixin import Goal, GoalProgrammingMixin
from rtctools.optimization.modelica_mixin import ModelicaMixin
from rtctools.util import run_optimization_problem

from rtctools_heat_network.heat_mixin import HeatMixin
from rtctools_heat_network.modelica_component_type_mixin import ModelicaComponentTypeMixin
from rtctools_heat_network.pycml.pycml_mixin import PyCMLMixin

if __name__ == "__main__":
    from model import Model
else:
    from .model import Model


class TargetDemandGoal(Goal):

    priority = 1

    order = 1

    def __init__(self, optimization_problem):
        self.target_min = optimization_problem.get_timeseries("Heat_demand")
        self.target_max = optimization_problem.get_timeseries("Heat_demand")
        self.function_range = (0.0, 2e5)
        self.function_nominal = 1e5

    def function(self, optimization_problem, ensemble_member):
        return optimization_problem.state("demand.Heat_demand")


class HeatModelica(
    HeatMixin,
    ModelicaComponentTypeMixin,
    GoalProgrammingMixin,
    CSVMixin,
    ModelicaMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def path_goals(self):
        return [TargetDemandGoal(self)]

    def post(self):
        super().post()


class HeatPython(
    HeatMixin,
    ModelicaComponentTypeMixin,
    GoalProgrammingMixin,
    CSVMixin,
    PyCMLMixin,
    CollocatedIntegratedOptimizationProblem,
):
    def __init__(self, *args, **kwargs):
        self.__model = Model()
        super().__init__(*args, **kwargs)

    def path_goals(self):
        return [TargetDemandGoal(self)]

    def post(self):
        super().post()

    def pycml_model(self):
        return self.__model


if __name__ == "__main__":
    a = run_optimization_problem(HeatModelica)
    b = run_optimization_problem(HeatPython)
