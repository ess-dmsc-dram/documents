## Background

The remit of the DMSC Instrument Data Group is to ready the Mantid Framework for ESS operations. To be applicable in 2023, The Mantid framework must keep pace with advances in the instrumentation. The framework will experience significant increases both data rates and the complexity of experiments over the coming years at all collaborating facilities. These problems have been identified and discussed in January 2016 at the [PMB](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes-2016-01-22.docx) and used to generate the Mantid 5-year plan.

Over the last 6-months, the ESS Instrument Data Group have been working on a number of new concepts of key fixes to the framework based on the [ESS performance report](https://github.com/mantidproject/documents/blob/master/Performance/performance_analysis_of_mantid_for_ess.pdf). These include but are not limited to:

* `HistogramData` - Consolidating and propagating the meaning of collected data as described [here](http://docs.mantidproject.org/nightly/concepts/HistogramData.html). Which has started to lead to some significant memory and speed gains in the framework. **Released as part of 3.8 Mantid**.  See [statistics](https://github.com/mantidproject/mantid/blob/master/docs/source/release/v3.8.0/framework.rst)
* `SpectrumInfo/GeometryInfo` - A better UI and caching layer for `Algorithm` authors, which provides improvements in both clarity and raw access performance. **Released as part of 3.8 Mantid**
* `Component` creation optimisation. Giving faster Instrument access by 30%. **Released as part of 3.7 Mantid**
* `IndexInfo` consolidation of indexing operations. Critical to scalable distributed data reduction. **Released as part of 3.7 Mantid**
* `Instrument 2.0` - An ongoing [super-prototype](https://github.com/DMSC-Instrument-Data/instrument-prototype) development stream. which offers very much faster read performance, lower memory overheads, and greater potential to support complex experiments than Mantid currently has.


## Problem

Our experience (with evidence above) of this large-scale refactoring over the last 6-12 months is that rollout of changes across the framework is extremely time consuming. A major bottleneck is the approximate 800 Algorithms which need to be individually treated and updated following these changes. To compound this, the DMSC Instrument Data group is facing financial cuts that reduce the staffing and the capacity to make these changes will be reduced.

**We need to reduce the large inertia to applying core changes in Mantid as a result of a very large codebase.** This will otherwise swallow the DMSC mantid effort.


## Solution Constraints

* We are looking at a permanent way to significantly reduce overheads for changes of this type. Temporary allocation of resources does not provide an adequate solution.
* The DMSC has successfully been working alongside ISIS, ILL and SNS partners on a shared codebase with a common deployment schedule and strategy. The level of cooperation between facilities has been exemplary. A wholesale forking the Mantid codebase would offer a quick fix, but would be very unwise in nearly all other respects. This approach should be ruled out.


## Proposed Strategies

### Remove Dead Algorithms

Usage tracking has been added to algorithms about half a year ago (end of Mantid version 3.5).
According to [statistics](algorithm-usage-summary.txt), in the order of 10% of all algorithms can be considered dead (not all of the apparent zero-use algorithms are really unused due to incomplete statistics, but in turn some of the algorithms used only a handful of times are actually unused, if we take into account misclicks and inadvertently activated tracking when running tests).
- Removing those algorithms could potentially reduce the rollout effort by a similar amount.
- On its own, a 10% reduction of rollout effort is not sufficient.
- Removing algorithms is met with resistance from other facilities and would not take immediate effect:
  Following a two-step approach of 1.) deprecation and 2.) removal this would take two releases, that is eight month from the time of writing (beginning of a release), which further limits the benefits.

### Long-term support of legacy interfaces

If the old interfaces were kept alive, rollout of new interfaces and functionality to the full framework would not be a necessity.
New functionality could be implemented in new modules, which in turn could be used in a small set of core algorithms that we choose to support.

There is a series of problems:

- A considerable number of our changes result in a complete rework of the underlying data structures.
  [Instrument-2.0](https://github.com/DMSC-Instrument-Data/instrument-prototype) is a key example for this and similar issues might arise with the workspace concept.
  Since the current implementation of, e.g., the instrument, does not provide a good abstraction it is not possible to change the underlying data structures without breaking changes in the interface.
  It is thus difficult to provide a legacy interface and doing so might require some additional development effort.
- Guarantees and invariants of new functionality in a new module will be broken if access via a legacy interface is possible.
- Currently, there are one or two ways to do the same thing, e.g., determining if a spectrum is a monitor, if we add a new interface without removing the old one there will be three.
- Maintaining a legacy interface will impose some limitations on the new design.

### Sci-py approach
The SNS 5-year plan as described to the [PMB](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes-2016-01-22.docx) states: **"the long-term plan for Mantid includes evolving Mantid to scipy-styled package"**.

Depending on the interpretation, this can be done by providing a series of small, well-contained, low- to medium-level libraries.
High-level functionality would be part of user scripts and not part of the Mantid core framework.

The key issue here is how this can be reconciled with (the development of) the current Mantid framework.
New modules can be built as part of the Mantid framework, but we would *not* do a rollout to existing algorithms.
More concretely:

- Instrument-2.0 gets implemented as a stand-alone Mantid library, i.e., without dependencies on the other Mantid modules, in parallel to the existing instrument code.
- We do *not* use it anywhere but simply ignore code in existing algorithms, apart from using them as a guideline for required functionality.
- Similarly, we would continue adding more and more small libraries.
- Workspaces are a key concept of Mantid, but in their current form they also represent one of the key issues of the framework.
  New libraries would probably be severely hindered by making them compatible with the current workspace infrastructure.
  Instead the libraries should work at a lower level, and eventually a replacement for workspaces could be provided.

The (current) big unknown with this approach is how we can tell if we are getting anywhere and how new functionality can eventually be combined with existing functionality.
It may turn out that is is never possible, i.e., existing algorithms might be dropped completely and be replaced by scripts that use the new Sci-py styled libraries at some point in the future.
But the implication is that we need to be certain that we will be capable of providing 100% of the required functionality using only the Sci-py styled libraries.

### Dediciated Cross-facility Core Effort

At operating facilities, the emphasis for many years has been on framework use rather than framework development. The delivery model in the Mantid program has been very successful in engaging users and ensuring that day-to-day issues are prioritised and fixed. However, this environment does not always foster the best practices when it comes to making core fixes, which may be seen as wasteful or uncessary to those who comission the development. One approach would be to re-address the balance of framework fix to framework utilisation in each development cycle. One way to ensure that developers have an increased amount of dedicated time for framework fixes may be to have members of the development team at each collaborating facility permanently responsible for the state of the Mantid framework, and not for the deliverables in a particular technique area.

* This would require buy-in from all facilities.
* The effort will help ensure the longevity of Mantid. However, it may look as though no 'useful' technique specific work is being done. * There is a sizeable associated cost.
* In the short term there will be a reduction in the amount of work that can be done in terms of feature additions. This has to be understood.

