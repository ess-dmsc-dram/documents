class: center, middle

# Docker

---

## What is it?

- Tool to package an application along with all dependencies, OS, etc

- Distribute easily, run on other host systems, in a sandboxed environment

- Isolated from anything that's installed

- Can have its own IP, network interfaces, etc

- Native to Linux, but can run on Windows/OSX via VM

---

## Differences to a VM

- Doesn't launch a full OS with all the bells and whistles

- Processes run directly on the host (but isolated)

- Very lightweight on resources, only takes as much as it needs

- No need to copy everything to run multiple instances

---

## Differences to a VM

- Usually used for commandline apps and services, GUI takes some work

- Usually only one process per container

- Will need to run in a VM itself, outside of Linux

---

## Images and Layers

An image contains everything needed. Images consist of several layers.

Many standard images provided on the DockerHub.

![image layers](https://docs.docker.com/engine/userguide/storagedriver/images/image-layers.jpg)

---

## Containers

A container is created when an image is run.

<img src="https://docs.docker.com/engine/userguide/storagedriver/images/container-layers-cas.jpg" width="600" />

---

## Running multiple instances

Very cheap, since image is reused.

![many_containers](https://docs.docker.com/engine/userguide/storagedriver/images/sharing-layers.jpg)

---

## Extend existing images

Most common way of creating images is to extend existing ones (usually an OS base image).

![extend](https://docs.docker.com/engine/userguide/storagedriver/images/saving-space.jpg)

---

## Running an image

If image not found on local machine, Docker tries downloading it from DockerHub.

```
$ docker run hello-world
$ docker run mikehart/motorsim
```
---

## Creating your own images

Images built based on a Dockerfile. Contains instructions to create image, similar to a Makefile.

```
FROM ubuntu:trusty

RUN apt-get update && apt-get install [...]

RUN git clone https://github.com/EuropeanSpallationSource/MCAG_setupMotionDemo.git \
    && [...]

COPY ./startup.sh /

CMD ["/startup.sh"]
```

Single command to build once Dockerfile created:
```
$ docker build -t account/image_name .
```

---

## Sharing your image

Images can be pushed to DockerHub, much like to a GitHub repository:

```
$ docker login --username=... --email=...
$ docker push account/image_name
```

And then pulled and run by anyone else:
```
$ docker pull account/image_name
$ docker run account/image_name
```

---

## When is this useful?

- Working on many projects with different or conflicting dependencies, avoid "polluting" host

- Share working setups without everyone having to install, configure, keep updated, etc

- Test networking functionality on a single machine

- Simulate networked systems, especially as part of unit tests
