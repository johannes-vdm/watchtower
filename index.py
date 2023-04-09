import time
import pytesseract
import cv2
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import json


from openai_functions import openai_response

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
directory = 'media'
initQuestion = ''
question = None
url = "http://localhost:3000/api/forward"


class LatestImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg') or event.src_path.endswith('.jpeg') or event.src_path.endswith('.png'):
            print(f"The latest uploaded image is now: {event.src_path}")
            print(f"{event.src_path}")
            img = cv2.imread(f"{event.src_path}")
            question = None
            try:
                config = ('--psm 6 --oem 3 --dpi 300')
                question = pytesseract.image_to_string(
                    img, lang='eng',  config=config)
                print(question)
                question = question.split('\n')

            except TypeError:
                print(f"Text could not be extracted: {event.src_path}")
            if (question):
                print(question)
                # response = text
                paragraph = '\n'.join(question)
                response = openai_response(prompt=(paragraph))
                # data=paragraph

                print(response)
                payload = json.dumps({
                    "data": response
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request(
                    "POST", url, headers=headers, data=payload)

                print(response.text)

                # url = "localhost:3000/api/forward"

                # headers = {
                #     'Content-Type': 'application/json'
                # }

                # response = requests.request(
                #     "POST", url, headers=headers, data=payload)

                # print(response.text)

            else:
                # prompt = 'what is the probability of cellular life in the universe?'
                # openai_response(prompt=prompt)
                print('no response')


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
