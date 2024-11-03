![image](https://github.com/user-attachments/assets/47824f75-26d1-4955-9d03-6db89aaca8cd)

# Project Overview
This project is a web crawler designed to download images from a specified website and store them in a local directory.

## How to use the crawler:
1. Navigate to the `project03-GlamiraImages` directory. <br>
2. Use this command: <br>
<code>python main.py</code> <br>
or: <br>
<code>python3 main.py</code> <br>
3. The images that are crawled will be stored in the `images` folder. <br>
Note: Sometimes the crawler will get error code 403. Trying to run the code again may help solve this error.

## Dependencies
```sh
pip install bs4
pip install logging
pip install requests
pip install urllib
pip install concurrent
pip install fake_useragent
```