#!/usr/bin/env python


# <~~~~~~{ WARNING }~~~~~~>
# This File can NOT be well executed through vs code's terminal, due to driver issues, the RunningDesktop on vs code's terminal is UNITY instead of GNOME, which causes various stupid fuckiiing problems!!! XDDD


import time
import sys
import os.path
from os import path
from os.path import expanduser
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from python_apps_enhancements.web import ui
from python_apps_enhancements.web.browser import chrome

home = expanduser("~")
cwd = os.getcwd()



def get_link(link):
    toFind = "gnome.org/extension/"
    extensionId_start = link.index(toFind)+len(toFind)
    extensionId_end = link.index("/", extensionId_start)
    extensionId = link[extensionId_start:extensionId_end]

    return "https://extensions.gnome.org/extension/"+extensionId+"/"


def get_versions(link):
    options = webdriver.ChromeOptions()
    options.add_argument("download.default_directory="+home+"/Downloads")

    browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
    browser.get(get_link(link))


    # Click the First Shell Select Option to Load the 2nd
    shell_first_option = ui.get_element(browser, "select.shell-version option:nth-of-type(2)")
    shell_first_option.click()

    # Shell Versions
    slc_shell_versions = ui.get_element(browser, "select.shell-version")
    # Extension Versions
    slc_extension_versions = ui.get_element(browser, "select.extension-version")


    arrShellVersions=ui.select.toArray(slc_shell_versions, "html")[1:]
    arrExtensionVersions=ui.select.toArray(slc_extension_versions, "html")[1:]

    browser.quit()
    return arrShellVersions, arrExtensionVersions


def get_shell_versions(link): return get_versions(link)[0]
def get_extension_versions(link): return get_versions(link)[1]


def download(link, location = cwd, shellVersion = None, extensionVersion = None, downloads_folder=None):
    # options = webdriver.ChromeOptions()
    # options.add_argument("download.default_directory="+home+"/Downloads")

    arrShellVersions=get_shell_versions(link)
    arrExtensionVersions=get_extension_versions(link)

    browser = chrome.Start(downloads_folder=downloads_folder)
    browser.get(get_link(link))


    if (shellVersion is None) or (shellVersion not in arrShellVersions):
        shellVersion=arrShellVersions[0]
    if (extensionVersion is None) or (extensionVersion not in arrExtensionVersions):
        extensionVersion=arrExtensionVersions[0]


    # Shell Versions
    slcShell = ui.get_element(browser, "select.shell-version")
    shellVersion = ui.select.getValueOfInnerHtml(slcShell, shellVersion)
    print("select.shell-version option[value='"+shellVersion+"']")
    selectedShell = ui.get_element(browser, "select.shell-version option[value='"+shellVersion+"']")
    selectedShell.click()


    # Extension Versions
    slcExtension = ui.get_element(browser, "select.extension-version")
    extensionVersion = ui.select.getValueOfInnerHtml(slcExtension, extensionVersion)
    print("select.extension-version option[value='"+extensionVersion+"']")
    selectedExtension = ui.get_element(browser, "select.extension-version option[value='"+extensionVersion+"']")
    selectedExtension.click()


    # time.sleep(5)
    time.sleep(15)
    # time.sleep(50)
    browser.quit()



    # WAIT FOR DOWNLOAD TO PROCESS
    # time.sleep(5) # Let the user actually see something!
    # driver.quit()


# print("https://extensions.gnome.org/extension/750/openweather/")
# print(get_versions("https://extensions.gnome.org/extension/750/openweather/"))


# print(get_versions("https://extensions.gnome.org/extension/750/openweather/"))
# print(download("https://extensions.gnome.org/extension/750/openweather/"))
