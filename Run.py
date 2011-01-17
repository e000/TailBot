import ConfigParser, os.path, sys, os
import TailBot
from twisted.internet import reactor
from twisted.python import log
log.startLogging(sys.stdout)
if __name__ == "__main__":
    
    try:
        configFile = sys.argv[1]
    except:
        configFile = 'config.cfg'

    try:
        config = ConfigParser.ConfigParser()
        config.read(configFile)
    except:
        print "Config File Not Found! [%s]" % configFile
        os.exit()
        
    try:
        server = config.get('ircd', 'server')
        port = config.getint('ircd', 'port')
        ssl = config.getboolean('ircd', 'ssl')
        channels = [c.strip() for c in config.get('ircd', 'channel').split(',')]
        nickname = config.get('ircd', 'nickname')
        files = [f.strip() for f in config.get('files', 'filenames').split(';')]
    except e:
        print "Invalid Configuration Directives! Run ConfigMaker.py [%s]" % e
        os.exit()
    
    print "[TailBot] starting with config file [%s]" % configFile
    print "Connecting to %s:%i [ssl=%s] as %s" % (server, port, ssl, nickname)
    print "Joining: %s" % (', '.join(channels))
    print "Tailing: %s" % (', '.join(files))
    
    factory = TailBot.TailBotFactory(channels, nickname)
    for file in files:
        factory.addTailFollower(file)
        
    if ssl:
        from twisted.internet import ssl
        reactor.connectSSL(server, port, factory, ssl.ClientContextFactory())
    else:
        reactor.connectTCP(server, port, factory)
        
    reactor.run()