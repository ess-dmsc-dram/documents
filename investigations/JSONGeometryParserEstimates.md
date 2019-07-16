# Go/No-Go Streamed Geometry
### Why not use filewriter?
The Json geometry is essentially in the nexus format. The filewrite is simply writing what it finds in the JSON string out to the nexus file (see below).
```json
{
  "nexus_structure": {
    "children": [
      {
        "type": "group",
        "name": "entry",
        "children": [
          {
            "type": "dataset",
            "name": "features",
            "dataset": {
              "type": "uint64",
              "size": [
                1
              ]
            },
            "values": [
              10138143369737382000
            ]
          },
          {
            "type": "group",
            "name": "instrument",
            "children": [
              {
                "type": "group",
                "name": "detector_1",
                "children": [
                  {
                    "type": "dataset",
                    "name": "depends_on",
                    "dataset": {
                      "type": "string"
                    },
                    "values": "/entry/instrument/detector_1/transformations/location"
                  },
                  {
                    "type": "dataset",
                    "name": "detector_number",
                    "dataset": {
                      "type": "int64",
                      "size": [
                        2,
                        2
                      ]
                    },
                    "values": [
                      [
                        0,
                        1
                      ],
                      [
                        2,
                        3
                      ]
                    ]
                  },
                  {
                    "type": "group",
                    "name": "pixel_shape",
                    "children": [
                      {
                        "type": "dataset",
                        "name": "faces",
                        "dataset": {
                          "type": "int32",
                          "size": [
                            1
                          ]
                        },
                        "values": [
                          0
                        ]
                      },
                      {
                        "type": "dataset",
                        "name": "vertices",
                        "dataset": {
                          "type": "float",
                          "size": [
                            4,
                            3
                          ]
                        },
                        "values": [
                          [
                            -0.0010000000474974513,
                            -0.0010000000474974513,
                            0
                          ],
                          [
                            0.0010000000474974513,
                            -0.0010000000474974513,
                            0
                          ],
                          [
                            0.0010000000474974513,
                            0.0010000000474974513,
                            0
                          ],
                          [
                            -0.0010000000474974513,
                            0.0010000000474974513,
                            0
                          ]
                        ],
                        "attributes": [
                          {
                            "name": "units",
                            "values": "m"
                          }
                        ]
                      },
                      {
                        "type": "dataset",
                        "name": "winding_order",
                        "dataset": {
                          "type": "int32",
                          "size": [
                            4
                          ]
                        },
                        "values": [
                          0,
                          1,
                          2,
                          3
                        ]
                      }
                    ],
                    "attributes": [
                      {
                        "name": "NX_class",
                        "values": "NXoff_geometry"
                      }
                    ]
                  },
                  {
                    "type": "group",
                    "name": "transformations",
                    "children": [
                      {
                        "type": "dataset",
                        "name": "beam_direction_offset",
                        "dataset": {
                          "type": "double",
                          "size": [
                            1
                          ]
                        },
                        "values": [
                          0.049
                        ],
                        "attributes": [
                          {
                            "name": "depends_on",
                            "values": "/entry/instrument/detector_1/transformations/orientation"
                          },
                          {
                            "name": "transformation_type",
                            "values": "translation"
                          },
                          {
                            "name": "units",
                            "values": "m"
                          },
                          {
                            "name": "vector",
                            "values": [
                              0,
                              0,
                              -1
                            ],
                            "type": "double"
                          }
                        ]
                      },
                      {
                        "type": "dataset",
                        "name": "location",
                        "dataset": {
                          "type": "double",
                          "size": [
                            1
                          ]
                        },
                        "values": [
                          0.971
                        ],
                        "attributes": [
                          {
                            "name": "depends_on",
                            "values": "/entry/instrument/detector_1/transformations/beam_direction_offset"
                          },
                          {
                            "name": "transformation_type",
                            "values": "translation"
                          },
                          {
                            "name": "units",
                            "values": "m"
                          },
                          {
                            "name": "vector",
                            "values": [
                              1,
                              0,
                              0
                            ],
                            "type": "double"
                          }
                        ]
                      },
                      {
                        "type": "dataset",
                        "name": "orientation",
                        "dataset": {
                          "type": "double",
                          "size": [
                            1
                          ]
                        },
                        "values": [
                          90
                        ],
                        "attributes": [
                          {
                            "name": "depends_on",
                            "values": "."
                          },
                          {
                            "name": "transformation_type",
                            "values": "rotation"
                          },
                          {
                            "name": "units",
                            "values": "deg"
                          },
                          {
                            "name": "vector",
                            "values": [
                              0,
                              1,
                              0
                            ],
                            "type": "double"
                          }
                        ]
                      }
                    ],
                    "attributes": [
                      {
                        "name": "NX_class",
                        "values": "NXtransformations"
                      }
                    ]
                  },
                  {
                    "type": "dataset",
                    "name": "x_pixel_offset",
                    "dataset": {
                      "type": "double",
                      "size": [
                        2,
                        2
                      ]
                    },
                    "values": [
                      [
                        -0.299,
                        -0.297
                      ],
                      [
                        -0.299,
                        -0.297
                      ]
                    ],
                    "attributes": [
                      {
                        "name": "units",
                        "values": "m"
                      }
                    ]
                  },
                  {
                    "type": "dataset",
                    "name": "y_pixel_offset",
                    "dataset": {
                      "type": "double",
                      "size": [
                        2,
                        2
                      ]
                    },
                    "values": [
                      [
                        -0.299,
                        -0.299
                      ],
                      [
                        -0.297,
                        -0.297
                      ]
                    ],
                    "attributes": [
                      {
                        "name": "units",
                        "values": "m"
                      }
                    ]
                  }
                ],
                "attributes": [
                  {
                    "name": "NX_class",
                    "values": "NXdetector"
                  }
                ]
              }
            ],
            "attributes": [
              {
                "name": "NX_class",
                "values": "NXinstrument"
              }
            ]
          },
          {
            "type": "group",
            "name": "monitor_1",
            "children": [
              {
                "type": "dataset",
                "name": "depends_on",
                "dataset": {
                  "type": "string"
                },
                "values": "/entry/monitor_1/transformations/transformation"
              },
              {
                "type": "dataset",
                "name": "detector_id",
                "dataset": {
                  "type": "int64"
                },
                "values": 90000
              },
              {
                "type": "group",
                "name": "events",
                "children": [
                  {
                    "type": "stream",
                    "stream": {
                      "topic": "monitor",
                      "source": "Monitor_Adc0_Ch1",
                      "writer_module": "ev42"
                    }
                  }
                ]
              },
              {
                "type": "dataset",
                "name": "name",
                "dataset": {
                  "type": "string"
                },
                "values": "Helium-3 monitor"
              },
              {
                "type": "group",
                "name": "transformations",
                "children": [
                  {
                    "type": "dataset",
                    "name": "transformation",
                    "dataset": {
                      "type": "double",
                      "size": [
                        1
                      ]
                    },
                    "values": [
                      -3.298
                    ],
                    "attributes": [
                      {
                        "name": "depends_on",
                        "values": "."
                      },
                      {
                        "name": "transformation_type",
                        "values": "translation"
                      },
                      {
                        "name": "units",
                        "values": "m"
                      },
                      {
                        "name": "vector",
                        "values": [
                          0,
                          0,
                          1
                        ],
                        "type": "double"
                      }
                    ]
                  }
                ],
                "attributes": [
                  {
                    "name": "NX_class",
                    "values": "NXtransformations"
                  }
                ]
              },
              {
                "type": "group",
                "name": "waveforms",
                "children": [
                  {
                    "type": "stream",
                    "stream": {
                      "topic": "monitor",
                      "source": "Monitor_Adc0_Ch1",
                      "writer_module": "senv"
                    }
                  }
                ]
              }
            ],
            "attributes": [
              {
                "name": "NX_class",
                "values": "NXmonitor"
              }
            ]
          },
          {
            "type": "group",
            "name": "sample",
            "children": [
              {
                "type": "dataset",
                "name": "description",
                "dataset": {
                  "type": "string"
                },
                "values": ""
              }
            ],
            "attributes": [
              {
                "name": "NX_class",
                "values": "NXsample"
              }
            ]
          }
        ],
        "attributes": [
          {
            "name": "NX_class",
            "values": "NXentry"
          }
        ]
      }
    ]
  }
}
```

 There is no sophisticated parsing are conversion to Nexus in memory. As such, there is no in-memory representation of instrument geometry. In order to re-use what is in the filewriter we will either need to write to file first the read, which will defeat the purpose of the exercise, or we will need to make invasive changes to both the filewriter and Mantid to create/parse an in-memory representation of the nexus geometry. It is far simpler to just go directly from JSON to the in-memory instrument.

### Initial impressions
So far a few unit tests have been written to probe the general structure of the JSON file and extact basic geometry components. It seems as though extraction of the detector information is relatively straightforward and will be able to make use of the `InstrumentBuilder` and `NexusFactory` without modification of either to produce the instrument. This is using the `JSONCpp` library which is relatively simple to use, although it is not the best library to work with. 

### Estimates
Given current progress on exploratory unit tests as well as the availability of the `NexusGeometry` builders, creating a `JSONGeometryParser` could take between 2-4 weeks of a single, experienced developer's time. This includes testing and integration into the `KafkaEventStreamDecoder`. This will all be subject to the availability of an actual stream of the instrument Geometry.
