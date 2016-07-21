fuel-plugin-designate
============

Plugin description:

This is Fuel Plugin for Designate used in Fuel Environment for deploying Designate

There are modifications for MOS 8.0 following are the changes 

Changes for Fuel Designate Plugin for MOS 8.0 
1. Puppet manifest to deploy repo (trusty/updates liberty)
2. Add predecessor for database (primary-database) in deployment_tasks.yaml
3. Add predecessor for keystone (primary-controller) in deployment_tasks.yaml
4. Add "installation for bind9" in designate-puppet
