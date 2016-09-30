## Background

The remit of the DMSC Instrument Data Group is to ready the Mantid Framework for ESS operations. To be applicable in 2023, The Mantid framework must keep pace with advances in the instrumentation. The framework will experience significant increases both data rates and the complexity of experiments over the coming years at all collaborating facilities. These problems have been identified and discussed in January 2016 at the [PMB](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes-2016-01-22.docx) and used to generate the Mantid 5-year plan.

Over the last 6-months, the ESS Instrument Data Group have been working on a number of new concepts of key fixes to the framework based on the [ESS performance report](https://github.com/mantidproject/documents/blob/master/Performance/performance_analysis_of_mantid_for_ess.pdf). These include but are not limited to:

* `HistogramData` - Consolidating and propagating the meaning of collected data as described [here](http://docs.mantidproject.org/nightly/concepts/HistogramData.html). Which has started to lead to some significant memory and speed gains in the framework. **Released as part of 3.8 Mantid**.  See [statistics](https://github.com/mantidproject/mantid/blob/master/docs/source/release/v3.8.0/framework.rst)
* `SpectrumInfo/GeometryInfo` - A better UI and caching layer for `Algorithm` authors, which provides improvements in both clarity and raw access performance. **Released as part of 3.8 Mantid**
* `Component` creation optimisation. Giving faster Instrument access by 30%. **Released as part of 3.7 Mantid**
* `IndexInfo` consolidation of indexing operations. Critical to scalable distributed data reduction. **Released as part of 3.7 Mantid**
* `Instrument 2.0` - An ongoing super-prototype development stream. which offers very much faster read performance, lower memory overheads, and greater potential to support complex experiments than Mantid currently has.

## Problem

Our experience of this large-scale refactoring over the last 6-12 months is that rollout of changes across the framework is extremely time consuming. A major bottleneck is the approximate 800 Algorithms which need to be individually treated and updated following these changes. To compound this, the DMSC Instrument Data group is facing financial cuts that reduce the staffing and the capacity to make these changes will be reduced.

**We need to reduce the large inertia to applying core changes in Mantid as a result of a very large codebase.** This will otherwise swallow the DMSC mantid effort.


## Solution Constraints

* We are looking at a permanent way to significantly reduce overheads for changes of this type. Temporary allocation of resources does not provide an adequate solution.
* The DMSC has successfully been working alongside ISIS, ILL and SNS partners on a shared codebase with a common deployment schedule and strategy. The level of cooperation between facilities has been exemplary. A wholesale forking the Mantid codebase would offer a quick fix, but would be very unwise in nearly all other respects. This approach should be ruled out.

## Proposed Strategies

### Remove Dead Algorithms
TODO

### Sci-py approach
The SNS 5-year plan as described to the [PMB](https://github.com/mantidproject/documents/blob/master/Project-Management/PMB/Minutes/PMBMinutes-2016-01-22.docx) states: **"the long-term plan for Mantid includes evolving Mantid to scipy-styled package"**. TODO ecosystem approach ..


