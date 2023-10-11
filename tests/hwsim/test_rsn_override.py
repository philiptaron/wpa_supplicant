# Test cases for RSNE/RSNXE overriding
# Copyright (c) 2023, Qualcomm Innovation Center, Inc.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import hostapd
from utils import *

def test_rsn_override(dev, apdev):
    """RSNE=WPA2-Personal/PMF-optional override=WPA3-Personal/PMF-required (with MLO parameters)"""
    check_sae_capab(dev[0])

    ssid = "test-rsn-override"
    params = hostapd.wpa2_params(ssid=ssid,
                                 passphrase="12345678",
                                 ieee80211w='1')
    params['rsn_override_key_mgmt'] = 'SAE SAE-EXT-KEY'
    params['rsn_override_pairwise'] = 'CCMP GCMP-256'
    params['rsn_override_mfp'] = '2'
    params['beacon_prot'] = '1'
    params['sae_groups'] = '19 20'
    params['sae_require_mfp'] = '1'
    params['sae_pwe'] = '2'
    hapd = hostapd.add_ap(apdev[0], params)
    bssid = hapd.own_addr()

    dev[0].scan_for_bss(bssid, freq=2412)
    bss = dev[0].get_bss(bssid)
    flags = bss['flags']
    if "PSK" in flags:
        raise Exception("Unexpected BSS flags: " + flags)
    if "-SAE+SAE-EXT-KEY-" not in flags:
        raise Exception("Unexpected BSS flags: " + flags)
    if "-GCMP-256+CCMP" not in flags:
        raise Exception("Unexpected BSS flags: " + flags)
    try:
        dev[0].set("sae_pwe", "2")
        dev[0].set("sae_groups", "")
        dev[0].connect(ssid, sae_password="12345678", key_mgmt="SAE",
                       ieee80211w="2", scan_freq="2412")
    finally:
        dev[0].set("sae_pwe", "0")

def test_rsn_override2(dev, apdev):
    """RSNE=WPA2-Personal/PMF-disabled override=WPA3-Personal/PMF-required (with MLO parameters)"""
    check_sae_capab(dev[0])

    ssid = "test-rsn-override"
    params = hostapd.wpa2_params(ssid=ssid,
                                 passphrase="12345678",
                                 ieee80211w='0')
    params['rsn_override_key_mgmt'] = 'SAE SAE-EXT-KEY'
    params['rsn_override_pairwise'] = 'CCMP GCMP-256'
    params['rsn_override_mfp'] = '2'
    params['beacon_prot'] = '1'
    params['sae_groups'] = '19 20'
    params['sae_require_mfp'] = '1'
    params['sae_pwe'] = '2'
    hapd = hostapd.add_ap(apdev[0], params)
    bssid = hapd.own_addr()

    dev[0].scan_for_bss(bssid, freq=2412)
    bss = dev[0].get_bss(bssid)
    flags = bss['flags']
    if "PSK" in flags:
        raise Exception("Unexpected BSS flags: " + flags)
    if "-SAE+SAE-EXT-KEY-" not in flags:
        raise Exception("Unexpected BSS flags: " + flags)
    if "-GCMP-256+CCMP" not in flags:
        raise Exception("Unexpected BSS flags: " + flags)
    try:
        dev[0].set("sae_pwe", "2")
        dev[0].set("sae_groups", "")
        dev[0].connect(ssid, sae_password="12345678", key_mgmt="SAE",
                       ieee80211w="2", scan_freq="2412")
    finally:
        dev[0].set("sae_pwe", "0")
