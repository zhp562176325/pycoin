import unittest

from pycoin.key.Keychain import Keychain
from pycoin.key.subpaths import subpaths_for_path_range
from pycoin.symbols.btc import network as BitcoinMainnet

BIP32 = BitcoinMainnet.ui._bip32node_class


class KeychainTest(unittest.TestCase):

    def test_keychain(self):
        keychain = Keychain()
        bip32_list = [BIP32.from_master_secret(_) for _ in [b"foo", b"bar"]]
        for bip32 in bip32_list:
            keychain.add_key_paths(bip32.public_copy(), subpaths_for_path_range("0-1/0-10"))
        keychain.add_secrets(bip32_list)
        for bip32 in bip32_list:
            for path in ["0/5", "1/2", "0/9"]:
                subkey = bip32.subkey_for_path("0/5")
                v = keychain.get(subkey.hash160())
                self.assertEqual(v[0], subkey.secret_exponent())
        v = keychain.get(b'0' * 32)
        self.assertEqual(v, None)
