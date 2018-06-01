## Induction ~1 week

* **Health and Safety Display Screen Equipment (Online Training)** - follow [this](https://staff.she.stfc.ac.uk/Pages/Staff/On-line-training.aspx) link
* Set up PC
* Read Mantid Induction training Course and Mantid in python course
  * [Mantid Introductory Course](http://www.mantidproject.org/Mantid_Basic_Course)
  * [Introduction to Python](http://www.mantidproject.org/Introduction_To_Python)
  * [Python in Mantid](http://www.mantidproject.org/Python_In_Mantid) and [Extending Mantid with Python](http://www.mantidproject.org/Extending_Mantid_With_Python)
* Read git workflow and other key developer documentation
  * [Intro to C++](http://www.mantidproject.org/New_Starter_C++_introduction)
  * [C++ Coding Standards](http://developer.mantidproject.org/Standards/CPPStandards.html)
  * [Mantid Coding Standards](http://developer.mantidproject.org/Standards/MantidStandards.html)
  * [Mantid git workflow](http://developer.mantidproject.org/GitWorkflow.html)
* Set up PC for Mantid related development
  * [Building Mantid](http://developer.mantidproject.org/GettingStarted.html)
* Useful tools
  * [online c++ interpreter](https://repl.it/) for quick prototyping.
  * [MSVC 2017 Community Edition IDE](https://www.visualstudio.com/downloads/)
  
## Improving code quality
* pick up maintenance issues from backlog. Not necessarily in this order:
  * https://github.com/mantidproject/mantid/issues/15284
  * https://github.com/mantidproject/mantid/issues/17927
  * https://github.com/mantidproject/mantid/issues/12994
  * https://github.com/mantidproject/mantid/issues/15267
  * https://github.com/mantidproject/mantid/issues/17372
  * https://github.com/mantidproject/mantid/issues/18937
* Assist with new workbench rollout

## Exposing Info Layers to Python
* Read working with [Instrument Access Layers](http://docs.mantidproject.org/nightly/concepts/InstrumentAccessLayers.html)
* [boost::python](https://www.boost.org/doc/libs/1_64_0/libs/python/doc/html/tutorial/index.html) for exposing C++ classes to python as modules.
  *  A few [examples](https://github.com/mantidproject/mantid/tree/master/Framework/PythonInterface/mantid/api/src/Exports) in the codebase.

## Long-term Project (Ideas)

* Port InstrumentRayTracer to work directly with "Instrument2.0", `ComponentInfo` etc. i.e have no dependance on `Instrument` type.
* Removing MRU list from EventList
* Writing nexus geometry files
* Assisting with requirements gathering for Hardware specifications?
