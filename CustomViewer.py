import shutil
import sys

from PIL import Image, ImageShow

class CustomViewer(ImageShow.UnixViewer):
   format = "PNG"
   options = {"compress_level": 1}

   def get_command_ex(self, file, **options):
      command = executable = "feh"
      return command, executable

if shutil.which("feh"):
   print(f'Registering custom viewer for PIL')
   ImageShow.register(CustomViewer, order=-1) # Insert as primary viewer
