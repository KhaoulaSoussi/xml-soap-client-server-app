from zeep import Client
import sys
import time
from os import listdir, path
from os.path import join, isfile
import bisect

cloud = Client('src/main/resources/BackupService.wsdl').service

folder = sys.argv[1]
path_components = folder.split('/')
folder_name = path_components[-1]
folder_path = folder + '/'
response = cloud.create_backup_folder(folder_name)
print("RESPONSE FROM SERVICE PROVIDER ==> ", response)
files = listdir(folder_path)		# this holds all file names
files_count = len(files)
# I had to add the following condition to discard the .DS_Store file added to folders in mac
if ".DS_Store" in files:
    files_count -= 1

# The following loop iterates over all files and sends each to the server using the upload_file method
# sub-folders are not supported
for f in files:
    file_path = join(folder_path, f)
    if isfile(file_path) and f != ".DS_Store":
        file = open(file_path, "rb")
        byte = file.read()
        file_size = len(byte)
        print("Uploading", f, "to the cloud...")
        response = cloud.upload_file(f, file_size, byte)
        print("RESPONSE FROM SERVICE PROVIDER ==> ", response)

old_files = files
last_modified_list = []
for f in files:
    file_path = join(folder_path, f)
    last_modified = path.getmtime(file_path)
    last_modified_list.append(last_modified)

while True:
    current_files = listdir(folder_path)
    current_last_modified_list = []
    for f in current_files:
        file_path = join(folder_path, f)
        last_modified = path.getmtime(file_path)
        current_last_modified_list.append(last_modified)
    print("Checking if any files were added...")
    # Iterate over the current version of the local files
    for idx, current_file in enumerate(current_files):
        file_path = join(folder_path, current_file)
        # If there is a current file that does not exist in the list of old files, it must've been added
        if isfile(file_path) and current_file not in old_files:
            print("Uploading", current_file, "to the cloud...")
            file = open(file_path, "rb")
            byte = file.read()
            file_size = len(byte)
            # Send the file bytes to the server using the upload_file method
            response = cloud.upload_file(current_file, file_size, byte)
            print("RESPONSE FROM SERVICE PROVIDER ==> ", response)
            # update the sorted list of old files by inserting into it the recently added file
            bisect.insort(old_files, current_file)
            # update the list of last modified timestamps by inserting into it
            # the last_modified attribute of the recently added file
            last_modified_list.insert(idx, current_last_modified_list[idx])
    print("Checking if any files were deleted...")
    # Iterate over the list of old files
    for idx, old_file in enumerate(old_files):
        # If there is an old file that does not exist in the current files list, it must've been deleted
        if old_file not in current_files:
            ans = input("Are you sure you want to delete " + old_file + " permanently from the backup folder? (Y/N) ")
            # Send a delete request to the server if the user confirms the permanent deletion
            if ans == 'Y' or ans == 'y':
                response = cloud.delete_file(old_file)
                # update the list of last modified timestamps by removing from it
                # the last_modified attribute of the recently deleted file
                last_modified_list.pop(idx)
                # update the list of old files by removing from it the recently deleted file
                old_files.remove(old_file)
                print("Deleting", old_file, "from the cloud...")
                print("RESPONSE FROM SERVICE PROVIDER ==> ", response)

    print("Checking if any files were modified...")
    # Iterate in parallel over old files and current files
    for idx, current_file in enumerate(current_files):
        if current_file == ".DS_Store":
            continue
        file_path = join(folder_path, current_file)
        # If the last modified timestamp of a file is different from its timestamp in the old files list
        # It must've been modified
        if current_last_modified_list[idx] != last_modified_list[idx]:
            print("Updating", current_file, "on the cloud...")
            file = open(file_path, "rb")
            byte = file.read()
            file_size = len(byte)
            # Send the file bytes to the server using the upload_file method
            response = cloud.upload_file(current_file, file_size, byte)
            print("RESPONSE FROM SERVICE PROVIDER ==> ", response)

    # Update old files
    old_files = current_files
    # Clear and refill the last modified list
    last_modified_list.clear()
    for f in old_files:
        file_path = join(folder_path, f)
        last_modified = path.getmtime(file_path)
        last_modified_list.append(last_modified)
    time.sleep(5)
    print("5 SECONDS LATER!")
