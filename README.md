fuel-plugin-designate
============

Plugin description:

This is Fuel Plugin for Designate used in Fuel Environment for deploying Designate

There are modifications for MOS 8.0 following are the changes 

Changes to Fuel Designate Plugin for MOS 8.0 

1. Puppet manifest to deploy repo (trusty/updates liberty) for designate packages
2. Add predecessor for database (primary-database) in deployment_tasks.yaml
3. Add predecessor for keystone (primary-controller) in deployment_tasks.yaml
4. Add "installation for bind9" in designate-puppet in designate.pp
5. Add bind9 and bin9utils in /usr/share/fuel-mirror/ubuntu.yaml  for creating mos and ubuntu mirrors
6. Add theforeman-dns to puppet modules on fuel master
7. Add manifests for Pool Manager and mDNS (missing in the original mos 7.0 plugin)
8. Removed pre_build_hook as there are changes in puppet-designate modules as well which are not in github

Additional Verify for PowerDNS

1. Add powerdns in the repo
2. Add powerdns puppet module 

Integrate Designate Dashboard by Manually Installing on all Controllers
https://github.com/openstack/designate-dashboard/tree/stable/liberty
Ensure the change to designatedashboard/__init__.py for pbr version

****Fixed(partial) neutron.py for Automatic FloatingIntegration from cirrus Floating IP integration (This file is as additional file)

****Fixed the PoolManager puppet config for nameservers and targets : Done

****Fixed the bind9 config (comment the added line)
