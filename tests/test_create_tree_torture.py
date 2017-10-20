import os
import subprocess
from sys import exit, version_info
from unittest import main, TestCase

def run_command(command):
    try:
        output = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        message = output.stdout.read()
        output.stdout.close()
        output.TerminateProcess()
    except Exception as e:
        message = e
    return message

py_version = version_info.major

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
        command = ['bwfmetaedit', '--ISFT=', self.test_file]
        devnull = run_command(command)

        # create 100 sub folders
        for i in range(100):
            sub_folder = os.path.join(self.test_files_dir, 'subfolder%i' % i)
            if not os.path.exists(sub_folder):
                os.mkdir(sub_folder)
                self.assertTrue(os.path.exists(sub_folder))

            # create another test wav file in the sub folder
            sub_test_file = os.path.join(sub_folder, 'test.wav')
            if not os.path.exists(sub_test_file):
                create_command = 'ffmpeg -f lavfi -i sine=frequency=1000:duration=90 -ac 2 {}'.format(sub_test_file)
                command = create_command.split(' ')
                devnull = run_command(command)
            self.assertTrue(os.path.exists(sub_test_file))
            command = ['bwfmetaedit', '--ISFT=', sub_test_file]
            devnull = run_command(command)

    def tearDown(self):
        # remove 100 sub folders
        for i in range(100):
            sub_folder = os.path.join(self.test_files_dir, 'subfolder%i' % i)
            sub_test_file = os.path.join(sub_folder, 'test.wav')

            # remove the subfolder test file
            os.remove(sub_test_file)
            self.assertFalse(os.path.exists(sub_test_file))

            # remove the subfolder
            os.rmdir(sub_folder)
            self.assertFalse(os.path.exists(sub_folder))

        # remove the test file
        os.remove(self.test_file)

        # remove the test file directory
        try:
            os.rmdir(self.test_files_dir)
        except Exception as e:
            print(e)

    def test_create_tree(self):
        pass
        # # run create_tree.py
        # os.chdir(self.test_files_dir)
        # create_command = 'python {}'.format(os.path.join(self.main_directory, 'create_tree.py'))
        # command = create_command.split(' ')
        # devnull = run_command(command)
        # hash_file = self.test_file+'.md5'
        # self.assertTrue(os.path.exists(hash_file))
        #
        # # The actual test
        # if py_version == 3:
        #     with open(hash_file, encoding='utf-8') as md5_file1:
        #         text1 = md5_file1.read()
        #         self.assertEqual(text1[0], ';')
        #         self.assertIn('delete_me_if_i_exist.wav', text1)
        #         self.assertIn(self.md5_hash_for_90s_wav, text1)
        #     hash_file2 = os.path.join(self.test_files_dir, 'subfolder', 'test2.wav.md5')
        #     with open(hash_file2, encoding='utf-8') as md5_file2:
        #         text2 = md5_file2.read()
        #         self.assertEqual(text2[0], ';')
        #         self.assertIn('test2.wav', text2)
        #         self.assertIn(self.md5_hash_for_90s_wav, text2)
        # else:
        #     with open(hash_file) as md5_file1:
        #         text1 = md5_file1.read()
        #         self.assertEqual(text1[0], ';')
        #         self.assertIn('delete_me_if_i_exist.wav', text1)
        #         self.assertIn(self.md5_hash_for_90s_wav, text1)
        #     hash_file2 = os.path.join(self.test_files_dir, 'subfolder', 'test2.wav.md5')
        #     with open(hash_file2) as md5_file2:
        #         text2 = md5_file2.read()
        #         self.assertEqual(text2[0], ';')
        #         self.assertIn('test2.wav', text2)
        #         self.assertIn(self.md5_hash_for_90s_wav, text2)
        #
        # os.remove(os.path.join(self.sub_folder, 'test2.wav.md5'))
        # self.assertFalse(os.path.exists(os.path.join(self.sub_folder, 'test2.wav.md5')))
        # os.remove(hash_file)
        # os.chdir(self.main_directory)

main()
