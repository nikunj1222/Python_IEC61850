# Python_IEC61850

This python library is build from mzAutomation pyiec61850 lib **(https://github.com/mz-automation/libiec61850)**.

The idea of this lib is to create some python code for IEC61850 implemenatation.


Following files were built from mzAutomation library for Windows :

_iec61850.exp
_iec61850.lib
_iec61850.pyd
iec61850.py

The example show some basic scripting capablities which can be developed for testing and troubleshooting IEC61850 servers.

More ideas are welcome.

Currently I am developing this library as per my needs.



**Building python library**
 
Install the following programs
**CMAKE https://cmake.org/download/
Swig https://swig.org/download.html 
Version > Python 3.6.8**
Make sure these programs are in the system path as shown below:
C:\Python36\Scripts;C:\Python36;C:\Python36\libs;C:\Program Files\Git\cmd;C:\Program Files\CMake\bin;C:\swigwin-4.0.1;C: \MinGW\bin

Open the Cmake application and download all the basic packages 

Download libiec61850 from the following link:
https://github.com/mz-automation/libiec61850

Open the CMAKE application and in source specify where the libiec61850 library is saved, in build the binaries specify the folder where it will be saved

In CMAKE press the configure button and select VisualStudio15 2017 option, press finish.

In the window that appears select BUILD_PYTHON_BINDINGS and deselect BUILD_EXAMPLES since if selected this generates an error

Press configure again and then generate.

This will generate in visual studio solution project in build folder defined in the CMAKE application.

2 files ** _iec61850.pyd and iec61850.py** will be created, copy these files to the address C:\Python36\Lib\site-packages

3 Open the the solution in VisualStudio 2017 and build the solution. After successful building following files is created.
**_iec61850.exp _iec61850.lib**
