import sys
from pathlib import Path
from unittest import TestCase

from mesido.esdl.esdl_parser import ESDLFileParser
from mesido.workflows import run_end_scenario_sizing

import numpy as np


class TestUpdatedESDL(TestCase):
    def test_updated_esdl(self):
        """
        Check that the updated ESDL resulting from optmizing a network, is correct by using the
        PoCTutorial and the Grow_workflow. This is done for the actual esdl file and the esdl
        string created by MESIDO. Both these resulting optimized energy systems should be identical
        and it is only the MESIDO esdl saving method that differs.

        Additional checks:
         - Check that the unique profile identification in profile_parser assigns the correct
         profile

        """

        root_folder = str(Path(__file__).resolve().parent.parent)
        sys.path.insert(1, root_folder)

        import examples.PoCTutorial.src.run_grow_tutorial
        from examples.PoCTutorial.src.run_grow_tutorial import EndScenarioSizingStagedHighs

        base_folder = (
            Path(examples.PoCTutorial.src.run_grow_tutorial.__file__).resolve().parent.parent
        )

        problem = run_end_scenario_sizing(
            EndScenarioSizingStagedHighs,
            base_folder=base_folder,
            esdl_file_name="PoC Tutorial.esdl",
            esdl_parser=ESDLFileParser,
        )

        # Save optimized esdl string
        optimized_esdl_string = problem.optimized_esdl_string
        file = open(
            Path.joinpath(base_folder, "model", "PoC Tutorial_GrowOptimized_esdl_string.esdl"), "w"
        )
        file.write(optimized_esdl_string)
        file.close()

        # Check the unique profile identification in profile_parser
        # Test that the correct demand profile is assigned to a demand as expected. Note that the
        # demand profiles are the adapted profiles (peak-hourly, rest-5daily). Therefore the
        # expected max and average hard-coded values are compared to the problem values.
        np.testing.assert_allclose(
            1201200.0,  # demand4_MW, multiplier 0.75
            max(problem.get_timeseries("HeatingDemand_b0ff.target_heat_demand").values),
        )
        np.testing.assert_allclose(
            720720.0,  # demand5_MW, multiplier 0.3
            max(problem.get_timeseries("HeatingDemand_8fbe.target_heat_demand").values),
        )
        np.testing.assert_allclose(
            916316.712,  # demand1_MW, multiplier 0.5
            max(problem.get_timeseries("HeatingDemand_08fd.target_heat_demand").values),
        )
        np.testing.assert_allclose(
            443413.79,  # demand4_MW, multiplier 0.75
            np.average(problem.get_timeseries("HeatingDemand_b0ff.target_heat_demand").values),
        )
        np.testing.assert_allclose(
            266048.27,  # demand5_MW, multiplier 0.3
            np.average(problem.get_timeseries("HeatingDemand_8fbe.target_heat_demand").values),
        )
        np.testing.assert_allclose(
            575570.74,  # demand1_MW, multiplier 0.5
            np.average(problem.get_timeseries("HeatingDemand_08fd.target_heat_demand").values),
        )


if __name__ == "__main__":
    import time

    start_time = time.time()

    a = TestUpdatedESDL()
    a.test_updated_esdl()

    print("Execution time: " + time.strftime("%M:%S", time.gmtime(time.time() - start_time)))
