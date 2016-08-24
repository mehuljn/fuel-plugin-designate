#fuel-plugin-designate

##Plugin description:

This is Fuel Plugin for Designate used in Fuel Environment for deploying Designate

## How to Use the plugin

### Git clone the plugin on fuel master
```
git clone https://github.com/mehuljn/fuel-plugin-designate
cd fuel-plugin-designate
```
### Using the fuel plugin builder build the plugin 
`fpb --build .` 

__If the above commands gives errors it might require come additional rpmbuild or deb packages which need to be installed__
### Once the Plugin is built ,use the below command to install the plugin in fuel
`fuel plugin --install <path to plugin rpm file>`

### The plugin should now be available under plugins in Fuel UI

### Once the deployment is completed ,for automatic integration please ensure that the new notification handler is used to replace the older neutron.py and base.py files

## Designate Dashboard

Integrate Designate Dashboard by Manually Installing on all Controllers
https://github.com/openstack/designate-dashboard/tree/stable/liberty
Ensure the change to designatedashboard/____init____.py for pbr version


## Changes to Fuel Designate Plugin for MOS 8.0 

1. Puppet manifest to deploy repo (trusty/updates liberty) for designate packages
2. Add predecessor for database (primary-database) in deployment_tasks.yaml
3. Add predecessor for keystone (primary-controller) in deployment_tasks.yaml
4. Add "installation for bind9" in designate-puppet in designate.pp
5. Add bind9 and bin9utils in /usr/share/fuel-mirror/ubuntu.yaml  for creating mos and ubuntu mirrors
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
