notice('MODULAR: designate/repo.pp')

$designate_hash    = hiera_hash('fuel-plugin-designate', {})
$public_ssl_hash = hiera('public_ssl')
$network_metadata = hiera_hash('network_metadata')

$use_designate = pick($designate_hash['metadata']['enabled'], true)


$designate_address_map = get_node_to_ipaddr_map_by_network_role(get_nodes_hash_by_roles($network_metadata, ['designate']), 'designate/api')

include apt

apt::source { "cloud-archive":
            location   => "http://ubuntu-cloud.archive.canonical.com/ubuntu",
            release    => "trusty-updates/liberty",
            repos      => " main",
            include_src=> false
}  
