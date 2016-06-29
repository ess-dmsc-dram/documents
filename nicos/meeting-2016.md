# Proposed agenda for meeting with NICOS team

## Scope

The following scopes should be covered at the meeting
  - Strategy for DMSC contributions to NICOS
  - Longer term development strategy (5 years)
  - Discussion of organisatory details for contribution
  - Development tutorial and/or code/design walkthrough

## Participants

The following people from the respective organizations are going to participate in the meeting:

  - FRM2: Jens Krüger, ...
  - DMSC: Jon Taylor, Simon Heybrock, Michael Wedel (invite David Brodrick)
  - STFC ISIS: Michael Hart, Owen Arnold
  
## Location

Where should we have the meeting? Jens suggested Garching or Copenhagen.

  - **Michael W.**: I suggest **Garching**, because otherwise many more people might want to join and there is a risk
    that the meeting then turns into a series of presentations about departments, control system architectures,
    timing systems and much more. All this is interesting but I think that belongs in a different meeting.

## Dates
Possible dates for the workshop from the respective organizations:
  - FRM2: Weeks 33 and 34 (August 16th - August 26th)
  - DMSC: August 22nd - August 25th
  - STFC ISIS: August 22nd - August 26th
  
The duration of the workshop should be two (full, if possible) days.
  
## Topics/Questions

### Short (!!!!) introductions
  - What have we done with NICOS so far
  - What would we like to do next
  - 10 minutes DMSC, 10 minutes STFC ISIS (max.)

### Development model/participation
  - Longer term development strategy (5 years) from the FRM2 perspective
  - Requirements for participation in development of NICOS components
  - Obtaining accounts for infrastructure (build servers, ticket system, status of developers)
  - Running build jobs locally (pylint, ...)
  - Forking for experiments?
  - Using infrastructure (build servers, etc.)
  - Should DMSC provide resources that can be integrated (Jenkins slaves...)
  - Participation in (video?)-meetings (weekly? monthly?)
  - Face-to-face meetings (yearly? twice per year?)
  - Who are the experts on which parts of the system? 
  - What's channels of communication are best?
  
### Detailed design/code walkthrough
  - Understanding details of NICOS' design better (ethos, creation & initialization of objects, scope of objects across processes...)
  - Which services communicate over which channels, short introduction to protocols
  - The scope and role of each service. How are they directed? What sequences do we need to be aware of?
  - Adding new device types (understanding the "right level of abstraction", where to add)
  - Guidelines for requiring packages (e.g. pyepics, pvaPy from our side later on)
  - Where to add tests, documentation
  - A small tutorial adding a new device might be useful (all steps from deciding where to put code to code review)
  - How to add 'views'/'synoptics' like the TAS test instrument over new setups.
  - Automated testing/Build server support
