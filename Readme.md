<a href="https://github.com/johannes-vdm/watchtower" target="_blank">View Source Code</a>

<i>Note that the Tesseract OCR engine must be installed on the system and the path to the 'tesseract.exe' file must be set appropriately via the 'pytesseract.pytesseract.tesseract_cmd' variable for the code to function correctly. Also, the 'BEACON_URL' environment variable must be set to the appropriate API endpoint URL for the script to send the NLP output.</i>

This Python script is designed to monitor a directory for new image files and perform OCR (optical character recognition) using the Tesseract library to extract text from the image. The extracted text is then passed to the OpenAI GPT-3 language model for natural language processing, and the resulting response is sent to a designated endpoint.

The code also includes error handling for cases where text cannot be extracted from an image, as well as for handling keyboard interrupts when the script is stopped.

## Dependencies
- pytesseract
- opencv-python
- watchdog
- requests
- pillow

## Configuration
pytesseract
The pytesseract module requires the Tesseract OCR engine to be installed on your system. In this script, the pytesseract configuration points to the tesseract.exe executable located in C:/Program Files/Tesseract-OCR/.

### .ENV
```env
OPENAI_API_KEY='' # Your API KEY 
MODEL_ENGINE='text-davinci-003' # Model Engine from OpenAI 
BEACON_URL='http://localhost:3000/api/watchtower'

```

## Directory
The directory variable should be set to the path of the directory you wish to monitor for new image files. The default is the `/media` directory.
beacon_url
The beacon_url variable should be set to the endpoint where you wish to send the OpenAI response.

## Execution
The script will continuously monitor the designated directory for new image files and perform OCR and OpenAI processing on each new file. The script can be run with the following command:

```shell
python main.py
```

## Code Review

Here, the pytesseract module is set up with its tesseract binary path. The directory variable is set to 'media' indicating that the script will monitor this folder for new image files. The initQuestion, and question variables are defined as empty strings and None, respectively. The beacon_url variable is set to the environment variable BEACON_URL.

The LatestImageHandler class extends the FileSystemEventHandler class from the watchdog module. The on_created method is called each time a new file is created in the monitored directory. If the file has a .jpg, .jpeg, or .png extension, the script will attempt to perform OCR on the image using pytesseract.

If text is successfully extracted from the image, the text is passed to the openai_response function, which sends the text to the OpenAI GPT-3 language model and returns a natural language response.

The text and response are then sent to the designated endpoint specified in beacon_url. If the OCR process fails to extract text from the image, the script will print a message indicating the failure.
```py
class LatestImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg') or event.src_path.endswith('.jpeg') or event.src_path.endswith('.png'):
            print(f"The latest uploaded image is now: {event.src_path}")
            print(f"{event.src_path}")
            # img = Image.open(event.src_path)
            img = cv2.imread(f"{event.src_path}")

            question = None
            try:
                config = (
                    '--psm 3 --oem 3')
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

                print(response)
                payload = json.dumps({
                    "data": response,
                    "info": paragraph
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request(
                    "POST", beacon_url, headers=headers, data=payload)

                print(response.text)
            else:
                print('no response')
```


Create a handler for file system events
```py
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

```

## OpenAI Function
```py
openai.api_key = os.environ.get('OPENAI_API_KEY')
model_engine = os.environ.get('MODEL_ENGINE')


def openai_response(prompt,
                    model=model_engine,
                    temperature=0,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    ).choices[0].text

    return response
```

An instance of the LatestImageHandler class is created and assigned to the event_handler variable. An Observer is created that monitors the directory for new files, and

## Available OpenAI Models

This can be set in the local .env file 
`MODEL_ENGINE='text-davinci-003'`

| MODELS     | Info         | DESCRIPTION                                                                                             |
| ---------- | ------------ | ------------------------------------------------------------------------------------------------------- |
| GPT-4      | Limited beta | A set of models that improve on GPT-3.5 and can understand as well as generate natural language or code |
| GPT-3.5    |              | A set of models that improve on GPT-3 and can understand as well as generate natural language or code   |
| DALL·E     | Beta         | A model that can generate and edit images given a natural language prompt                               |
| Whisper    | Beta         | A model that can convert audio into text                                                                |
| Embeddings |              | A set of models that can convert text into a numerical form                                             |
| Moderation |              | A fine-tuned model that can detect whether text may be sensitive or unsafe                              |
| GPT-3      |              | A set of models that can understand and generate natural language                                       |
| Codex      | Deprecated   | A set of models that can understand and generate code, including translating natural language to code   |