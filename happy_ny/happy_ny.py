import sys
import time
import getpass
import argparse
import numpy as np
from tqdm import tqdm
from selenium import webdriver


parser = argparse.ArgumentParser()
parser.add_argument(
    'login',
    help='login for your vk account',
    type=str
)
parser.add_argument(
    '-c',
    '--chromedriver_path',
    help='path to chromedriver',
    type=str
)
parser.add_argument(
    '-q',
    '--quiet',
    help='quiet process of congratulation',
    action='store_true'
)



args = parser.parse_args()

login = args.login
print('Please, enter your password.')
password = getpass.getpass()
path = './chromedriver'
if args.chromedriver_path:
    path = args.chromedriver_path
q = False
if args.quiet:
    q = True

try:
    driver = webdriver.Chrome(executable_path=path)
except Exception as e:
    print("Enter right path to chromedriver")
    print(str(e))
    sys.exit()


def scroll_to_the_end(driver=driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        r = np.abs(np.random.normal())
        pause = r * (r < 5) + 0.25
        time.sleep(pause)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def log_in(login, password, driver=driver):
    login_box = driver.find_element_by_id('index_email')
    login_box.click()
    login_box.send_keys(login)
    password_box = driver.find_element_by_id('index_pass')
    password_box.click()
    password_box.send_keys(password)
    btn = driver.find_element_by_id('index_login_button')
    btn.click()


tmps = [
    'С новым годом!',
    "Добра, веселья, радости в Новом Году!)",
    'Здоровья и успехов в новом году! ^_^'
]


def generate_conglatulations(s=tmps):
    size = np.random.randint(low=1, high=len(s))
    res = np.random.choice(s, size=size, replace=False)
    return '\n'.join(res)


close_class = 'box_x_button'


def close(driver=driver):
    driver.find_element_by_class_name(close_class).click()


def sleep_help(r):
    return 2 + r * (r < 3)


def get_friends(driver=driver):
    friends = driver.find_elements_by_class_name('friends_user_info')
    return friends


def make_message(driver=driver, s=tmps):
    mail = driver.find_element_by_id('mail_box_editable')
    mail.send_keys(generate_conglatulations(s))


def get_friend_name(f):
    name = f.text.split('\n')[0]
    return name


def click_friend(f):
    f.click()


def happy_NY(friends, q):
    name = ''
    for friend in tqdm(friends):
        ### not queit
        if not q:
            name = get_friend_name(f)
            print('Trying to congratulate ' + name + "...")
        r = np.abs(np.random.normal())
        time.sleep(sleep_help(r * 0.999))
        try:
            click_friend(friend)
            time.sleep(sleep_help(r))
            try:
                make_message()
                close()
                if not q:
                    print(name + ' is congratulated!')
            except Exception as e:
                if not q:
                    print(name + " is not congratulated :(")
                print(str(e))
                close()
            r = np.abs(np.random.normal())
            time.sleep(sleep_help(r))
        except Exception as e:
            print(str(e))


# Let's go!
driver.get('https://vk.com/')
# Login!
log_in(login, password)
# Get list of friends!
driver.get('https://vk.com/friends')
scroll_to_the_end()
friends = get_friends()
# Try to congratulate
happy_NY(friends, q)

