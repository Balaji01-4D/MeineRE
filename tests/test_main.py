import asyncio
import os
import unittest

from Meine.main import CLI


class main_test(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):

        self.a = "mk /home/balaji/testings/newlycreated.py"
        self.a_path = "/home/balaji/testings/newlycreated.py"
        self.del_a = "del /home/balaji/testings/newlycreated.py"
        self.b = "mkdir /home/balaji/testings/newly"
        self.b_path = "/home/balaji/testings/newly"
        self.del_b = "del /home/balaji/testings/newly"
        self.c = "rename /home/balaji/testings/pdf/50MB-TESTFILE.ORG.pdf as 50MB.pdf"
        self.c_path = "/home/balaji/testings/pdf/50MB.pdf"
        self.del_c = "del /home/balaji/testings/pdf/50MB.pdf"

    async def test_03_deleted(self):
        await CLI(self.del_a)
        await CLI(self.del_b)

        self.assertFalse(os.path.exists(self.a_path))
        self.assertFalse(os.path.exists(self.b_path))

    async def test_01_created(self):
        await CLI(self.a)
        await CLI(self.b)
        self.assertTrue(os.path.exists(self.a_path))
        self.assertTrue(os.path.exists(self.b_path))

    async def test_02_rename(self):
        await CLI(self.c)
        self.assertTrue(os.path.exists(self.c_path))


if __name__ == "__main__":
    unittest.main()
