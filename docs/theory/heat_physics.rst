.. _chp_heat_physics:

Heat Physics
============

Mesido models thermal power (:math:`\dot{Q}`), volumetric flow (:math:`\dot{V}`), and head (:math:`H`) for DHS systems.
These variables are modelled over all time-steps :math:`K` and for each asset in the system :math:`A`.
An asset :math:`a \in A` in the system is modelled using a set of in-ports, denoted by :math:`I^a_{in} \neq \emptyset`, and a set of out-ports, denoted by :math:`I^a_{out} \neq \emptyset`, with :math:`I^a` denoting the union of these two sets.
For an asset :math:`a` the three variables :math:`\dot{Q}_i, \dot{V}_i`, and :math:`H_i` denote the thermal power, volumetric flow and head for port :math:`i \in I^a`. For readability, the variables and equations of the model, given below, are defined without indexing the variables and sets for each time-step.
The equations below are assumed to hold for every time-step, unless otherwise specified.

Modelling specifically these three variables allows to ensure a hydraulically feasible solution whilst linearizing the physics.
Energy changes are modelled with the assumption of a constant temperature throughout the network.
Although this assumption is not realistic, the linearization made will show that the effects of these assumptions are relatively small and conservative to the objective function outcome.

General Physics
---------------

The DHS is modelled as a closed loop system and thus at every time-step and for every asset, mass balance should hold.
The system is modeled with constant temperature and thus constant density and specific heat.
The mass balance is provided as a volumetric flow balance in :eq:`eq:flow_balance`.

.. math::
    :label: eq:flow_balance

    \sum_{i \in I^a} \dot{V}_{i} = 0 \;\; \forall a \in A


To garuantee energy balance :eq:`eq:general_energy_balance` is applied.

.. math::
    :label: eq:general_energy_balance

    \sum_{i \in I} \dot{Q}_i + \dot{Q}^a_{consumed} = 0 \;\; \forall a \in A

:math:`\dot{Q}^a_{consumed}` is the thermal power consumed by asset :math:`a`.
The power losses for the asset are included in this variable. Furthermore, the convention that positive consumed power is equal to thermal power production of an asset.

Network Physics
---------------

Pipe
~~~~
The main function of a pipe is to transport thermal power.
It loses part of this thermal power to the surroundings as the ambient temperature is lower, thus :math:`\dot{Q}^a_{consumed}` equals the (negative) losses incurred in the pipe in :eq:`eq:general_energy_balance`.

The thermal power losses are approximated with :eq:`eq:heat_loss`, utilizing the Bohm model, :cite:`bohm`.

.. math::
    :label: eq:heat_loss

    \dot{Q}^a_{consumed} = L^a( (U_2 - U_1)T_{amb} + U_1 T_{sup} - U_2 T_{ret})\delta^a_{discon} \forall a \in A_{pipes}

where

.. math::
    :label: eq:pipe_heat_loss_U1

    U_1 = \frac{R_{subsoil} + R_{ins}}{(R_{subsoil} + R_{ins})^2 - R_{neighbour}^2}

.. math::
    :label: eq:pipe_heat_loss_U2

    U_2 = \frac{R_{neighbour}}{(R_{subsoil} + R_{ins})^2 - R_{neighbour}^2}

.. math::
    :label: eq:pipe_heat_loss_Rins

    R_{ins} = \sum_i \frac{ln(\frac{d^a_{outer}}{d^a_{inner}})}{2\pi k}

.. math::
    :label: eq:pipe_heat_loss_Rneigh

    R_{neighbour} = \frac{ln(1 + (2H/2d^a_{outer})^2)}{4 \pi k_{subsoil}},

.. math::

    R_{subsoil} = \frac{ln(\frac{4H}{d^a_{outer}})}{2 \pi k_{subsoil} }.

.. math::

    \delta^a_{discon} \in \{0, 1\} \;\; \forall a \in A_{pipes}

