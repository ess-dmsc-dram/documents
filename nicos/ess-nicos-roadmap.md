ESS contributions to NICOS
==========================

This is a work in progress document for a meeting with the NICOS developer team in late May/early June.

Organisation
------------
 - this has large overlap with document from meeting last year :) Maybe we should "write this down somewhere" this time
 - does everybody have all the accounts they need git/gerrit/slack...? ("get started" page for new developers or similar?)
 - DMSC contribution to infrastructure? build servers? ESS artifactory interesting for hosting packages?
 - issues will be tracked in redmine - ESS tag/separate area?
 - participation in meetings/interaction
    * ESS ECP workshops every 6 month - interesting?
    * weekly/monthly? developer meetings - video conferencing?
    * frequency for face-to-face meetings? organize working in same place (code camp or similar) if time allows?
 - inclusion of ESS staff in general maintenance tasks (contributing effort for non ESS-related issues)
 - ensure knowledge of ESS instrument control "lives in NICOS" (documentation etc) (important for staff turnover)
    
ESS specific developments
-------------------------
 - Similar to custom/frm2
 - Should contain ESS specific generic setups/device types
    * Example: EPICS motor record is totally generic, ESS motors will have some extensions (additional PVs)
    * Pending final (single disk) chopper EPICS interface, integrate.
 - Continue work on higher level multi-disk chopper systems
    * Should be composed of single chopper disks
    * Users should be able to set wavelength (-band) and resolution in some cases
    * Wavelength frame multiplication (WFM)
    * Should start simple with two-disk example from the meeting last year, then more complex cases
    * Could think of doing math in separate module for re-use


EPICS
-----
 - improve support for EPICS ChannelAccess devices using pyepics
    * better default implementation of doStatus (using EPICS alarm states)
    * implement callback-based poller that monitors PVs and updates cache
    * improve EpicsMotor and move into "core" system

 - support pvAccess using pvaPy module
    * pending use cases from ICS/DM beyond "plain PVs"
    * should eventually also replace pyepics for ChannelAccess


Integration with other DMSC infrastructure
------------------------------------------
 - Deployment strategy/implementation (mainly with DST group, possibly ICS)
    * compatibility of server components (daemon, cache, poller, ...) with Centos 7.1 (rpm packages, analoguous to deb)
    * automated server deployment & configuration (environment variables to select correct instrument
      on specific machine etc)
    * compatibility of client components (mainly GUI) with Centos 7.1 and Mac OS X (likely used by many ESS beamline scientists)
    * installation of client and potentially server in EEE development environment (also Centos 7.1)
    * driven forward as part of LDPC (live data prototype collaboration)

 - Control & query the DM group's aggregator (what gets aggregated), file writing, ...
    * interface to detector data for all ESS instruments
    * pending exact protocol/mechanism, prototyping at V20
    * distribution of responsibility between NICOS/aggregator (filenames, ...)
    * potentially aggregate quantities derived by NICOS (wavelenghts, ...)
    * also driven forward in LDPC
    
 - Logging
    * It should be possible to log directly into graylog, preferably using Jonas' python package
    * As an intermediate solution there could be a logstash (or similar) instance to monitor logfiles

 - Integration with Mantid
    * InstrumentView-widget as first step for visualisation
    * towards data processing scripts (either on local machine or on remote - depends on data streaming/file writing?)


Integration with ICS infrastructure
-----------------------------------
 - Some unknowns (IOC status/control, ChannelFinder yes or no, further PV abstractions?)
 - relevance of EPICS time stamps for NICOS (potentially required in cache, etc)
 - "Engineering GUIs" where available - CSS launcher for certain devices depending on user rights
 - For now: Pure EPICS client with no further knowledge of architecture


Instrument integration
----------------------
 - tool for driving forward all of the above
 - Setup for simple instrument
    * One possibility is MAGIC - relatively little hardware
    * Another possibility could be using the AMOR simulation provided by PSI, also little hardware
 - Create simulated hardware if necessary (either NICOS or further down)
 - Leave out data acquisition until interfaces are clear (see above)
 - Work with instrument team on setup, workflows, potentially UI
 - will help uncover open questions
