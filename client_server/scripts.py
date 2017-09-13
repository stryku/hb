import subprocess
import consts


def textcleaner(in_file, out_file):
    return subprocess.call([consts.SCRIPTS_DIR + 'run_cleaner',
                            in_file,
                            out_file])