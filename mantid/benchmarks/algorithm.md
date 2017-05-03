# Algorithm performance

## Benchmark results

| What | time [s] |
| ---- | -------- |
| create with AlgorithmFactory | 2e-5 |
| empty `initialize()` | 1e-5 |
| empty `execute()` | 1e-4 |
| 1 workspace property `initialize()` | 4e-5 |
| 1 workspace property `setProperty()` | 1e-5 |
| 1 workspace property `execute()` | 4e-4 |
| 10 workspace properties `initialize()` | 5e-5 |
| 10 workspace properties `setProperty()` | 2e-5 |
| 10 workspace properties `execute()` | 5e-4 |

# Conclusion

Creating and running an algorithm has a combined baseline overhead of approximately 0.001 seconds, i.e., we could potentially run 1000 algorithms per second.
