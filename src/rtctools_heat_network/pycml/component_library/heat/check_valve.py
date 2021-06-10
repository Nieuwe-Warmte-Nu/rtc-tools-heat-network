from numpy import nan

from rtctools_heat_network.pycml import Variable

from .heat_two_port import HeatTwoPort


class CheckValve(HeatTwoPort):
    def __init__(self, name, **modifiers):
        super().__init__(name, **modifiers)

        self.component_type = "check_valve"

        self.Q_nominal = 1.0
        self.T_supply = nan
        self.T_return = nan
        self.dT = self.T_supply - self.T_return
        self.cp = 4200.0
        self.rho = 988.0
        self.Heat_nominal = self.cp * self.rho * self.dT * self.Q_nominal

        self.add_variable(Variable, "Q", nominal=self.Q_nominal, min=0.0)

        self.add_variable(Variable, "H_in")
        self.add_variable(Variable, "H_out")
        self.add_variable(Variable, "dH", min=0.0)

        self.add_equation(self.HeatIn.Q - self.Q)
        self.add_equation(self.HeatIn.Q - self.HeatOut.Q)

        self.add_equation(self.HeatIn.H - self.H_in)
        self.add_equation(self.HeatOut.H - self.H_out)
        self.add_equation(self.dH - (self.HeatOut.H - self.HeatIn.H))

        self.add_equation((self.HeatIn.Heat - self.HeatOut.Heat) / self.Heat_nominal)
