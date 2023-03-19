import os.path
import subprocess
from enum import Enum

import winapps


class IDEInfo:
    def __init__(self, folderName):
        self.folderName = folderName

    def is_installed(self):
        return len(list(winapps.search_installed(self.folderName))) > 0

    def path(self):
        if not self.is_installed():
            return None
        binFolder = os.path.join(next(winapps.search_installed(self.folderName)).install_location, "bin")
        return os.path.join(binFolder, [l for l in os.listdir(binFolder) if l.endswith("64.exe")][0])


class IDE(Enum):
    """
    Enumeration of all IDEs to use in all pyjetbrains functions
    """
    PYCHARM = IDEInfo("PyCharm")
    """IDE for Python"""
    INTELLIJ_IDEA = IDEInfo("IntelliJ IDEA")
    """IDE for Java"""
    PHPSTORM = IDEInfo("PhpStorm")
    """IDE for PHP"""
    RIDER = IDEInfo("JetBrains Rider")
    """IDE for C#"""
    WEBSTORM = IDEInfo("WebStorm")
    """IDE for HTML, CSS and JS"""
    CLION = IDEInfo("CLion")
    """IDE for C and C++"""
    GOLANG = IDEInfo("GoLang")
    """IDE for GoLang"""
    RUBYMINE = IDEInfo("RubyMine")
    """IDE for Ruby"""


class IDENotFoundError(Exception):
    __module__ = Exception.__module__


def is_installed(ide):
    """
    Checks if provided IDE is installed on device.
    :param ide: JetBrains IDE as type of Enumeration
    :return: true if IDE is installed, false otherwise
    """
    if not isinstance(ide, IDE):
        raise TypeError("ide parameter is not type of IDE")
    return ide.value.is_installed()


def open(ide, *paths, line=None, column=None):
    """
    Open an arbitrary file or folder in IDE, optionally specifying where to put the caret after opening.

    When you specify the path to a file, IDE opens it in the LightEdit mode, unless it belongs to a project that is already open or there is special logic to automatically open or create a project (for example, in case of Maven or Gradle files). If you specify a directory with an existing project, PyCharm opens this project. If you open a directory that is not a part of a project, PyCharm adds the .idea directory to it, making it a project.

    :param ide: IDE you want to open files with
    :param paths: Paths to files or folders you want to open
    :param line: Line position of caret cursor
    :param column: Column position of caret cursor
    :raise IDENotFoundError: if IDE is not installed on this device
    """
    if not is_installed(ide):
        raise IDENotFoundError(f"IDE '{ide.name}' is not installed on this device.")
    cmd = [ide.value.path()]
    if line is not None and isinstance(line, int):
        cmd += ["--line", str(line)]
    if column is not None and isinstance(column, int):
        cmd += ["--column", str(column)]
    subprocess.Popen(cmd + [*paths], creationflags=subprocess.CREATE_NO_WINDOW)
