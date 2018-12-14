Live event-streaming performance
----

### Wednesday
- 12:30 - 13:15 - Lamar and Dan arrive (Lunch)
- 13:15 - 14:15 - Revisit requirements (pixel counts, timeline)
- 14:15 - 15:30 - Discuss changes implemented by Lamar after benchmarking listener performance.
- 15:30 - 16:30 - Discuss/Discover potential performance bottlenecks

### Thursday 
- 9:00 - 12:00 - What do we actually need (Capture the requirements for the listener)?
  - For example: If it is just for the instrument view, we do not actually require a event list for every pixel --- a single intensity value and a way to obtain the histogram would be sufficient.
- 12:00 - 13:00 - Lunch (Lamar will possibly meet with Jon Taylor at this time).
- 13:00 - 15:00 - Discuss different approaches to resolving bottlenecks (may or may not require MPI)
  - What other solutions are there, apart from MPI.
- 15:00 - 16:30 - If enough progress is made, start sketching prototype.

### Friday
- 9:00 - 11:00 - Final discussions/prototyping
- 11:00 - 12:00 - Discuss 2019 High-level milestones.
- 12:00 - Lamar depart..

## Results

### Live streaming performance

- Pixel counts and event rates at medium-term accellerator power (up to 2 MW or more) are such that optimizing the current stream listerer seems like an achievable solution.
- Avoid distributed MPI implementation for the time being, due to much higher complexity, cost, and unclear benefit given the event rate time line.
- Most promising optimization outlined by the benchmark below:
  Currently the listern insert events of every chunk directly into an `EventWorkspace`, instead of waiting for the time out (which can be many seconds, i.e., hundreds of pulses).
  If we accumulate events from multiple pulses we can sort the events and insert in bigger chunks, i.e., we have better locality of memory access.

