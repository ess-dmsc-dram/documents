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
 - Deployment strategy/implementation (mainly with DST group)
    * compatibility of server components (daemon, cache, poller, ...) with Centos 7.1
    * automated server deployment & configuration (environment variables to select correct instrument
      on specific machine etc)
    * compatibility of client components (mainly GUI) with Centos 7.1 and Mac OS X
    * driven forward as part of LDPC (live data prototype collaboration)

 - Control & query the DM group's aggregator (what gets aggregated), file writing, ...
    * interface to detector data for all ESS instruments
    * pending exact protocol/mechanism, prototyping at V20
    * distribution of responsibility between NICOS/aggregator (filenames, ...)
    * potentially aggregate quantities derived by NICOS (wavelenghts, ...)
    * also driven forward in LDPC

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
 - Setup for simple instrument (my suggestion is MAGIC - relatively little hardware)
 - Create simulated hardware (either NICOS or further down)
 - Leave out data acquisition until interfaces are clear (see above)
 - Work with instrument team on setup, workflows, potentially UI
 - will help uncover open questions
