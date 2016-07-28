import sys
from cx_Freeze import setup, Executable

build_exe_options = {
"include_msvcr": True   #skip error msvcr100.dll missing
}

base=None

if sys.platform=='win32':
    base="WIN32GUI"


setup(  name = "PR to SimulReflec",
        version = "1.0",
        description = "A program for merging reflectometry .dat files into a suitable format for SimulReflec",
        options = {"build_exe": build_exe_options},
        executables = [Executable("PRtoSimulReflec.pyw", base=base)])
