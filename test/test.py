"""Unit test for pycp

You can set environnent variable DEBUG to 1
to not remove temporary directories created during test.

(Useful for diagnostic)
"""

import unittest
import tempfile  # for mkdtemp
import shutil
import pycp
import sys
import os
import time



class CpTestCase(unittest.TestCase):
    def setUp(self):
        """Put some empty files and directories in a temporary
        directory

        """
        cur_dir = os.path.abspath(os.path.dirname(__file__))
        cur_test = os.path.join(cur_dir, "test_dir")
        temp_dir = tempfile.mkdtemp("pycp-test")
        self.test_dir = os.path.join(temp_dir, "test_dir")
        shutil.copytree(cur_test, self.test_dir)
        self.previous_dir = os.getcwd()

    def test_zero(self):
        sys.argv=["pycp"]
        self.assertRaises(SystemExit, pycp.main, "copy")


    def test_cp_file_file(self):
        "a_file -> a_file.back"
        # cp a_file a_file.back
        a_file      = os.path.join(self.test_dir, "a_file")
        a_file_back = os.path.join(self.test_dir, "a_file.back")

        sys.argv = ["pycp", a_file, a_file_back]
        pycp.main("copy")
        self.assertTrue(os.path.exists(a_file_back))


    def test_cp_file_dir(self):
        "a_file -> b_dir"
        a_file = os.path.join(self.test_dir, "a_file")
        b_dir  = os.path.join(self.test_dir, "b_dir")
        os.mkdir(b_dir)
        sys.argv = ["pycp", a_file, b_dir]
        pycp.main("copy")
        dest = os.path.join(b_dir, "a_file")
        self.assertTrue(os.path.exists(dest))


    def test_cp_dir_dir_1(self):
        "a_dir -> b_dir (b_dir does not exist)"
        a_dir = os.path.join(self.test_dir, "a_dir")
        b_dir = os.path.join(self.test_dir, "b_dir")
        sys.argv = ["pycp", a_dir, b_dir]
        pycp.main("copy")
        c_file = os.path.join(b_dir, "c_file")
        d_file = os.path.join(b_dir, "c_file")
        self.assertTrue(os.path.exists(c_file))
        self.assertTrue(os.path.exists(d_file))

    def test_cp_dir_dir_2(self):
        "a_dir -> b_dir (b_dir exists)"
        a_dir = os.path.join(self.test_dir, "a_dir")
        b_dir = os.path.join(self.test_dir, "b_dir")
        os.mkdir(b_dir)
        sys.argv = ["pycp", a_dir, b_dir]
        pycp.main("copy")
        c_file = os.path.join(b_dir, "a_dir", "c_file")
        d_file = os.path.join(b_dir, "a_dir", "c_file")
        self.assertTrue(os.path.exists(c_file))
        self.assertTrue(os.path.exists(d_file))

    def test_no_source(self):
        "d_file -> d_file.back but d_file does not exists"
        d_file = os.path.join(self.test_dir, "d_file")
        sys.argv = ["pycp", d_file, "d_file.back"]
        self.assertRaises(SystemExit, pycp.main, "copy")


    def test_no_dest(self):
        "a_file -> d_dir but d_dir does not exists"
        a_file = os.path.join(self.test_dir, "a_file")
        d_dir  = os.path.join(self.test_dir, "d_dir/")
        sys.argv = ["pycp", a_file, d_dir]
        self.assertRaises(SystemExit, pycp.main, "copy")


    def test_several_sources_1(self):
        "a_file b_file c_file"
        a_file = os.path.join(self.test_dir, "a_file")
        b_file = os.path.join(self.test_dir, "b_file")
        c_file = os.path.join(self.test_dir, "c_file")
        sys.argv = ["pycp", a_file, b_file, c_file]
        self.assertRaises(SystemExit, pycp.main, "copy")


    def test_several_sources_2(self):
        "a_file b_file c_dir but c_dir does not exists"
        a_file = os.path.join(self.test_dir, "a_file")
        b_file = os.path.join(self.test_dir, "b_file")
        c_dir  = os.path.join(self.test_dir, "c_dir" )
        sys.argv = ["pycp", a_file, b_file, c_dir]
        self.assertRaises(SystemExit, pycp.main, "copy")


    def test_overwrite_1(self):
        "a_file -> b_file and b_file already exists (unsafe)"
        a_file = os.path.join(self.test_dir, "a_file")
        b_file = os.path.join(self.test_dir, "b_file")
        sys.argv = ["pycp", a_file, b_file]
        pycp.main("copy")
        b_file_desc = open(b_file, "r")
        b_contents  = b_file_desc.read()
        b_file_desc.close()
        self.assertEquals(b_contents, "a\n")


    def test_overwrite_2(self):
        "a_file -> b_file and b_file already exists (safe)"
        a_file = os.path.join(self.test_dir, "a_file")
        b_file = os.path.join(self.test_dir, "b_file")
        sys.argv = ["pycp", "--safe",  a_file, b_file]
        pycp.main("copy")
        b_file_desc = open(b_file, "r")
        b_contents  = b_file_desc.read()
        b_file_desc.close()
        self.assertEquals(b_contents, "b\n")


    def tearDown(self):
        """Remove the temporary directory

        """
        if os.environ.get("DEBUG"):
            print "not removing", self.test_dir
        else:
            shutil.rmtree(self.test_dir)




if __name__ == "__main__" :
    unittest.main()

