# Useful information for new Mantid developers at DMSC

## Developers

- Lamar Moore (ISIS in-kind, primarily Windows user)
- Owen Arnold (ISIS in-kind, primarily OSX user)
- Simon Heybrock (ESS/DMSC, primarily Linux user)

Our Kanban board can be found on [Confluence](https://jira.esss.lu.se/secure/RapidBoard.jspa?rapidView=355&projectKey=DR).

## General

- The Mantid collaboration uses Slack for team communication, join `mantid.slack.com`.
  - In addition to the default channels, `#tech-qa` is useful for technical questions.
  
- There are several Mantid Training courses that we offer to users covering the UI, scripting and extending Mantid. For a new developer to the team [Mantid Basic Course](http://www.mantidproject.org/Mantid_Basic_Course) probably offers the best holistic introduction to Mantid.

- Detailed information on developing for Mantid can be found on its [homepage](http://www.mantidproject.org/Main_Page), in particular the [development section](http://developer.mantidproject.org/). You should in particular read [Git Workflow](http://developer.mantidproject.org/GitWorkflow.html) as it describes the complete process or adding features to Mantid.

- DMSC is running two Ubuntu build servers for the collaboration, one of the is dedicated for performance tests.
  The servers running in the DST VM environment.
  Except for configuration changes or updating software there is no need to interact with the build servers.
  We build on our workstations and the build servers are used for the pool used for the pull requests on github.

- The overall project structure of Mantid is flat and primarily based on facility-specific groups/needs.
  An attempt to change this is described in the [Core Team proposal](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Mantid%20core%20team%20proposal.docx), which was an initiative by ESS in 2017.
  It has been approved but has not been resourced appropriately yet.

## Repositories

- [Mantid](https://github.com/mantidproject/mantid)
- [Mantid documents repository](https://github.com/mantidproject/documents), containing meeting notes, design documents, presentations, ...
- [DMSC Instrument Data Group](https://github.com/DMSC-Instrument-Data) contains several repositories from the Instrument Data group.
  This group has since been split in two, experiment control is now part of Data Management and data reduction (Mantid) is now part of Data Analysis but the joint github organization remains.
  Relevant repositories for Mantid developers are:
  - [Documents](https://github.com/DMSC-Instrument-Data/documents), containing meeting notes and other documentation.
  - Several prototypes that are no longer in active use but may be of interest: [Live-data prototype](https://github.com/DMSC-Instrument-Data/live-data-prototype), [Instrument prototype](https://github.com/DMSC-Instrument-Data/instrument-prototype), [NeXus event loader prototype](https://github.com/DMSC-Instrument-Data/nexus-sandbox), [boost::mpi tests](https://github.com/DMSC-Instrument-Data/boost-mpi-sandbox).
  - [Helper tool for parsing algorithm usage statistics of Mantid](https://github.com/DMSC-Instrument-Data/mantid-algorithm-usage)
- [Workspace sandbox](https://github.com/mantidproject/workspace-sandbox) contains notes and prototypes of "core team" work aimed at replacing/superseding the current workspace types in Mantid.

## Resources

- [Accelerated C++](https://www.amazon.co.uk/Accelerated-Practical-Programming-Example-Depth/dp/020170353X) for C++ refresher. Lacking more modern aspects of the language but a good foothold.

- [C++ Common Knowldge](https://www.amazon.co.uk/Common-Knowledge-Essential-Intermediate-Programming/dp/0321321928) is a very easy read and has very good explanations for traps and useful language features. Focuses on C++03, but much of it still relevant.

- [What every programmer should know about memory](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwjn2cX1jcPaAhUQKlAKHSIpAGUQFggyMAE&url=https%3A%2F%2Fpeople.freebsd.org%2F~lstewart%2Farticles%2Fcpumemory.pdf&usg=AOvVaw3VY2lnCBaI-B57Dric65cb) is the bible for basic understanding of CPUs and making efficient use of their capabilities.

- *Effective Modern C++* by Scott Meyers is an excellent resource for getting up to date with C++11 and C++14.
  Mantid is currently using C++11.

- *Clean Code* by Robert Martin is a great book that will make you write better code.
  I found that the later parts with detailed case studies are not so useful.
  Also, in some cases things seem to be pushed slightly too far, so not everything should be followed blindly to the extreme.
  Nevertheless this is absolutely recommended.
  
- Ask on slack, lots of developers very happy to help out and discuss things

## Travel

### Harwell (ISIS)

- Getting from London Heathrow to ISIS (Harwell Campus):
  1. Take the Rail-Air from Heathrow to Reading (usually good WiFi on the bus).
     If at terminal 5 you can buy tickets at the National Express counter (turn left after exiting the baggage claim area, counter is on your left).
  2. Short train ride from Reading to Didcot Parkway.
  3. Taxi to Harwell Campus (ISIS) reception.
- Accomodation 
  Onsite there is [Ridgeway House](https://stfc.ukri.org/about-us/where-we-work/rutherford-appleton-laboratory/ridgeway-house/) this is the most convenient for access to the lab. There is however very little within walking distance of the hotel, so many visitors stay in one of the surrounding villages or towns. Best to ask advice from the ISIS team prior to booking.
 
