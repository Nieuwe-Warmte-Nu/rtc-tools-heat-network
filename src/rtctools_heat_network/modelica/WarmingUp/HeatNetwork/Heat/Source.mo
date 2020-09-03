within WarmingUp.HeatNetwork.Heat;

block Source
  import SI = Modelica.SIunits;
  extends HeatTwoPort;
  parameter String component_type = "source";

  parameter Real T_supply = 75.0;
  parameter Real T_return = 45.0;
  parameter Real dT = T_supply - T_return;
  parameter Real cp = 4200.0;
  parameter Real rho = 988.0;
  parameter Real head_loss = 0.0;
  parameter Real Heat_nominal = cp * rho * dT;

  // Assumption: heat in/out and added is nonnegative
  // Heat in the return (i.e. cold) line is zero
  Modelica.SIunits.Heat Heat_source(min=0.0, nominal=cp * rho * dT);
  Modelica.SIunits.Heat Heat_in(min=0.0, max=0.0, nominal=cp * rho * dT);
  Modelica.SIunits.Heat Heat_out(min=0.0, nominal=cp * rho * dT);
equation
  (HeatOut.Heat - (HeatIn.Heat + Heat_source))/Heat_nominal = 0.0;

  (Heat_out - HeatOut.Heat) / Heat_nominal = 0.0;
  (Heat_in - HeatIn.Heat) / Heat_nominal = 0.0;
end Source;