```cpp
#include <benchmark/benchmark.h>

#include <numeric>
#include <random>
#include <vector>

#include <tbb/parallel_sort.h>

static void BM_EventInsertion_direct(benchmark::State &state) {
  size_t nSpec = state.range(0);
  size_t nEvent = state.range(1);

  std::random_device rd;
  std::mt19937 mt(rd());
  std::uniform_int_distribution<int> dist(0, nSpec - 1);

  std::vector<std::tuple<int64_t, double, int64_t>> events;
  events.reserve(nEvent);
  for (size_t i = 0; i < nEvent; ++i) {
    events.emplace_back(dist(mt), 0.0, 0);
  }

  for (auto _ : state) {
    std::vector<std::vector<std::tuple<double, int64_t>>> eventLists(nSpec);
    for (const auto &event : events) {
      eventLists[std::get<0>(event)].emplace_back(std::get<1>(event),
                                                  std::get<2>(event));
    }
  }
  state.SetItemsProcessed(state.iterations() * nEvent);
}
BENCHMARK(BM_EventInsertion_direct)
    ->RangeMultiplier(4)
    ->Ranges({{100000, 10000000}, {2 << 16, 2 << 23}});

static void BM_EventInsertion_sorting(benchmark::State &state) {
  size_t nSpec = state.range(0);
  size_t nEvent = state.range(1);

  std::random_device rd;
  std::mt19937 mt(rd());
  std::uniform_int_distribution<int> dist(0, nSpec - 1);

  std::vector<std::tuple<int64_t, double, int64_t>> events;
  events.reserve(nEvent);
  for (size_t i = 0; i < nEvent; ++i) {
    events.emplace_back(dist(mt), 0.0, 0);
  }

  for (auto _ : state) {
    std::vector<std::vector<std::tuple<double, int64_t>>> eventLists(nSpec);
    std::sort(events.begin(), events.end(), [](const auto &a, const auto &b) {
      return std::get<0>(a) < std::get<0>(b);
    });
  }
  state.SetItemsProcessed(state.iterations() * nEvent);
}
BENCHMARK(BM_EventInsertion_sorting)
    ->RangeMultiplier(4)
    ->Ranges({{100000, 10000000}, {2 << 16, 2 << 23}});

static void BM_EventInsertion_sorted(benchmark::State &state) {
  size_t nSpec = state.range(0);
  size_t nEvent = state.range(1);

  std::random_device rd;
  std::mt19937 mt(rd());
  std::uniform_int_distribution<int> dist(0, nSpec - 1);

  std::vector<std::tuple<int64_t, double, int64_t>> events;
  events.reserve(nEvent);
  for (size_t i = 0; i < nEvent; ++i) {
    events.emplace_back(dist(mt), 0.0, 0);
  }

  for (auto _ : state) {
    std::vector<std::vector<std::tuple<double, int64_t>>> eventLists(nSpec);
    tbb::parallel_sort(events.begin(), events.end(),
                       [](const auto &a, const auto &b) {
                         return std::get<0>(a) < std::get<0>(b);
                       });
    for (const auto &event : events) {
      eventLists[std::get<0>(event)].emplace_back(std::get<1>(event),
                                                  std::get<2>(event));
    }
  }
  state.SetItemsProcessed(state.iterations() * nEvent);
}
BENCHMARK(BM_EventInsertion_sorted)
    ->RangeMultiplier(4)
    ->Ranges({{100000, 10000000}, {2 << 16, 2 << 23}});

static void BM_EventInsertion_sorted_threaded_insert(benchmark::State &state) {
  size_t nSpec = state.range(0);
  size_t nEvent = state.range(1);

  std::random_device rd;
  std::mt19937 mt(rd());
  std::uniform_int_distribution<int> peak_dist(0, (nSpec - 1) / 20);
  std::uniform_int_distribution<int> dist(0, nSpec - 1);

  std::vector<std::tuple<int64_t, double, int64_t>> events;
  events.reserve(nEvent);
  for (size_t i = 0; i < nEvent; ++i) {
    if (i < 0.9 * nEvent)
      events.emplace_back(peak_dist(mt), 0.0, 0);
    else
      events.emplace_back(dist(mt), 0.0, 0);
  }

  for (auto _ : state) {
    std::vector<std::vector<std::tuple<double, int64_t>>> eventLists(nSpec);
    tbb::parallel_sort(events.begin(), events.end(),
                       [](const auto &a, const auto &b) {
                         return std::get<0>(a) < std::get<0>(b);
                       });
    constexpr int n_thread = 24;
    std::array<size_t, n_thread + 1> bounds;
    bounds[0] = 0;
    for (int thread = 1; thread < n_thread; ++thread) {
      bounds[thread] = events.size() / n_thread * thread;
      while (bounds[thread] + 1 < events.size() &&
             std::get<0>(events[bounds[thread]]) ==
                 std::get<0>(events[bounds[thread] + 1]))
        ++bounds[thread];
    }
    bounds[n_thread] = events.size();

#pragma omp parallel for num_threads(24)
    for (int thread = 0; thread < n_thread; ++thread) {
      for (size_t i = bounds[thread]; i < bounds[thread + 1]; ++i) {
        const auto &event = events[i];
        eventLists[std::get<0>(event)].emplace_back(std::get<1>(event),
                                                    std::get<2>(event));
      }
    }
    size_t count = 0;
    for (const auto &list : eventLists)
      count += list.size();
    if (count != events.size()) {
      fprintf(stderr, "%lu %lu\n", count, events.size());
      throw std::runtime_error("lost events.");
    }
  }
  state.SetItemsProcessed(state.iterations() * nEvent);
}
BENCHMARK(BM_EventInsertion_sorted_threaded_insert)
    ->RangeMultiplier(4)
    ->Ranges({{100000, 10000000}, {2 << 16, 2 << 23}});

BENCHMARK_MAIN();
```

Result:

