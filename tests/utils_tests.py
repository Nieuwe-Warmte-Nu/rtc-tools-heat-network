from unittest import TestCase

import numpy as np


def demand_matching_test(solution, results):
    """ "Test function to check whether the heat demand of each consumer is matched"""
    len_times = 0.0
    for d in solution.heat_network_components.get("demand", []):
        if len(solution.times()) > 0:
            len_times = len(solution.times())
        else:
            len_times = len(solution.get_timeseries(f"{d}.target_heat_demand").values)
        target = solution.get_timeseries(f"{d}.target_heat_demand").values[0:len_times]
        np.testing.assert_allclose(target, results[f"{d}.Heat_demand"], atol=1.0e-3, rtol=1.0e-6)


def _get_component_temperatures(solution, results, component, side=None):
    if side:
        return_id = solution.parameters(0)[f"{component}.{side}.T_return_id"]
    else:
        return_id = solution.parameters(0)[f"{component}.T_return_id"]
    if f"{return_id}_temperature" in results.keys():
        return_t = results[f"{return_id}_temperature"]
    else:
        if side:
            return_t = solution.parameters(0)[f"{component}.{side}.T_return"]
        else:
            return_t = solution.parameters(0)[f"{component}.T_return"]
    if side:
        supply_id = solution.parameters(0)[f"{component}.{side}.T_supply_id"]
    else:
        supply_id = solution.parameters(0)[f"{component}.T_supply_id"]
    if f"{supply_id}_temperature" in results.keys():
        supply_t = results[f"{supply_id}_temperature"]
    else:
        if side:
            supply_t = solution.parameters(0)[f"{component}.{side}.T_supply"]
        else:
            supply_t = solution.parameters(0)[f"{component}.T_supply"]
    dt = supply_t - return_t
    return supply_t, return_t, dt


