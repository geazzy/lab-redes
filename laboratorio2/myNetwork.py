from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink  # Importar TCLink para controle de tráfego

def setupNetwork():
    # Criar a rede com controlador, switches e links com controle de tráfego
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink)

    # Adicionar o controlador
    info('*** Adicionando controlador\n')
    net.addController('c0')

    # Adicionar roteador NAT e habilitar encaminhamento IP
    info('*** Adicionando roteador NAT e habilitando encaminhamento IP\n')
    r1 = net.addNAT('r1', connect=None, ip='10.100.0.1/30')
    r1.cmd('sysctl net.ipv4.ip_forward=1')

    # Adicionar o segundo roteador e habilitar encaminhamento IP
    info('*** Adicionando segundo roteador e habilitando encaminhamento IP\n')
    r2 = net.addHost('r2', ip='10.100.0.2/30')
    r2.cmd('sysctl net.ipv4.ip_forward=1')

    # Adicionar switches
    info('*** Adicionando switches\n')
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')

    # Adicionar links entre roteadores e switches com restrições de largura de banda e atraso
    info('*** Adicionando links\n')
    net.addLink(r1, r2, intfName1='r1-eth0', intfName2='r2-eth0',
                params1={'ip': '10.100.0.1/30'}, 
                params2={'ip': '10.100.0.2/30'},
                bw=100, delay='10ms')
    net.addLink(s1, r2, intfName2='r2-eth1', 
                params2={'ip': '10.100.1.1/26'},
                bw=100, delay='10ms')
    net.addLink(s2, r2, intfName2='r2-eth2', 
                params2={'ip': '10.100.2.1/23'},
                bw=100, delay='10ms')

    # Adicionar hosts
    info('*** Adicionando hosts\n')
    h1 = net.addHost('h1', ip='10.100.1.2/26', defaultRoute='via 10.100.1.1')
    h2 = net.addHost('h2', ip='10.100.1.3/26', defaultRoute='via 10.100.1.1')
    h3 = net.addHost('h3', ip='10.100.2.2/23', defaultRoute='via 10.100.2.1')
    h4 = net.addHost('h4', ip='10.100.2.3/23', defaultRoute='via 10.100.2.1')

    # Conectar hosts aos switches com restrições de largura de banda e atraso
    info('*** Conectando hosts aos switches\n')
    net.addLink(h1, s1, bw=100, delay='10ms')
    net.addLink(h2, s1, bw=100, delay='10ms')
    net.addLink(h3, s2, bw=100, delay='10ms')
    net.addLink(h4, s2, bw=100, delay='10ms')

    # Iniciar a rede
    info('*** Iniciando a rede\n')
    net.start()

    # Configurar NAT e rotas nos roteadores
    info('*** Configurando NAT e rotas\n')
    r1.cmd('iptables -t nat -A POSTROUTING -o enp0s1 -j MASQUERADE')
    r1.cmd('ip route add 10.100.1.0/26 via 10.100.0.2 dev r1-eth0')
    r1.cmd('ip route add 10.100.2.0/23 via 10.100.0.2 dev r1-eth0')
    r2.cmd('ip route add default via 10.100.0.1 dev r2-eth0')
    r2.cmd('iptables -t nat -A POSTROUTING -o r2-eth0 -j MASQUERADE')
    
    # Desabilitar systemd-resolved e configurar DNS em todos os hosts e roteadores
    dns_server_ip = '10.100.1.2'  # IP do servidor DNS (h1)
    info('*** Configurando DNS\n')
    devices = [r1, r2, h1, h2, h3, h4]
    for device in devices:
        device.cmd('systemctl stop systemd-resolved')
        device.cmd('systemctl disable systemd-resolved')
        device.cmd('rm /etc/resolv.conf')
        device.cmd(f'echo "nameserver {dns_server_ip}" > /etc/resolv.conf')
        # Definir FQDN para cada dispositivo
        device.cmd(f'echo "{device.IP()} {device.name}.mininet.local" >> /etc/hosts')
        
    h1.cmd('rm /etc/resolv.conf')
    h1.cmd(f'echo "nameserver 1.1.1.1" > /etc/resolv.conf')

    # Configurar h1 como um servidor DNS usando BIND
    info('*** Configurando h1 como servidor DNS\n')
    h1.cmd('apt-get update && apt-get install -y bind9')
    h1.cmd('service bind9 start')
    h1.cmd('echo "zone \\"mininet.local\\" { type master; file \\"/etc/bind/db.mininet.local\\"; };" >> /etc/bind/named.conf.local')
    h1.cmd('echo "$TTL 1D" > /etc/bind/db.mininet.local')
    h1.cmd('echo "@       IN SOA  ns.mininet.local. root.mininet.local. (1 8H 4H 4W 1D)" >> /etc/bind/db.mininet.local')
    h1.cmd('echo "        IN NS   ns" >> /etc/bind/db.mininet.local')
    h1.cmd('echo "ns      IN A    10.100.1.2" >> /etc/bind/db.mininet.local')
    # Adicionar entradas FQDN para cada dispositivo
    for device in devices:
        h1.cmd(f'echo "{device.name}      IN A    {device.IP()}" >> /etc/bind/db.mininet.local')
    h1.cmd('service bind9 restart')

    # Testar a taxa de transferência entre h1 e r1
    info("Testando largura de banda entre h1 e r1\n")
    net.iperf((h1, r1), l4Type='UDP')

    # Executar o CLI
    info('*** Executando CLI\n')
    CLI(net)

    # Parar a rede
    info('*** Parando a rede\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setupNetwork()
