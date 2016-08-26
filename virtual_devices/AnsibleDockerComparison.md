# Ansible vs Docker Comparison

The purpose of this document is to assess the suitability of using [Ansible](https://www.ansible.com/) vs [Docker](https://www.docker.com/) as solutions to a variety of scenarios and goals in the context of Instrument Control at the [ESS](https://europeanspallationsource.se/).


## What is Ansible?

Ansible is a deployment, automation and orchestration engine. It harnesses SSH to remotely configure and manage an `inventory` of machines based on previously defined `playbooks` and/or `roles`. [YAML](http://yaml.org/) is used to define all of these.

Inventories define and group all the hosts you want Ansible to be aware of. You can then run playbooks, apply roles or execute ad hoc commands against individual hosts or groups of hosts. Playbooks can be used to apply multiple roles to multiple hosts or groups. Roles are a collection of tasks, templates, variable definitions, etc that collectively define an aspect of what you expect a host to support once the role is applied. Roles can be distributed and shared using [Ansible Galaxy](https://galaxy.ansible.com/).

For example, a "webserver" role might contain all instructions needed to install and configure an apache server. A "devmachine" role might similarly contain instructions to set up various compilers and IDEs. Using a playbook, you might apply "webserver" to Host A, "devmachine" to Host B, and both to Host C; the hosts having been defined in an inventory. Ansible will SSH into the various hosts and ensure they have the required software installed, configured as defined, that versions match, and apply changes where necessary.


## What is Docker?

Docker harnesses LXC ([LinuxContainers](https://linuxcontainers.org/)) technology to encapsulate a service or application in a sandbox environment, which contains everything required to run it, in any host environment, without the overhead of a full VirtualMachine.

To build this sandbox environment, you define a `Dockerfile` which contains the instructions required to install and configure the software you wish to run, along with any dependencies, and the environment you want it to run in. Docker can execute those instructions to create a binary package, which is called an `image`. Images can be distributed using the [DockerHub](https://hub.docker.com/), by setting up a private repository, or by exporting and importing them as tarballs.

Images are executed on the host hardware and using the host kernel. However, they are run in a `container` with their own environment (potentially based on a different distro) and their own network stack. By default, they are given their own, isolated loopback and an adapter, with their own IP, on a virtual network that is shared with all other containers. Docker comes with built-in features that allow mapping ports on this network to ports on real adapters connected to the host.

The above are features of the core Docker Engine. Docker additionally provides a variety of tools and services, such as Docker Swarm and Docker Compose, which are currently beyond the scope of this comparison.


## Feature Overlap

As is probably evident from the above paragraphs, there isn't very much overlap between Ansible and Docker. These are two very different technologies that focus on solving different problems.

It would be worthwhile investigating Docker Compose and Docker Swarm in detail, as there are likely to be more parallels between them and Ansible than between Docker Engine and Ansible. This comparison focuses primarily on Docker Engine.

Where there is some overlap in terms of scenarios these two technologies address, the solutions and approaches often differ drastically:

Scenario | Ansible Approach | Docker Approach
-------- | ---------------- | ---------------
Define the environment a service should run in. | Use YAML to define tasks to run in order to set up the environment and install the service. | Use a Dockerfile to define commands to execute in order to set up the environment and install the service.
Share a defined service and environment with other users. | Ansible Galaxy can be used to share roles that define what is needed to install and configure the service. These can then be run against a specified host set it up accordingly. | DockerHub can be used to share binary images that have been built using a Dockerfile and contain everything needed to run the service. These can then be executed directly on the local machine.
Run a service in a defined environment. | Run a playbook, a text-based set of instructions, to apply a role and/or run tasks against a specified host via SSH | Run a previously built or downloaded binary image that contains everything required. Running the image creates a sandboxed container based on it. The service runs inside the container.
Manage versions of environment and service configuration. | Playbooks are often stored and tracked in version control, such as GitHub. Roles and associated assets might be kept there as well, or uploaded to Ansible Galaxy. To run a particular version of a service and environment, you must apply that particular version of playbook/roles against a host. | Dockerfiles and associated assets are often stored and tracked in version control, such as GitHub. Built images are typically pushed to DockerHub. Images can be tagged with a version. Multiple versions may coexist on DockerHub, be pulled by clients, and even be executed simultaneously on the same machine. To run a particular version, you reference it like this: `docker run user/image:version`. When omitted, ":version" defaults to ":latest".
 |  | 

## Ansible Focus

There are a number of scenarios where Ansible excels.

Scenario | Ansible Approach | Docker Approach
-------- | ---------------- | ---------------
Apply configuration(s) across many machines. | An inventory defines your available hosts, and a playbook may refer to them to apply roles. Ansible will SSH into the hosts and run commands to apply the defined configuration to them. | Docker Engine does not deal with multiple hosts. Its purpose is to run containers on the local machine. Docker Compose + Swarm may have features in that direction.
Manage, run commands, update configuration files across multiple machines. | Playbooks aren't limited to installing and setting up services. They can run arbitrary commands, so a set of them may be used to orchestrate and control a cluster of services. | Docker has no equivalent to my knowledge. Compose+Swarm appear limited to startup and shutdown of containers on a cluster of machines, at first glance.
 |  | 

## Docker Focus

There are a number of scenarios where Docker excels.

Scenario | Ansible Approach | Docker Approach
-------- | ---------------- | ---------------
Run a configuration based on a different distro on your host | Ansible doesn't make any provisions for portability as far as I can tell. Playbooks/roles define a set of commands to run. It is up to you to ensure portability where possible/necessary. | Docker images are inherently portable due to containing everything required to run. Some special circumstances notwithstanding, they will run natively on any modern Linux distribution. Windows and OSX are supported via virtualisation.
Run multiple different configurations on a single machine | Ansible makes no special provisions for this. You may of course apply multiple playbooks to the same host. They will execute their tasks in sequence. If there are no conflicts, this works as expected. If there are conflicting tasks, the last to run will take effect. | Since each container runs in a sandbox environment of its own, there is no need to worry about conflicting configurations or dependencies. Since containers are extremely lightweight, and the service effectively runs natively, hundreds of containers may be run on the same machine, limited primarily by the weight of the service itself.
Run multiple instances of the same configuration on a single machine | Ansible makes no attempt to support anything like this. You may, of course, use it to orchestrate Docker or Vagrant to automate setting this up for you. | Multiple containers may be launched based on the same image. You may pass different parameters to each of them. So you might have one `plankton` image that contains your simulation framework and, based on what parameters you pass in when you run it, the launched container might run a chopper, a temperature controller or a power supply simulator. Since each is running in its own sandbox, there's not need to worry about multiple instances interfering with each other.
Simulate a network of machines running a variety of services on a single machine | Ansible makes no attempt to support anything like this. You may, of course, use it to orchestrate Docker or Vagrant to automate setting this up for you. | All running containers receive an IP in the 172.17.0.0/16 range on the docker0 virtual network interface. The host machine is assigned 172.17.0.1. Containers and host may communicate freely on this network. Since they each have their own IP, similar services can bind to the same port number without concern for conflicts. Ports may also be forwarded between containers and the host's network adapters.
 |  | 

## Conclusions and Commentary

My impression is that that these are two very different technologies that serve very different purposes. As alluded to above, I see no reason why Ansible couldn't be used to automate and orchestrate Docker, which, in turn, provides containerisation and portability.

As mentioned, it might be worthwhile to spend some time investigating Docker Compose and Swarm, to see if there are more parallels there. There likely are, but my impression of those services is that they are focused mostly on load balancing and "cloudification", if you will.

Better candidates for comparison with Ansible might be [Puppet](https://puppet.com) or [Quattor](http://www.quattor.org/).