def heat_to_discharge_test(solution, results):
    """
    Test to check if the discharge and heat flow are correlated as how the constraints are intented:
    - demand clusters: HeatIn should be smaller or equal to discharge multiplied with the supply
    temperature due to potential heatlosses in the network, HeatOut should be fixed at the return
    temperature.
    - sources: HeatIn should be smaller or equal to discharge multiplied with the return
    temperature due to potential heatlosses in the network, HeatOut should be fixed at the supply
    temperature.
    - buffers/ates: when discharging should act like sources, when charging like demand clusters.
    - pipes: the absolute value of HeatIn and HeatOut should both be smaller than the absolute value
     of discharge with the temperature. Taking the absolute value because based on direction the
     discharge and heatflow can be negative.
    """
    test = TestCase()
    tol = 1.0e-3
    for d in solution.heat_network_components.get("demand", []):
        cp = solution.parameters(0)[f"{d}.cp"]
        rho = solution.parameters(0)[f"{d}.rho"]
        # return_id = solution.parameters(0)[f"{d}.T_return_id"]
        # if f"{return_id}_temperature" in results.keys():
        #     return_t = results[f"{return_id}_temperature"]
        # else:
        #     return_t = solution.parameters(0)[f"{d}.T_return"]
        # supply_id = solution.parameters(0)[f"{d}.T_supply_id"]
        # if f"{supply_id}_temperature" in results.keys():
        #     supply_t = results[f"{supply_id}_temperature"]
        # else:
        #     supply_t = solution.parameters(0)[f"{d}.T_supply"]
        # dt = supply_t - return_t
        # dt = solution.parameters(0)[f"{d}.dT"]
        supply_t, return_t, dt = _get_component_temperatures(solution, results, d)
        np.testing.assert_allclose(
            results[f"{d}.Heat_demand"],
            results[f"{d}.HeatIn.Heat"] - results[f"{d}.HeatOut.Heat"],
            atol=tol,
        )
        np.testing.assert_allclose(
            results[f"{d}.HeatOut.Heat"], results[f"{d}.Q"] * rho * cp * return_t
        )
        test.assertTrue(
            expr=all(results[f"{d}.HeatIn.Heat"] <= results[f"{d}.Q"] * rho * cp * supply_t + tol)
        )
        test.assertTrue(
            expr=all(results[f"{d}.Heat_demand"] <= results[f"{d}.Q"] * rho * cp * dt + tol)
        )

    for d in solution.heat_network_components.get("source", []):
        cp = solution.parameters(0)[f"{d}.cp"]
        rho = solution.parameters(0)[f"{d}.rho"]
        # dt = solution.parameters(0)[f"{d}.dT"]
        # return_id = solution.parameters(0)[f"{d}.T_return_id"]
        # return_t = results[f"{return_id}_temperature"]
        # supply_id = solution.parameters(0)[f"{d}.T_supply_id"]
        # supply_t = results[f"{supply_id}_temperature"]
        # dt = supply_t - return_t
        # supply_t = solution.parameters(0)[f"{d}.T_supply"]
        # return_t = solution.parameters(0)[f"{d}.T_return"]
        supply_t, return_t, dt = _get_component_temperatures(solution, results, d)

        test.assertTrue(
            expr=all(results[f"{d}.Heat_source"] >= results[f"{d}.Q"] * rho * cp * dt - tol)
        )
        np.testing.assert_allclose(
            results[f"{d}.HeatOut.Heat"], results[f"{d}.Q"] * rho * cp * supply_t, atol=tol
        )
        test.assertTrue(
            expr=all(results[f"{d}.HeatIn.Heat"] <= results[f"{d}.Q"] * rho * cp * return_t + tol)
        )

    for d in [
        *solution.heat_network_components.get("ates", []),
        *solution.heat_network_components.get("buffer", []),
    ]:
        cp = solution.parameters(0)[f"{d}.cp"]
        rho = solution.parameters(0)[f"{d}.rho"]
        # return_id = solution.parameters(0)[f"{d}.T_return_id"]
        # return_t = results[f"{return_id}_temperature"]
        # supply_id = solution.parameters(0)[f"{d}.T_supply_id"]
        # supply_t = results[f"{supply_id}_temperature"]
        # dt = supply_t - return_t
        # dt = solution.parameters(0)[f"{d}.dT"]
        # supply_t = solution.parameters(0)[f"{d}.T_supply"]
        # return_t = solution.parameters(0)[f"{d}.T_return"]
        supply_temp, return_temp, dt = _get_component_temperatures(solution, results, d)
        indices = results[f"{d}.HeatIn.Q"] >= 0
        if isinstance(supply_temp, float):
            supply_t = supply_temp
        else:
            supply_t = supply_temp[indices]
        if isinstance(return_temp, float):
            return_t = return_temp
        else:
            return_t = return_temp[indices]
        test.assertTrue(
            expr=all(
                results[f"{d}.HeatIn.Heat"][indices]
                <= (results[f"{d}.HeatIn.Q"][indices] * rho * cp * supply_t + tol)
            )
        )
        np.testing.assert_allclose(
            results[f"{d}.HeatOut.Heat"][indices],
            results[f"{d}.HeatIn.Q"][indices] * rho * cp * return_t,
            atol=tol,
        )
        indices = results[f"{d}.HeatIn.Q"] <= 0
        if isinstance(supply_t, float):
            supply_t = supply_temp
        else:
            supply_t = supply_temp[indices]
        if isinstance(return_temp, float):
            return_t = return_temp
        else:
            return_t = return_temp[indices]
        np.testing.assert_allclose(
            results[f"{d}.HeatIn.Heat"][indices],
            results[f"{d}.HeatIn.Q"][indices] * rho * cp * supply_t,
            atol=tol,
        )

        test.assertTrue(
            expr=all(
                results[f"{d}.HeatOut.Heat"][indices]
                >= (results[f"{d}.HeatIn.Q"][indices] * rho * cp * return_t - tol)
            )
        )

    for d in [
        *solution.heat_network_components.get("heat_exchanger", []),
        *solution.heat_network_components.get("heat_pump", []),
        *solution.heat_network_components.get("heat_pump_elec", []),
    ]:
        for p in ["Primary", "Secondary"]:
            cp = solution.parameters(0)[f"{d}.{p}.cp"]
            rho = solution.parameters(0)[f"{d}.{p}.rho"]
            # return_id = solution.parameters(0)[f"{d}.{p}.T_return_id"]
            # return_t = results[f"{return_id}_temperature"]
            # supply_id = solution.parameters(0)[f"{d}.{p}.T_supply_id"]
            # supply_t = results[f"{supply_id}_temperature"]
            # dt = supply_t - return_t
            supply_t, return_t, dt = _get_component_temperatures(solution, results, d, p)
            # dt = solution.parameters(0)[f"{d}.{p}.dT"]
            # supply_t = solution.parameters(0)[f"{d}.{p}.T_supply"]
            # return_t = solution.parameters(0)[f"{d}.{p}.T_return"]

            heat_out = results[f"{d}.{p}.HeatOut.Heat"]
            heat_in = results[f"{d}.{p}.HeatIn.Heat"]

            discharge = results[f"{d}.{p}.Q"]
            heat = results[f"{d}.{p}_heat"]

            if p == "Primary":
                np.testing.assert_allclose(heat_out, discharge * rho * cp * return_t)
                test.assertTrue(expr=all(heat_in <= discharge * rho * cp * supply_t + tol))
                test.assertTrue(expr=all(heat <= discharge * rho * cp * dt + tol))
            elif p == "Secondary":
                test.assertTrue(expr=all(heat >= discharge * rho * cp * dt - tol))
                np.testing.assert_allclose(heat_out, discharge * rho * cp * supply_t)
                test.assertTrue(expr=all(heat_in <= discharge * rho * cp * return_t + tol))

    for p in solution.heat_network_components.get("pipe", []):
        cp = solution.parameters(0)[f"{p}.cp"]
        rho = solution.parameters(0)[f"{p}.rho"]
        carrier_id = solution.parameters(0)[f"{p}.carrier_id"]
        indices = results[f"{p}.Q"] > 0
        if f"{carrier_id}_temperature" in results.keys():
            temperature = results[f"{carrier_id}_temperature"][indices]
        else:
            temperature = solution.parameters(0)[f"{p}.temperature"]
        test.assertTrue(
            expr=all(
                results[f"{p}.HeatIn.Heat"][indices]
                <= results[f"{p}.Q"][indices] * rho * cp * temperature + tol
            )
        )
        test.assertTrue(
            expr=all(
                results[f"{p}.HeatOut.Heat"][indices]
                <= results[f"{p}.Q"][indices] * rho * cp * temperature + tol
            )
        )
        indices = results[f"{p}.Q"] < 0
        if f"{carrier_id}_temperature" in results.keys():
            temperature = results[f"{carrier_id}_temperature"][indices]
        else:
            temperature = solution.parameters(0)[f"{p}.temperature"]
        test.assertTrue(
            expr=all(
                results[f"{p}.HeatIn.Heat"][indices]
                >= results[f"{p}.Q"][indices] * rho * cp * temperature - tol
            )
        )
        test.assertTrue(
            expr=all(
                results[f"{p}.HeatOut.Heat"][indices]
                >= results[f"{p}.Q"][indices] * rho * cp * temperature - tol
            )
        )
        indices = results[f"{p}.Q"] == 0
        if f"{carrier_id}_temperature" in results.keys():
            temperature = results[f"{carrier_id}_temperature"][indices]
        else:
            temperature = solution.parameters(0)[f"{p}.temperature"]
        np.testing.assert_allclose(
            results[f"{p}.HeatIn.Heat"][indices],
            results[f"{p}.Q"][indices] * rho * cp * temperature,
            atol=tol,
            err_msg=f"{p} has mismatch in heat to discharge",
        )
        np.testing.assert_allclose(
            results[f"{p}.HeatOut.Heat"][indices],
            results[f"{p}.Q"][indices] * rho * cp * temperature,
            atol=tol,
            err_msg=f"{p} has mismatch in heat to discharge",
        )


