# -*- coding: utf-8 -*-

import platform
import re
import subprocess
import sys
import traceback
import os
import shutil
import glob
import time, datetime
import xbmc
import xbmcgui
import xbmcaddon

__addon__ = xbmcaddon.Addon()
__addonID__ = __addon__.getAddonInfo('id')
__addonname__ = __addon__.getAddonInfo('name')
__path__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')
__LS__ = __addon__.getLocalizedString
__IconOk__ = xbmc.translatePath(os.path.join(__path__, 'resources', 'media', 'disc.png'))
__IconError__ = xbmc.translatePath(os.path.join(__path__, 'resources', 'media', 'error.png'))

# PREDEFINES

# Platform and Version
OS = platform.system()
V = platform.version()

# max. Resolution: Full-HD, HDTV, SDTV (PAL), SDTV (NTSC)
MAXDIM = ['--maxWidth 1920 --maxHeight 1080', '--maxWidth 1280 --maxHeight 720', '--maxWidth 720 --maxHeight 576', '--maxWidth 720 --maxHeight 480']

# Encoding quality: High, Normal, Low
QUALITY = ['-q 18', '-q 20', '-q 22', '-q 24', '-q 26']

# Greyscaling (Black&White Sources)
BW = '--greyscale'

# foreign audiotracks
ALLTRACKS = '-a 1,2,3,4,5,6,7,8,9,10'

# Converts filesizes to a human readable format (e.g. 123456 bytes to 123.4 KBytes)

def fmt_size(num, suffix='Bytes'):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if abs(num) < 1024:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= float(1024)
    return "%.1f% s%s" % (num, 'T', suffix)

