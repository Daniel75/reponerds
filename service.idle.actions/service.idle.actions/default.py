# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html


import xbmc
import xbmcgui
import xbmcaddon
addon = xbmcaddon.Addon("service.idle.actions")
ONE_PER_STARTUP_DONE = False
ONE_AFTER_TIMEOUT_DONE = False


class MyIdleActions(xbmcgui.Window):
    def __init__(self):
        global ONE_PER_STARTUP_DONE
        global ONE_AFTER_TIMEOUT_DONE
        
        IDLE_TIME = 0
        IS_IDLE = False
        
        while (not xbmc.abortRequested):
            TIMEOUT = int(addon.getSetting('on__idle_time_min'))*60
            
            if xbmc.getGlobalIdleTime() <= 5:
                IDLE_TIME = 0                
                ONE_AFTER_TIMEOUT_DONE = False

                if IS_IDLE:
                    if addon.getSetting('after__after_idle_action_enabled') == 'true':
                        self.afterIDLE()
                    IS_IDLE = False

            if IDLE_TIME > TIMEOUT:
                if addon.getSetting('on__service_enabled') == 'true':
                    if not xbmc.Player().isPlaying():
                        IS_IDLE = True

                        actiontype = addon.getSetting('on__action_type')

                        if actiontype == 'one per startup':
                            if not ONE_PER_STARTUP_DONE:
                                ONE_PER_STARTUP_DONE = True
                                self.onIDLE()

                        if actiontype == 'one after timeout':
                            if not ONE_AFTER_TIMEOUT_DONE:
                                ONE_AFTER_TIMEOUT_DONE = True
                                self.onIDLE()                            

                        if actiontype == 'repeat with timeout':
                            IDLE_TIME = 0
                            self.onIDLE()

                        if actiontype == 'one per second after timeout':
                            self.onIDLE()                                                    


            if xbmc.Player().isPlaying():
                IDLE_TIME = 0
            else:
                IDLE_TIME = IDLE_TIME + 1

            xbmc.sleep(1000)




    def onIDLE(self):
        action = addon.getSetting('on__action')
            
        if (action == 'Minimize') or (action == 'Quit') or (action == 'Powerdown') or (action == 'Hibernate') or (action == 'Suspend'):
            xbmc.executebuiltin('xbmc.' + action + '()')

        if (action == 'RunScript') or (action == 'RunAppleScript'):
            xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__file_scripts') + ', ' + addon.getSetting('on__optional_parameter') + ')')

        if (action == 'System.Exec') or (action == 'System.ExecWait'):
            if addon.getSetting('on__execute_file_cmd') == 'File':
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__file_execs') + ', ' + addon.getSetting('on__optional_parameter') + ')')
            if addon.getSetting('on__execute_file_cmd') == 'CMD':
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__cmd') + ')')

        if action == 'PlayMedia':
            windowtype = addon.getSetting('on__windowtype')
            if windowtype == 'Fullscreen':
                windowtypeint = 0
            if windowtype == 'Preview':
                windowtypeint = 1

            if addon.getSetting('on__type_playmedia') == 'Playlist':
                if addon.getSetting('on__isdir') == 'true':
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                else:
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__file_playmedia') + ', ' + str(windowtypeint) + ', ' + addon.getSetting('on__offset') + ')')

            if addon.getSetting('on__type_playmedia') == 'Audio/Video-File':
                if addon.getSetting('on__isdir') == 'true':
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                else:
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__file_playmedia') + ', ' + str(windowtypeint) + ')')

            if (addon.getSetting('on__type_playmedia') == 'URL'):
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__url_playmedia') + ', ' + str(windowtypeint) + ')')            

        if action == 'SlideShow':
            if addon.getSetting('on__slideshow_recursive'):
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__folder') + ', ' + 'recursive' + ', ' + addon.getSetting('on__slideshow_randomtype') + ')')
            else:
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__folder') + ', ' + addon.getSetting('on__slideshow_randomtype') + ')')

        if action == 'RecursiveSlideShow':
            xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__folder') + ')')

        if action == 'UpdateLibrary':
            if addon.getSetting('on__update_clean_library') == 'music':
                xbmc.executebuiltin('xbmc.' + action + '(music)')
            if addon.getSetting('on__update_clean_library') == 'video':
                xbmc.executebuiltin('xbmc.' + action + '(video' + ', ' + addon.getSetting('on__opt_fol__upd_vid_lib') + ')')

        if action == 'CleanLibrary':
            xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('on__update_clean_library') + ')')

        if action == 'PlayDVD':
            dvdstate = xbmc.getDVDState()
            dlg = xbmcgui.Dialog()
            if dvdstate == 1:                
                dlg.ok('Error', 'Drive not ready')
            elif dvdstate == 16:
                dlg.ok('Error', 'Tray open')
            elif dvdstate == 64:
                dlg.ok('Error', 'No media')
            else:
                xbmc.executebuiltin('xbmc.' + action + '()')

        # Future Gotham addition
