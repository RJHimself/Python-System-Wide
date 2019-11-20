#!/usr/bin/env python3
#exe: py-gnome-extensions


import ast
import sys
import atexit


@atexit.register
def on_script_exit():
    if len(sys.argv) < 2: return

    def convert_values(value):
        #  This Function converts Numbers like "Int" or "Float" from "strings" coming from the terminal to the actual Types, like "Int" and "Float"

        try: value = ast.literal_eval(value)
        except: value=value
        return value


    args=""
    function_name=sys.argv[1]
    if len(sys.argv) > 2: args=list(map(convert_values, sys.argv[2:]))
    getattr(sys.modules[__name__], "%s" % function_name)(*args)


# WARNING:
# ALL of The Code above is what makes this Script able to be Called in a Terminal
# This type of python cli is at least possible with python 3.7.5 (64 bits)
# ------------------------------------------------------------------------


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



def get_link(link):
    toFind = "gnome.org/extension/"
    extensionId_start = link.index(toFind)+len(toFind)
    extensionId_end = link.index("/", extensionId_start)
    extensionId = link[extensionId_start:extensionId_end]

    return "https://extensions.gnome.org/extension/"+extensionId+"/"


def get_versions(link):
    browser = chrome.Start()
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


def download(link, downloads_folder=None, shellVersion = None, extensionVersion = None):
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
    selectedShell = ui.get_element(browser, "select.shell-version option[value='"+shellVersion+"']")
    selectedShell.click()


    # Extension Versions
    slcExtension = ui.get_element(browser, "select.extension-version")
    extensionVersion = ui.select.getValueOfInnerHtml(slcExtension, extensionVersion)
    selectedExtension = ui.get_element(browser, "select.extension-version option[value='"+extensionVersion+"']")
    selectedExtension.click()


    # WAIT FOR DOWNLOAD TO PROCESS
    time.sleep(15)
    browser.quit()
