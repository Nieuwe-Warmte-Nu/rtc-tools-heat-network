<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" esdlVersion="v2107" version="2" name="case1_elec" id="b9a86f6b-02b4-4ab3-b2f3-608647c28e0e" description="Single source, single sink">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="2bb5f647-e4ff-490a-9642-ccf9274d9c40">
    <carriers xsi:type="esdl:Carriers" id="f6672aa2-7723-4945-92fa-b99846f58c92">
      <carrier xsi:type="esdl:ElectricityCommodity" voltage="230.0" id="a04bdbac-5198-477b-9989-d99c3c001eaf" name="Electricity"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="67052ed2-f139-4936-9cd8-b4c419bf2cfa" name="Untitled instance">
    <area xsi:type="esdl:Area" id="960acb90-32e0-4754-821d-f53e5567974b" name="Untitled area">
      <asset xsi:type="esdl:ElectricityProducer" name="ElectricityProducer_b95d" id="b95dc1f7-e189-4745-8c12-3d626faf4d44" power="1000.0">
        <geometry xsi:type="esdl:Point" lat="51.96451418555131" CRS="WGS84" lon="4.416246414184571"/>
        <port xsi:type="esdl:OutPort" name="Out" id="ee8afa6b-b78b-42fc-acaa-8b47e8680c19" carrier="a04bdbac-5198-477b-9989-d99c3c001eaf" connectedTo="86f5473a-c2de-488f-9193-7aa8fe14edad"/>
      </asset>
      <asset xsi:type="esdl:ElectricityDemand" name="ElectricityDemand_2af6" id="2af646f3-f6ec-4086-baf6-df08a225c7d9" power="1000.0">
        <geometry xsi:type="esdl:Point" lat="51.96619321496721" CRS="WGS84" lon="4.421074390411378"/>
        <port xsi:type="esdl:InPort" name="In" id="3f5a40fd-1a3e-4bd0-a0da-7bca9f891328" connectedTo="d0d25328-6989-4933-ba30-7f9e1b47b8a0" carrier="a04bdbac-5198-477b-9989-d99c3c001eaf"/>
      </asset>
      <asset xsi:type="esdl:ElectricityCable" length="245.5" name="ElectricityCable_238f" id="238feeba-231f-49b6-b5fc-ae3bfee9e6a5" capacity="32660">
        <geometry xsi:type="esdl:Line" CRS="WGS84">
          <point xsi:type="esdl:Point" lat="51.96477860380529" lon="4.417126178741456"/>
          <point xsi:type="esdl:Point" lat="51.965849481781945" lon="4.4202589988708505"/>
        </geometry>
        <port xsi:type="esdl:InPort" name="In" id="86f5473a-c2de-488f-9193-7aa8fe14edad" connectedTo="ee8afa6b-b78b-42fc-acaa-8b47e8680c19" carrier="a04bdbac-5198-477b-9989-d99c3c001eaf"/>
        <port xsi:type="esdl:OutPort" name="Out" id="d0d25328-6989-4933-ba30-7f9e1b47b8a0" carrier="a04bdbac-5198-477b-9989-d99c3c001eaf" connectedTo="3f5a40fd-1a3e-4bd0-a0da-7bca9f891328"/>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
