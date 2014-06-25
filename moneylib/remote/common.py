import os
import subprocess
import time
from contextlib import contextmanager

class XvfbException(Exception):
    pass

@contextmanager
def xvfb(display_num=12):
    display = ':' + str(display_num)

    if (os.path.exists('/tmp/.X{}-lock'.format(display_num)) or
            os.path.exists('/tmp/.X11-unix/X{}'.format(display_num))):
        raise XvfbException(('Cannot start Xvfb because display {} is already '
                'taken').format(display))

    with open('xvfb.log','w') as logfile:
        # create Xvfb process
        process = subprocess.Popen(['Xvfb', display, '-nolisten', 'tcp'],
                stdout=logfile, stderr=subprocess.STDOUT)
        time.sleep(2)
        if process.poll() != None:
            raise XvfbException(('Xvfb failed to start (return code: '
                    '{})').format(process.returncode))

        # set DISPLAY environment variable
        old_display = os.environ['DISPLAY'] if 'DISPLAY' in os.environ else None
        os.environ['DISPLAY'] = display

        try:
            # return to calling code
            yield

            if process.poll() != None:
                raise XvfbException(('Xvfb stopped running unexpectedly (return '
                    'code: {})').format(process.returncode))
        finally:
            # revert DISPLAY to old value
            if old_display == None:
                del os.environ['DISPLAY']
            else:
                os.environ['DISPLAY'] = old_display

            # stop process
            process.terminate()
