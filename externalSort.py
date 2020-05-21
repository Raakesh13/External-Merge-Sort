import sys
import shutil
import os
import heapq
# from createFile import create_large_file


class heapnode:

    def __init__(
            self,
            line,
            fileHandler,
    ):
        self.line = line
        self.fileHandler = fileHandler


class externalMergeSort:
    def __init__(self, filePath, small_file_size, available_ram_size):
        self.filePath = filePath
        self.sorted_filehandlerheapnode_list = []
        self.currentDirectory = os.getcwd()
        self.sortedDirectoryPath = os.path.join(
            self.currentDirectory, "sortedFiles")
        self.noOfInputFiles = None
        self.small_file_size = small_file_size
        self.available_ram_size = available_ram_size

    def heapify(
            self,
            arr,
            i,
            n,
    ):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left].line < arr[i].line:
            smallest = left
        else:
            smallest = i

        if right < n and arr[right].line < arr[smallest].line:
            smallest = right

        if i != smallest:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            self.heapify(arr, smallest, n)

    def construct_heap(self, arr):
        l = len(arr) - 1
        mid = l // 2
        while mid >= 0:
            self.heapify(arr, mid, l)
            mid -= 1

    def mergeSortedtempFiles_low_level(self):
        heapnode_list = []
        sorted_output = []
        for filehandler in self.sorted_filehandlerheapnode_list:
            filehandler.seek(0, 0)
            line = filehandler.readline()
            heapnode_list.append(heapnode(line, filehandler))

        out = open("output.txt", "w")
        self.construct_heap(heapnode_list)
        with open('output.txt', 'a') as out:
            while True:
                _min = heapnode_list[0]
                if _min.line == "~~~~~~~~~~~":
                    break
                sorted_output.append(_min.line)
                fileHandler = _min.fileHandler
                line = fileHandler.readline()

                if not line:
                    line = "~~~~~~~~~~~"

                heapnode_list[0] = heapnode(line, fileHandler)
                self.heapify(heapnode_list, 0, len(heapnode_list))

                if sys.getsizeof(sorted_output) >= self.available_ram_size:
                    out.write(''.join(sorted_output))
                    sorted_output = []
            out.write(''.join(sorted_output))
        shutil.rmtree(self.sortedDirectoryPath)
        return "large file sorted"

    def splitAndSortFile(self):
        if os.path.exists(self.sortedDirectoryPath):
            shutil.rmtree(self.sortedDirectoryPath)
            os.mkdir(self.sortedDirectoryPath)
        else:
            os.mkdir(self.sortedDirectoryPath)

        with open(self.filePath, 'r') as file:
            buffer = file.readlines(self.small_file_size)
            buffer = sorted(buffer)
            while '\n' in buffer:
                buffer.remove('\n')
            while '' in buffer:
                buffer.remove('')
            i = 1
            while True:
                if not buffer:
                    break

                buffer = sorted(buffer)

                inputFile = open(self.sortedDirectoryPath +
                                 "/input"+str(i)+".txt", "w")
                inputFile.write(''.join(buffer))
                self.sorted_filehandlerheapnode_list.append(
                    open(self.sortedDirectoryPath + "/input"+str(i)+".txt", "r"))

                i += 1
                buffer = file.readlines(self.small_file_size)
            self.noOfInputFiles = i


if __name__ == '__main__':
    filepath = "/home/rakesh/Python_Projects/externalSorting/largefile.txt"
    smallfilesize = 1024*1024*100
    available_ram_size = 1024*1024*70
    ob = externalMergeSort(
        filePath=filepath, small_file_size=smallfilesize, available_ram_size=available_ram_size)
    ob.splitAndSortFile()
    ob.mergeSortedtempFiles_low_level()