:math:`T_{sup}, T_{ret}`, and :math:`T_{amb}` represent the supply, return and ambient temperatures.
:math:`A_{pipes}` define the set of pipes with :math:`L^a` being the length of pipe :math:`a`.
:math:`\delta^a_{discon}` is a boolean variable to model if pipe :math:`a` is in use for a specific time-step.
:math:`d^a_{inner}` and :math:`d^a_{outer}` are the inner and outer diameters of pipe :math:`a` and :math:`k_{subsoil}` is a constant used to model the resistance of the subsoil.
:math:`\delta^a_{discon}` is modelled by:

.. math::

    \dot{Q}_{i} + \delta_{discon}M \geq 0 \;\; \forall i \in I^{a} \;\; \forall a \in A_{pipes},

.. math::

    \dot{Q}_{i} - \delta_{discon}M \leq 0 \;\; \forall i \in I^a \;\; \forall a \in A_{pipes}.

Here :math:`M` is a sufficiently large constant used in a method called the big-M method :cite:`vielma2015mixed`.

The thermal power loss is assumed to be constant as the pipe temperature is assumed to be constant.
The outgoing temperatures at the assets (e.g. supply at the source and return at the demand) are used to ensure an overestimation of the thermal loss. In reality the temperature w.r.t. the ambient decreases as the temperature drops over the pipe with the energy loss.

Typical temperature drops in the primary network are up to 3 degrees, this implies that for medium temperature networks, operating at 75 degrees and with an ambient of 15 degrees, the error for the heat loss estimation is less than :math:`\frac{3}{75-15} \approx 5\%`.

Inequality constraints are used to relate the volumetric flow :math:`\dot{V}` and the heat flow :math:`\dot{Q}` through pipes as a compensation of heat losses is required.
Please note that the :math:`\dot{V}` and the heat flow :math:`\dot{Q}` will be related by equality constraints for the outgoing flow at the assets, ensuring that the thermal power propagates correctly through the network.

.. math::
    :label: eq:pipe_heat2discharge1

    \dot{Q}_{i} - c_p \rho T^a \dot{V} - (1 - \delta^a_{dir})M \leq 0  \;\; \forall i \in I^a \;\; \forall a \in A_{pipes},

.. math::
    :label: eq:pipe_heat2discharge2

    \dot{Q}_{i} - c_p \rho T^{a} \dot{V} + \delta^a_{dir}M \geq 0 \;\; \forall i \in I^a
    \;\; \forall a \in A_{pipes},

.. math::
    :label: eq:pipe_flow_dir

    \delta^a_{dir} \in \{ 0, 1 \} \;\; \forall a \in A_{pipes}.

Here :math:`T^a` is the temperature inside pipe :math:`a`, :math:`c_p` and :math:`\rho` are the specific heat capacity and density of water and :math:`M` is a sufficiently large constant number.
:math:`\delta^a_{dir}` is the variable for  flow direction in the pipe, where a value of :math:`1` indicates a positive flow (from in-port to out-port). This is modelled using:

.. math::
    :label: eq:flowdir1

    \dot{Q}^a_{i} - \delta^a_{dir}M \leq 0 \;\; \forall i \in I^a \;\; \forall a \in A_{pipes},

.. math::
    :label: eq:flowdir2

    \dot{Q}_{i} + (1 - \delta_{dir})M \geq 0 \;\; \forall i \in I^{a} \;\; \forall a \in A_{pipes}.

Within a hydraulically coupled system the volume is assumed to be preserved as result of the mass balance and constant temperature, therefore :eq:`eq:flow_balance` is applied to pipes.
Pipes give resistance opposing the flow in the flow of head loss, :math:`dH`. This head loss must be compensated by pumps which are assumed to be located at sources and storage assets:

.. math::
    :label: eq:pipe_head

    H^a_{in} - dH = H^a_{out} \;\; \forall a \in A_{pipes}.

