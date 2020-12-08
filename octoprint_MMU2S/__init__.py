# coding=utf-8
from __future__ import absolute_import
import serial# needs pyserial installed
import octoprint.plugin


### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import octoprint.printer

class Mmu2sPlugin(octoprint.plugin.SettingsPlugin,
                  octoprint.plugin.AssetPlugin,
                  octoprint.plugin.TemplatePlugin,
                  octoprint.plugin.SimpleApiPlugin):

    def __init__(self):
        self.currentMaterial = 99
        self.runinDistance = 350.0
        self.overdriveX = -100.0
        self.overdriveY = -50.0
        self.initialized = 0
        self.currentTemperature = 0.0
        self.yaxisPositions = [19.5, 16.0, 0.0, 0.0, 0.0]
        self.xaxisPositions = [0, 14, 28, 42, 56]
        self.ser = serial.Serial("/dev/ttyUSB1",250000)
        if not self.ser.write("M92 X400 Y100 E143.784\n".encode("utf-8")):
            self._logger.info("failed to serial write")

    ##~~ SettingsPlugin mixin
    def get_settings_defaults(self):
        return dict(
            # put your plugin's default settings here
        )

    ##~~ AssetPlugin mixin
    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/MMU2S.js"],
            css=["css/MMU2S.css"],
            less=["less/MMU2S.less"]
        )

    def get_api_commands(self):
        return dict(
            initializeMMU2S=[],
            unloadAllFilament=[],
            unloadCurrentFilament=[],
            loadFilament=["material"]
        )

    def unloadFromPrinter(self):
        # Stub
        return

    def loadIntoPrinter(self):
        # Stub
        return

    def isPrinterHot(self):
        if self.currentTemperature > 200:
            return 1
        else:
            return 0

    def on_api_command(self, command, data):
        if not self.isPrinterHot():
            self._logger.debug("Printer must be hot before MMU2S can be used")
            return
        if command == "unloadAllFilament":
            self.unloadAllFilament()
        elif command == "initializeMMU2S":
            self.initializeMMU2S()
        elif command == "loadFilament":
            self.loadFilament(data["material"])

    def initializeMMU2S(self):
        self._logger.info("initializing MMU2S properties")
        self.initialized = 1
        if not self.ser.write(("G1 Y" + str(self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("failed to serial write")
        elif not self.ser.write("M83\n".encode("utf-8")):
            self._logger.info("failed to serial write")
        self.unloadAllFilament()
        self._logger.debug("Succesful Initialization")

    def unloadAllFilament(self):
        if not self.initialized:
            self._logger.info("MMU2S must be initialized before changing filament")
            return
        self._logger.info("unloading filament")
        self.unloadFromPrinter()
        if not self.ser.write("G1 Y" + str(self.yaxisPositions[0] + self.overdriveY) + "\n".encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 E-" + str(self.runinDistance) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 Y" + str(self.yaxisPositions[1] + self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 E-" + str(self.runinDistance) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 Y" + str(self.yaxisPositions[2] + self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 E-" + str(self.runinDistance) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 Y" + str(self.yaxisPositions[3] + self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 E-" + str(self.runinDistance) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 Y" + str(self.yaxisPositions[4] + self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        elif not self.ser.write(("G1 E-" + str(self.runinDistance) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
        self.currentMaterial = 101
        if not self.ser.write(("G1 X" + str(self.overdriveX) + " Y" + str(self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")

    def loadFilament(self, material):
        if not self.initialized:
            self._logger.info("MMU2S must be initialized before changing filament")
            return
        elif not (self.currentMaterial == 101) or (self.currentMaterial == material) :
            if not self.unloadMaterial(self.currentMaterial):
                self._logger.info("Failed to unload material")
                return
        if material == 0:
            if self.currentMaterial == 0:
                return
            self._logger.info("Attempting to load material 0")
            if not self.ser.write(("G1 X" + str(self.xaxisPositions[0] + self.overdriveX) + " Y" + str(self.yaxisPositions[0] + self.overdriveY) + "\n").encode("utf-8")):
                self._logger.info("Serial command failed to write")
                return
            elif not self.ser.write(("G1 E" + str(self.runinDistance) + "\n").encode("utf-8")):
                self._logger.info("Serial command failed to write")
                return
            elif not self.ser.write(("G1 Y" + str(0 + self.overdriveY) + "\n").encode("utf-8")):
                self._logger.info("Serial command failed to write")
                return
            #TODO build in extruder feed
            self.currentMaterial = 0
        if material == 1:
            if self.currentMaterial == 1:
                return
            self._logger.info("Attempting to load material 1")
            if not self.ser.write(("G1 X" + str(self.xaxisPositions[1] + self.overdriveX) + " Y" + str(self.yaxisPositions[1] + self.overdriveY) + "\n").encode("utf-8")):
                self._logger.info("Serial command failed to write")
                return
            elif not self.ser.write(("G1 E" + str(self.runinDistance) + "\n").encode("utf-8")):
                self._logger.info("Serial command failed to write")
                return
            elif not self.ser.write(("G1 Y" + str(0 + self.overdriveY) + "\n").encode("utf-8")):
                self._logger.info("Serial command failed to write")
                return
            self.loadIntoPrinter()
            self.currentMaterial = 1

    def unloadMaterial(self, material):
        self.unloadFromPrinter()
        if not self.ser.write(("G1 Y" + str(self.yaxisPositions[material] + self.overdriveY) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
            return 0
        elif not self.ser.write(("G1 E-" + str(self.runinDistance) + "\n").encode("utf-8")):
            self._logger.info("Serial command failed to write")
            return 0
        return 1

    ##~~ Softwareupdate hook
    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return dict(
            MMU2S=dict(
                displayName="MMU2S Controller",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="Andrewjp97",
                repo="MMU2S-Clone",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/Andrewjp97/MMU2S-Clone/archive/{target_version}.zip"
            )
        )

    def get_temps(self, comm, parsed_temps):
        self._logger.debug('Temps received')  # Log that temps have been received
        temps = parsed_temps
        if temps == parsed_temps:
            self.currentTemperature = parsed_temps['T0'][0]  # Start the threading Timer object
        return parsed_temps  # return the temps to octoprint

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
# __plugin_name__ = "Mmu2s Plugin"

# Starting with OctoPrint 1.4.0 OctoPrint will also support to run under Python 3 in addition to the deprecated
# Python 2. New plugins should make sure to run under both versions for now. Uncomment one of the following
# compatibility flags according to what Python versions your plugin supports!
#__plugin_pythoncompat__ = ">=2.7,<3" # only python 2
#__plugin_pythoncompat__ = ">=3,<4" # only python 3
#__plugin_pythoncompat__ = ">=2.7,<4" # python 2 and 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Mmu2sPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
        "octoprint.comm.protocol.temperatures.received": __plugin_implementation__.get_temps
    }