class LoungeRipper():

    class NoProfileEnabledException(Exception): pass
    class NoProfileSelectedException(Exception): pass
    class SystemSettingUndefinedException(Exception): pass
    class RemovableMediaNotPresentException(Exception): pass
    class MakemkvExitsNotProperlyException(Exception): pass
    class HandBrakeCLIExitsNotProperlyException(Exception): pass
    class RipEncodeProcessStatesToBGException(Exception): pass
    class AbortedRipCompletedException(Exception): pass
    class KillCurrentProcessCalledException(Exception): pass
    class CleanUpTempFolderException(Exception): pass
    class CouldNotFindValidFilesException(Exception): pass
    class CurrentProcessAbortedException(Exception): pass
    class UnexpectedGlobalError(Exception): pass

    def __init__(self):

        self.src = None
        self.destfolder = None
        self.extensions = ['*.mkv', '*.ts', '*.m2ts', '*.mp4', '*.mpg', '*.mpeg', '*.avi', '*.flv', '*.wmv', '*.264', '*.mov']
        self.task = None
        self.process_all = None

        # Profile settings

        self.profile = None
        self.ripper = None
        self.encoder = None

        # Other

        self.ProgressBG = xbmcgui.DialogProgressBG()
        self.Dialog = xbmcgui.Dialog()
        self.Monitor = xbmc.Monitor()

        self.getSystemSettings()

    def isComplete(self):
        return True if __addon__.getSetting('completition').upper() == 'TRUE' else False

    def setComplete(self, iscomplete):
        __addon__.setSetting('completition', 'true' if iscomplete else 'false')

    def getSystemSettings(self):
        self.ripper_executable = __addon__.getSetting('makemkvcon')
        self.encoder_executable = __addon__.getSetting('HandBrakeCLI')
        self.tempfolder = __addon__.getSetting('tempfolder').rstrip('\\')
        self.basefolder = __addon__.getSetting('basefolder')
        self.subfolder = True if __addon__.getSetting('subfolder').upper() == 'TRUE' else False
        self.del_tf = True if __addon__.getSetting('deltempfolder').upper() == 'TRUE' else False

        self.nativelanguage = __addon__.getSetting('nativelanguage')
        # Parse the 3 letter language code from selection
        self.lang3 = re.search( r"(.*\()(.*)\)", self.nativelanguage).group(2)

        self.updatelib = True if __addon__.getSetting('updatelib').upper() == 'TRUE' else False
        self.driveid = __addon__.getSetting('driveid')
        self.eject = True if __addon__.getSetting('eject').upper() == 'TRUE' else False

    def getUserProfile(self):
        _profiles = []
        if self.getProcessPID(self.ripper_executable) or self.getProcessPID(self.encoder_executable):
            _profiles.append(__LS__(30038))
        else:
            for _profile in ['p1_', 'p2_', 'p3_', 'p4_', 'p5_', 'p6_', 'p7_']:
                if __addon__.getSetting(_profile + 'enabled') == 'true':
                    _profiles.append(__addon__.getSetting(_profile + 'profilename'))
            if os.listdir(self.tempfolder) != []: _profiles.append(__LS__(30039))
            if not self.isComplete(): _profiles.append(__LS__(30062))
        if not _profiles:
            raise self.NoProfileEnabledException()

        _idx = xbmcgui.Dialog().select(__LS__(30010), _profiles)
        if _idx == -1:
            raise self.NoProfileSelectedException()

        self.profile = {}
        for _profile in ['p1_', 'p2_', 'p3_', 'p4_', 'p5_', 'p6_', 'p7_']:
            if __addon__.getSetting(_profile + 'profilename') == _profiles[_idx]:
                self.task = _profiles[_idx]
                self.profile['resolution'] = MAXDIM[int(__addon__.getSetting(_profile + 'resolution'))]
                self.profile['quality'] = QUALITY[int(__addon__.getSetting(_profile + 'quality'))]
                self.profile['mintitlelength'] = int(re.match('\d+', __addon__.getSetting(_profile + 'mintitlelength')).group()) * 60
                self.profile['mode'] = int(__addon__.getSetting(_profile + 'mode'))
                self.profile['foreignaudio'] = ALLTRACKS if __addon__.getSetting(_profile + 'foreignaudio').upper() == 'TRUE' else ''
                self.profile['blackandwhite'] = BW if __addon__.getSetting(_profile + 'blackandwhite').upper() == 'TRUE' else ''
                self.profile['additionalhandbrakeargs'] = __addon__.getSetting(_profile + 'additionalhandbrakeargs')

        if _profiles[_idx] == __LS__(30038):
            _procpid = self.getProcessPID(self.ripper_executable)
            if _procpid:
                self.notifyLog('Killing ripper process with PID %s' % _procpid)
                self.killProcessPID(_procpid, process=self.ripper_executable)
                self.setComplete(True)
            _procpid = self.getProcessPID(self.encoder_executable)
            if _procpid:
                self.notifyLog('Killing encoder process with PID %s' % _procpid)
                self.killProcessPID(_procpid, process=self.encoder_executable)
            raise self.KillCurrentProcessCalledException()
        if _profiles[_idx] == __LS__(30039):
            self.delTempFolder(force=True)
            raise self.CleanUpTempFolderException()
        if _profiles[_idx] == __LS__(30062):
            self.buildDestFileAndFolder()
            self.copyfile(os.path.join(self.tempfolder, self.src), os.path.join(self.destfolder, self.destfile))
            self.delTempFolder(file=os.path.join(self.tempfolder, self.src))

            if self.updatelib: xbmc.executebuiltin('UpdateLibrary(video)')

            raise self.AbortedRipCompletedException()

    def notifyLog(self, message, level=xbmc.LOGNOTICE):
        xbmc.log('[%s] %s' % (__addonID__, message.encode('utf-8')), level)
            
    # Function to write a traceback report to logfile

    def traceError(self, err, exc_tb):
        while exc_tb:
            tb = traceback.format_tb(exc_tb)
            self.notifyLog('%s' % err, level=xbmc.LOGERROR)
            self.notifyLog('in module: %s' % (sys.argv[0].strip() or '<not defined>'), level=xbmc.LOGERROR)
            self.notifyLog('at line:   %s' % traceback.tb_lineno(exc_tb), level=xbmc.LOGERROR)
            self.notifyLog('in file:   %s' % tb[0].split(",")[0].strip()[6:-1],level=xbmc.LOGERROR)
            exc_tb = exc_tb.tb_next            

    def checkSystemSettings(self):

        if not self.ripper_executable:
            raise self.SystemSettingUndefinedException()
        if not self.encoder_executable:
            raise self.SystemSettingUndefinedException()
        if not self.tempfolder:
            raise self.SystemSettingUndefinedException()
        if not self.basefolder:
            raise self.SystemSettingUndefinedException()

    def getProcessPID(self, process):
        if not process: return False
        if OS == 'Linux':
            _syscmd = subprocess.Popen(['pidof', process], stdout=subprocess.PIPE)
            PID = _syscmd.stdout.read().strip()
            return PID if PID > 0 else False
        elif OS == 'Windows':
            _tlcall = 'TASKLIST', '/FI', 'imagename eq %s' % os.path.basename(process)
            _syscmd = subprocess.Popen(_tlcall, shell=True, stdout=subprocess.PIPE)
            PID = _syscmd.communicate()[0].strip().split('\r\n')
            if len(PID) > 1 and os.path.basename(process) in PID[-1]:
                return PID[-1].split()[1]
            else: return False
        else:
            self.notifyLog('Running on %s, could not determine PID of %s' % (OS, process))
            return False

    def killProcessPID(self, pid, process=None):
        if OS == 'Linux':
            _syscmd = subprocess.call('kill -9 %s' % pid, shell=True)
        elif OS == 'Windows':
            _syscmd = subprocess.call('TASKKILL /F /IM %s' % os.path.basename(process), shell=True)
        else: pass

    def delTempFolder(self, force=False, file=None):
        #
        # delete old temp files recursive if there any, but only if there's no previous rip/encode running
        #
        if self.getProcessPID(self.ripper_executable) or self.getProcessPID(self.encoder_executable):
            self.notifyLog('Couldn\'t clearing up folder %s, ripper or encoder active' % self.tempfolder)
            return False
        elif not self.del_tf and not force:
            self.notifyLog('Not allowed clearing up folder %s due settings' % self.tempfolder)
            return False
        else:
            try:
                if file is None:
                    self.notifyLog('Clearing up folder %s' % self.tempfolder)
                    for item in os.walk(self.tempfolder, False):
                        for dir in item[1]:
                            path = os.path.join(item[0], dir)
                            if os.path.islink(path):
                                os.unlink(path)
                            else:
                                os.rmdir(path)

                        for file in item[2]:
                            path = os.path.join(item[0], file)
                            os.unlink(path)
                else:
                    self.notifyLog('Remove %s' % file)
                    if os.path.isfile(file): os.remove(file)

                # set interrupted flag to false because there is'nt to continue anymore
                self.setComplete(True)

            except Exception, e:
                pass

    def buildDestFileAndFolder(self, title=''):
        rips = []
        for ext in self.extensions: rips.extend(glob.glob(os.path.join(self.tempfolder, ext)))
        _fsize = 0
        if len(rips) == 1:
            _fsize = os.path.getsize(rips[0])
            self.src = os.path.basename(rips[0]).decode('utf-8')
            self.process_all = False
        elif len(rips) > 1:

            # Ask for multiple processing if it's not done before

            if self.del_tf and self.process_all is None:
                self.process_all = False if self.Dialog.yesno(__addonname__, __LS__(30059), autoclose=60000) == 0 else True
                self.notifyLog('Process multiple files: %s' % (self.process_all))
                
            self.notifyLog('More than one file present. Search for the largest file')
            for rip in rips:
                if os.path.getsize(rip) > _fsize:
                    self.src = os.path.basename(rip).decode('utf-8')
                    _fsize = os.path.getsize(rip)
            if self.profile['mode'] == 0 or self.profile['mode'] == 1:
                self.notifyLog('Suggest that %s with a size of %s is main movie' % (self.src, fmt_size(_fsize)))
        if _fsize > 0:
            _dest = datetime.datetime.now().strftime('%Y-%m-%d.%H-%M-%S')
            _basename = os.path.splitext(self.src)[0]
            if '_t0' in _basename: _basename = _basename[:-4]
            if 'title' in _basename and title == '':
                kb = xbmc.Keyboard('', __LS__(30030))
                kb.doModal()
                if kb.isConfirmed() and kb.getText() != '': _dest = kb.getText()
            elif not 'title' in _basename:
                _dest = _basename
            elif title:
                _dest = title

            _dest = _dest.replace('_', ' ')
            _w = ''
            for _wp in _dest.split(): _w += _wp.capitalize() + ' '
            _dest = _w.strip()

            self.destfile = _dest + '.mkv'
            if self.subfolder:
                self.destfolder = os.path.join(self.basefolder, _dest)
            else:
                self.destfolder = self.basefolder
            if not os.path.exists(self.destfolder): os.makedirs(self.destfolder)
        else:
            raise self.CouldNotFindValidFilesException()
    
    def pollSubprocess(self, process_exec, process, header):
        _val = ''
        message = __LS__(30063)
        _m = __LS__(30063)
        percent = 0
        _p = 0
        _startsb = time.mktime(time.localtime())
        self.ProgressBG.create('%s V.%s - %s' % (__addonname__, __version__, header), message)
        try:
            _comm = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
            while not xbmc.abortRequested or not self.Monitor.waitForAbort():
                while  _comm.poll() is None:

                    if xbmc.abortRequested or self.Monitor.abortRequested(): break
                    if percent != _p or message != _m:
                        if percent > 0.4 and message == 'Encoding':
                            _elapsed = time.mktime(time.localtime()) - _startsb
                            _remaining = datetime.timedelta(seconds=int(100 * _elapsed/percent - _elapsed))
                            self.ProgressBG.update(int(percent), '%s V.%s - %s' % (__addonname__, __version__, header), __LS__(30029) % (message, percent, _remaining))
                            self.notifyLog('%s: %s%% done (%s remaining)' % (message, percent, _remaining))
                        else:
                            self.ProgressBG.update(int(percent), '%s V.%s - %s' % (__addonname__, __version__, header), __LS__(30040) % (message, percent))
                            self.notifyLog('%s: %s%% done' % (message, percent))

                        _p = percent
                        _m = message

                    data = _comm.stdout.readline().decode('utf-8', 'ignore').split(':')
                    if 'PRGC' in data[0]:
                        _val = data[1].replace('\n', '').split(',')
                        message = _val[2].replace('"', '')
                    elif 'PRGT' in data[0]:
                        _val = data[1].replace('\n', '').split(',')
                        message = _val[2].replace('"', '')
                    elif 'PRGV' in data[0]:
                        _val = data[1].replace('\n', '').split(',')
                        percent = (int(_val[0]) * 100 / int(_val[2]))
                    elif 'Encoding' in data[0]:
                        message = data[0]
                        _val = data[1].replace('\n', '').split(',')
                        percent = float(re.match('^ [0-9]+(\.[0-9])', _val[1]).group())
                    elif 'MSG' in data[0]:
                        _val = data[1].replace('\n', '').split(',')
                        self.notifyLog( _val[3].replace('"', ''))
                    else:
                        pass

                self.ProgressBG.close()
                break
        except Exception, e:
            pass

        if self.ProgressBG is not None: self.ProgressBG.close()
        self.notifyLog('%s finished with status %s' % (process_exec, _comm.poll()))
        return _comm.poll()

    def copyfile(self, source, dest):
        self.setComplete(False)
        src_size = os.path.getsize(source)
        self.notifyLog('Start copying file to \'%s\'' % dest)
        self.ProgressBG.create('%s - %s' % (__addonname__, __version__), '')
        percent = 0
        if self.del_tf:
            self.ProgressBG.update(percent, '%s - %s' % (__addonname__, __version__), __LS__(30040) % (__LS__(30041), percent))
            shutil.move(source, dest)
            percent = 100
            self.ProgressBG.update(percent, '%s - %s' % (__addonname__, __version__), __LS__(30040) % (__LS__(30041), percent))
        else:
            bf_size = 1024 * 1024 * 16
            bf_max = os.path.getsize(source) / bf_size
            bf_count = 0

            try:
                with open(source, 'rb') as src, open(dest,'wb') as dst:
                    while True:
                        _buffer = src.read(bf_size)
                        if not _buffer: break
                        if xbmc.abortRequested or self.Monitor.abortRequested(): break
                        dst.write(_buffer)
                        percent = int(100 * bf_count / bf_max)
                        self.ProgressBG.update(percent, '%s - %s' % (__addonname__, __version__), __LS__(30040) % (__LS__(30041), percent))
                        bf_count += 1

                    src.close()
                    dst.close()
                    self.notifyLog('Copying file to \'%s\' finished' % dest)
            except Exception, e:
                pass

        xbmc.sleep(1000)
        self.ProgressBG.close()

        if os.path.getsize(dest) != src_size:
            raise self.CurrentProcessAbortedException()
        else:
            self.setComplete(True)

    def start(self):

        self.notifyLog('Engage Lounge Ripper %s on %s %s' % (__version__, OS, V))
        self.checkSystemSettings()
        self.getUserProfile()

        if self.profile['mode'] == 0 or self.profile['mode'] == 1:
            #
            # RIP ONLY / RIP AND ENCODE
            #
            # Check if media is present in drive [driveno]
            # raise self.MediaIsNotPresentException if isn't

            _foundmedia = False
            _title = ''
            try:
                _rv = subprocess.check_output('"%s" info list -r' % self.ripper_executable, stderr=subprocess.STDOUT, shell=True)
            except subprocess.CalledProcessError, e:
                _rv = e.output

            for _line in iter(_rv.splitlines()):
                _item = _line.decode('utf-8').replace('"', '').split(',')
                if 'DRV:' in _item[0] and _item[5] != '':
                    self.notifyLog('Reported media on \'%s\': %s' % (_item[6], _item[5]))
                    _foundmedia = True
                    _title = _item[5]
                    break;

            if not _foundmedia: raise self.RemovableMediaNotPresentException()
            self.ripper = '"%s" mkv -r --messages=-stdout --progress=-same --decrypt disc:%s all --minlength=%s "%s"' % \
                          (self.ripper_executable,
                          self.driveid,
                          self.profile['mintitlelength'],
                          self.tempfolder)

            self.notifyLog('Ripper command line: %s' % self.ripper)

            _rv = self.pollSubprocess(self.ripper_executable ,self.ripper, _title)
            if _rv == None:
                if self.profile['mode'] == 0: self.setComplete(False)
                raise self.RipEncodeProcessStatesToBGException()
            if _rv != 0: raise self.MakemkvExitsNotProperlyException()
            if self.eject:
                xbmc.executebuiltin('EjectTray()')
                self.notifyLog('Eject disc')
            self.buildDestFileAndFolder(title=_title)

        if self.profile['mode'] == 0:
            #
            # RIP ONLY - WE ARE READY
            #
            self.notifyLog('Encoding of \'%s\' not required in this profile' % self.destfile)
            self.copyfile(os.path.join(self.tempfolder, self.src), os.path.join(self.destfolder, self.destfile))

        while True:
            if self.profile['mode'] == 1 or self.profile['mode'] == 2:
                #
                # RIP AND ENCODE / ENCODE ONLY
                #
                if self.profile['mode'] == 2:
                    #
                    # ENCODE ONLY - EXPECT FILE(S) IN TEMPFOLDER, USING LARGEST
                    #
                    self.buildDestFileAndFolder()

                # self.encoder = '"%s" -i "%s" -o "%s" -f mkv -d slower -N %s --native-dub -m -Z "High Profile" -s 1 %s %s %s %s %s 2>&1' % \
                self.encoder = '"%s" -i "%s" -o "%s" -f mkv --decomb fast -N %s --native-dub -m -Z "High Profile" -s 1 %s %s %s %s %s 2>&1' % \
                               (self.encoder_executable,
                               os.path.join(self.tempfolder, self.src),
                               os.path.join(self.destfolder, self.destfile),
                               self.lang3,
                               self.profile['foreignaudio'],
                               self.profile['quality'],
                               self.profile['blackandwhite'],
                               self.profile['resolution'],
                               self.profile['additionalhandbrakeargs'])

                self.notifyLog('Encoder command line: %s' % self.encoder)

                _rv = self.pollSubprocess(self.encoder_executable, self.encoder, self.destfile)
                if _rv == None:
                    raise self.RipEncodeProcessStatesToBGException()
                if _rv != 0:
                    raise self.HandBrakeCLIExitsNotProperlyException()
                #
                # READY
                #
            self.delTempFolder(file=os.path.join(self.tempfolder, self.src))
            self.Dialog.notification(__addonname__, __LS__(30049) % (__addonname__, self.task), __IconOk__)

            if self.process_all is None or not self.process_all: break

        if self.updatelib: xbmc.executebuiltin('UpdateLibrary(video)')
        self.notifyLog('switch off Lounge Ripper')

