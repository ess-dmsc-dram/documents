# Event compression in Mantid

The *CompressEvent* algorithm was mentioned as a possibility of handling large
amounts of events which are located closer than the instrument resolution
with respect to each other. In this case the algorihtm would effectively bundle
neighbouring events into weighted events.


## Algorihtm description

The algorithm performs the following steps:
1. Sort event lists
2. For each spectrum on the workspace call `compressEvents` on the associated
  event list

### `void EventList::compressEvents(double tolerance, EventList *destination)`

```
def compress(to_compress, tolerance):
  out_list = new WeightedNoTimeContainer()

  total_time_of_flight = 0
  number_events_recorded = 0
  weight = 0
  error_squared = 0

  last_tof = -inf
  for event in to_compress:
    if event.tof - last_tof:
      weight += event.weight
      error_squared += event.error_squared
      number_events += 1
      total_time_of_flight += event.tof
    else:
      if number_events_recorded > 0:
        out_list.add_event(total_time_of_flight / number_events_recorded, weight, error_squared)
      weight = event.weight
      error_squared = event.error_squared
      number_events = 1
      total_time_of_flight = event.tof
      last_tof = event.tof
  return out_list
```

This is a pretty simple compression mechanism. A small issue is that you
might end up with different compressions if you were to go through the list
in reverse.


## Usage in reductions

The algorihtm is used in several reductions at the SNS. However none of the reductions
seems to make use of the MD facilities that Mantid has to offer.


## Considerations regarding resolution
