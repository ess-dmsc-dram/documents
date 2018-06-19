# Evaluation of the KafkaStreamer for ESS
## Motivation
The KafkaStreamer has been previously developed to support live streaming of event data from a kafka broker into Mantid. The purpose of this document is to present an evaluation of the this streamer in the context of the ESS. The ESS will make use of a Kafka architecture which produces messages at a rate fixed to the frequency of the neutron source, 14Hz (frames per second). Therefore, any live streaming mechanism in Mantid should be able to support the consumption of kafka messages at or above 14Hz for sensible event detection rates. ESS instruments are expected to produce detection rates in the 10<sup>7</sup>Hz range or ~714286 events per kafka message.

## Live Consumption Tests
The first stage of testing involved the scenario where the instrument data is inspected in the absence of any data reduction. A single workstation was used to run a docker image which contained the configuration for a Kafka broker. Data was published to the broker using the `main_nexusPublisher` which can be found [here](https://github.com/ess-dmsc/NeXus-Streamer). The `main_nexusPublisher` accepts event nexus files and publishes events to a kafka stream. This application also supports producing random events at user-defined rates, based on an input nexus file, which facilitated stress testing Mantid for our purposes. All instructions for the setup of the broker and using the `main_nexusPulisher` can be found in the link above.

Three instruments with varying numbers of detectors were chosen for this investigation. Due, to the limitations of the current implementation of the `main_nexusPublisher` we were restricted to using ISIS nexus files. The selected instruments were:

Instrument|Number of Detectors
---|---
SANS2D|122'888
MERLIN|286'729
WISH (10 panel)|778'245

### Results
![Trend1](figure_1.png)

The figure above shows the trend in event rate versus message consumption rate. The `MonitorLiveData` timeout was set to one second. SANS2D was able to maintain a 23Hz consumption rate at 10<sup>7</sup> event rate with a 1 second refresh rate of the live listener. Enabling the instrument view for inspection did not seem to affect the message consumption rate for any of the instruments. Both MERLIN and WISH were unable to support rates of 10<sup>7</sup> with consumption rates of 7Hz and 3hz respectively. At 10<sup>6</sup>, MERLIN consumed Kafka messages at a rate of 93Hz and WISH at 38Hz.

![Trend2](figure_2.png)

The above figure shows that increasing the `MonitorLiveData` timeout can result in a slight improvement in performance. This is however very limited and efforts to improve the listener design for performance should not depend too heavily on this.

## Effects of Live Processing

### Rebin
Running the `Rebin` algorithm on a chunk-by-chunk basis seems to have no deleterious effects on rates. 