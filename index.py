import time
import pytesseract
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from openai_functions import openai_response

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
directory = 'media'

initialResp = 'What is the correct answer out of the following:'

class LatestImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg') or event.src_path.endswith('.jpeg') or event.src_path.endswith('.png'):
            print(f"The latest uploaded image is now: {event.src_path}")
            print(f"{event.src_path}")
            img = cv2.imread(f"{event.src_path}")
            response = None
            try:
                config = ('-l eng --oem 1 --psm 3')
                text = pytesseract.image_to_string(img, config=config)
                print(text)
                text = text.split('\n')
                response = text
            except TypeError:
                print(f"Text could not be extracted: {event.src_path}")

            if (response):
                print(openai_response(prompt=(initialResp+response)))
            else:
                prompt = 'what is the universe about?'
                openai_response(prompt=prompt)
                print(openai_response(prompt=prompt))


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
