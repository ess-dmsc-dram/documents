## Running Plankton

This sections covers where you can find Plankton, how you can run it, and how to configure it to interact with other software.


### Plankton Repositories

Plankton source repository:

https://github.com/DMSC-Instrument-Data/plankton

Some auxilliary files are stored here (for now):

https://github.com/DMSC-Instrument-Data/plankton-misc


### Plankton on DockerHub

Plankton images on DockerHub:

https://hub.docker.com/r/dmscid/plankton/

You can also find the base images used to build the plankton image there:

https://hub.docker.com/r/dmscid/epics-base/
https://hub.docker.com/r/dmscid/epics-pcaspy/


### Running the Plankton Image

To launch an instance of Plankton (a container) in a terminal:
```
$ docker run -it dmscid/plankton --parameters pv_prefix=SIM:
```

Since we didn't specify the *-d*etach option, this runs the same way it would if you ran it natively; attached .

To detach from a running container -- send it to the background but keep it running -- use the `CTRL-P` `CTRL-Q` combo. (Note: This doesn't work with the `--rm` option... if you try, your terminal will freeze until you stop the container from a different terminal).

You can check that it's still running with the `docker ps` command:
```
$ docker ps
```

Note that every container receives a unique ID hash and a unique generated name, both of which can be used to identify it.

To re-attach to a running container, use `docker attach` command and pass in the hash or name:
```
$ docker attach hungry_spence
```

You can shut down an attached container with `CTRL-C`. You can also issue a `docker stop` command if the container is detached or running in a different terminal:
```
$ docker stop hungry_spence
```

### Interacting with CS Studio

Make sure you have a container running with `SIM:` as the prefix:
```
$ docker run -itd dmscid/plankton --parameters pv_prefix=SIM:
```

Start up CS Studio and open the `chopper.opi` file.

Since we've already configured CSS, and the OPI looks for PVs with the SIM: prefix, it should connect automatically.

Play around with the simulation and see if it behaves as you would expect based on the UML diagram.


### Interacting with NICOS

Make sure you have a container running with `SIM:` as the prefix:
```
$ docker run -itd dmscid/plankton --parameters pv_prefix=SIM:
```

Launch NICOS from a terminal:
```
$ cd /home/plankton/Workshop/nicos-core
$ INSTRUMENT=essiip bin/nicos-demo -MEW
```

You may need to click the "Setups" button in the left panel and select "choppersimulation".

In the NICOS console, you can pull up a reference for the chopper object:
```
>> help(chopper)
```
