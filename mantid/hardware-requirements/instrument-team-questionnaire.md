# Data reduction hardware requirements --- Questionnaire for guiding discussions with instrument teams

## Introduction

- DMSC needs to buy hardware, amongst other things for data reduction.
  It is important for you as an instrument scientist that we get a good estimate on the requirements.
  - Availability needs to be ensured.
  - There will be no computers at the beamline.
  - Data reduction will often not be doable on a laptop due to data volume.

## Required information

1. What is a similar reduction workflow (in Mantid) at an operating facility (should be ISIS or SNS) that we can use for benchmarking?
   - Could be several if the instrument has different operating modes.
   - Are there any major differences to this workflow for your instrument, if so what are they?

2. What are the build-out phases of the instrument?
   For each phase, we need to know in particular:
   - Detector pixel counts and coverage.
   - Estimated typical event rates, given depending on:
     - Accelerator power.
     - Initial vs. "final" moderator.
     - Detector coverage.
     - Implicitly, the sample size?
       We are assuming that in the early days with low accelator power the experiments would not be run with the smallest samples the instrument was designed for.
      That is, we *cannot* just scale down figures given, e.g., in instrument proposals with the accelerator power since that would give too low numbers?
   - What is the typical length of a single run (single measurement for a given sample)?
     Could be given as wall clock time or as event count.

3. Can you think of anything else that is "unusual" at your instrument?
   - Example: Are there large event-mode monitors?
     This is known to have caused issues at SNS.

4. What number of users (including instrument scientists) do you expect to work and login per day to use the remote-desktop service?

5. Is it essential that remote-desktop sessions can be suspended and resumed?
   - Yes (workflow similar to closing and reopening your laptop lid):
     - For how long after the experiment would this be required?
       [ ] 1 day
       [ ] 1 week
       [ ] other
   - No (workflow similar to shutting down and rebooting your laptop):
     - What is an acceptable boot time?
       [ ] < 10 s
       [ ] < 1 min
       [ ] < 5 min
