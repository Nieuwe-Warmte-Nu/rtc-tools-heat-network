<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" id="415d9426-dae2-4194-88ad-607793871425" description="" esdlVersion="v2401" name="Untitled EnergySystem" version="6">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="7997daa8-8ded-4f31-96b2-6842510f43f2">
    <carriers xsi:type="esdl:Carriers" id="6e119417-37a2-4dfd-a493-95f4b68d0235">
      <carrier xsi:type="esdl:ElectricityCommodity" voltage="50000.0" name="Elec" id="e1077d81-b32a-4004-9a33-db65c96b5f4c"/>
      <carrier xsi:type="esdl:GasCommodity" name="Hydrogen" pressure="15.0" id="14831e6c-c3bb-4763-8300-9658a365ee54"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="791c9938-3b6c-47b3-bcc5-0328ffd687bd" name="Untitled Instance">
    <area xsi:type="esdl:Area" id="3f8efe6b-ccda-4054-85d0-38cbcd6977da" name="Untitled Area">
      <asset xsi:type="esdl:WindPark" name="WindPark_9074" technicalLifetime="20.0" power="2000000000.0" id="90740caf-4fbd-45ed-8ea3-6af19c76256c" surfaceArea="1294320493">
        <port xsi:type="esdl:OutPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="Out" connectedTo="8f93331f-7785-4213-a6e0-d120a8f0fba7" id="fd1689e6-1339-4b77-8f8f-94acc57c752f"/>
        <geometry xsi:type="esdl:Polygon" CRS="WGS84">
          <exterior xsi:type="esdl:SubPolygon">
            <point xsi:type="esdl:Point" lon="2.9498291015625004" lat="52.311837071418886"/>
            <point xsi:type="esdl:Point" lon="3.8726806640625004" lat="52.48612543090347"/>
            <point xsi:type="esdl:Point" lon="3.6694335937500004" lat="52.68304276227743"/>
            <point xsi:type="esdl:Point" lon="2.9223632812500004" lat="52.47274306920925"/>
          </exterior>
        </geometry>
        <costInformation xsi:type="esdl:CostInformation" id="cced62ec-db9f-476c-995b-9dae86ecc08f">
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" id="0c34c932-7857-4f8f-b1b3-d7fbe04d300c" value="255000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="WATT" unit="EURO" id="9dc9c866-79ee-4a72-9982-8d3d7e04d3aa" description="Cost in EUR/MW" perMultiplier="MEGA" physicalQuantity="COST"/>
          </fixedMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:ElectricityDemand" name="ElectricityDemand_f833" power="2000000000.0" technicalLifetime="20.0" id="f8339608-af60-4b32-945b-521e6f7b8098">
        <port xsi:type="esdl:InPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="In" connectedTo="69ba58df-cb90-4ebd-843e-d5b9865aeacd" id="ac3fc355-1545-4b78-a46c-1b0908f5ccde"/>
        <geometry xsi:type="esdl:Point" lon="4.872436523437501" CRS="WGS84" lat="52.36553758871974"/>
      </asset>
      <asset xsi:type="esdl:Electrolyzer" minLoad="20000000" name="Electrolyzer_6327" effMaxLoad="69.0" technicalLifetime="20.0" efficiency="63.0" maxLoad="200000000" id="6327ee2b-9f17-432f-8d15-b034422eab79" power="200000000.0" effMinLoad="67.0">
        <port xsi:type="esdl:InPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="In" connectedTo="e2422830-d8e7-4652-a281-1d841c61e2cd" id="d81bb99d-1508-4b13-bc13-1f1a149d481d"/>
        <port xsi:type="esdl:OutPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="Out" connectedTo="272d0690-117e-4f69-bd34-ed24b2dc6f0b" id="5e58c0e2-5db4-4f6a-8aab-2c880d499c14"/>
        <geometry xsi:type="esdl:Point" lon="3.6419677734375004" CRS="WGS84" lat="52.579688026538726"/>
        <costInformation xsi:type="esdl:CostInformation" id="995670aa-a117-4569-a89b-e3a63935c829">
          <fixedMaintenanceCosts xsi:type="esdl:SingleValue" id="63836d94-a84b-4137-8274-e926ace66a9f" value="15000.0">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="WATT" unit="EURO" id="1b39bf48-df74-4fcf-b94b-a23593fa965b" description="Cost in EUR/MW" perMultiplier="MEGA" physicalQuantity="COST"/>
          </fixedMaintenanceCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:GasDemand" name="GasDemand_4146" power="500000000.0" technicalLifetime="20.0" id="41466625-a14b-43a9-9a13-93d34a4ea6ff">
        <port xsi:type="esdl:InPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="In" connectedTo="f0b7ab61-b983-45ed-9274-887ccaadfce0" id="121a1b8d-758b-4b35-92fa-894435965e85"/>
        <geometry xsi:type="esdl:Point" lon="4.707641601562501" CRS="WGS84" lat="52.633062890594374"/>
        <costInformation xsi:type="esdl:CostInformation" id="14964bd8-8eb0-4525-bcb4-0d03c1252a2b">
          <variableOperationalCosts xsi:type="esdl:SingleValue" id="5c63dce1-8a70-44f3-b6b9-476587ff73bb">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="GRAM" id="4a4516c3-372a-4a6c-b25a-dcc8dca30545" unit="EURO" description="Cost in EUR/kg" physicalQuantity="COST" multiplier="KILO"/>
          </variableOperationalCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:GasStorage" name="GasStorage_9172" maxChargeRate="100000000.0" workingVolume="1000.0" technicalLifetime="20.0" maxDischargeRate="100000000.0" id="9172f2eb-e1f4-4230-9495-396504f7c3c6">
        <port xsi:type="esdl:InPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="In" connectedTo="c3a78fa8-b482-4bcd-bad2-fd4c971b2565" id="b2bd6049-3e2e-443c-aa36-ba893135cf82"/>
        <geometry xsi:type="esdl:Point" lon="3.8177490234375004" CRS="WGS84" lat="52.566334145326486"/>
        <costInformation xsi:type="esdl:CostInformation" id="6f57c644-a1de-4c79-a707-76a6741c02b9">
          <fixedOperationalCosts xsi:type="esdl:SingleValue" id="ee900804-4f57-4488-a932-5c2a7102b4e8">
            <profileQuantityAndUnit xsi:type="esdl:QuantityAndUnitType" perUnit="GRAM" id="6ae2e528-2275-47b0-81a9-97517e478150" unit="EURO" description="Cost in EUR/kg/yr" physicalQuantity="COST" multiplier="KILO" perTimeUnit="YEAR"/>
          </fixedOperationalCosts>
        </costInformation>
      </asset>
      <asset xsi:type="esdl:Bus" name="Bus_24cf" technicalLifetime="20.0" id="24cf77d5-b66e-4362-9132-1065425d2c6a">
        <port xsi:type="esdl:InPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="In" connectedTo="fd1689e6-1339-4b77-8f8f-94acc57c752f" id="8f93331f-7785-4213-a6e0-d120a8f0fba7"/>
        <port xsi:type="esdl:OutPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="Out" connectedTo="ca9db1df-cad3-45db-8115-fc6844467c6e d81bb99d-1508-4b13-bc13-1f1a149d481d" id="e2422830-d8e7-4652-a281-1d841c61e2cd"/>
        <geometry xsi:type="esdl:Point" lon="3.7298583984375004" CRS="WGS84" lat="52.466050361889515"/>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" name="ElectricityCable_e388" technicalLifetime="20.0" length="78291.5" id="e3880640-ef13-484f-819c-47f2dc41429d" capacity="2000000000.0">
        <port xsi:type="esdl:InPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="In" connectedTo="e2422830-d8e7-4652-a281-1d841c61e2cd" id="ca9db1df-cad3-45db-8115-fc6844467c6e"/>
        <port xsi:type="esdl:OutPort" carrier="e1077d81-b32a-4004-9a33-db65c96b5f4c" name="Out" connectedTo="ac3fc355-1545-4b78-a46c-1b0908f5ccde" id="69ba58df-cb90-4ebd-843e-d5b9865aeacd"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="3.7298583984375004" lat="52.466050361889515"/>
          <point xsi:type="esdl:Point" lon="4.872436523437501" lat="52.36553758871974"/>
        </geometry>
      </asset>
      <asset xsi:type="esdl:Joint" name="Joint_2503" id="2503e1c2-e928-4331-bf0b-d41b5f1289fd">
        <port xsi:type="esdl:InPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="In" connectedTo="5e58c0e2-5db4-4f6a-8aab-2c880d499c14" id="272d0690-117e-4f69-bd34-ed24b2dc6f0b"/>
        <port xsi:type="esdl:OutPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="Out" connectedTo="1ab8ab85-2824-4606-a2ac-709596d8367b b2bd6049-3e2e-443c-aa36-ba893135cf82" id="c3a78fa8-b482-4bcd-bad2-fd4c971b2565"/>
        <geometry xsi:type="esdl:Point" lon="3.750457763671875" CRS="WGS84" lat="52.5992941670283"/>
      </asset>
      <asset xsi:type="esdl:Pipe" length="64730.1" name="Pipe_910d" id="910d3cd0-715a-423c-b67a-52fb967c85b4" diameter="DN400">
        <port xsi:type="esdl:InPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="In" connectedTo="c3a78fa8-b482-4bcd-bad2-fd4c971b2565" id="1ab8ab85-2824-4606-a2ac-709596d8367b"/>
        <port xsi:type="esdl:OutPort" carrier="14831e6c-c3bb-4763-8300-9658a365ee54" name="Out" connectedTo="121a1b8d-758b-4b35-92fa-894435965e85" id="f0b7ab61-b983-45ed-9274-887ccaadfce0"/>
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lon="3.750457763671875" lat="52.5992941670283"/>
          <point xsi:type="esdl:Point" lon="4.707641601562501" lat="52.633062890594374"/>
        </geometry>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
