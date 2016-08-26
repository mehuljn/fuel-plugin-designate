#fuel-plugin-designate

##Plugin description:

This is Fuel Plugin for Designate used in Fuel Environment for deploying Designate

## How to Use the plugin

### Edit the file /usr/share/fuel-mirror/ubuntu.yaml as follows
```
#Add the following after - xinetd
- "xinetd"
- "bind9"
- "bind9utils"
```

### On Fuel Master node add puppet module theforeman-dns (for bind9 backend support) __internet connectivity would be required__
```
puppet module install theforeman-dns
```

### Install fuel-plugin-builder to build plugins
```
pip install fuel-plugin-builder
(you may need to download python-pip as well)
```

### Git clone the plugin on fuel master
```
git clone https://github.com/mehuljn/fuel-plugin-designate
cd fuel-plugin-designate
```
### Using fuel plugin builder build the final plugin 
`fpb --build .` 

__If the above commands gives errors it might require come additional rpmbuild or deb packages which need to be installed__
### Once plugin build is completed ,install or import the plugin in fuel
`fuel plugin --install <path to plugin rpm file>`

### This newly built plugin should now be available under plugins tab in Fuel UI

#### Once above steps are completed ,for automatic neutron integration please ensure that the new notification handler is used and designate dashboard is installed.

## Designate Dashboard

Integrate Designate Dashboard by Manually Installing on all Controllers
https://github.com/openstack/designate-dashboard/tree/stable/liberty

Ensure the change to designatedashboard/____init____.py for pbr version is completed


## Changes to Fuel Designate Plugin for MOS 8.0 

1. Puppet manifest to deploy repo (trusty/updates liberty) for designate packages
2. Add predecessor for database (primary-database) in deployment_tasks.yaml
3. Add predecessor for keystone (primary-controller) in deployment_tasks.yaml
4. Add "installation for bind9" in designate-puppet in designate.pp
5. Add bind9 and bind9utils in /usr/share/fuel-mirror/ubuntu.yaml  for creating mos and ubuntu mirrors
6. Add theforeman-dns to puppet modules on fuel master
7. Add manifests for Pool Manager and mDNS (missing in the original mos 7.0 plugin)
8. Removed pre_build_hook as there are changes in puppet-designate modules as well which are not in github
9. Added feature to select "bind9" or "powerdns" backend to enviornment

## Additional Verifications for PowerDNS(WIP)

1. Add powerdns in the repo
2. Add powerdns puppet module 
3. Changes to manifests for powedns as per heira (WIP)


## Some Fixes
1. Fixed(partial) neutron.py for Automatic FloatingIntegration from cirrus Floating IP integration (This file is as additional file)
2. Fixed the PoolManager puppet config for nameservers and targets
3. Fixed the bind9 config (comment the added line)