In reality the steady-state head losses are closely modelled with a quadratic relation w.r.t. :math:`\dot{V}`. To approximate the quadratic behaviour a set of linear inequalities is used, see :numref:`inequalitydH`. The general form of the inequalities is given below in :eq:`eq:pipe_head_loss1`-:eq:`eq:pipe_hp2` These inequalities force the head loss to be greater or equal to the approximated quadratic curve. Although this will not enforce a physically feasible answer the optimizer will in practice drag the solution to an equality constraint as the objective function will minimize cost that reduces with lower pressure drop.

.. _inequalitydH:

.. figure:: ../images/linearlines.png
    :figwidth: 6.94792in
    :align: center

    Schematic visualization of how the linear constraints are fitted to the head loss curve.

This method with linear inequalities is only valid when every unique route the flow can take in the network has a control valve to compensate non-physical head loss induced by the optimizer. This was a valid assumption for the use-case in this research, alternatively a (piece-wise) linear equality constraint between min and max flow-rate can be applied for cases where this assumption is invalid.

Note that the big M method is used in combination with the flow direction integers to allow the inequality constraints to work both for positive and negative flow and to allow for disabling the constraints when no flow is going through the pipe.

.. math::
    :label: eq:pipe_head_loss1

    dH - (\alpha_j \dot{V} + \beta_j) + (\delta^a_{discon} + 1-\delta^a_{dir})M\geq 0 \\ \forall (\alpha_j, \beta_j) \;\; \forall a \in A_{pipes},

.. math::
    :label: eq:pipe_head_loss2

    dH - (\alpha_j\dot{V} + \beta_j) - (\delta^a_{discon} + \delta^a_{dir})M\leq 0 \\  \forall (\alpha_j, \beta_j) \;\; \forall a \in A_{pipes}.

Where :math:`(\alpha_j, \beta_j)` are the coefficients and constants of the linear equations used to approximate the quadratic equation.

Similar as with head loss the hydraulic power, :math:`HP^a`, required to overcome the head losses is modelled with a set of linear inequalities:

.. math::
    :label: eq:pipe_hp1

    HP^a - (c_j\dot{V} + d_j)  + (\delta^a_{discon} + 1-\delta^a_{dir})M \geq 0 \\
    \forall (c_j, d_j) \;\; \forall a \in A_{pipes},

.. math::
    :label: eq:pipe_hp2

    HP^a - (c_j\dot{V} + d_j)  - (\delta_{discon}(k) - 1-\delta_{dir})M\geq 0 \\
    \forall (c_j, d_j) \;\; \forall a \in A_{pipes}.

Here :math:`(c_j, d_j)` are the coefficients and constants of the linear equations used to approximate the quadratic equation.

Node
~~~~

A node needs to conserve the flow with :eq:`eq:flow_balance` and the energy with :eq:`eq:general_energy_balance` where no energy losses, production and consumption occurs.

To make the solution hydraulically feasible it is enforced that all heads connected to the node have to be equal:

.. math::
    :label: eq:node_head

    H_i = H^a \;\; \forall i \in I^a \;\; a \in A_{nodes},

where :math:`A_{nodes}` is the set of all nodes and :math:`H^a` is the headloss for node :math:`a`.

Asset Physics
-------------

Source
~~~~~~

The main function of a source is to add thermal power to the network that can be consumed, or is lost to the ambient.
The energy balance of the addition of thermal power is ensured by :eq:`eq:general_energy_balance` with :math:`\dot{Q}^a_{consumed}` is set to the (negative) value of the produced amount of heat.

The addition of energy is executed by increasing the temperature of the incoming cold water of the return network to the outgoing supply temperature.
Therefore, the volumetric flow-rate is linked to the outgoing thermal power with the outgoing supply temperature using:
%

.. math::
    :label: eq:source_heat2discharge

    \sum_{i \in I^a_{out}} \dot{Q}^a_i = c_p \rho \dot{V}^a T_{sup} \;\; \forall a \in A_{prod},

with :math:`A_{prod}` the set of all producers. Note that we assume that every producer has only a single in- and a single out-port.

