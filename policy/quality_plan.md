## Quality Assurance Policy

The project Data Reduction coding standards will follow those of Mantid
<http://www.mantidproject.org/Coding_Standards>. The exact framework for
Instrument Control is yet to be determined in detail. However, the same
policy will follow whereby that projects coding standards will take
precedence.

Code should be open source and freely distributed. To ensure longevity,
lower maintenance costs, and ensure long-term QA support, any development
work against existing projects should be delivered and merged back to
those projects.

## 1 Requirements Review Policy

Requirements will be reviewed by the Group Lead for Instrument Data. Expert knowledge and a
range of stakeholders should be given the opportunity to contribute to
requirements gathering and analysis.

## 2 Design

Major design choices will be reviewed and approved by developers from
outside the group or facility from which they originated. Designs should
be shared via a design document. Design documents should be version
controlled and where possible co-located with the code.

## 3 User Interface Policy

This project will use User Centred Design techniques throughout.

## 4 Functional Testing Policy

Each module will be tested internally within the team by a member of the
team that did not write that module.

## 5 Performance Testing Policy

The system will be deployed on representative hardware under simulated
realistic load prior to being rolled out. Benchmarking of performance
should be used to cover performance critical regions.

## 6 Prototypes

Prototypes may be generated outside of the above restrictions. If a
prototype is not disposable, it must be made to fit the aforementioned
quality requirements prior to production use. Prototypes should be version
controlled in git, publically available, and provide good documentation
for setup and execution.

## 7 Philosophy

Final deliverable dates are on very large timescales as far as usual software projects are concerned. Given the long timeline for ESS transition into operation, we must ensure that any software development is of a sustainable and maintainable quality that allows for a long software lifetime. Quality and stability should not be sacrificed for short-term solutions or for hasty additions of new features. All DMSC/Instrument-Data group projects will be run with the philosophy of building software capital for the DMSC.
