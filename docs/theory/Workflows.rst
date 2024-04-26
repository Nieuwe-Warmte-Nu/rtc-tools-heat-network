.. _chp_workflows:

Design Toolkit Workflows
========================

This page eleborates on the available Design TOolkit workflows within MESIDO.
The Design Toolkit is a subsidy funded project (NieuweWarmteNu) to help different organizatons in the Districht heating value chain with sketch and conceptual design of District Heating Systems (DHS).
For more information see : https://nwn.nu/projecten/innovaties/design-toolkit-warmtenetten/.
MESIDO is by no means limited to only these workflows, but it is left to the user itself to define the most logical workflow if the ones below are unsuitable.

Currently two main workflows are provided:

* EndScenarioSizing
* GrowSimulator

These two workflows for now only cover the district heat network commodity.

EndScenarioSizing
-----------------

The EndScenarioSizing Workflow is designed to optimize a district heating network for both asset (pipes, sources, storages, etc.) sizing and operational strategy for lowest Total Cost of Ownership.
This workflow comes in a few variants that give the user the possibility to trade-off computational time with model assumptions.

* (EndScenarioSizingNoHeatLosses)
* EndScenarioSizing
* EndScenarioSizingDiscounted
* EndScenarioSizingHeadLoss
* EndScenarioSizingHeadLossDiscounted

EndScenarioSizing
-----------------

The EndScenarioSizing workflow in short:

* The user needs to give a district heating network in ESDL file format in which:
    * The user puts all the already present assets and potential assets of the system.
    * Specifies the cost coefficients for all assets (e.g. EUR/MW for sizing of source).
    * Specifies all the maximum sizes of the assets (e.g XX MW for sources, DN 400 for a pipe).
    * Specifies the demand profiles in hourly resolution for a full year at all demands in the system.
* The optimization routine will start by matching all the heat demands.
* After matching the demands it minimizes for system cost where both CAPEX and OPEX over lifetime are minimizes. This allows the optimizer to make trade-offs between investments and potential operational benefits (and vice-versa).
* It uses a representative year and extrapolates the results to approximate cost over the lifetime.
* It creates a smaller mathematical representation of the optimization problem by utilizing a time horizon where by default 5 day timesteps are used except for the peak day where hourly resolution is used.
    * The hourly resolution in the peak day is used to ensure that the system is sized to satisfy the demands under maximum load condition.
    * The 5 day time-steps are used for the remainder of the year to approximate the OPEX of the system utilizing the average thermal powers.
    * This means that also all time-series results will be in this adapted time-line.

A two stage optimization approach is used for faster optimization.
In the first stage the system is optimized without heat losses in the network.
This allows for a much easier mathematical representation of the problem an hence much faster optimization.
In a second stage the heat losses in the network are taken into account, however now the problem is bounded with the information of the first stage.
Pipes will only be allowed to be at least as large as the result of the first stage and one DN size larger.
Furthermore, the flow directions will be utilized if the flow meets a minimum threshold value.
Lastly, sources will now have a lower bound with the minimum of the first stage.

In its default configuration the workflow has the following main assumptions:

* The whole network is realized instantaneously, as a single year is optimized and extrapolated for the lifetime.
    * In reality the realization of DHS is done in phases over a period of years. Hence this assumption is not valid, but allows the user to judge the long term feasibilty of the DHS system. For closing business case computation the effects of phased realization should be taken into account.
* Pressure drops are not taken into account, a maximum flow velocity of 3 m/s is used to limit the pressure-drop per meter in the pipes.
    * This assumptions is ok/valid when the user is still in a phase where the exact location of (booster-)pumps is to be determined and hence limiting the sizing of pipes with pressuredrop calculations would not be representative.
    * Note that EndScenarioSizingHeadLoss can be used when the user wants the pressure-drop functionality.
* Investment costs are not discounted and all assets depreciate to zero over the system lifetime.
    * This assumption comes out of an initial development phase, by now EndScenarioDiscounted can be used.
* It is assumed that the user provides sufficient possibilities to the optimizer to match the heat demands.
    * The optimization will become a lot slower in case demands cannot be satisfied. If the user cannot garuantee to have sufficient assets to fullfill the demand it is advised to use slack (peak) sources.
* It is assumed that the tank storage in the network can only be used for intra day buffering and hence can only be used by the optimizer for the peak day.
    * If this assumption is not valid an extension of the workflow is required.
* It is assumed that seasonal storage is cyclic over calendar year, meaning that at the beginning and end of the year the same amount of thermal energy must be stored in the seasonal storage.
    * This assumption is required to ensure that the results of a single year can be extrapolated over the lifetime.

For the assumptions on the physics and cost modelling the reader is referred to the respective modelling pages.

EndScenarioSizingNoHeatLosses
-----------------------------

The EndScenarioSizingNoHeatLosses workflow provides all the same functionality as the standard EndScenarioSizing, except that heat losses in the network are not modelled.
This means that the required thermal energy of the system is underestimated and hence mainly the OPEX will be underestimated.
This workflow has the advantage that it is much faster than the default EndScenarioSizing (typically > factor 10).
Therefore, it is recommended to use this workflow in the initial phases of analysis with larger networks.
This workflow will allows to make quicker iterations on the input ESDL file and debug posssible errors in a shorter time-frame.

EndScenarioSizingNoHeatLosses workflow should not be used as a replacement of the EndScenarioSizing workflow as heat losses can be up to 20% of the demand and should not be neglected for design.


EndScenarioSizingDiscounted
---------------------------

The EndScenarioSizingDiscounted provides everything the EndScenarioSizing workflow provides, but also:

* The ability to account for varying depreciation times of assets in the system.
* The ability to take into account a discount rate for the CAPEX of assets.


EndScenarioSizingHeadLoss
-------------------------

The EndScenarioSizingHeadLoss provides everything the EndScenarioSizing workflow provides, but also:

* It takes into account the pressure drops in the network.
* It computes the hydraulic power and thereby the pumping power. It is assumed that every source will have a pump. The pumping cost will be computed with the electricity price profile if an electricity carrier is specified in the ESDL file.

