#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    def build(self, **_opts):
        r1 = self.addNode('r1', cls=LinuxRouter, ip='10.100.0.1/30')
        r2 = self.addNode('r2', cls=LinuxRouter, ip='10.100.0.2/30')

        # Add 2 switches
        s0 = self.addSwitch('s0')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add host-switch links
        self.addLink(s0, r1, intfName2='r1-eth0', params2={'ip': '10.100.0.1/30'})
        self.addLink(s0, r2, intfName2='r2-eth0', params2={'ip': '10.100.0.2/30'})
        self.addLink(s1, r2, intfName2='r2-eth1', params2={'ip': '192.168.1.1/26'})
        self.addLink(s2, r2, intfName2='r2-eth2', params2={'ip': '192.168.2.1/23'})

        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1', ip='192.168.1.2/26', defaultRoute='via 192.168.1.1')
        h2 = self.addHost(name='h2', ip='192.168.1.3/26', defaultRoute='via 192.168.1.1')
        h3 = self.addHost(name='h3', ip='192.168.2.2/23', defaultRoute='via 192.168.2.1')
        h4 = self.addHost(name='h4', ip='192.168.2.3/23', defaultRoute='via 192.168.2.1')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)

def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()

    r1 = net.getNodeByName('r1')
    r2 = net.getNodeByName('r2')

    # Adiciona interface externa ao roteador R1
    r1.cmd('ifconfig r1-eth1 0')
    r1.cmd('dhclient r1-eth1')

    # # Adiciona interface externa ao roteador R2
    # r2.cmd('ifconfig r2-eth0 0')
    # r2.cmd('dhclient r2-eth0')

    # # Ativa o encaminhamento IP nos roteadores
    # for router in [r1, r2]:
    #     router.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Configura NAT no roteador R1 para acesso à Internet
    r1.cmd('iptables -t nat -A POSTROUTING -o r1-eth1 -j MASQUERADE')

    # Mostrar configuração de interfaces
    info('*** Configurações de interfaces no R1:\n')
    info(r1.cmd('ifconfig'))

    info('*** Tabela de roteamento no R1:\n')
    info(r1.cmd('route'))

    info('*** Configurações de interfaces no R2:\n')
    info(r2.cmd('ifconfig'))

    info('*** Tabela de roteamento no R2:\n')
    info(r2.cmd('route'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
