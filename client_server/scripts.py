import consts
import utils


def textcleaner(in_file, out_file):
    command = 'textcleaner -g -e stretch -f 25 -o 20 -t 30 -s 1 -T'.split()
    command.append(in_file)
    command.append(out_file)
    #command = [consts.SCRIPTS_DIR + 'run_cleaner.sh',
     #          in_file,
      #         out_file]
    return utils.run_process(command)


def tesseract(filename):
    command = ['tesseract', '-l', 'hb', '--tessdata-dir', '.', filename, 'stdout']
    return utils.run_process(command)

