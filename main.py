import os
import time
from selenium.webdriver import Firefox
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import subprocess
import sys, shutil
def merge_segments(video_folder):
    # Create videos.txt
    videos_list_path = os.path.join(video_folder,'videos.txt')
    with open(videos_list_path, 'w') as videos_list_file:
        videos_list = os.listdir(video_folder)
        videos_list = sorted(videos_list)
        videos_list = [x for x in videos_list if '.mp4' in x]
        for video in videos_list:
            videos_list_file.write('file %s\n'%video)
    print(" ".join(["ffmpeg",'-hide_banner','-v','fatal',"-f","concat","-i",videos_list_path,"-c","copy",[x for x in video_folder.split('/') if x is not ''][-1]]))
    return subprocess.run([
        "ffmpeg",
        '-hide_banner',
        '-v',
        'fatal',
        "-f",
        "concat",
        "-i",
        videos_list_path,
        "-c",
        "copy",
        os.path.join(video_folder, [x for x in video_folder.split('/') if x is not ''][-1]+'.mp4')
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

class Uploader:
    def __init__(self, folder, profile, username, password):
        self.folder = folder
        self.username = username
        self.password = password
        firefox_options = FirefoxOptions()
        firefox_profile = FirefoxProfile('/home/aniquetahir/.mozilla/firefox/'+profile)
        firefox_options.add_argument('-headless')
        self.webdriver = Firefox(firefox_profile, executable_path='/home/aniquetahir/youtube-upload-folder/geckodriver',firefox_options=firefox_options, firefox_binary='/home/aniquetahir/firefox/firefox')

    def login(self):
        w = self.webdriver
        w.implicitly_wait(10)
        w.get("https://accounts.google.com/signin/v2/identifier?uilel=3&passive=true&service=youtube&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26next%3D%252F%26app%3Ddesktop%26hl%3Den&hl=en&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
        email_field = w.find_elements_by_css_selector('input#identifierId')[0]
        email_field.send_keys(self.username)
        next = w.find_element_by_id("identifierNext")
        next.click()

        time.sleep(10)
        # WebDriverWait(w, 20).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        # )

        passw = w.find_element_by_css_selector('input[type="password"]')
        passw.send_keys(self.password)
        next = w.find_element_by_id("passwordNext")
        next.click()
        pass

    def uploadFolder(self):
        w = self.webdriver
        w.get('https://www.youtube.com/upload')
        time.sleep(5)
        w.get('https://www.youtube.com/upload')

        WebDriverWait(w, 20).until(
            EC.presence_of_element_located((By.ID, "start-upload-button-single"))
        )

        # Get list of files
        folders = []
        files = []
        for p_folder, c_folders, c_files in list(os.walk(self.folder)):
            folders.append(p_folder)
            m_name = [x for x in p_folder.split('/') if x is not ''][-1]
            merge_segments(p_folder)
            files.append(os.path.join(p_folder, m_name+'.mp4'))

        # files = [y for x in files for y in x]

        for file in files:
            self.upload_file(file)
            time.sleep(10)

        self.wait_for_uploads()
        self.remove_folders(folders)
        # self.remove_files(files)
        w.close()

    def remove_folders(self, folders):
        for folder in folders:
            shutil.rmtree(folder)

    def remove_files(self, files):
        for file in files:
            os.unlink(file)

    def wait_for_uploads(self):
        alert_message = self.webdriver.find_element_by_css_selector('#bulk-active-alert .yt-alert-message')
        alert_message = alert_message.text
        while 'still uploading' in alert_message:
            time.sleep(120)
            alert_message = self.webdriver.find_element_by_css_selector('#bulk-active-alert .yt-alert-message')
            alert_message = alert_message.text

    def upload_file(self, file_location):
        upload_input = self.webdriver.find_element_by_css_selector('input[type="file"][multiple]')
        upload_input.send_keys(file_location)
        # upload_input.submit()

import sys
if __name__=="__main__":
    folder = sys.argv[1]
    profile = sys.argv[2]
    username = ''
    password = ''
    uploader = Uploader(folder, profile, username, password)
    # uploader.login()
    uploader.uploadFolder()
    pass
