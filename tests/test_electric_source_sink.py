from pathlib import Path
from unittest import TestCase

import numpy as np


from rtctools.util import run_optimization_problem

from rtctools_heat_network.esdl.esdl_parser import ESDLFileParser
from rtctools_heat_network.esdl.profile_parser import ProfileReaderFromFile

# TODO: still have to make test where elecitricity direction is switched:
# e.g. 2 nodes, with at each node a producer and consumer, first one node medium demand, second
# small demand and then increase the demand of the second node such that direction changes


class TestMILPElectricSourceSink(TestCase):
    def test_source_sink(self):
        """
        Tests for an electricity network that consist out of a source, a cable and a sink.

        Checks:
        - Check that the caps set in the esdl work as intended
        - Check that the consumed power is always>= 0.
        - Check for energy conservation with consumed power, lost power and produced power.
        - Check that the voltage drops over the line.
        - Check the Electricity_source/demand variable is correctly set.
        - Check that minimum voltage is exactly matched.
        - Check that power at the demands equals the current * voltage.

        """

        import models.unit_cases_electricity.source_sink_cable.src.example as example
        from models.unit_cases_electricity.source_sink_cable.src.example import ElectricityProblem

        base_folder = Path(example.__file__).resolve().parent.parent
        tol = 1e-10

        solution = run_optimization_problem(
            ElectricityProblem,
            base_folder=base_folder,
            esdl_file_name="case1_elec.esdl",
            esdl_parser=ESDLFileParser,
            profile_reader=ProfileReaderFromFile,
            input_timeseries_file="timeseries.csv",
        )
        results = solution.extract_results()
        parameters = solution.parameters(0)

        max_ = solution.bounds()["ElectricityDemand_2af6__max_size"][0]
        v_min = solution.parameters(0)["ElectricityCable_238f.min_voltage"]

        # Test if capping is ok
        power_consumed = results["ElectricityDemand_2af6.ElectricityIn.Power"]
        smallerthen = all(power_consumed <= np.ones(len(power_consumed)) * max_)
        self.assertTrue(smallerthen)
        biggerthen = all(power_consumed >= np.zeros(len(power_consumed)))
        self.assertTrue(biggerthen)

        # Test energy conservation
        power_consumed = results["ElectricityDemand_2af6.ElectricityIn.Power"]
        power_delivered = results["ElectricityProducer_b95d.ElectricityOut.Power"]
        power_loss = results["ElectricityCable_238f.Power_loss"]
        total_power_dissipation = power_consumed + power_loss
        self.assertIsNone(
            np.testing.assert_allclose(total_power_dissipation, power_delivered, rtol=1e-4),
            msg="No energy conservation. Total demand is not equal to total delivery.",
        )
        biggerthen = all(power_loss >= np.zeros(len(power_loss)))
        self.assertTrue(biggerthen)

        # Test that voltage goes down
        v_in = results["ElectricityCable_238f.ElectricityIn.V"]
        v_out = results["ElectricityCable_238f.ElectricityOut.V"]
        np.testing.assert_array_less(v_out, v_in)
        biggerthen = all(v_out >= (v_min - tol) * np.ones(len(v_out)))
        self.assertTrue(biggerthen)

        for source in solution.energy_system_components.get("electricity_source", []):
            np.testing.assert_allclose(
                results[f"{source}.Electricity_source"],
                results[f"{source}.ElectricityOut.Power"],
                atol=1.0e-6,
            )

        for demand in solution.energy_system_components.get("electricity_demand", []):
            np.testing.assert_allclose(
                results[f"{demand}.Electricity_demand"],
                results[f"{demand}.ElectricityIn.Power"],
                atol=1.0e-6,
            )
            np.testing.assert_allclose(
                results[f"{demand}.ElectricityIn.V"],
                parameters[f"{demand}.min_voltage"],
                atol=1.0e-3,
            )
            np.testing.assert_allclose(
                results[f"{demand}.ElectricityIn.V"] * results[f"{demand}.ElectricityIn.I"],
                results[f"{demand}.ElectricityIn.Power"],
                atol=1.0e-3,
            )

    def test_source_sink_max_curr(self):
        """
        Check bounds on the current, this is achieved by increasing the demand forcing the current
        to its max.

        Checks:
        - Check that the caps set in the esdl work as intended
        - Check that the consumed power is always>= 0.
        - Check for energy conservation with consumed power, lost power and produced power.
        - Check that the voltage drops over the line.
        - Check that the current limit is not exceeded
        - Check that minimum voltage is exactly matched
        - Check that power at the demands equals the current * voltage

        """

        import models.unit_cases_electricity.source_sink_cable.src.example as example
        from models.unit_cases_electricity.source_sink_cable.src.example import (
            ElectricityProblemMaxCurr,
        )

        base_folder = Path(example.__file__).resolve().parent.parent

        solution = run_optimization_problem(
            ElectricityProblemMaxCurr,
            base_folder=base_folder,
            esdl_file_name="case1_elec.esdl",
            esdl_parser=ESDLFileParser,
            profile_reader=ProfileReaderFromFile,
            input_timeseries_file="timeseries.csv",
        )
        results = solution.extract_results()
        parameters = solution.parameters(0)

        max_power_transport = (
            parameters["ElectricityCable_238f.min_voltage"]
            * parameters["ElectricityCable_238f.max_current"]
        )  # This max is based on max current and voltage requirement at consumer
        v_min = parameters["ElectricityCable_238f.min_voltage"]  # set as minimum voltage for cables

        tolerance = 1e-10  # due to computational comparison

        # Test if capping is ok (capping based on max power as result of v_min*Imax)
        power_consumed = results["ElectricityDemand_2af6.ElectricityIn.Power"]
        smallerthen = all(
            power_consumed - tolerance <= np.ones(len(power_consumed)) * max_power_transport
        )
        self.assertTrue(smallerthen)
        demand_target = solution.get_timeseries(
            "ElectricityDemand_2af6.target_electricity_demand"
        ).values
        np.testing.assert_allclose(
            power_consumed,
            np.minimum(demand_target, np.ones(len(power_consumed)) * max_power_transport),
        )
        biggerthen = all(power_consumed >= np.zeros(len(power_consumed)))
        self.assertTrue(biggerthen)

        # Test energy conservation
        power_consumed = results["ElectricityDemand_2af6.ElectricityIn.Power"]
        power_delivered = results["ElectricityProducer_b95d.ElectricityOut.Power"]
        power_loss = results["ElectricityCable_238f.Power_loss"]
        total_power_dissipation = power_consumed + power_loss
        self.assertIsNone(
            np.testing.assert_allclose(total_power_dissipation, power_delivered, rtol=1e-4),
            msg="No energy conservation. Total demand is not equal to total delivery.",
        )
        biggerthen = all(power_loss >= np.zeros(len(power_loss)))
        self.assertTrue(biggerthen)

        # Test that voltage goes down
        v_in = results["ElectricityCable_238f.ElectricityIn.V"]
        v_out = results["ElectricityCable_238f.ElectricityOut.V"]
        np.testing.assert_array_less(v_out, v_in)
        biggerthen = all(v_out >= v_min * np.ones(len(v_out)) - tolerance)
        self.assertTrue(biggerthen)

        # Test that max current is not exceeded and is constant along path (since no nodes included)
        current_demand = results["ElectricityDemand_2af6.ElectricityIn.I"]
        current_producer = results["ElectricityProducer_b95d.ElectricityOut.I"]
        current_cable = results["ElectricityCable_238f.ElectricityOut.I"]
        np.testing.assert_allclose(current_demand, current_cable)
        np.testing.assert_allclose(current_cable, current_producer)
        biggerthen = all(
            parameters["ElectricityCable_238f.max_current"] * np.ones(len(current_demand))
            >= current_demand - tolerance
        )
        self.assertTrue(biggerthen)

        for demand in solution.energy_system_components.get("electricity_demand", []):
            np.testing.assert_allclose(
                results[f"{demand}.ElectricityIn.V"],
                parameters[f"{demand}.min_voltage"],
                atol=1.0e-3,
            )
            np.testing.assert_allclose(
                results[f"{demand}.ElectricityIn.V"] * results[f"{demand}.ElectricityIn.I"],
                results[f"{demand}.ElectricityIn.Power"],
                atol=1.0e-3,
            )
