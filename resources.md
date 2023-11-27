# Nomad Documentation
* [Overview of Nomad](https://developer.hashicorp.com/nomad/tutorials/get-started/gs-overview)
* [Repo of Nomad Examples](https://github.com/angrycub/nomad_example_jobs)

## Component Documentation
* [Important to get Docker Images into Nomad](https://developer.hashicorp.com/nomad/docs/job-specification/artifact)
* [Network Block Infomation](https://developer.hashicorp.com/nomad/docs/job-specification/network)

### Task Drivers
* [Docker Driver](https://developer.hashicorp.com/nomad/docs/drivers/docker)
    * [Fun problems with untagged docker images](https://discuss.hashicorp.com/t/offline-docker-image-exec/26269/4)
* [QEMU Driver](https://developer.hashicorp.com/nomad/docs/drivers/qemu)
* [Task Driver](https://developer.hashicorp.com/nomad/docs/drivers/exec)

## Likely Important for Later
* [CNI networking interface for future networking groups](https://developer.hashicorp.com/nomad/docs/networking/cni)
* https://www.qemu.org/docs/master/system/devices/net.html
* https://interrupt.memfault.com/blog/emulating-raspberry-pi-in-qemu
* [Templating will be useful for lab networks](https://www.qemu.org/docs/master/system/vm-templating.html). It will save space and time if we continue using QEMU to emulate old hardware.

# Other Things
* [Many Docker Image Examples](https://github.com/docker/awesome-compose/tree/master)