##        if action == 'ActivateScreensaver':
##            xbmc.executebuiltin('xbmc.' + action + '()')


        xbmc.sleep(1000)
        if xbmc.Player().isPlaying():
            while (not xbmc.abortRequested):            
                TIMEOUT = int(addon.getSetting('on__idle_time_min'))
                IDLE_TIME = xbmc.getGlobalIdleTime()
                if IDLE_TIME < TIMEOUT:
                    xbmc.executebuiltin('xbmc.PlayerControl(Stop)')
                    break

            xbmc.sleep(1000)



    def afterIDLE(self):
        action = addon.getSetting('after__action')
            
        if (action == 'Minimize') or (action == 'Quit') or (action == 'Powerdown') or (action == 'Hibernate') or (action == 'Suspend'):
            xbmc.executebuiltin('xbmc.' + action + '()')

        if (action == 'RunScript') or (action == 'RunAppleScript'):
            xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__file_scripts') + ', ' + addon.getSetting('after__optional_parameter') + ')')

        if (action == 'System.Exec') or (action == 'System.ExecWait'):
            if addon.getSetting('after__execute_file_cmd') == 'File':
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__file_execs') + ', ' + addon.getSetting('after__optional_parameter') + ')')
            if addon.getSetting('after__execute_file_cmd') == 'CMD':
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__cmd') + ')')

        if action == 'PlayMedia':
            windowtype = addon.getSetting('after__windowtype')
            if windowtype == 'Fullscreen':
                windowtypeint = 0
            if windowtype == 'Preview':
                windowtypeint = 1

            if addon.getSetting('after__type_playmedia') == 'Playlist':
                if addon.getSetting('after__isdir') == 'true':
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                else:
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__file_playmedia') + ', ' + str(windowtypeint) + ', ' + addon.getSetting('after__offset') + ')')

            if addon.getSetting('after__type_playmedia') == 'Audio/Video-File':
                if addon.getSetting('after__isdir') == 'true':
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__folder_playmedia') + ', ' + str(windowtypeint) + ')')
                else:
                    xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__file_playmedia') + ', ' + str(windowtypeint) + ')')

            if (addon.getSetting('after__type_playmedia') == 'URL'):
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__url_playmedia') + ', ' + str(windowtypeint) + ')')            

        if action == 'SlideShow':
            if addon.getSetting('after__slideshow_recursive'):
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__folder') + ', ' + 'recursive' + ', ' + addon.getSetting('after__slideshow_randomtype') + ')')
            else:
                xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__folder') + ', ' + addon.getSetting('after__slideshow_randomtype') + ')')

        if action == 'RecursiveSlideShow':
            xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__folder') + ')')

        if action == 'UpdateLibrary':
            if addon.getSetting('after__update_clean_library') == 'music':
                xbmc.executebuiltin('xbmc.' + action + '(music)')
            if addon.getSetting('after__update_clean_library') == 'video':
                xbmc.executebuiltin('xbmc.' + action + '(video' + ', ' + addon.getSetting('after__opt_fol__upd_vid_lib') + ')')

        if action == 'CleanLibrary':
            xbmc.executebuiltin('xbmc.' + action + '(' + addon.getSetting('after__update_clean_library') + ')')

        if action == 'PlayDVD':
            dvdstate = xbmc.getDVDState()
            dlg = xbmcgui.Dialog()
            if dvdstate == 1:                
                dlg.ok('Error', 'Drive not ready')
            elif dvdstate == 16:
                dlg.ok('Error', 'Tray open')
            elif dvdstate == 64:
                dlg.ok('Error', 'No media')
            else:
                xbmc.executebuiltin('xbmc.' + action + '()')

        # Future Gotham addition
##        if action == 'ActivateScreensaver':
##            xbmc.executebuiltin('xbmc.' + action + '()')


        xbmc.sleep(1000)
        if xbmc.Player().isPlaying():
            while (not xbmc.abortRequested):            
                TIMEOUT = int(addon.getSetting('after__idle_time_min'))
                IDLE_TIME = xbmc.getGlobalIdleTime()
                if IDLE_TIME < TIMEOUT:
                    xbmc.executebuiltin('xbmc.PlayerControl(Stop)')
                    break

            xbmc.sleep(1000)


            

class MyMonitor(xbmc.Monitor):
    def onSettingsChanged(self):
        global ONE_PER_STARTUP_DONE
        global ONE_AFTER_TIMEOUT_DONE
        
        if ((addon.getSetting('on__action_type') == 'one per startup') or (addon.getSetting('on__action_type') == 'one after timeout')) and (addon.getSetting('on__service_enabled') == 'true'):
            dlg = xbmcgui.Dialog()
            if dlg.yesno('Activate Action?', 'Do you want to activate the action for the next time?'):
                ONE_PER_STARTUP_DONE = False
                ONE_AFTER_TIMEOUT_DONE = False
            else:
                ONE_PER_STARTUP_DONE = True
                ONE_AFTER_TIMEOUT_DONE = True
        


Monitor = MyMonitor()
IdleActions = MyIdleActions()
del IdleActions
