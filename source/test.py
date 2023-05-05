import os

os.chdir(r"C:\Users\home\Desktop\python\schedule_project\mitp-project\source")

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Files in %r: %s" % (cwd, files))