This equality constraint ensures that the thermal power cannot be larger than what physically can be transported by the flow. Applying only equality constraints on the outgoing heat of assets, except from pipes, allows to consider temperature regimes, their corresponding heat losses and volumetric flows without modelling the temperature.
No constraints are set on the returning flow to the producer as this is already implied by heat flow constraints on pipes. The optimizer will drag the solution to the minimum amount of thermal power to produce for minimizing cost.

The errors as a result of not modelling the temperature, e.g. linearizing the problem,  can be observed in various parts of the costs.
The heat losses will be overestimated resulting in a conservative estimation w.r.t. the cost of the thermal energy produced.
Furthermore, the overestimation in thermal power will result in an overestimation of the flow and thus of the transportation and pipe sizing cost.

It is assumed that the source acts within the hydraulically coupled network and does not add or subtract mass, which under the assumption of constant temperature ensures the flow balance :eq:`eq:flow_balance`.

It is assumed that every source has a pump to reach its desired flow-rate and head:

.. math::
    :label: eq:source_pump_dh

    H^a_{in} + dH_{pump} = H^a_{out} \;\; \forall a \in A_{prod}.

Since we assume that a producer has only a single in- and a single out-port, :math:`H^a_{in}` and :math:`H^a_{out}` are the head values of the specific pipes connected to these ports, and :math:`dH_{pump}` is the compensation provided by the pump of the asset.

Demand
~~~~~~

Contrary to a source, a demand's function is to extract thermal power from the network, defined by :eq:`eq:general_energy_balance` where :math:`\dot{Q}^a_{consumed}` is the consumed thermal energy by the demand.

Likewise to a source, no additional constraints are required to link the heat flow and volumetric flow at the in-going supply side of the demand as this is already implied by all other network constraints.
An equality constraint is used to link outgoing thermal power and volumetric flow with the return temperature of the network:

.. math::
    :label: eq:consumer_heat2discharge

    \sum_{i \in I^a_{out}} \dot{Q}^a_i = c_p \rho \dot{V}^a T_{ret} \;\; \forall a \in A_{demand},

where :math:`A_{demand}` is the set of demand assets.

Important to note, is that this combination of constraints for the producers and demands, results in a smaller achieved temperature difference at the demand than the difference between the given temperatures for the supply and return side. And a larger achieved temperature difference at the producer.
The choice on where a temperature is fixed results in different errors as already explained at the producers.

Again it is assumed that a demand also acts within the hydraulically coupled system under the same assumptions, see :eq:`eq:flow_balance`.

Every demand is assumed to have a control valve to regulate its flow. Typically, a minimum head loss should be maintained:

.. math::
    :label: eq:demand_head

    H^a_{in} - dH_{valve} = H^a_{out} \;\; \forall a \in A_{demand}.

Storage
~~~~~~~

Storage assets in the network can have the function to add time flexibility with the production and consumption of energy in the network. For shorter periods this capability is provided by tanks, storage over seasons is done with \gls{ht-ates}, \cite{drijver2019state}. Both are modelled with equivalent logic and their own specific parameters.

The amount of thermal power extracted from or provided to the network subtracted by the losses in the storage is defined as :math:`\dot{Q}^{a}_{consumed}` by:

.. math::
    :label: eq:change_stored_heat

    \dot{Q}^{a}_{consumed} =  \sum_{i \in I^a_{in}} \dot{Q}^{a}_{i} -  \sum_{i \in I^a_{out}} \dot{Q}^{a}_{i} - \dot{Q}^{a}_{loss} \;\; \forall a \in A_{storage},

where :math:`\dot{Q}^{a}_{in}`, :math:`\dot{Q}^{a}_{out}` and :math:`\dot{Q}^{a}_{loss}` define the heat entering, leaving and heat loss of the storage asset respectively.
The consumed heat of the storage assets is equated to the change change in stored heat, :math:`\dot{Q}^{a}_{stored}`:


.. math::
    :label: eq:stored_heat

    \dot{Q}^{a}_{consumed} = \dot{Q}^{a}_{stored} \;\; \forall a \in A_{storage}


