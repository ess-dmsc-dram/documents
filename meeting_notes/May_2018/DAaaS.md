## Data Analysis as a Service

Meeting with F Barnsley from SCD. 31st May 2018.

## Problem DAaaS solves

1. Data sizes too great. Sizes >50TB for some imaging datasets
1. Compute cannot be done in a reasonable time (if at all) on standard hardware such as average consumer laptops
1. Installation can be complex particularly when multiple tools are involved

## How it Works

* Single image per facility
* Images are spun-up and runtime customisations are applied (software installed) and they are allocated to pools
* Ansible is used for provisioning, and VMs are hosted on SCD's open stack cloud
* Pools are of a fixed size, configured VM instances wait in pools for users (this gives very fast availability)
* When the VM is provided to a user a persistant home directory is created for the user (if it doesn't already exist) 
* VMs are allocated for a 48 hour period, after which they are destroyed

## Current Status

* Cross facilty VM images created
* Cross facility users at RAL

## Effort

* SCD have new funding 2018 to expand and consolidate this service. SCD aims to have one permanant member of staff per facility to support the service. I think this is probably going to be too little for wide-scale adoption
* The provider is not yet providing 100% uptime for this service, though they have been asked to do so, and that forms a future objective. This would definitely affect the effort estimates above.

## Other
* At present hardware is generic, though some labelled VMs are run on hardware with GPU availability. Future plan is for greater customisation at this level (without making the user aware of choices), may be done by the actual image/provisioning/technique list.
* Excitations group at ISIS are currently the greatest neutron users of this DAaaS facility
* Who owns the VM images / VM instance scripts did not seem clear
* Centos7 currently used for VMs
* This is not a framework as such (more of a strategy) too much depends of the quirks of each facility to describe as something that could be customised and deployed at a different site
* DAaaS is meant as a replacement for NoMachine. DAaaS users are automatically given access to previous NoMachine home directories.