def energy_conservation_test(solution, results):
    """Test to check if the energy is conserved at each timestep"""
    energy_sum = np.zeros(len(solution.times()))

    for d in solution.heat_network_components.get("demand", []):
        energy_sum -= results[f"{d}.Heat_demand"]

    for d in solution.heat_network_components.get("buffer", []):
        energy_sum -= results[f"{d}.Heat_buffer"]

    for d in solution.heat_network_components.get("source", []):
        energy_sum += results[f"{d}.Heat_source"]

    for d in solution.heat_network_components.get("ates", []):
        energy_sum -= results[f"{d}.Heat_ates"]

    for d in solution.heat_network_components.get("heat_exchanger", []):
        energy_sum -= results[f"{d}.Primary_heat"] - results[f"{d}.Secondary_heat"]

    for d in solution.heat_network_components.get("heat_pump", []):
        energy_sum += results[f"{d}.Power_elec"]

    for d in solution.heat_network_components.get("heat_pump_elec", []):
        energy_sum += results[f"{d}.Power_elec"]

    for p in solution.heat_network_components.get("pipe", []):
        energy_sum -= abs(results[f"{p}.HeatIn.Heat"] - results[f"{p}.HeatOut.Heat"])
        if f"{p}__is_disconnected" in results.keys():
            p_discon = results[f"{p}__is_disconnected"].copy()
            p_discon[p_discon < 0.5] = 0  # fix for discrete value sometimes being 0.003 or so.
            np.testing.assert_allclose(
                results[f"{p}__hn_heat_loss"] * (1 - p_discon),
                abs(results[f"{p}.HeatIn.Heat"] - results[f"{p}.HeatOut.Heat"]),
                atol=1e-3,
            )

    np.testing.assert_allclose(energy_sum, 0.0, atol=1e-3)
