from numpy import nan

from rtctools_heat_network.pycml import Variable
from rtctools_heat_network.pycml.component_library.milp._internal import BaseAsset
from rtctools_heat_network.pycml.component_library.milp.heat.heat_four_port import HeatFourPort


class HeatPump(HeatFourPort, BaseAsset):
    """
    The heatpump component is used to model a water-water heatpump.
    A constant COP is used to model the electricity use of the heatpump. A power cap is set
    on the primary side to model physical constraints on the amount of milp transfer.

    The milp to discharge constraints are set in the HeatMixin. The primary side is modelled as a
    demand, meaning it consumes energy from the primary network and gives it to the secondary side,
    where the secondary side acts like a source to the secondary network. This also means that milp
    can only flow from primary to secondary.
    """

    def __init__(self, name, **modifiers):
        super().__init__(
            name,
            **self.merge_modifiers(
                dict(),
                modifiers,
            ),
        )

        self.component_type = "heat_pump"
        self.efficiency = nan
        self.COP = nan  # TODO: maybe set this to a standard value if not set in esdl.
        self.minimum_pressure_drop = 1.0e5  # 1 bar of pressure drop
        self.nominal = (
            self.Secondary.Q_nominal * self.Secondary.rho * self.Secondary.cp * self.Secondary.dT
        )
        self.pump_efficiency = 0.5
        self.elec_power_nominal = self.nominal / self.COP

        # Assumption: milp in/out and added is nonnegative

        self.add_variable(Variable, "Primary_heat", min=0.0)
        self.add_variable(Variable, "Secondary_heat", min=0.0)
        self.add_variable(Variable, "Heat_flow", nominal=self.nominal)
        self.add_variable(Variable, "Power_elec", min=0.0)
        self.add_variable(Variable, "dH_prim", max=0.0)
        self.add_variable(Variable, "dH_sec", min=0.0)

        # Hydraulically decoupled so Heads remain the same
        # #TODO: can't these two equations be moved to the non_storagecomponent?
        self.add_equation(self.dH_prim - (self.Primary.HeatOut.H - self.Primary.HeatIn.H))
        self.add_equation(
            (
                self.minimum_pressure_drop * self.Primary.Q
                - (self.Primary.HeatIn.Hydraulic_power - self.Primary.HeatOut.Hydraulic_power)
            )
            / (self.Primary.Q_nominal * self.Primary.nominal_pressure)
        )
        self.add_equation(self.dH_sec - (self.Secondary.HeatOut.H - self.Secondary.HeatIn.H))
        self.add_equation(
            (
                self.Pump_power
                - (self.Secondary.HeatOut.Hydraulic_power - self.Secondary.HeatIn.Hydraulic_power)
            )
            / (self.Secondary.Q_nominal * self.Secondary.nominal_pressure)
        )

        self.add_equation(
            ((self.Primary_heat + self.Power_elec - self.Secondary_heat) / self.nominal)
        )

        self.add_equation(
            (
                (self.Primary_heat - (self.Primary.HeatIn.Heat - self.Primary.HeatOut.Heat))
                / self.nominal
            )
        )
        self.add_equation(
            (
                (self.Secondary_heat - (self.Secondary.HeatOut.Heat - self.Secondary.HeatIn.Heat))
                / self.nominal
            )
        )
        self.add_equation((self.Heat_flow - self.Secondary_heat) / self.nominal)
