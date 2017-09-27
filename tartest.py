import os
import tarfile
import gzip

tar = tarfile.open("ttar.tar.gz", "w:gz")
for root, dir, files in os.walk("F:\share\python"):
    for file in files:
        fullpath = os.path.join(root, file)
        tar.add(fullpath)
tar.close()
