from direct.directnotify.DirectNotifyGlobal import directNotify
import fnmatch
import os
from panda3d.core import Multifile, Filename, VirtualFileSystem

import yaml


APPLICABLE_FILE_PATTERNS = ('*.mf', 'ambience.yaml')
CONTENT_EXT_WHITELIST = ('.jpg', '.jpeg', '.rgb', '.png', '.ogg', '.ttf')


class ContentPackError(Exception):
    pass


class ContentPacksManager:
    notify = directNotify.newCategory('ContentPacksManager')
    notify.setInfo(True)

    def __init__(self, filepath='contentpacks/', sortFilename='sort.yaml'):
        self.filepath = filepath
        self.sortFilename = os.path.join(self.filepath, sortFilename)

        if __debug__:
            self.mountPoint = '../resources'
        else:
            self.mountPoint = '/'

        self.vfs = VirtualFileSystem.getGlobalPtr()

        self.sort = []
        self.ambience = {}

    def isApplicable(self, filename):
        """
        Returns whether or not the specified file is applicable.
        """
        # Does this file exist?
        if not os.path.exists(os.path.join(self.filepath, filename)):
            return False

        # Does this file match one of the applicable file patterns?
        basename = os.path.basename(filename)
        for pattern in APPLICABLE_FILE_PATTERNS:
            if fnmatch.fnmatch(basename, pattern):
                return True

        return False

    def applyMultifile(self, filename):
        """
        Apply the specified multifile.
        """
        mf = Multifile()
        mf.openReadWrite(Filename(os.path.join(self.filepath, filename)))

        # Discard content with non-whitelisted extensions:
        for subfileName in mf.getSubfileNames():
            ext = os.path.splitext(subfileName)[1]
            if ext not in CONTENT_EXT_WHITELIST:
                mf.removeSubfile(subfileName)

        self.vfs.mount(mf, self.mountPoint, 0)

    def applyAmbience(self, filename):
        """
        Apply the specified ambience configuration file.
        """
        with open(os.path.join(self.filepath, filename), 'r') as f:
            self.ambience.update(yaml.load(f) or {})

    def apply(self, filename):
        """
        Apply the specified content pack file.
        """
        self.notify.info('Applying %s...' % filename)
        basename = os.path.basename(filename)
        if basename.endswith('.mf'):
            self.applyMultifile(filename)
        elif basename == 'ambience.yaml':
            self.applyAmbience(filename)

    def applyAll(self):
        """
        Using the sort configuration, recursively apply all applicable content
        pack files under the configured content packs directory.
        """
        # First, read the sort configuration:
        self.readSortConfig()

        # Next, apply the sorted files:
        for filename in self.sort[:]:
            if self.isApplicable(filename):
                self.apply(filename)
            else:
                self.notify.warning('Invalidating %s...' % filename)
                self.sort.remove(filename)

        # Apply the non-sorted files:
        for root, _, filenames in os.walk(self.filepath):
            root = root[len(self.filepath):]
            for filename in filenames:
                filename = os.path.join(root, filename).replace('\\', '/')

                # Ensure this file isn't sorted:
                if filename in self.sort:
                    continue

                # Ensure this file is applicable:
                if not self.isApplicable(filename):
                    continue

                # Apply this file, and add it to the sort configuration:
                self.apply(filename)
                self.sort.append(filename)

        # Finally, write the new sort configuration:
        self.writeSortConfig()

    def readSortConfig(self):
        """
        Read the sort configuration.
        """
        if not os.path.exists(self.sortFilename):
            return
        with open(self.sortFilename, 'r') as f:
            self.sort = yaml.load(f) or []

    def writeSortConfig(self):
        """
        Write the sort configuration to disk.
        """
        with open(self.sortFilename, 'w') as f:
            for filename in self.sort:
                f.write('- %s\n' % filename)

    def getAmbience(self, group):
        """
        Returns the ambience configurations for the specified group.
        """
        return self.ambience.get(group, {})