The storage needs an equality constraints for thermal power to volumetric flow on the outgoing flow to the supply network when it is discharging and acting like a source and on the outgoing flow to the return network when it is charging and acting like a demand.
This is achieved by using the big M method to activate the constraints during charging, :eq:`eq:storage_heat2discharge1` and :eq:`eq:storage_heat2discharge2`, and during discharging, :eq:`eq:storage_heat2discharge3` and :eq:`eq:storage_heat2discharge4`.
For this purpose the flow direction integer of the connecting pipe is used, such that :math:`\delta_{dir}` is 1 for charging.

.. math::
    :label: eq:storage_heat2discharge1

     \sum_{i \in I^a_{in}} \dot{Q}^{a}_{i} - c_p \rho \dot{V}^{a} T_{sup} \leq 0 \;\; \forall a \in A_{storage}

.. math::
    :label: eq:storage_heat2discharge2

     \sum_{i \in I^a_{in}} \dot{Q}^{a}_{i} - c_p \rho \dot{V}^{a} T_{sup} + \delta^{a}_{dir} M \geq 0 \;\; \forall a \in A_{storage}

.. math::
    :label: eq:storage_heat2discharge3

     \sum_{i \in I^a_{out}} \dot{Q}^{a}_{i} - c_p \rho \dot{V}^{a} T_{ret} \geq 0 \;\; \forall a \in A_{storage}

.. math::
    :label: eq:storage_heat2discharge4

     \sum_{i \in I^a_{out}} \dot{Q}^{a}_{i} - c_p \rho \dot{V}^{a} T_{ret} - (1-\delta^{a}_{dir}) M \leq 0 \;\; \forall a \in A_{storage}

For simplicity it is assumed that the loss scales linearly with the amount of stored heat:

.. math::
    :label: eq:storage_loss

    \dot{Q}^{a}_{loss} = \beta^{a} Q^{a}_{stored} \;\; \forall a \in A_{storage},

where :math:`Q^{a}_{stored}` is the heat stored in the storage asset and :math:`\beta` is the efficiency factor.

For tanks it is assumed that they are cylindrical and radiate heat over their their surface area. This is done as this surface area increases linearly with the stored heat, see :eq:`eq:etatank`. A radiation coefficient, :math:`c_r`, of 1 :math:`W/m^2` is used as an approximation.

.. math::
    :label: eq:etatank

    \beta_{tank} = \frac{2c_r}{r\rho c_p}

For an \gls{ht-ates} a first approximation for heat loss is based on an efficiency that is reached in a period of time. In this research a value of 70\% over 100 days is used.

.. math::

    \beta_{HTATES} = \eta^{\frac{1}{time}}


Similarly as for the other assets the storage assets are assumed to act within the hydraulically coupled system, nonetheless the volumetric flow balance requires additional equations.
The storage is modelled as an asset with two variable volumes, one for the cold and one for the warm water. The total in- and outflow of the storage will be equal, however, the volumes inside the storage might vary under the condition that the sum remains constant and is equal to the total volume of storage:%, modelled using :eq:`eq:storage_volume_constant`.

.. math::
    :label: eq:storage_volume_constant

    \dot{V}^{a}_{warm}-\dot{V}^{a}_{cold}=0 \;\; \forall a \in A_{storage},

where :math:`\dot{V}^{a}_{warm}` and :math:`\dot{V}^{a}_{cold}`, respectively denote the change in volume of the warm and cold water.
The warm volume will increase and decrease with the volumetric flow passing the storage:

.. math::
    :label: eq:storage_volume_change

    \dot{V}^{a}-\dot{V}^{a}_{warm}=0 \;\; \forall a \in A_{storage}.

The storage assets are assumed to have both a pump and a valve to regulate their flow rate:

.. math::
    :label: eq:source_pump

    H^{a}_{in} + dH^{a}_{pump} - dH^{a}_{valve} = H^{a}_{out} \;\; \forall a \in A_{storage},

where :math:`dH^{a}_{pump}` is a compensation of the pressure increase by the pump of the storage asset and :math:`dH^{a}_{valve}` is a compensation of the pressure decrease by the control valve of the storage asset.


