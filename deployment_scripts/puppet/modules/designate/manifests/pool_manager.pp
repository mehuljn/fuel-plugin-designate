# == Class designate::sink
#
# Configure designate sink service
#
# == Parameters
#
# [*package_ensure*]
#  (optional) The state of the package
#  Defaults to 'present'
#
# [*sink_package_name*]
#  (optional) Name of the package containing sink resources
#  Defaults to sink_package_name from designate::params
#
# [*enabled*]
#  (optional) Whether to enable services.
#  Defaults to true
#
# [*service_ensure*]
#  (optional) Whether the designate sink service will be running.
#  Defaults to 'running'
#
# [*enabled_notification_handlers*]
#  (optional) List of notification handlers to enable, configuration of
#  these needs to correspond to a [handler:my_driver] section below or
#  else in the config.
#  Defaults to undef
#
class designate::pool_manager (
  $package_ensure                = present,
  $poolman_package_name             = undef,
  $enabled                       = true,
  $service_ensure                = 'running',
  $enabled_notification_handlers = undef,
) inherits designate {
  include ::designate::params

  designate::generic_service { 'pool_manager':
    enabled        => $enabled,
    manage_service => $service_ensure,
    ensure_package => $package_ensure,
    package_name   => pick($poolman_package_name, $::designate::params::poolman_package_name),
    service_name   => $::designate::params::poolman_service_name,
  }

#  if $enabled_notification_handlers {
#    designate_config {
#      'service:sink/enabled_notification_handlers':  value => join($enabled_notification_handlers,',')
#    }
#  } else {
    designate_config {
#      'service:sink/enabled_notification_handlers':  ensure => absent

      'service:pool_manager/pool_id':  value => '794ccc2c-d751-44fe-b57f-8894c9f5c842';
      'pool:794ccc2c-d751-44fe-b57f-8894c9f5c842/nameservers': value => '0f66b842-96c2-4189-93fc-1dc95a08b012';
      'pool:794ccc2c-d751-44fe-b57f-8894c9f5c842/targets': value => 'f26e0b32-736f-4f0a-831b-039a415c481e';
      'pool_nameserver:0f66b842-96c2-4189-93fc-1dc95a08b012/port': value => '53';
      'pool_nameserver:0f66b842-96c2-4189-93fc-1dc95a08b012/host': value => '127.0.0.1';
      'pool_target:f26e0b32-736f-4f0a-831b-039a415c481e/options': value => 'port: 53, host: 127.0.0.1';
      'pool_target:f26e0b32-736f-4f0a-831b-039a415c481e/masters': value => '127.0.0.1:5354';
      'pool_target:f26e0b32-736f-4f0a-831b-039a415c481e/type': value => 'bind9';
    }
#  }

}
