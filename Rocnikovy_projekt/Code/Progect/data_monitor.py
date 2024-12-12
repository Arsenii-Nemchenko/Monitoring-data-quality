import os.path


# DataMonitor class
class DataMonitor:
    def __init__(self, folder):
        self.folder = folder
        self.processed_files = set()


    def new_files(self):
        if os.path.exists(self.folder):
            all_files = [file for file in os.listdir(self.folder)]


            new_files = []
            for file in all_files:
                if not self.processed_files.__contains__(file):
                    new_files.append(os.path.join(self.folder, file))
                    self.processed_files.add(file)
            return new_files

        else:
            return []


t = DataMonitor(r"C:\Users\Arsen\Desktop\Rocnikovy_projekt")

print(t.new_files())