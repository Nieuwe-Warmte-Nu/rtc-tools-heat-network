from rtctools_heat_network.pycml import Connector, Variable

from .._internal.electricity_component import ElectricityComponent


class ElectricityPort(ElectricityComponent, Connector):
    """
    The electricity port is used to model the variables at a port where two assets are connected.
    For electricity networks we model the electrical power (P), the voltage (V) and the current (I).
    """

    def __init__(self, name, **modifiers):
        super().__init__(name, **modifiers)

        self.add_variable(Variable, "Power")
        self.add_variable(Variable, "V", min=0.0)
        self.add_variable(Variable, "I")


class ElectricityTwoPort(ElectricityComponent):
    """
    For electricity components that transport power we have a two port component.
    """

    def __init__(self, name, **modifiers):
        super().__init__(name, **modifiers)

        self.add_variable(ElectricityPort, "ElectricityIn")
        self.add_variable(ElectricityPort, "ElectricityOut")
