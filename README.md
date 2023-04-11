
**SingularGPT** is a open source project that automates your device using ChatGPT & GPT-4.

With 🚀 **SingularGPT** you can easily instruct your device with simple text based queries.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abhiprojectz/SingularGPT/blob/master/SGPT_Quickstart.ipynb)

> For example: 

Let's say you need to click on button that have a text as 'File' just say it: 

**Query:** Hey, please click on the item with text File.

It will perform the action by processing your query, turning them to its undernstandable instructions and execute them.

---



# :star2: Demo 

https://user-images.githubusercontent.com/64596494/230719544-a9bee6f2-4158-4784-b0ed-260bea7be067.mp4



---


# :star2: How to Use ?

You may just run it in google colab with a GPU.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/abhiprojectz/SingularGPT/blob/master/SGPT_Quickstart.ipynb)

**Follow these steps carefully**

1. Clone the repository using `git clone https://github.com/abhiprojectz/SingularGPT.git` and `cd` into the concerned directory

2. Install all the requirements

```
pip install -r requirements.txt
```

Make sure that you run this command in the same directory where the `requirements.txt` file is located.

3. If you are in linux then install below libs

```sh 

!sudo apt-get install xvfb xorg xserver-xorg scrot imagemagick x11-utils xdotool

```

4. Create a .env file and place your OPENAI_API key and change your platform name in `config/CONFIG.py`

if you are on linux set as: `_PLATFORM` as linux [By default is `windows`]

5. Run this file `main.py` by passing your query.

```py

python main.py

```

6. Use `SingularGPT` bot if you are stuck or raise a issue

7. Make sure your instructions are in `script.py` file.


## :star2: Quickstart

Create a `.env` file with `OPENAI_API` and place your openai_api key there or pass as environment variable.

Put automation scripts in `script.py` and run it.

Write your prompt query in `Prompts/prompts.txt` file or,
pass as a string in the `main.py` file.

```py
# Run the main script.
python main.py
```

---


**To visualize this see this bot on Poe**

![](https://user-images.githubusercontent.com/64596494/230727123-b01d6607-9f08-4abe-ae00-bda1eacbc5bf.PNG)


![djlkdj](https://user-images.githubusercontent.com/64596494/230751800-1100bfa5-f9a7-4971-9224-6f0c442b5df1.PNG)



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

**Locate and perform actions to the element that is left or right or even the most nearest element to it.**

ZexUI is a standalone library that uses image processing techniques for GUI automation.

---


#  :star2: Automations lib apis

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

+ Build automations scripts by its own

+ Automates your device


---

# :star2: Breakdown of the project

This projects is made possible with the help of various fields in computer science such as AI based vision, Custom libs, device automation and internal logic processing using the latest ChatGPT & GPT-4.

In short:

AI computer vision + Automation (ZexUI) + GPT


---

# :star2: Features 

+ No crawling mechanism
+ Elements detection
+ Text detection
+ Components detection based on estimates
+ Automate your device using NLP instructions
+ Adds-on in a very lightweight presets
+ Works even headless on a x11 server


# :star2: Help 

Considering leaving a star.


# :star2: Docs

Help in writing the docs for the project.

---

