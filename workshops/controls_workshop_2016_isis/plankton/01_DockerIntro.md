## Quick Docker Intro

This section gives a brief overview of Docker and how to use it during this workshop.


### What is Docker

Docker is a way to package and distribute software in isolated, runnable units called "images" (when referring to the packaged unit) or "containers" (when referring to an instance of a running image).

We use it for our device simulation framework, Plankton, because it has some very useful features in this context:

- Images ship with all dependencies packaged in (Avoids clogged host system, dependency hell, version mismatches)
- You can run multiple containers from one image, passing in different arguments to each one
- Each container has its own isolated, sandboxed environment
- Each container has its own network interface, with its own IP, on a virtual network
- Launching multiple containers in a predetermined setup can be set up using Docker Compose

Some issues to watch out for:

- Native support only on Linux; Windows and OS X run containers in a VM via Docker Machine
- Can lead to difficulties reaching the virtual network from the host OS


### Setting up Docker

Already set up for you in the VM!

Instructions for setting up on Linux may be found [here](https://github.com/DMSC-Instrument-Data/documents/blob/master/virtual_devices/DockerIntro.md).


### Pushing and Pulling from DockerHub

[DockerHub](https://hub.docker.com) is the public image repository provided by Docker.

To pull an image from the DockerHub repository:
```
$ docker pull hello-world
```

To view images in your local repository:
```
$ docker images
```

To push images from your local repository to your DockerHub account:
```
$ docker login
$ docker push myusername/myimage
```

### Running Existing Images

To run any local image (or images on DockerHub, which will be `pull`ed automatically):
```
$ docker run hello-world
```

Most images you will want to run in **i**nteractive **t**erminal mode, and pass in arguments:
```
$ docker run -it alpine sh
```

Often, you'll want to run an image as a **d**aemon, in the background:
```
$ docker run -itd alpine sh -c "sleep 10"
```

To list running containers:
```
$ docker ps
```

To list **a**ll containers (including stopped ones):
```
$ docker ps -a
```

### Building Your Own  Images

Instructions for building a Docker image are stored in a `Dockerfile` (much like a `Makefile`).

We probably won't get into details of Dockerfiles during this workshop. 

Plankton ships with a Dockerfile that can be used to build it. It's unlikely you'll need to modify it, even if you add files to Plankton.

To build an image based on the Dockerfile in the current directory:
```
$ docker build -t myusername/myimage .
```
