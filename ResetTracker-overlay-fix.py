import os, time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

file_paths = ['obs/EnterAvg.txt', 'obs/NPH.txt']
fix_paths = ['obs/EnterAvg_fix.txt', 'obs/NPH_fix.txt']

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File {event.src_path} has been modified")
        if os.path.basename(event.src_path) == os.path.basename(file_paths[0]):
            print("enterAvg")
            with open(event.src_path, mode='r') as f1:
                self.data = float(f1.read())
                print(round(self.data, 1))
                self.fixed_enterAvg = self.time_format(self.data)
                print(self.fixed_enterAvg)
                with open(fix_paths[0], 'w+') as f2:
                    f2.write(self.fixed_enterAvg)

        elif os.path.basename(event.src_path) == os.path.basename(file_paths[1]):
            print("NPH")
            with open(event.src_path, mode='r') as f1:
                self.data = float(f1.read())
                print(self.data)
                self.fixed_nph = round(self.data, 2)
                print(self.fixed_nph)
                with open(fix_paths[0], 'w+') as f2:
                    f2.write(str(self.fixed_nph))
                
    def time_format(self, number):
        minutes = int(number // 60)
        seconds = round((number - (minutes * 60)), 1)
        return f"{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    for afile in fix_paths:
        txtFile = open(afile, mode='w+')
        if afile == fix_paths[0]:
            txtFile.write(str("00:00.0"))
        else:
            txtFile.write(str("0.00"))
        txtFile.close()

    with open('obs/EnterCount.txt', mode='w+') as f:
        f.write(str("0"))

    event_handler = MyHandler()
    observer = Observer()

    print("start")

    observer.schedule(event_handler, path='obs', recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(100)
        observer.stop()
    finally:
        observer.stop()