```sh
$ ./benchmark/event_insertion_benchmark --benchmark_min_time=4
2018-12-14 08:26:55
Running ./benchmark/event_insertion_benchmark
Run on (24 X 3200 MHz CPU s)
CPU Caches:
  L1 Data 32K (x12)
  L1 Instruction 32K (x12)
  L2 Unified 256K (x12)
  L3 Unified 15360K (x2)
***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
--------------------------------------------------------------------------------------------------
Benchmark                                                           Time           CPU Iterations
--------------------------------------------------------------------------------------------------
BM_EventInsertion_direct/100000/131072                        8408458 ns    8408339 ns        680   14.8662M items/s
BM_EventInsertion_direct/262144/131072                       10619193 ns   10619052 ns        540   11.7713M items/s
BM_EventInsertion_direct/1048576/131072                      24094597 ns   24094373 ns        226   5.18793M items/s
BM_EventInsertion_direct/4194304/131072                      87407299 ns   87405626 ns         66   1.43011M items/s
BM_EventInsertion_direct/10000000/131072                    170387620 ns  170384894 ns         33    751.24k items/s
BM_EventInsertion_direct/100000/262144                       17320323 ns   17320183 ns        314    14.434M items/s
BM_EventInsertion_direct/262144/262144                       25828916 ns   25828706 ns        210   9.67915M items/s
BM_EventInsertion_direct/1048576/262144                      53479541 ns   53479114 ns        103   4.67472M items/s
BM_EventInsertion_direct/4194304/262144                     126133089 ns  126130906 ns         45   1.98207M items/s
BM_EventInsertion_direct/10000000/262144                    208710791 ns  208692357 ns         27   1.19794M items/s
BM_EventInsertion_direct/100000/1048576                      97679484 ns   97678281 ns         56   10.2377M items/s
BM_EventInsertion_direct/262144/1048576                     155323357 ns  155321540 ns         36   6.43826M items/s
BM_EventInsertion_direct/1048576/1048576                    280624884 ns  280622618 ns         20    3.5635M items/s
BM_EventInsertion_direct/4194304/1048576                    405669242 ns  405663239 ns         14    2.4651M items/s
BM_EventInsertion_direct/10000000/1048576                   500775546 ns  500767328 ns         10   1.99694M items/s
BM_EventInsertion_direct/100000/4194304                     392704994 ns  392700523 ns         14   10.1859M items/s
BM_EventInsertion_direct/262144/4194304                     584960305 ns  584949681 ns         10    6.8382M items/s
BM_EventInsertion_direct/1048576/4194304                   1067790324 ns 1067778963 ns          5   3.74609M items/s
BM_EventInsertion_direct/4194304/4194304                   1605269957 ns 1605240378 ns          5   2.49184M items/s
BM_EventInsertion_direct/10000000/4194304                  1807885438 ns 1807847767 ns          4   2.21258M items/s
BM_EventInsertion_direct/100000/16777216                   1666477214 ns 1666450797 ns          3   9.60124M items/s
BM_EventInsertion_direct/262144/16777216                   2306427422 ns 2306389158 ns          2   6.93725M items/s
BM_EventInsertion_direct/1048576/16777216                  3295876208 ns 3295843848 ns          2    4.8546M items/s
BM_EventInsertion_direct/4194304/16777216                  5455321552 ns 5455250623 ns          1   2.93295M items/s
BM_EventInsertion_direct/10000000/16777216                 5279873861 ns 5279805413 ns          1   3.03041M items/s
BM_EventInsertion_sorting/100000/131072                       2457884 ns    2457869 ns       2255   50.8571M items/s
BM_EventInsertion_sorting/262144/131072                       2598437 ns    2598415 ns       2164   48.1063M items/s
BM_EventInsertion_sorting/1048576/131072                      7314099 ns    7314050 ns        754   17.0904M items/s
BM_EventInsertion_sorting/4194304/131072                     60222688 ns   60211238 ns         92   2.07602M items/s
BM_EventInsertion_sorting/10000000/131072                   141763932 ns  141761320 ns         40   902.926k items/s
BM_EventInsertion_sorting/100000/262144                       5142582 ns    5142536 ns       1078   48.6141M items/s
BM_EventInsertion_sorting/262144/262144                       5375013 ns    5374977 ns       1008   46.5118M items/s
BM_EventInsertion_sorting/1048576/262144                      9974556 ns    9974488 ns        557   25.0639M items/s
BM_EventInsertion_sorting/4194304/262144                     62114238 ns   62113214 ns         88   4.02491M items/s
BM_EventInsertion_sorting/10000000/262144                   144278078 ns  144244009 ns         38   1.73317M items/s
BM_EventInsertion_sorting/100000/1048576                     24957991 ns   24957776 ns        218   40.0677M items/s
BM_EventInsertion_sorting/262144/1048576                     26130786 ns   26130559 ns        210   38.2694M items/s
BM_EventInsertion_sorting/1048576/1048576                    28601931 ns   28601741 ns        188   34.9629M items/s
BM_EventInsertion_sorting/4194304/1048576                    81653356 ns   81651931 ns         64   12.2471M items/s
BM_EventInsertion_sorting/10000000/1048576                  166268366 ns  166265530 ns         33   6.01448M items/s
BM_EventInsertion_sorting/100000/4194304                    116489180 ns  116487980 ns         43   34.3383M items/s
BM_EventInsertion_sorting/262144/4194304                    119509924 ns  119508585 ns         41   33.4704M items/s
BM_EventInsertion_sorting/1048576/4194304                   126816688 ns  126814619 ns         37   31.5421M items/s
BM_EventInsertion_sorting/4194304/4194304                   185579774 ns  185576039 ns         29   21.5545M items/s
BM_EventInsertion_sorting/10000000/4194304                  268542423 ns  268537201 ns         20   14.8955M items/s
BM_EventInsertion_sorting/100000/16777216                   598818226 ns  598810052 ns          8   26.7197M items/s
BM_EventInsertion_sorting/262144/16777216                   620786443 ns  620777660 ns          8   25.7741M items/s
BM_EventInsertion_sorting/1048576/16777216                  697045848 ns  696971062 ns          7   22.9565M items/s
BM_EventInsertion_sorting/4194304/16777216                  796846553 ns  796832103 ns          6   20.0795M items/s
BM_EventInsertion_sorting/10000000/16777216                1076670601 ns 1076645752 ns          5    14.861M items/s
BM_EventInsertion_sorted/100000/131072                        6423433 ns    6423363 ns        866   19.4602M items/s
BM_EventInsertion_sorted/262144/131072                        8071764 ns    8071634 ns        688   15.4863M items/s
BM_EventInsertion_sorted/1048576/131072                      14893196 ns   14893036 ns        374   8.39318M items/s
BM_EventInsertion_sorted/4194304/131072                      72189254 ns   72187306 ns         75   1.73161M items/s
BM_EventInsertion_sorted/10000000/131072                    150787033 ns  150782822 ns         37   848.903k items/s
BM_EventInsertion_sorted/100000/262144                        9907378 ns    9907301 ns        564   25.2339M items/s
BM_EventInsertion_sorted/262144/262144                       13889743 ns   13888568 ns        402   18.0004M items/s
BM_EventInsertion_sorted/1048576/262144                      21022839 ns   21021014 ns        266   11.8929M items/s
BM_EventInsertion_sorted/4194304/262144                      81809491 ns   81801531 ns         68   3.05618M items/s
BM_EventInsertion_sorted/10000000/262144                    164513473 ns  164496850 ns         33   1.51979M items/s
BM_EventInsertion_sorted/100000/1048576                      23048104 ns   23046022 ns        241   43.3914M items/s
BM_EventInsertion_sorted/262144/1048576                      40377218 ns   40373741 ns        130   24.7686M items/s
BM_EventInsertion_sorted/1048576/1048576                     65655707 ns   65649295 ns         83   15.2325M items/s
BM_EventInsertion_sorted/4194304/1048576                    124380979 ns  124367270 ns         44    8.0407M items/s
BM_EventInsertion_sorted/10000000/1048576                   230366239 ns  230337645 ns         25   4.34145M items/s
BM_EventInsertion_sorted/100000/4194304                      81744800 ns   81741681 ns         64   48.9346M items/s
BM_EventInsertion_sorted/262144/4194304                      94116005 ns   94114545 ns         53   42.5014M items/s
BM_EventInsertion_sorted/1048576/4194304                    199251682 ns  199246301 ns         27   20.0757M items/s
BM_EventInsertion_sorted/4194304/4194304                    349437106 ns  349425863 ns         17   11.4473M items/s
BM_EventInsertion_sorted/10000000/4194304                   402828995 ns  402822052 ns         11   9.92994M items/s
BM_EventInsertion_sorted/100000/16777216                    211700150 ns  211697153 ns         23   75.5797M items/s
BM_EventInsertion_sorted/262144/16777216                    297690694 ns  297686056 ns         17   53.7479M items/s
BM_EventInsertion_sorted/1048576/16777216                   362840655 ns  362834239 ns         15   44.0973M items/s
BM_EventInsertion_sorted/4194304/16777216                   809394322 ns  809290720 ns          7   19.7704M items/s
BM_EventInsertion_sorted/10000000/16777216                 1124704540 ns 1124678170 ns          5   14.2263M items/s
```

