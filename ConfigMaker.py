import ConfigParser, os.path, sys


def add_section(config, section):
    if not config.has_section(section):
        config.add_section(section)

def getLn(prompt, config, section, option, specific = None, default = False):
    def validate(input):
        if not specific:
            return True
        elif isinstance(specific, list):
            return input.lower() in specific
        elif callable(specific):
            return specific(input)
        else:
            return p != ''
            
    if config.has_option(section, option):
        defValue = config.get(section, option)
    elif default:
        defValue = default
    else:
        defValue = False
    
    if defValue:
        p = raw_input('%s [%s]: ' % (prompt, defValue)).strip()
        if not p:
            config.set(section, option, defValue)

    else:
        p = raw_input('%s: ' % (prompt)).strip()
    
    if p:
        if not validate(p):
            print "That doesn't look like the right type of value. Try again?!"
            return getLn(prompt, config, section, option, specific)
        config.set(section, option, p)


config = ConfigParser.RawConfigParser()

print "TailBot automatic configuration generator."

try:
    configFile = sys.argv[1]
except:
    configFile = 'config.cfg'

print "Using configuration file %s" % configFile

if os.path.exists(configFile):
    config.read(configFile)
    
print "Configuring IRC Connection:"
add_section(config, 'ircd')

getLn("server", config, 'ircd', 'server')
getLn("ssl", config, 'ircd', 'ssl', ['true', 'false'], 'false')

ssl = config.getboolean('ircd', 'ssl')
getLn("port", config, 'ircd', 'port', lambda s: s.isdigit(), 6697 if ssl else 6667)
getLn("nickname", config, 'ircd', 'nickname', default = 'TailBot')
getLn('channels (seperate with ,)', config, 'ircd', 'channel', lambda s: all([s.startswith('#') for s in s.split(',')]), '#tail')
print "Files to tail, seperate files with a ';'"
add_section(config, 'files')
getLn('files', config, 'files', 'filenames')

print "Writing Configuration File",
config.write(open(configFile, 'wb'))
print '[DONE]'
