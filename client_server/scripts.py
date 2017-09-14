import consts
import utils


def textcleaner(in_file, out_file):
    command = [consts.SCRIPTS_DIR + 'run_cleaner.sh',
               in_file,
               out_file]
    return utils.run_process(command)


def tesseract(filename):
    command = [consts.SCRIPTS_DIR + 'run_tesseract.sh',
               filename]
    return utils.run_process(command)
