import os
import subprocess
import sys
from time import sleep
from unittest import main, TestCase

def ffmpeg_there():
    '''
    This function looks for ffmpeg and bwfmetaedit in the system path.

    This function was copied from a personal project, and then extended for
    windows compatibility here. https://github.com/jamessam/tomp3

    - Jim, 19 January 2017
    '''
    ffmpeg, bwfmetaedit = False, False

    f_command = ['ffmpeg', '-h']
    b_command = ['bwfmetaedit']

    # Look for FFMPEG
    try:
        output = subprocess.Popen(f_command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, universal_newlines=True)
        message = output.stdout.read()
        output.stdout.close()
        if 'ffmpeg version' in message:
            ffmpeg = True
    except FileNotFoundError:
        pass

    # Look for bwfmetaedit
    try:
        output = subprocess.Popen(b_command, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, universal_newlines=True)
        message = output.stdout.read()
        output.stdout.close()
        if 'Usage: "bwfmetaedit' in message:
            bwfmetaedit = True
    except FileNotFoundError:
        pass

    return ffmpeg, bwfmetaedit

ff, bwf = ffmpeg_there()
if not ff or not bwf:
    sys.exit('Please install FFMPEG and bwfmetaedit before you test these scripts.')


def run_command(command):
    try:
        output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        message = output.stdout.read()
        output.stdout.close()
    except Exception as e:
        message = e
    return message


class FunctionalTests(TestCase):
    md5_hash_for_90s_wav = 'a82ba680ec7dba3b5176dedbdf49a30d'
    main_directory = os.getcwd()
    test_files_dir = os.path.join(main_directory, 'test_files')

    def setUp(self):
        # setup the test file directory
        if not os.path.exists(self.test_files_dir):
            os.mkdir(self.test_files_dir)
        self.assertTrue(os.path.exists(self.test_files_dir))

        # create the test file
        self.test_file = os.path.join(self.test_files_dir, 'delete_me_if_i_exist.wav')
        if not os.path.exists(self.test_file):
            create_test_wav = 'ffmpeg -f lavfi -i sine=frequency=1000:duration=90 -ac 2 %s' % self.test_file
            command = create_test_wav.split(' ')
            devnull = run_command(command)
        self.assertTrue(os.path.exists(self.test_file))

        # rip out the ISFT field
        command = ['bwfmetaedit', '--ISFT=', self.test_file]
        devnull = run_command(command)

    def tearDown(self):
        # remove the test file
        os.remove(self.test_file)
        # remove the test file directory
        try:
            os.rmdir(self.test_files_dir)
        except Exception as e:
            print(e)

    def test_create(self):
        print('\nTesting create now\n')
        # create the test md5 file
        os.chdir(self.test_files_dir)
        create_command = 'python {}'.format(os.path.join(self.main_directory, 'create.py'))
        command = create_command.split(' ')
        devnull = run_command(command)
        hash_file = self.test_file+'.md5'
        self.assertTrue(os.path.exists(hash_file))

        # The actual test
        with open(hash_file, encoding='utf-8') as md5_file:
            text = md5_file.read()
            self.assertEqual(text[0], ';')
            self.assertIn('delete_me_if_i_exist.wav', text)
            self.assertIn(self.md5_hash_for_90s_wav, text)

        # remove the test file md5
        os.remove(hash_file)
        self.assertFalse(os.path.exists(hash_file))
        os.chdir(self.main_directory)
        sleep(0.5)

    def test_create_tree(self):
        print('\nTesting create_tree now\n')
        # create the sub folder
        sub_folder = os.path.join(self.test_files_dir, 'subfolder')
        if not os.path.exists(sub_folder):
            os.mkdir(sub_folder)
        self.assertTrue(os.path.exists(sub_folder))

        # create another test wav file in the sub folder
        os.chdir(sub_folder)
        if not os.path.exists(os.path.join(sub_folder, 'test2.wav')):
            create_command = 'ffmpeg -f lavfi -i sine=frequency=1000:duration=90 -ac 2 test2.wav'
            command = create_command.split(' ')
            devnull = run_command(command)
        self.assertTrue(os.path.exists(os.path.join(sub_folder, 'test2.wav')))
        command = ['bwfmetaedit', '--ISFT=', os.path.join(sub_folder, 'test2.wav')]
        devnull = run_command(command)

        # run create_tree.py
        os.chdir(self.test_files_dir)
        create_command = 'python {}'.format(os.path.join(self.main_directory, 'create_tree.py'))
        command = create_command.split(' ')
        devnull = run_command(command)
        hash_file = self.test_file+'.md5'
        self.assertTrue(os.path.exists(hash_file))

        # The actual test
        with open(hash_file, encoding='utf-8') as md5_file1:
            text1 = md5_file1.read()
            self.assertEqual(text1[0], ';')
            self.assertIn('delete_me_if_i_exist.wav', text1)
            self.assertIn(self.md5_hash_for_90s_wav, text1)
        hash_file2 = os.path.join(self.test_files_dir, 'subfolder', 'test2.wav.md5')
        with open(hash_file2, encoding='utf-8') as md5_file2:
            text2 = md5_file2.read()
            self.assertEqual(text2[0], ';')
            self.assertIn('test2.wav', text2)
            self.assertIn(self.md5_hash_for_90s_wav, text2)

        os.remove(os.path.join(sub_folder, 'test2.wav'))
        os.remove(os.path.join(sub_folder, 'test2.wav.md5'))
        self.assertFalse(os.path.exists(os.path.join(sub_folder, 'test2.wav')))
        self.assertFalse(os.path.exists(os.path.join(sub_folder, 'test2.wav.md5')))
        os.rmdir(sub_folder)
        os.remove(hash_file)
        sleep(0.5)

main()
