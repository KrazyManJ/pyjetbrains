import os.path
import subprocess
from enum import Enum

JETBRAINS_FOLDER_PATH = os.path.join("C:\\","Program Files","JetBrains")

class IDEInfo:
    def __init__(self, folderName, executable):
        self.folderName = folderName
        self.executable = executable

    def is_installed(self):
        return len([i for i in os.listdir(JETBRAINS_FOLDER_PATH) if self.folderName in i]) > 0

    def path(self):
        if not self.is_installed():
            return None
        ide_folder = os.path.join(JETBRAINS_FOLDER_PATH, [i for i in os.listdir(JETBRAINS_FOLDER_PATH) if self.folderName in i][0])
        exe = os.path.join(ide_folder, "bin", f"{self.executable}.exe")
        return exe

class IDE(Enum):
    PYCHARM = IDEInfo("PyCharm", "pycharm64")
    INTELLIJ_IDEA = IDEInfo("IntelliJ IDEA", "idea64")
    PHPSTORM = IDEInfo("PhpStorm", "phpstorm64")
    RIDER = IDEInfo("JetBrains Rider", "rider64")

def open(ide, *paths):
    subprocess.Popen([ide.value.path(),*paths])
