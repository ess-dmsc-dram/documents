## Motivation for choosing Mantid for data reduction at ESS

#### Infrastructure

1. Multiplatform (Linux, Windows, OSX)
1. Website maintenance and hosting
1. Getting started with Mantid development is well documented on a website (building, running tests, ...). Dependency packages for developers
1. Big number of build servers hosted by partner facilities
1. Well set-up continuous integration environment
1. Several layers of automated testing for large parts of the code base (unit tests, system tests, "documentation" tests)
1. Code-reviews

The amount of effort going into setup and running this infrastructure should not be underestimated.
Setting up such a system on our own would eat up a major part of our effort.

#### Mantid

1. International neutron user community and neutron scientist are familiar with Mantid
1. Mantid may be lacking (for ESS) in terms of performance, functionality, and maintainability, but the partner facilities mostly agree and are open to change
1. Partner facilities may (currently) not have sufficient resources to support improvements in performance, functionality, and maintainability, but their long term goals are aligned with many of the ESS goals, so there is potential for increasing their involvement. Note that this cannot happen on the developer level since their hands are tied and they are usually 100% occupied by supporting current instruments and experiments at their facilities.
1. Works now
1. A lot of the functionality we require is there already
1. Python scripting for C++ backend combines easy scripting with performance
1. ESS will not have working instruments for years to come. It would be extremely difficult to develop the right (working) software against a specification. Development effort we put into Mantid can be tested, used, and continuously validated for many years at other facilities *now*. This is a really major risk mitigation for ESS.
