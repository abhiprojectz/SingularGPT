
**SingularGPT** is a open source project that aims to automate complex tasks such as device automation using the latest trending LLM models that is  ChatGPT & GPT-4.

With 🚀 **SingularGPT** you can easily instruct your device such as your PC using Natural language, with built in logic processing.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abhiprojectz/SingularGPT/blob/master/SGPT_Quickstart.ipynb)

> For example: 

Let's say you wish to accomplish any task on your device instead of writing automation scripts, then testing it further debugging it, playing around with co-ordinates. 

**Query:** Hey, please click on the item with text "Document Writer" after that click on the image with path "image.png" after that scroll down and then find element that is top of text "File" , double left click it.


The **SingularGPT** will process it and does the task.


---



# :star2: Demo 

https://user-images.githubusercontent.com/64596494/230719544-a9bee6f2-4158-4784-b0ed-260bea7be067.mp4



---

# :star2: How it locates element ?

The old way using X_PATH or CSS/JS Selectors or by just co-ordinates.

```py

element_xpath = driver.find_element(By.XPATH, "//a[@href='/login']")
element_xpath.click()

# or 

element_css = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
element_css.click()

```

> No, it uses the new GUI element detection techniques.


Nopes ! 

```py

zex.text('Menu').click()
zex.text('Edit').FindLeftOf().click() # Used to locate the element that is just left side of the target element.

```

---

**You may even locate and perform actions to the element that is left or right or even the most nearest element to it.**

ZexUI is a standalone library that uses image processing techniques for GUI automation.

---

# :star2: Installation

Make sure this project currently works on linux and x11 servers.

You may just run it in google colab with a GPU.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abhiprojectz/SingularGPT/blob/master/SGPT_Quickstart.ipynb)

The `requirements.txt` file specifies the following packages:

- `paddleocr`: A deep learning-based optical character recognition (OCR) toolkit.
- `opencv-python-headless`: A computer vision library that provides real-time computer vision applications.
- `google-cloud-vision`: A cloud-based OCR service that can be used to extract text from images.
- `numpy`: A fundamental package for scientific computing in Python.
- `matplotlib`: A visualization library in Python for 2D plots and graphs.

You can install these packages, along with their dependencies, using the following command: 

```
pip install -r requirements.txt
```

Make sure that you run this command in the same directory where the `requirements.txt` file is located.

## :star2: Quickstart

Create a `.env` file with `OPENAI_API` and place your openai_api api there or pass as environment variable.

Write your prompt query in `Prompts/prompts.txt` file or,
pass as a string in the `main.py` file.

```py
# Run the main script.
python main.py
```

---

# Automations lib apis

Here are some methods and thier usage.

Sure! Here are the descriptions for each method:

- `text()`: This method is used to locate a text element on the webpage based on the text content provided in the query.

- `textRegex()`: This method is used to locate a text element on the webpage based on a regular expression provided in the query.

- `textContains()`: This method is used to locate a text element on the webpage that contains a specific word provided in the query.

- `image()`: This method is used to locate an image element on the webpage based on the image path provided in the query.

- `findLeftOf()`: This method is used to locate an element that is to the left of the text/image provided in the query.

- `findRightOf()`: This method is used to locate an element that is to the right of the text/image provided in the query.

- `findTopOf()`: This method is used to locate an element that is above the text/image provided in the query.

- `findBottomOf()`: This method is used to locate an element that is below the text/image provided in the query.

- `findNearestTo()`: This method is used to locate the element that is nearest to the text/image provided in the query.

- `click()`: This method is used to click on the element that is located using the text/image or any other method.

- `mouseMove()`: This method is used to move the mouse to the element that is located using the text/image or any other method.

- `scroll_up()`: This method is used to scroll up the webpage.

- `scroll_down()`: This method is used to scroll down the webpage.

- `scroll_left()`: This method is used to scroll left on the webpage.

- `scroll_right()`: This method is used to scroll right on the webpage.

... More are on the docs. 

# :star2: Project roadmap 

This project is still in developemnt but its ready for linux (ubuntu).
You may directly test it in Google Colab.

+ Linux - done 

+ Windows - pending

+ Android - pending

Come, star the project and let's build it together.

---

**This is what this project aims and tries to achieve the same.**

 :star2: So, here's how the things works under the hood:

+ Converts Natural language query to automation scripts that further can be used to achieve the task 

+ SingularGPT Process your screen, gets the required data what's being asked.

+ Generates commands to achieve the task.

---

# :star2: What SingularGPT can do ?

+ Recognize what's on your screen 

+ Even what's on your headless server using x11

+ Can internally process them.

+ Automates your device

+ Build automations scripts by its own

+ Build custom functions to achieve what GPT can suggest.

> It's not over...

+ Write assignments for real ! Yes not joking, [RealWriterGPT] this project is in development it uses SingularGPT + RealWriterGPT + IOT development boards and stuffs to achieve. 

> Uses tensorflow to generate handwriting.

So, that you can just says it "Please write my assignment using Addon:RealWriterGPT from the questions placed on desktop with text "questions".

---

# :star2: Breakdown of the project

This projects is made possible with the help of various fields in computer science such as AI based vision, Custom libs, device automation and internal logic processing using the latest ChatGPT & GPT-4.

In short:

AI computer vision + Automation (ZexUI) + GPT

---

# :star2: Docs 

It's currently in development.

---

# :star2: Features 

+ No crawling mechanism , no hassle instead AI based component detection
+ Elements detection
+ Text detection
+ Components detection based on estimates
+ Automate your device using NLP instructions
+ Adds-on in a very lightweight presets that saves time and money
+ Works even headless on a x11 server
+ Internal logic processing for complex tasks


# :star2: Help 

Considering leaving a star.


# :star2: Docs

Help in writing the docs for the project.

---

