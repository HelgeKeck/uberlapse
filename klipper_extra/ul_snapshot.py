import logging
import subprocess

class UlSnapshot:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.gcode = self.printer.lookup_object('gcode')
        self.gcode.register_command('UL_SNAPSHOT', self.cmd_UL_SNAPSHOT, desc=("Calls the uberlapse server to take a image"))

    def cmd_UL_SNAPSHOT(self, gcmd):
        reactor = self.printer.get_reactor()
        try:
            proc = subprocess.Popen("wget http://192.168.0.199:9090/capture", shell=True)
        except Exception:
            logging.exception("shell_command: Command {%s} failed" % (self.name))
            raise self.gcode.error("Error running command {%s}" % (self.name))
        if self.verbose:
            self.proc_fd = proc.stdout.fileno()
            self.gcode.respond_info("Running Command {%s}...:" % (self.name))
            hdl = reactor.register_fd(self.proc_fd, self._process_output)
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
        if self.verbose:
            if self.partial_output:
                self.gcode.respond_info(self.partial_output)
                self.partial_output = ""
            if complete:
                msg = "Command {%s} finished\n" % (self.name)
            else:
                msg = "Command {%s} timed out" % (self.name)
            self.gcode.respond_info(msg)
            reactor.unregister_fd(hdl)
            self.proc_fd = None
        self.gcode.respond_info('Ok\n')
            

def load_config(config):
    return UlSnapshot(config)