import time
import pytesseract
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

directory = 'media'


class LatestImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg') or event.src_path.endswith('.jpeg') or event.src_path.endswith('.png'):
            print(f"The latest uploaded image is now: {event.src_path}")
            print(f"{event.src_path}")
            img = cv2.imread(f"{event.src_path}")
            # print(img)
            config = ('-l eng --oem 1 --psm 3')
            text = pytesseract.image_to_string(img, config=config)
            # print text
            text = text.split('\n')
            print(text)

# Create a handler for file system events
event_handler = LatestImageHandler()

# Create an observer for the directory
observer = Observer()
observer.schedule(event_handler, directory, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
