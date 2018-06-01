name           | Jenkins name                | comment
-------------- | --------------------------- | ---
mantid-build01 | ess-ubuntu-performancetests | runs the Mantid performance test
mantid-build02 | -                           | old attempt to get other OS (Windows?) build server running?
mantid-build03 | -                           | old attempt to get other OS (Windows?) build server running?
mantid-build04 | ess-ubuntu-builder-1        |
mantid-build05 | -                           | old attempt to get other OS (OSX?) build server running?

ssh config to reach builder servers from within DMSC:

```
Host build-gateway
  ProxyCommand ssh -q ssh2 nc ssh0 22

Host ess-ubuntu-performancetests
  ProxyCommand ssh -q build-gateway nc mantid-build01 22

Host ess-ubuntu-builder-1
  ProxyCommand ssh -q build-gateway nc mantid-build04 22

Host ess-ubuntu-builder-2
  ProxyCommand ssh -q build-gateway nc mantid-build06 22
```

Direct IPs are 192.168.10.10[146], etc.

- The account used for building an configuring Jenkins is `builder`.
  Cannot be reached via ssh, use separate user and use `su - builder`.
- Edit `/etc/ssh/group.allow` to allow login for new users.
- Jenkins config is in `/home/builder/jenkins_scripts`.
  Edit `script.sh` with new node name/secret.
