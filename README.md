# CPE178P_E01_2T2526_Project
Foundations of AI with Huawei MindSpore and OpenHarmony OS Project

## How to Run Codes:

### Model Training:

**NOTICE:**
Make sure you have Python 3.10 or higher installed. You can download it from python.org and install it like any normal program. After installing, open a terminal or command prompt and check it by running `python --version`. It should print your Python version.

If you want, you can create a virtual environment to keep project dependencies separate by running `python -m venv venv` or you can just install it globally but just know that it may cause conflicts with other applications. Activate it with venv\Scripts\activate if you are on Windows, or source venv/bin/activate if you are on Mac or Linux.

**Installing dependencies:**
*Note: If you are using "uv" rather than only using "pip", just type `uv` before `pip` before installing the required dependencies.*
Install PyTorch. If you have a GPU and want faster training, run:
`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130`
If you only have a CPU, run:
`pip install torch torchvision torchaudio`
Install the YOLO package from Ultralytics by running:
`pip install -U ultralytics`

**Checking directories:**
Make sure the directories of the folders inside the dataset looks like this:
```
dataset/train/images
dataset/train/labels
dataset/val/images
dataset/val/labels
dataset/test/images
dataset/test/labels
```
Also, make sure there is a data.yaml file inside the dataset folder that describes the dataset and the class names. The code will automatically create any missing folders, but you need to make sure that the images and labels in the correct folders.

**Running the Model training code:**
*Via: Terminal*
Once everything is ready, run the code by opening a terminal, going to the directrory in the project folder containing `training_script.py` which is in "SurfaceCrackDetectionProgram" folder and typing `python training_script.py`.
*Via: VSCode or any preferred IDE*
Just click the button in your chosen IDE that runs the python file:

The code will:
-Set the working directory to the project folder
-Check that the dataset exists
-Download the YOLO model yolo26s.pt automatically if it is missing
-Train the model for 5 epochs (you can change the number of epochs and batch size in the code)
-Apply mild image augmentations to improve validation (if possible)
-Save the trained weights and results in the folder runs/detect

If you have a GPU, the code will use it automatically. If not, it will run on the CPU, which is much slower.

### Running the Surface Crack Detection application itself:

**Installing dependencies:**
*Note: If you are using "uv" rather than only using "pip", just type `uv` before `pip` before installing the required dependencies.*
Install Flet for the user interface by running:
`pip install 'flet[all]'`
Install FastAPI and the server to run it:
`pip install "fastapi[standard]"`

**Opening the server**
To open the server, open the terminal, go to the directory where the server folder is located and run this line of code in the terminal:
*In a virtual environment:*
fastapi dev main.py
*In a global enironment:*
python -m fastapi dev main.py

Once the `starting development server` text popped up, you are good to run the client code.

**Running the client code**
*Via: Terminal*
Run the code by opening a terminal, going to the client folder which is in "SurfaceCrackDetectionProgram" folder and typing `python main.py` once in the correct directory.
*Via: VSCode or any preferred IDE*
Just click the button in your chosen IDE that runs the python file:

Once the application pops up, you are good to go.

### How to use the application:

There are three main parts of the app:
File selector (Left box)
Analyze Surface Button
Output

To use the app for surface crack detections, click the left box to pick the image file that you are choosing (unsupported files such as pdf, doc, and etc. won't work, only image files).
Once the file is chosen, click the "Analyze Surface" button in the app.
The results will pop up afterwards in the output box on the right. It will display if:
-There are any cracks
-How many cracks
-The confidence of the model.

