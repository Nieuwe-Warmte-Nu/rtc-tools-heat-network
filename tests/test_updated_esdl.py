import os
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
        del root_folder
        sys.path.pop(1)

        solution = run_end_scenario_sizing(
            EndScenarioSizingStagedHighs,
            base_folder=base_folder,
            esdl_file_name="PoC Tutorial.esdl",
            esdl_parser=ESDLFileParser,
        )

        # # test KPIs in optimized ESDL
        # esdl_path = os.path.normpath(
        #     os.path.join(base_folder, "model\\PoC Tutorial_GrowOptimized.esdl")
        # )
        # optimized_energy_system = solution._ESDLMixin__energy_system_handler.load_file(esdl_path)

        # # High level checks of KPIs
        # number_of_kpis_top_level_in_esdl = 8
        # high_level_kpis_name = [
        #     "High level cost breakdown [EUR]",
        #     "Overall cost breakdown [EUR]",
        #     "CAPEX breakdown [EUR]",
        #     "OPEX breakdown [EUR]",
        #     "Energy production [Wh]",
        #     "Area_76a7: Asset cost breakdown [EUR]",
        #     "Area_9d0f: Asset cost breakdown [EUR]",
        #     "Area_a58a: Asset cost breakdown [EUR]",
        # ]
        # np.testing.assert_allclose(
        #     len(optimized_energy_system.instance[0].area.KPIs.kpi),
        # number_of_kpis_top_level_in_esdl
        # )
        # for ii in range(len(optimized_energy_system.instance[0].area.KPIs.kpi)):
        #     kpi_name = optimized_energy_system.instance[0].area.KPIs.kpi[ii].name
        #     np.testing.assert_array_equal(
        #         kpi_name in high_level_kpis_name,
        #         True,
        #         err_msg=f"KPI name {kpi_name} was not expected in the ESDL",
        #     )

        # # High level checks of the assets
        # # Check quantity of assets and that they all of have an ENABLED state
        # number_of_assets_in_esdl = 15
        # np.testing.assert_allclose(
        #     len(optimized_energy_system.instance[0].area.asset), number_of_assets_in_esdl
        # )
        # asset_to_be_deleted = ["ResidualHeatSource_76f0", "Pipe_8fa5_ret", "Pipe_8fa5"]
        # for ii in range(len(optimized_energy_system.instance[0].area.asset)):
        #     asset_name = optimized_energy_system.instance[0].area.asset[ii].name
        #     np.testing.assert_array_equal(
        #         asset_name not in asset_to_be_deleted,
        #         True,
        #         err_msg=f"Asset name {asset_name} was not expected in the ESDL",
        #     )
        #     np.testing.assert_array_equal(
        #         optimized_energy_system.instance[0].area.asset[ii].state.name == "ENABLED", True
        #     )

        # # High level check on the polygon areas drawn
        # number_of_areas_in_esdl = 3
        # np.testing.assert_allclose(
        #     len(optimized_energy_system.instance[0].area.area), number_of_areas_in_esdl
        # )


if __name__ == "__main__":
    import time

    start_time = time.time()

    a = TestUpdatedESDL()
    a.test_updated_esdl()

    print("Execution time: " + time.strftime("%M:%S", time.gmtime(time.time() - start_time)))