##############################################################################################################
###                                                                                                        ###
###                                                         MAIN                                           ###
###                                                                                                        ###
##############################################################################################################

Ripper = LoungeRipper()
try:
    Ripper.start()
except Ripper.NoProfileEnabledException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30050))
    Ripper.notifyLog('No profiles enabled', level=xbmc.LOGERROR)
except Ripper.NoProfileSelectedException:
    Ripper.notifyLog('No profile selected, exit %s' % __addonname__)
except Ripper.SystemSettingUndefinedException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30052))
    Ripper.notifyLog('One or more system settings are invalid', level=xbmc.LOGERROR)
except Ripper.CouldNotFindValidFilesException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30056) % Ripper.tempfolder)
    Ripper.notifyLog('Could not find any valid files in %s' % Ripper.tempfolder, level=xbmc.LOGERROR)
except Ripper.RemovableMediaNotPresentException:
    Ripper.notifyLog('Could not detect removable media or media isn\'t present or not readable', level=xbmc.LOGERROR)
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30057))
except Ripper.MakemkvExitsNotProperlyException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30053))
    Ripper.notifyLog('%s don\'t work as expected, possibly too old, key invalid or another error has occured' % Ripper.ripper_executable, level=xbmc.LOGERROR)
except Ripper.HandBrakeCLIExitsNotProperlyException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30054))
    Ripper.notifyLog('An error occured while encoding with %s' % Ripper.encoder_executable, level=xbmc.LOGERROR)
