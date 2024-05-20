from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def setupNetwork():
    net = Mininet(controller=Controller, switch=OVSKernelSwitch)

    # Add controller
    info('*** Adding controller\n')
    net.addController('c0')

    # Add NAT router and configure IP forwarding
    info('*** Adding NAT router and enabling IP forwarding\n')
    r1 = net.addHost('r1', ip='10.100.0.1/30')  # Corrigido para addHost
    r1.cmd('sysctl net.ipv4.ip_forward=1')

    # Add second router and configure IP forwarding
    r2 = net.addHost('r2', ip='10.100.0.2/30')
    r2.cmd('sysctl net.ipv4.ip_forward=1')

    # Add switches
    info('*** Adding switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Add links between routers and switches
    info('*** Adding links\n')
    net.addLink(r1, r2, intfName1='r1-eth0', intfName2='r2-eth0', params1={'ip': '10.100.0.1/30'}, params2={'ip': '10.100.0.2/30'})
    net.addLink(s1, r2, intfName2='r2-eth1', params2={'ip': '10.100.1.1/26'})
    net.addLink(s2, r2, intfName2='r2-eth2', params2={'ip': '10.100.2.1/23'})

    # Add hosts
    info('*** Adding hosts\n')
    h1 = net.addHost('h1', ip='10.100.1.2/26', defaultRoute='via 10.100.1.1')
    h2 = net.addHost('h2', ip='10.100.1.3/26', defaultRoute='via 10.100.1.1')
    h3 = net.addHost('h3', ip='10.100.2.2/23', defaultRoute='via 10.100.2.1')
    h4 = net.addHost('h4', ip='10.100.2.3/23', defaultRoute='via 10.100.2.1')

    # Connect hosts to switches
    info('*** Connecting hosts to switches\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)

    # Start the network
    info('*** Starting network\n')
    net.start()

    # Configurar NAT e rotas nos roteadores
    info('*** Configurando NAT e rotas\n')
    r1.cmd('iptables -t nat -A POSTROUTING -o enp0s1 -j MASQUERADE')
    r1.cmd('ip route add 10.100.1.0/26 via 10.100.0.2 dev r1-eth0')
    r1.cmd('ip route add 10.100.2.0/23 via 10.100.0.2 dev r1-eth0')

    r2.cmd('ip route add default via 10.100.0.1 dev r2-eth0')
    r2.cmd('iptables -t nat -A POSTROUTING -o r2-eth0 -j MASQUERADE')

    # Run the CLI
    info('*** Running CLI\n')
    CLI(net)

    # Stop the network
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setupNetwork()
