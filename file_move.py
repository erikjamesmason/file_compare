import os
import shutil
import datetime
import logging
import zipfile

start_time = datetime.datetime.now()
print(start_time)


def all_tree_view(pathloc):
    for root, dirs, files in os.walk(pathloc):
        print("root: " + str(root))
        path = root.split(os.sep)
        print("path: " + str(path))
        print("other root: " + str(os.path.basename(root)))
        for file in files:
            print("file: " + str(file))

def replace_filename(parent):
    for root_dir, dirs, files in os.walk(parent):
        for f in files:
            file_title, ext = os.path.splitext(f)
            if "." in file_title:
                new_title = file_title.replace(".", "_")
                os.rename(
                    os.path.join(root_dir, f),
                    os.path.join(root_dir, new_title + ext)
                )


def copy_over_files(parent, src, dest):
    """This function targets a container (parent) directory, makes a zip folder at a certain location,
    then looks to another folder to make a list of files inside that folder.
    From there, it moves files around that are not in the list/log. A naive way
    to check for duplicates"""

    def unzip_file_move(container, destination, pattern):
        """ this takes the parent directory (container,
        the destination (where the extracted files will be placed,
        and the pattern of files to extract (in this case, zip).
        the script will walk (os.walk) through all directories in container,
        find the zip files, and extract them to the destination.
        Paired with move_up() function, it would extract the zip files
        and then place them in the container (parent directory)"""
        import fnmatch
        pattern = pattern
        print("starting unzip")
        for root_dir, dirs, files in os.walk(container):

            for filename in fnmatch.filter(files, pattern):
                print("Found zip file: % s: " % os.path.join(root_dir, filename))
                print("root dir of zip is: % s " % root_dir)
                print("ext part of zip is: % s " % filename)
                zipfile.ZipFile(os.path.join(root_dir, filename)).extractall(
                    os.path.join(destination, filename))
        print("finished unzip")

    unzip_file_move(parent, dest, "*.zip")

    def move_up_files(pathname):
        """This function moves up files from subdirectories in Source (src)
        to Destination (dst) which is the parent directory.
        The intention is to reduce amount of recursion from different subfolders.
        shutil.move() seems to be very slow, though."""

        print("starting move_up_files: ")
        folder = pathname
        subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]

        move_counter = 0
        for sub in subfolders:
            for f in os.listdir(sub):
                src = os.path.join(sub, f)
                dst = os.path.join(folder, f)
                shutil.move(src, dst)
                move_counter += 1
                print(move_counter)

        print("ending move_up_files: ")
        print(datetime.datetime.now() - start_time)
    move_up_files(src)

    def make_zip(location, name):
        today = datetime.datetime.now().strftime("%y-%m-%d")
        print("Creating Zip: ")
        files_zip = zipfile.ZipFile(str(location)
                                    + '_'
                                    + str(today)
                                    + '_'
                                    + str(os.path.split(name)[1])
                                    + '3.zip', 'w')

        print("created Zip at: ")
        print(location)
        print(name)
        return files_zip

    files_zip = make_zip(dest, src)

    def create_tracking_list(location):
        print("Creating tracking list: ")
        data_files = []
        for root, dirs, files in os.walk(location, topdown=True):
            for name in files:
                data_files.append(os.path.join(root, name))

            for name in dirs:
                data_files.append(os.path.join(root, name))

            return data_files

    data = create_tracking_list(dest)
    print("Tracking list complete")

    print("Starting File Move")
    for folder, _, files in os.walk(src):
        counter = 0
        for file in files:
            data = data
            log = open('file_move.log', 'r')
            if file not in log.read() and file not in data:

                files_zip.write(os.path.join(folder, file),
                                os.path.relpath(os.path.join(folder, file), src),
                                compress_type=zipfile.ZIP_DEFLATED)
                counter += 1
                print(str(counter) + ' - ' + str(file))
                filename = file
                logging.info(f'{filename}')
            else:

                pass
        print('Total files processed: ' + str(counter))
    files_zip.close()
    return files_zip


def move_files(source, destination):
    file_names = os.listdir(source)

    for file_name in file_names:
        print(file_name)

        destination = os.path.join(destination, file_name)
        shutil.move(os.path.join(source, file_name), destination)


def main():
    print('Timing Started: ')

    tdp = r'Y:\TDP\WIM_and_WS\WIM_Raw\raw_files'
    mscve = r'Y:\TDP\WIM_and_WS\WIM_Raw\MSCVE_RawData'
    # tdp = r'C:\Users\ejmason\Documents\Robocopy_Test\tdp_test'
    # mscve = r'C:\Users\ejmason\Documents\Robocopy_Test\mscve_test'
    root = r'Y:\TDP\WIM_and_WS\WIM_Raw'

    zipped = r'Y:\TDP\WIM_and_WS\WIM_Raw'

    logging.basicConfig(filename=r'C:\Users\ejmason\PycharmProjects\file_compare\file_move.log',
                        format='%(message)s',
                        filemode='a',
                        level=logging.INFO)

    filename = ''

    print("starting copy_over_files: ")
    copy_over_files(root, mscve, tdp)
    print(datetime.datetime.now() - start_time)
    print("ending copy_over_files: ")

    print('Total Time: ')
    print(datetime.datetime.now() - start_time)


if __name__ == '__main__':
    main()
