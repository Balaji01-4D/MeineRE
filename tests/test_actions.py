import unittest
from pathlib import Path
from Meine.Actions import File
import asyncio
import os
import shutil


class TestFile(unittest.IsolatedAsyncioTestCase):
    files = File()

    async def asyncSetUp(self):
        self.test_folder = Path('test_folder')
        self.test_file = self.test_folder / 'test_file.txt'
        self.test_destination = Path('destination')
        self.moving_file = self.test_folder / 'moving_file.py'
        self.moving_folder = self.test_folder / 'moving_folder'
        self.copying_file = self.test_folder / 'copying_file.c'
        self.copying_folder = self.test_folder / 'copying_folder'
        self.rename_file = self.test_folder / 'oldname.c'
        self.rename_folder = self.test_folder / 'oldfolder'
        
        await self.files.Create_Folder(self.test_folder)
        await self.files.Create_Folder(self.test_destination)

        await self.files.Create_Folder(self.moving_folder)
        await self.files.Create_Folder(self.copying_folder)
        await self.files.Create_Folder(self.rename_folder)

        await self.files.Create_File(self.moving_file)
        await self.files.Create_File(self.copying_file)
        await self.files.Create_File(self.rename_file)

    

    async def asyncTearDown(self):
        if (os.path.exists(self.test_file)):
            os.remove(self.test_file)
        if (os.path.exists(self.test_folder)):
            shutil.rmtree(self.test_folder)    
        if (os.path.exists(self.test_destination)):
            shutil.rmtree(self.test_destination)
        if (os.path.exists(self.moving_folder)):
            shutil.rmtree(self.moving_folder)    
        if (os.path.exists(self.copying_folder)):
            shutil.rmtree(self.copying_folder)



    async def test_create_folder(self):
        self.assertTrue(os.path.exists(self.test_folder))
        self.assertTrue(os.path.isdir(self.test_folder))
        self.assertTrue(os.path.exists(self.test_destination))
        self.assertTrue(os.path.isdir(self.test_destination))
        self.assertTrue(os.path.exists(self.moving_folder))
        self.assertTrue(os.path.isdir(self.moving_folder))
        self.assertTrue(os.path.exists(self.copying_folder))
        self.assertTrue(os.path.isdir(self.copying_folder))
        self.assertTrue(os.path.isdir(self.rename_folder))
    
    async def test_create_file(self):
        await self.files.Create_File(self.test_file)
        self.assertTrue(os.path.exists(self.test_file))
        self.assertTrue(os.path.isfile(self.test_file))
        self.assertTrue(os.path.exists(self.moving_file))
        self.assertTrue(os.path.exists(self.copying_file))
        self.assertTrue(os.path.isfile(self.moving_file))
        self.assertTrue(os.path.isfile(self.copying_file))          
        self.assertTrue(os.path.isfile(self.rename_file))
        self.assertTrue(os.path.exists(self.rename_file))


    async def test_delete_file(self):
        await self.files.Delete_File(self.test_file)
        self.assertFalse(os.path.exists(self.test_file))
        

    async def test_delete_folder(self):
        await self.files.Delete_Folder(self.test_folder)
        self.assertFalse(os.path.exists(self.test_folder))

    
    async def test_copy_folder(self):
        await self.files.Copy_Folder(self.copying_folder,self.test_destination)
        self.assertTrue(os.path.exists(self.test_destination / self.copying_folder.name))
        self.assertTrue(os.path.exists(self.copying_folder))

    async def test_move_folder(self):
        await self.files.Move_Folder(self.moving_folder,self.test_destination)
        self.assertTrue(os.path.exists(self.test_destination / self.moving_folder.name))
        self.assertFalse(os.path.exists(self.moving_folder))
    
    async def test_copy_file(self):
        await self.files.Copy_File(self.copying_file,self.test_destination)
        self.assertTrue(os.path.exists(self.test_destination / self.copying_file.name))
        self.assertTrue(os.path.exists(self.copying_file))

    async def test_move_file(self):
        await self.files.Move_Folder(self.moving_file,self.test_destination)
        self.assertTrue(os.path.exists(self.test_destination / self.moving_file.name))
        self.assertFalse(os.path.exists(self.moving_file))

    
    async def test_rename_file(self):
        newname = Path('newname.c')
        self.assertFalse(os.path.exists(newname))
        await self.files.Rename_file(self.rename_file,newname)
        self.assertTrue(os.path.exists(newname))
            
    async def test_rename_folder(self):
        newname = Path('newfolder')
        self.assertFalse(os.path.exists(newname))
        await self.files.Rename_file(self.rename_folder,newname)
        self.assertTrue(os.path.exists(newname))
        
    
    

if __name__ == '__main__':
    unittest.main()
    


        