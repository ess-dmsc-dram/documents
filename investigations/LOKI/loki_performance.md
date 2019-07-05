# LOKI Live Reduction Performance in Mantid

## Motivation

The [LOKI instrument](https://europeanspallationsource.se/instruments/loki) for small angle neutron scattering is scheduled to be one of the first instruments to come online for the ESS. As such, one of the [High Level DMSC Milestones](https://confluence.esss.lu.se/pages/viewpage.action?pageId=262411283) is to ensure the data reduction software can cope with the proposed instrument flux in a live data reduction scenario. LOKI will be ~1Mpixels with an incident flux between 10<sup>5</sup>Hz and 10<sup>8</sup>Hz (worst case). This represents a significant processing and storage challenge for the ESS. Since Mantid has been chosen as the data-reduction platform at the ESS, it is critical that the software can cope with the expected data rates in preparation for hot comissioning and early science in mid 2023. The maximum instrument flux during these phases is set to be ~10<sup>7</sup>Hz. This document outlines the current performance of the Mantid framework and recommendations for improvements which may allow performance to meet the requirements.

## Scope
This document only covers performance benchmarks for the LOKI instrument based on the geometry described in the proceeding section. A general benchmarking exercise of the live data reduction in Mantid was performed [here](https://github.com/DMSC-Instrument-Data/documents/blob/master/investigations/Live%20Reduction/LiveReductionInvestigation.md) and this document may be referenced within. 

## LOKI Geometry
The LOKI Geometry used for these tests are as specified in the engineering diagrams below. This design supersedes the initial BandGEM approach and will be utilizing a straw tube implementation. This decision to use straw tubes was fixed in early 2018. The instrument consists of 864 tubes (6048 straws) with an intrinsic resolution of 5mm. Straw lengths vary between 1.2m and 0.5m which gives a total pixel count of 1,245,880pixels.
![geometry](loki_geometry.png)
![mantid](loki_mantid.png)

## Build-out Phases

Currently "Day 1" operations for LOKI are set to commence November 2022. The initial instrument will contain the rear detector bank and 2 panels (one horizontal and one vertical) in the front and middle banks each. The resulting instrument will consist of ~473K pixels. However based on initial simulations, most of the detected neutron beam will be concentrated on the rear bank. The remaining banks are currently set to be added to the final instrument between 1-5 years beyond 2022. Hot commissioning and early science for this instrument are set for mid 2023 with full operations at the start of 2025.

## Hardware 

The hardware used for these tests is as follows:

- 128GB RAM
- Intel(R) Core(TM) i9-9920X CPU @ 3.50GHz
- Target Linux Platform (OpenMP is a hard requirement)

## Live Consumption Tests
### Event rates
This document only explores performance at a target rate of 10<sup>7</sup>events/s as a worst case since day 1 instrument flux of 1MW, ramping up to 2MW, will not result in an incident flux beyond this for LOKI. See [ess-hardware-requirements-report-v1.pdf](report.pdf) produced by Simon Heybrock.

### Measurement Interpretation
The ESS pulse rate for neutrons is expected to be **14Hz**. This will be the rate at which messaged will be produced in the Kafka system and therefore consumed by Mantid. Measurements are taken in this context. If Mantid is capable of processing events (writing events to in-memory data structures and performing basic reduction) at this rate at a target neutron flux, this indicates that Mantid can cope with the event rate.
### Previous Efforts
The performance of Mantid for live data streaming/reduction was evaluated and results presented in the following document [LiveReductionInvestigation](https://github.com/DMSC-Instrument-Data/documents/blob/master/investigations/Live%20Reduction/LiveReductionInvestigation.md). Following from this work Lamar Moore (ISIS), Dan Nixon (ISIS/ESS-in-kind) and Simon Heybrock (ESS) met December 2018 in Copenhagen to discuss and prototype strategies for addressing performance bottlenecks in this area. The result of this work can be found [here](https://github.com/DMSC-Instrument-Data/documents/blob/master/meeting_notes/December_2018/agenda.md). After this meeting the team reached the following conclusions:

- Optimizing Mantid to satisfy ESS performance requirements is achievable with current time and resource.
- The optimization effort can be carried out without the need for MPI (distribution of the event stream for use on a HPC Cluster).
- The optimizations can be implemented within 2-3 person months.

**There were previous small optimizations made as part of the live reduction investigation which resulted in small performance improvements in the live streamer. Tests conducted in this investigation started with these small optimizations as opposed to the state of the current Mantid release.**
### Random Data Test (Writing to Workspace)
#### Data
The data was generated using the following tools ESS-based tools:

- [python-nexus-utilities](https://github.com/ess-dmsc/python-nexus-utilities)
- [generate-nexus-files](https://github.com/ess-dmsc/generate-nexus-files)
- [NeXus-Streamer](https://github.com/ess-dmsc/NeXus-Streamer)

An Mantid XML instrument definition file (IDF) was produced based on the geometry described above ([LOKI IDF](LOKI_Tube_Definition.xml)). The IDF was fed into `generate-nexus-files` to produce the corresponding Nexus geometry file. This file was streamed to a kafka broker which existed in a containerised (Docker) instance on the local computer so that network effects could be ignored. The nexus streamer was used in random mode so that large numbers of fake, random data could be produced for all banks at a pre-determined rate.
#### LOKI Performance with Random Data
The initial test for LOKI at 10<sup>7</sup>Hz yielded a maximum kafka message consumption rate in Mantid of ~6Hz. This initial test was performed without the optimizations mentioned in the *Previous Efforts* section of this document. They were also performed on a machine with the following specifications:

- 64GB RAM
- 7th Gen Intel Core i7 Quad Core (8 threads) 8MB SmartCache

Subsequently, further optimizations to the Mantid live reduction code was performed by Dan Nixon. The detail of which is outlined below:

*Instead of received events (from the Kafka stream) being immediately inserted into an EventWorkspace they are instead stored in a buffer held by the decoder.
When this buffer is full (where full is a number of events set by the user) it is sorted to place events from the same detector in the same period adjacent to one another. This locality is then used to allow those events to be inserted into the EventWorkspace in parallel (as division of the work across threads can guarantee no EventList is accessed on multiple threads).*

*Instead of storing a hash map of detector to workspace index (which is slow to index), a vector is created where the indices represent detector numbers and the values are the associated workspace index (which is much faster to index but would typically use more memory).*

These optimizations pushed the achievable kafka message consumption rate to >20Hz which satisfies, and exceeds, the 14Hz target.

#### Conclusion
Even with random data (noise), which represents the worst case scenario for event collection, Mantid is able to cope with an event rate of 10<sup>7</sup>Hz. **N.B** This is only for writing events to the Workspace and performing a simple rebin to histogram for the output workspace.

### MCStas/Geant4 Simulated Data Test 

Realistic LOKI data was generated by Judith Houston (ESS LoKI instrument scientist) using McStas and Geant4. This simulated data was ingested into Mantid to produce a Nexus file which could be used in the `NeXus-Streamer` for our test purposes. The dataset consists of neutrons scattered on the rear LOKI panel ignoring the front 2 banks (as pictured below).

![LOKI Geant4 data](loki_geant4.png)

The data file contained ~1M events which represented a single pulse. In order to generate a longer run, data was duplicated over 840 pulses (60 second run at 14Hz). This data was then streamed into Kafka and used to test consumption rates and data reduction rates.

#### Writing To Workspace

Data consumption rates averaged ~24Hz (messages) at an event rate of ~1.4e<sup>7</sup>Hz. This utilized a 30s timeout for `MonitorLiveData` and a basic `Rebin` operation for displaying data on the instrument. The event buffer stored 2.5e<sup>7</sup> events before writing to the workspace.

##### Scaling
There was previous work done in investigating how well the live streamer in Mantid scales and was presented in this document [LiveReductionInvestigation](https://github.com/DMSC-Instrument-Data/documents/blob/master/investigations/Live%20Reduction/LiveReductionInvestigation.md). Scaling for LOKI ingesting the simulated data showed the following trend:

`#` of threads|Message Consumption Rate (Hz)
---|---
1|80
4|234
8|299
16|472
24|194

Note that at 24 threads it is assumed the host system is oversubscribed due to running Mantid, Kafka broker and NeXus publisher simultaneously.

#### With Live Reduction Script

The test for live reduction was carried out using the following basic script (taken from previous tests):

**Test SANS Script**
```python
# SANS Reduction Realistic
ConvertUnits(InputWorkspace="accum_events", OutputWorkspace="ws", Target="Wavelength")
FindCenterOfMassPosition(InputWorkspace="ws", Output="CentreOfMass")
com = mtd["CentreOfMass"]
beam = com.column(1)
MoveInstrumentComponent(Workspace="ws", ComponentName="Panel_9_horz_1000_back", X=beam[0], Y=beam[1], RelativePosition=True)
MoveInstrumentComponent(Workspace="ws", ComponentName="Panel_1_horz_1200_top", X=beam[0], Y=beam[1], RelativePosition=True)
SANSSolidAngleCorrection(InputWorkspace="ws", OutputWorkspace="ws", DetectorTubes=False, DetectorWIng=False)
SANSAbsoluteScale(InputWorkspace="ws", OutputWorkspace="ws", ScalingFactor=0.99)
Rebin(InputWorkspace="ws", OutputWorkspace="ws", Params="74294664", PreserveEvents=False)
Q1D(DetBankWorkspace="ws", OutputWorkspace="SANSReduced", SolidAngleWeighting=False, OutputBinning="1,5,100")
```

Data consumption rates averaged ~18Hz (messages) at an event rate of ~1.4e<sup>7</sup>Hz. All other configurations were fixed as in the previous case.

### Summary and Final Conclusions
The final optimizations added to Mantid have facilitated live streaming which will meet expected requirements for coping with projected instrument flux. The scalability of the solution also demonstrates that as processor architectures improve and scale in future, iterations, we will be in a good position to manage increasing flux. There are currently no recommended actions required for parallelisation/distribution of Mantid for live streaming.

#### SANS Workflow Recommendation
The profiling tools developed by Neil Vaytet (ESS) highlighted that the SANS workflow does not seem to make effective use of multi-threaded architectures (figure below).  

![Sans Reduction Profile](sansreductionprofile.png)

An investigation into parallelising Mantid algorithms used in the SANS workflow may allow us to squeeze some extra performance out of the live reduction pipeline. However, the performance rate is currently limited by the ingest into Mantid.


 
