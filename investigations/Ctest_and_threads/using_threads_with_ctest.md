# What is the right combination of Nthreads and -j with ctest?

## Introduction

While investigating tests that were failing with a `Timeout` error on the build servers, I found
that running builds with `ctest -j 8` was probably over-subscribing the servers as no limit was
being set on the number of OpenMP threads each instance of `ctest` was allowed to use. This has
potentially important consequences for the total time the builds take to complete and could be
improved.

## Results

I ran the `AllTests` suite, including `PerformanceTests`, but excluding the GUI `MantidPlot`
tests, varying the maximum number of threads `MultiThreaded.MaxCores` in
`~/.mantid/Mantid.user.properties`. Figure 1 below shows the results.

**Note:** `MultiThreaded.MaxCores` had to also be modified in
`Framework/Kernel/src/ConfigService.cpp` as the one in `~/.mantid` gets over-written with a
template by the `SystemTests`.

Machine used: HP Z820 workstation with 12 cores: 2x Intel(R) Xeon(R) CPU E5-2630 v2 @ 2.60GHz. 
Hyper-threading is enabled, yielding 24 available threads in total.

![Figure 1](https://raw.githubusercontent.com/DMSC-Instrument-Data/documents/master/investigations/Ctest_and_threads/ctest_threads_vs_j.png)

**Figure 1:** The x axis shows the max number of threads allowed in
`~/.mantid/Mantid.user.properties`. The y axis is the total runtime for `ctest -E MantidPlot`.

The first thing is that if you take the orange curve for `-j 4` for example, the total runtime for
the unit tests is independent of the number of threads used.

What makes a build complete faster is making use of `-j`. However, by default, there is no limit on
the number of threads in `~/.mantid/Mantid.user.properties`. So on a computer that has 12 cores (= 
24 threads if hyper-threading), if you use `-j 12`, you will also be using 24 threads per instance 
of `ctest` = 288 threads all running at the same time.

The coloured markers and their associated colorbar was an attempt at showing by how much the system 
is being overloaded. It is showing the number of threads requested by the ctest
(`j * MultiThreaded.MaxCores` in `Mantid.user.properties`) divided by the total number of threads 
available on the machine (24 on my workstation).

It shows that over-subscribing the system a little does not impact the timings much, but when we
start going above 5 times the total number of available threads (i.e. when the markers turn green),
the timings take a turn for the worse.

Even if the fastest builds are achieved when using only 1 or 2 threads, going to 4 or 6 threads
impacts runtimes in only a very minimal way, and makes sure we are still testing the openmp
sections when running the tests.

Finally, I also tried going a little further in `-j`, and I was able to squeeze a little more 
performance that way (not shown in Figure 1). The fastest runtime I achieved was 237 s by using
`-j 24` and 2 threads. Doing the same with 4-6 threads slowed things down again. A close second,
at 239 s, was `-j 22` and 2 threads.

## Conclusion

### Safe solution

On a build server, find out how many physical cores are there and set `-j` to that number. Then 
have a cap on the number of threads of about `Total_N_threads_available / 4`.

### Maximum performance

One could also go all in with the `-j` option and set that number to `Total_N_threads_available`.
In that case I would choose a small fixed number for `MultiThreaded.MaxCores=2` (or maybe 4), just 
to make sure OpenMP is still being used in the builds. Timings on a different machine (my laptop)
confirm that this is the fastest solution.
