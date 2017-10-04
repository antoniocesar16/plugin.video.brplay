# -*- coding: utf-8 -*-

import os
import sys
import urllib
import vod

from resources.lib.modules import control, cache
# from resources.lib.modules import trakt

sysaddon = sys.argv[0]
syshandle = int(sys.argv[1])

artPath = control.artPath() ; addonFanart = control.addonFanart()

# traktCredentials = trakt.getTraktCredentialsInfo()
# traktIndicators = trakt.getTraktIndicatorsInfo()

class navigator:
    def root(self):
        self.add_directory_item(32001, 'liveChannels', 'live.png', 'DefaultLive.png')
        self.add_directory_item(32002, 'vodChannels', 'ondemand.png', 'DefaultOnDemand.png')

        if control.is_globosat_available():
            self.add_directory_item(32080, 'featured', 'featured.png', 'DefaultMovies.png')
            self.add_directory_item(32090, 'favorites', 'favorites.png', 'DefaultMovies.png')
            self.add_directory_item(32095, 'watchlater', 'userlists.png', 'DefaultMovies.png')
            self.add_directory_item(32096, 'watchhistory', 'years.png', 'DefaultMovies.png')

        self.add_directory_item(32010, 'searchMenu', 'search.png', 'DefaultMovies.png')

        # control.addSortMethod(int(sys.argv[1]), control.SORT_METHOD_LABEL_IGNORE_FOLDERS)

        control.content(syshandle, 'files')

        self.end_directory()

    def searchMenu(self):
        control.idle()

        t = control.lang(32010).encode('utf-8')
        k = control.keyboard('', t); k.doModal()
        q = k.getText() if k.isConfirmed() else None

        if q is None or q == '': return

        url = '%s?action=search&q=%s&page=1' % (sys.argv[0], urllib.quote_plus(q))
        control.execute('Container.Update(%s)' % url)

    def search(self, query, page):
        vod.Vod().search(query, page)

    def clear_cache(self):
        control.idle()

        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')

        if not yes:
            return

        cache.delete_file()

        control.clear_credentials()

        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')

    def cache_auth(self):
        import resources.lib.modules.globosat.scraper_vod as scraper_vod

        cache.get(scraper_vod.get_authorized_channels, 1)

    def add_directory_item(self, name, query, thumb, icon, queue=False, isAction=True, isFolder=True):
        try: name = control.lang(name).encode('utf-8')
        except: pass
        url = '%s?action=%s' % (sysaddon, query) if isAction else query
        thumb = os.path.join(artPath, thumb) if not artPath is None else icon
        item = control.item(label=name)
        item.setArt({'icon': thumb, 'thumb': thumb})
        if not addonFanart is None: item.setProperty('Fanart_Image', addonFanart)
        control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)

    def end_directory(self):
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


