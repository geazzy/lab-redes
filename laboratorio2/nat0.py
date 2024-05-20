from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI

def setupNetwork():
    net = Mininet(controller=Controller, switch=OVSKernelSwitch)

    # Adiciona um controlador
    info('*** Adicionando controlador\n')
    net.addController('c0')

    # Adiciona um switch
    info('*** Adicionando switch\n')
    s1 = net.addSwitch('s1')

    # Adiciona NAT
    info('*** Adicionando NAT\n')
    nat = net.addNAT().configDefault()
    
    # Adiciona hosts
    info('*** Adicionando hosts\n')
    h1 = net.addHost('h1', ip='10.0.0.10/24', defaultRoute='via 10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.20/24', defaultRoute='via 10.0.0.1')


    # Conecta os hosts ao switch
    info('*** Conectando hosts ao switch\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    # Inicia a rede
    info('*** Iniciando a rede\n')
    net.start()

    # Executa a CLI do Mininet
    info('*** Executando CLI\n')
    CLI(net)

    # Encerra a rede
    info('*** Encerrando a rede\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    setupNetwork()
