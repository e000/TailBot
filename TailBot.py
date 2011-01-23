#!/usr/bin/env python

from twisted.internet.protocol import ReconnectingClientFactory
from twisted.words.protocols.irc import IRCClient
from twisted.internet import reactor
import FollowTail

class TailBot(IRCClient):
    def __init__(self):
        self.channelsIn = set()
    
    @property
    def nickname(self):
        return self.factory.nickname
    
    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)
        for tail, caller in self.factory.tails:
            caller.addCallback(self.fileUpdated)
            
    def connectionLost(self, reason):
        for tail, caller in self.factory.tails:
            caller.removeCallback(self.fileUpdated)
            
    def joined(self, channel):
        self.channelsIn.add(channel.lower())
        
    def left(self, channel):
        self.channelsIn.discard(channel.lower())
        
    def kickedFrom(self, channel, *a):
        self.channelsIn.discard(channel.lower())
        reactor.callLater(1, self.join, channel)
        
    def fileUpdated(self, line, filename):
        for channel in self.channelsIn:
            self.msg(channel, '[%s] %s' % (filename, line))
    
    
class TailBotFactory(ReconnectingClientFactory):
    protocol = TailBot
    def __init__(self, channels, nickname):
        self.tails = []
        self.channels = channels
        self.nickname = nickname
        
    def addTailFollower(self, filename):
        callback = FollowTail.ChainCallback()
        tail = FollowTail.FollowTail(filename, callback)
        self.tails.append((tail, callback))
        tail.start()
        
        
        