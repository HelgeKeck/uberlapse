import subprocess
import logging

class Uberlapse:

    def __init__(self, config):
        self.name = config.get_name().split()[-1]
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.timeout = config.getfloat('timeout', 2., above=0.)
        self.url = "http://192.168.0.10:9090"
        self.endpoint = ""
        self.gcode.register_command('UL_SNAPSHOT', self.cmd_UL_SNAPSHOT, desc=("Calls the uberlapse server to take a image"))
        self.gcode.register_command('UL_RENDER', self.cmd_UL_RENDER, desc=("Calls the uberlapse server to start the timelapse rendering"))
        self.gcode.register_command('UL_RESET', self.cmd_UL_RESET, desc=("Calls the uberlapse server to reset it"))

    def cmd_UL_SNAPSHOT(self, param):
        self.endpoint = "/capture"
        self._call_URL(self)

    def cmd_UL_RENDER(self, param):
        self.endpoint = "/render"
        self._call_URL(self)

    def cmd_UL_RESET(self, param):
        self.endpoint = "/reset"
        self._call_URL(self)

    def _call_URL(self, param):
        reactor = self.printer.get_reactor()

        try:
            proc = subprocess.Popen("wget " + self.url + self.endpoint, shell=True)
        except Exception:
            logging.exception("Uberlapse: Command {%s} failed" % (self.name))
            raise self.gcode.error("Error calling url {%s}" % (self.url + self.endpoint))

        eventtime = reactor.monotonic()
        endtime = eventtime + self.timeout
        complete = False
        while eventtime < endtime:
            eventtime = reactor.pause(eventtime + .05)
            if proc.poll() is not None:
                complete = True
                break
        if not complete:
            proc.terminate()

        self.gcode.respond_info('Ok\n')


def load_config(config):
    return Uberlapse(config)
