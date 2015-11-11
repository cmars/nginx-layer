import os
import pwd
import shutil
from subprocess import check_call

from charmhelpers.core import hookenv, host
from charmhelpers.core.templating import render
from charmhelpers.fetch import apt_update, apt_install
from charms.reactive import hook, when, when_not, is_state, set_state, remove_state
from charms.reactive.helpers import data_changed
from charms.reactive.bus import get_states


@hook('install')
def install():
    apt_update()
    apt_install(['nginx'])


@hook('config-changed')
def config_changed():
    set_state('nginx.available')
    set_state('nginx.start')


@when('reverseproxy.available', 'nginx.started')
def setup(reverseproxy):
    services = reverseproxy.services()
    if not data_changed('reverseproxy.services', services):
        return
    config = hookenv.config()
    render(source="default",
        target="/etc/nginx/sites-available/default",
        owner="root",
        perms=0o644,
        context={
            'cfg': config,
            'services': services,
        })
    host.service_reload('nginx')


@when('nginx.start')
@when_not('nginx.started')
def start_nginx():
    host.service_start('nginx')
    set_state('nginx.started')


@when('nginx.started')
@when_not('nginx.start')
def stop_nginx():
    host.service_stop('nginx')
    remove_state('nginx.started')


@when('nginx.started')
def nginx_started():
    hookenv.open_port(80)
    hookenv.status_set('active', 'Ready')
