from rtctools.optimization.timeseries import Timeseries
from rtctools.util import run_optimization_problem


def run_heat_network_optimization(heat_class, qht_class, *args, **kwargs):
    heat_problem = run_optimization_problem(heat_class, *args, **kwargs)
    results = heat_problem.extract_results()
    times = heat_problem.times()

    directions = {}

    hot_pipes = [p for p in heat_problem.heat_network_components["pipe"] if p.endswith("_hot")]

    for p in hot_pipes:
        heat_in = results[p + ".HeatIn.Heat"]
        heat_out = results[p + ".HeatOut.Heat"]

        if not heat_problem.parameters(0)[p + ".disconnectable"]:
            # Flow direction is directly related to the sign of the heat
            direction_pipe = (heat_in >= 0.0).astype(int) * 2 - 1
        elif heat_problem.parameters(0)[p + ".disconnectable"]:
            direction_pipe = (heat_in >= 0.0).astype(int) * 2 - 1
            # Disconnect a pipe when the heat entering the component is only used
            # to account for its heat losses. There are three cases in which this
            # can happen.
            direction_pipe[((heat_in > 0.0) & (heat_out < 0.0))] = 0
            direction_pipe[((heat_in < 0.0) & (heat_out > 0.0))] = 0
            direction_pipe[((heat_in == 0.0) | (heat_out == 0.0))] = 0
        directions[p] = Timeseries(times, direction_pipe)

        # NOTE: The assumption is that the orientation of the cold pipes is such that the flow
        # is always in the same direction as its "hot" pipe companion.
        cold_pipe = f"{p[:-4]}_cold"
        directions[cold_pipe] = directions[p]

    buffer_target_discharges = {}
    parameters = heat_problem.parameters(0)

    for b in heat_problem.heat_network_components.get("buffer", []):
        cp = parameters[f"{b}.cp"]
        rho = parameters[f"{b}.rho"]
        delta_temperature = parameters[f"{b}.T_supply"] - parameters[f"{b}.T_return"]
        heat_flow_rate_to_discharge = 1 / (cp * rho * delta_temperature)
        buffer_target_discharges[b] = Timeseries(
            times, results[f"{b}.Heat_buffer"] * heat_flow_rate_to_discharge
        )

    qth_problem = run_optimization_problem(
        qht_class,
        *args,
        flow_directions=directions,
        buffer_target_discharges=buffer_target_discharges,
        **kwargs,
    )

    return heat_problem, qth_problem
