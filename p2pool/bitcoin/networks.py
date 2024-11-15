import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack

nets = dict(
    ###Neisklar: IMPORTANT!!!!!!!!!!!!!1111!!11einself
    ###          The SUBSIDY_FUNC is NOT correctly in terms of keeping the minimum 1 FRQ
    ###          Reward for the end of the regular mining period. Means: it will work now
    ###          and some time in the future. I think a simple max(..., 1) around it will fix it
    ###          Maybe the dust threshold should also be rised somewhat, since we only have 5 decimals...
    cnotecoin=math.Object(
        P2P_PREFIX='05fea503'.decode('hex'),
        P2P_PORT=18491,
        ADDRESS_VERSION=28,
        RPC_PORT=18490,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'c-noteaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 100*100000000,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        BLOCK_PERIOD=100, # s
        SYMBOL='C-NOTE',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'CnoteCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/CnoteCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.c-note'), 'c-note.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://cnote.cryptorrency.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://cnote.cryptorrency.com/address/',
        ### Neisklar: normally 2**24 should be 2**20 BUT the cnotecoin enabled minerd is coded so that it only detects hashes below 0x000000xxxxxxx
        ###           and 2*20 would be 0x00000FFFF, maybe changing that in the miner  would be a good idea for slower ones... 
		### Update:   the minerd is (at least in GitHub) updated so that it would also detect targets below 2**24 (0x000000xxxx..), (FairQuarks starts with 2**20 (0x00000xxxx...))
		###           maybe for new standalone p2pools it's a good choice at the beginning, but ONLY when new hashing power is gradually added...
        #SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**24 - 1), 
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**20 - 1), 
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),
    cnotecoin_testnet=math.Object(
        P2P_PREFIX='011a39f7'.decode('hex'),
        P2P_PORT=18371,
        ADDRESS_VERSION=119,
        RPC_PORT=18372,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'cnotecoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2048*100000000 >> (height + 1)//60480,
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        BLOCK_PERIOD=30, # s
        SYMBOL='tFRQ',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'FairQuark') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/FairQuark/') if platform.system() == 'Darwin' else os.path.expanduser('~/.cnotecoin'), 'cnotecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://none.yet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://none.yet/address/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**24 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),
    ### Neisklar: that local one was a local testnet
    #fairquark_local=math.Object(
        #P2P_PREFIX='011a39f7'.decode('hex'),
        #P2P_PORT=19333,
        #ADDRESS_VERSION=119,
        #RPC_PORT=19334,
        #RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
        #    'fairquarkaddress' in (yield bitcoind.rpc_help()) and
        #    (yield bitcoind.rpc_getinfo())['testnet']
        #)),
        #SUBSIDY_FUNC=lambda height: 2048*100000000 >> (height + 1)//60480,
        #BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        #POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('quark_hash').getPoWHash(data)),
        #BLOCK_PERIOD=30, # s
        #SYMBOL='tFRQ',
        #CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'FairQuark') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/FairQuark/') if platform.system() == 'Darwin' else os.path.expanduser('~/fairquark-testnet-box/1/'), 'fairquark.conf'),
        #BLOCK_EXPLORER_URL_PREFIX='https://none.yet/',
        #ADDRESS_EXPLORER_URL_PREFIX='https://none.yet/',
        #SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**24 - 1),
        #DUMB_SCRYPT_DIFF=1,
        #DUST_THRESHOLD=1e8,
    #),	

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
