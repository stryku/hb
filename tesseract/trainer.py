from subprocess import call

BUILD_DIR='build'
FONTa='Fake Receipt'
LANG='hb'
OUTPUTBASE = LANG + '.' + FONTa


def call_shell(command):
    splitted = command.split()
    call(splitted)
    print(command)


def text2image(text_file):
    splitted = str('text2image --text=' + text_file + ' --fonts_dir ..').split()
    splitted.append('--outputbase=' + OUTPUTBASE)
    splitted.append('--font=Fake Receipt')
    call(splitted)


def training():
    command = ['tesseract', OUTPUTBASE + '.tif', OUTPUTBASE, 'box.train.stderr']
    call(command)


def unicharset():
    command = ['unicharset_extractor',
               OUTPUTBASE + '.box']
    call(command)


def clustering():
    command = ['mftraining',
               '-F', '../font_properties',
               '-U', 'unicharset',
               OUTPUTBASE + '.tr']
    call(command)


def cntraining():
    command = ['cntraining', OUTPUTBASE + '.tr']
    call(command)


def cp_with_prefix(filename, prefix):
    call_shell('cp ' + filename + ' ' + prefix + '.' + filename)


def prepare_for_combine():
    cp_with_prefix('unicharset', LANG)
    cp_with_prefix('shapetable', LANG)
    cp_with_prefix('normproto', LANG)
    cp_with_prefix('inttemp', LANG)
    cp_with_prefix('pffmtable', LANG)


def combine():
    command = ['combine_tessdata', LANG + '.']
    call(command)


def copy_combined():
    name = LANG + '.traineddata'
    call_shell('cp ' + name + ' ../tessdata/' + name)


text2image('../training_text.txt')
training()
unicharset()
clustering()
cntraining()
prepare_for_combine()
combine()
copy_combined()
