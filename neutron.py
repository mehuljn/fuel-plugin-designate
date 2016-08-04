# Copyright 2012 Bouvet ASA
#
# Author: Endre Karlson <endre.karlson@bouvet.no>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from oslo_config import cfg
from oslo_log import log as logging

from designate.notification_handler.base import BaseAddressHandler

from keystoneclient.v2_0 import client as keystone_c
from neutronclient.v2_0 import client as neutron_c
from novaclient.v2 import client as nova_c



LOG = logging.getLogger(__name__)

cfg.CONF.register_group(cfg.OptGroup(
    name='handler:neutron_floatingip',
    title="Configuration for Neutron Notification Handler"
))

cfg.CONF.register_opts([
    cfg.ListOpt('notification-topics', default=['notifications']),
    cfg.StrOpt('control-exchange', default='neutron'),
    cfg.StrOpt('keystone_auth_uri', default=None),
    cfg.StrOpt('domain-id', default=None),
    cfg.MultiStrOpt('format', default=[
                    '%(octet0)s-%(octet1)s-%(octet2)s-%(octet3)s.%(domain)s'])
], group='handler:neutron_floatingip')


class NeutronFloatingHandler(BaseAddressHandler):
    """Handler for Neutron's notifications"""
    __plugin_name__ = 'neutron_floatingip'

    def get_exchange_topics(self):
        exchange = cfg.CONF[self.name].control_exchange

        topics = [topic for topic in cfg.CONF[self.name].notification_topics]

        return (exchange, topics)

    def get_event_types(self):
        return [
            'floatingip.update.end',
            'floatingip.delete.start'
        ]


    def _scrub_instance_name(name=""):
        scrubbed = ""
        for char in name:
            if char.isalnum() or char == '.' or char == '-':
                scrubbed += char
            else:
                scrubbed += '-'
            if len(scrubbed) == 63:
                return scrubbed
        return scrubbed



    def _get_instance_info(self, kc, port_id):
        """Returns information about the instance associated with the neutron `port_id` given.
        Given a Neutron `port_id`, it will retrieve the device_id associated with
        the port which should be the instance UUID.  It will then retrieve and
        return the instance name and UUID for the instance.  Note that the
        `port_id` must the one associated with the instance, not the floating IP.
        Neutron floating ip notifications will contain the instance's port_id.
        """

        def _scrub_instance_name(name=""):
            scrubbed = ""
            for char in name:
                if char.isalnum() or char == '.' or char == '-':
                    scrubbed += char
                else:
                    scrubbed += '-'
                if len(scrubbed) == 63:
                    return scrubbed
            return scrubbed

        neutron_endpoint = kc.service_catalog.url_for(service_type='network',
                                                      endpoint_type='internalURL')
        nc = neutron_c.Client(token=kc.auth_token,
                              tenant_id=kc.auth_tenant_id,
                              endpoint_url=neutron_endpoint)
        port_details = nc.show_port(port_id)
        instance_id = port_details['port']['device_id']
        instance_info = {'id': instance_id}
        LOG.debug('Instance id for port id %s is %s' % (port_id, instance_id))

        nova_endpoint = kc.service_catalog.url_for(service_type='compute',
                                                   endpoint_type='internalURL')
        nvc = nova_c.Client(auth_token=kc.auth_token,
                            tenant_id=kc.auth_tenant_id,
                            bypass_url=nova_endpoint)
        server_info = nvc.servers.get(instance_id)
        LOG.debug('Instance name for id %s is %s' % (instance_id, server_info.name))
        instance_info['original_name'] = server_info.name
        instance_info['scrubbed_name'] = _scrub_instance_name(server_info.name)
        if instance_info['original_name'] != instance_info['scrubbed_name']:
            LOG.warn('Instance name for id %s contains characters that cannot be used'
                    ' for a valid DNS record. It was scrubbed from %s to %s'
                    % (instance_id, instance_info['original_name'], instance_info['scrubbed_name']))
            instance_info['name'] = instance_info['scrubbed_name']
        else:
            instance_info['name'] = instance_info['original_name']

        return instance_info



    def process_notification(self, context, event_type, payload):
        LOG.debug('%s received notification - %s' %
                  (self.get_canonical_name(), event_type))

        domain_id = cfg.CONF[self.name].domain_id
        kauth_url = cfg.CONF[self.name].keystone_auth_uri
        LOG.debug("Keystone Auth URL is " + str(kauth_url))

        if event_type.startswith('floatingip.delete'):
            self._delete(domain_id=domain_id,
                         resource_id=payload['floatingip_id'],
                         resource_type='floatingip')
        elif event_type.startswith('floatingip.update'):
            if payload['floatingip']['fixed_ip_address']:
                address = {
                    'version': 4,
                    'address': payload['floatingip']['floating_ip_address']
                }
                LOG.debug("Create DNS entry for port_id " + str(payload['floatingip']['port_id']))
                
                kc = keystone_c.Client(token=context['auth_token'],\
                                       tenant_id=context['tenant_id'],\
                                       auth_url=kauth_url)

                port_id = payload['floatingip']['port_id']
		instance_info = self._get_instance_info(kc, port_id)
		LOG.debug("The instance name is " + str(instance_info['name']))

                extra = payload.copy()
                extra.update({'instance_name': instance_info['name'],\
                                  'instance_short_name': instance_info['name'].partition('.')[0],\
                                  'domain': domain_id})

                self._create(addresses=[address],
                             extra=extra,
                             domain_id=domain_id,
                             resource_id=payload['floatingip']['id'],
                             resource_type='floatingip')
            elif not payload['floatingip']['fixed_ip_address']:
                self._delete(domain_id=domain_id,
                             resource_id=payload['floatingip']['id'],
                             resource_type='floatingip')
