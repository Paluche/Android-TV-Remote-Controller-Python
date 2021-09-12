"""Module handling the search for an androidtvremote service using ZeroConf.
"""

from typing import Callable
from time import sleep
from zeroconf import ServiceBrowser, Zeroconf

BrowsingCallback = Callable[
    [str, list, int, dict],
    None
]

ANDROID_TV_REMOTE_SERVICE_TYPE = '_androidtvremote._tcp'

class BrowsingListener():
    def __init__(self, callback: BrowsingCallback):
        self.callback = callback
        self.services = {}

    def remove_service(self, zeroconf, type_, name):
        """remove_service. Method called when a service has been removed.

        :param zeroconf: Zeroconf instance that run the browsing.
        :param type_: Type of the service removed.
        :param name: Name of the service removed.
        """
        # no-op

    def add_service(self, zeroconf, type_, name):
        """add_service. Method called when a service has been added.

        :param zeroconf: Zeroconf instance that run the browsing.
        :param type_: Type of the service added.
        :param name: Name of the service added.
        """
        self.update_service(zeroconf, type_, name)

    def update_service(self, zeroconf, type_, name):
        """update_service. Method called when a service has been updated.

        :param zeroconf: Zeroconf instance that run the browsing.
        :param type_: Type of the service added.
        :param name: Name of the service added.
        """
        service_info = zeroconf.get_service_info(type_, name)

        device_name = name.split('.')[0]

        for address in service_info.addresses:
            self.callback(device_name,
                          address,
                          service_info.port,
                          service_info.properties)


def browse_for_android_tv_remote_service(callback, domain='local'):
    zeroconf = Zeroconf()
    listener = BrowsingListener(callback)
    search_type = f'{ANDROID_TV_REMOTE_SERVICE_TYPE}.{domain}.'
    browser = ServiceBrowser(zeroconf, search_type, listener=listener)


    sleep(15)
    browser.cancel()
