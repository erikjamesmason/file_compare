from filecmp import dircmp

# from: https://docs.python.org/3/library/filecmp.html

def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


tdp = r'Y:\TDP\WIM_and_WS\WIM_Raw\raw_files'
mscve = r'Y:\TDP\WIM_and_WS\WIM_Raw\MSCVE_RawData'
dcmp = dircmp(mscve, tdp)

print_diff_files(dcmp)
