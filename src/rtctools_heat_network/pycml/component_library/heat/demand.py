from rtctools_heat_network.pycml import Variable

from ._non_storage_component import _NonStorageComponent


class Demand(_NonStorageComponent):
    """
    The demand component is there to extract thermal power (Heat) out of the network. Typically,
    this component is used to model aggregated demands.

    The heat to discharge constraints are set in the HeatMixin. We enforce that the outgoing
    temperature of the demand matches the absolute thermal power, Q * cp * rho * T_ret == Heat,
    similar as with the sources. This allows us to guarantee that the flow can always carry the
    heat and that thermal losses are always estimated conservatively. It also implicitly assumes
    that the temperature drops in the network are small and thus satisfy minimum temperature
    requirements.
    """

    def __init__(self, name, **modifiers):
        super().__init__(
            name,
            **self.merge_modifiers(
                dict(
                    HeatIn=dict(Heat=dict(min=0.0)),
                    HeatOut=dict(Heat=dict(min=0.0)),
                ),
                modifiers,
            ),
        )

        self.component_type = "demand"

        # Assumption: heat in/out and extracted is nonnegative
        # Heat in the return (i.e. cold) line is zero
        self.add_variable(Variable, "Heat_demand", min=0.0, nominal=self.Heat_nominal)

        self.add_equation(
            (self.HeatOut.Heat - (self.HeatIn.Heat - self.Heat_demand)) / self.Heat_nominal
        )

        self.add_equation((self.Heat_flow - self.Heat_demand) / self.Heat_nominal)
