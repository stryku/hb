import consts
import utils


def textcleaner(in_file, out_file):
    command = [consts.SCRIPTS_DIR + 'run_cleaner.sh',
               in_file,
               out_file]
    return utils.run_process(command)


def tesseract(filename):
    command = ['tesseract', '-l', 'hb', '--tessdata-dir', '.', filename, 'stdout']
    return utils.run_process(command)