except Ripper.RipEncodeProcessStatesToBGException:
    Ripper.notifyLog('Rip/Encode processes turns into a background process')
    Ripper.notifyLog('After this toolchain may be broken and incomplete')
    Ripper.notifyLog('You can continue processing of toolchain afterwards')
except Ripper.AbortedRipCompletedException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30058))
    Ripper.notifyLog('A previous incomplete rip was completed')
except Ripper.KillCurrentProcessCalledException:
    Ripper.notifyLog('All current ripper and encoders terminated')
except Ripper.CleanUpTempFolderException:
    ok = Ripper.Dialog.ok(__addonname__, __LS__(30046) % Ripper.tempfolder)
    Ripper.notifyLog('Temporary folder %s cleaned' % Ripper.tempfolder)
except Ripper.CurrentProcessAbortedException:
    Ripper.notifyLog('Last operation could not completed. Check results', level=xbmc.LOGERROR)
except Exception, e:
    Ripper.traceError(e, sys.exc_traceback)
del Ripper

# ToDo:
#   New option: build ISO backup
#   ripper command:  makemkvcon backup -r --messages=-stdout --progress=-same --decrypt --cache=16 --noscan disc:0 /path/to/dirToBuild
#   ISO builder (BR): genisoimage -l -udf -allow-limited-size -input-charset utf-8 -o /path/to/output.iso /path/to/dirToBuild
#   ISO builder (DVD): genisoimage -dvd-video -o /path/to/output.iso /path/to/dirToBuild
#
#   ISO builder WIN: %PathToImgBurn% /MODE BUILD /BUILDMODE IMAGEFILE /SRC %SRC% /DEST %DEST% /FILESYSTEM "UDF" /UDFREVISION "2.50" \
#                    /VOLUMELABEL "%FolderNameOnly%" /CLOSE /NOIMAGEDETAILS /ROOTFOLDER "YES" /START
#
#   Linux: genisoimage has to be installed (apt-get genisoimage)
#   Windows: ImgBurn has to be installed
#
#   Determine if DVD or BR: use foldernames (VIDEO_TS, AUDIO_TS; BDMV, CERTIFICATE)