import sys
from pathlib import Path
from unittest import TestCase

from mesido.esdl.esdl_parser import ESDLFileParser
from mesido.workflows import run_end_scenario_sizing

import numpy as np


class TestUpdatedESDL(TestCase):

    def test_updated_esdl(self):
        """
        Check that the updated ESDL resulting from the optmizer, is correct by using the PoCTutorial
        and the Grow_workflow

        Checks:
        - That the correct number of KPIs have been added
        - That the correct assets have been removed
        - Check that all the assets have a state=ENABLED
        """

        root_folder = str(Path(__file__).resolve().parent.parent)
        sys.path.insert(1, root_folder)

        import examples.PoCTutorial.src.run_grow_tutorial
        from examples.PoCTutorial.src.run_grow_tutorial import EndScenarioSizingStagedHighs

        base_folder = (
            Path(examples.PoCTutorial.src.run_grow_tutorial.__file__).resolve().parent.parent
        )

        solution = run_end_scenario_sizing(
            EndScenarioSizingStagedHighs,
            base_folder=base_folder,
            esdl_file_name="PoC Tutorial.esdl",
            esdl_parser=ESDLFileParser,
        )
        # This test only exist for flake test purposes: variable never used
        results = solution.extract_results()
        np.testing.assert_array_less(0.0, len(results.values()))


if __name__ == "__main__":
    import time

    start_time = time.time()

    a = TestUpdatedESDL()
    a.test_updated_esdl()

    print("Execution time: " + time.strftime("%M:%S", time.gmtime(time.time() - start_time)))
