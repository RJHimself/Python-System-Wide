#!/usr/bin/env python


import time
import sys
import os.path
from os import path
from os.path import expanduser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from apps_enhancements.web import ui
from apps_enhancements.web import browser

home = expanduser("~")
cwd = os.getcwd()
driver = webdriver.Chrome("/usr/bin/chromedriver")


def get_link(link):
    toFind = "gnome.org/extension/"
    extensionId_start = link.index(toFind)+len(toFind)
    extensionId_end = link.index("/", extensionId_start)
    extensionId = link[extensionId_start:extensionId_end]

    return "https://extensions.gnome.org/extension/"+extensionId+"/"


def get_versions(link):
    driver.get(get_link(link))


    # Shell Versions
    shellFirstOption = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.shell-version option:nth-of-type(2)"))
    )
    slcShellVersions = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.shell-version"))
    )
    shellFirstOption.click()


    # Extension Versions
    extensionFirstOption = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.extension-version option:nth-of-type(2)"))
    )
    slcExtensionVersions = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.extension-version"))
    )


    arrShellVersions=ui.select.toArray(slcShellVersions, "html")[1:]
    arrExtensionVersions=ui.select.toArray(slcExtensionVersions, "html")[1:]

    return arrShellVersions, arrExtensionVersions
    driver.quit()


def get_shell_versions(link): return get_versions(link)[0]
def get_extension_versions(link): return get_versions(link)[1]


def download(link, location = cwd, shellVersion = None, extensionVersion = None):
    driver.get(get_link(link))

    arrShellVersions=get_shell_versions(link)
    arrExtensionVersions=get_extension_versions(link)


    if (shellVersion is None) or (shellVersion not in arrShellVersions):
        shellVersion=arrShellVersions[0]
    if (extensionVersion is None) or (extensionVersion not in arrExtensionVersions):
        extensionVersion=arrExtensionVersions[0]


    # Shell Versions
    slcShell = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.shell-version"))
    )

    shellVersion = ui.select.getValueOfInnerHtml(slcShell, shellVersion)
    selectedShell = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.shell-version option[value='"+shellVersion+"']"))
    )
    selectedShell.click()


    # Extension Versions
    slcExtension = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.extension-version"))
    )

    extensionVersion = ui.select.getValueOfInnerHtml(slcExtension, extensionVersion)
    selectedExtension = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select.extension-version option[value='"+extensionVersion+"']"))
    )


    print("FUCK 3")

    time.sleep(5)
    # selectedExtension.click()
    time.sleep(50)



    # WAIT FOR DOWNLOAD TO PROCESS
    # time.sleep(5) # Let the user actually see something!
    # driver.quit()


# print("https://extensions.gnome.org/extension/750/openweather/")
# print(get_versions("https://extensions.gnome.org/extension/750/openweather/"))


# print(get_versions("https://extensions.gnome.org/extension/750/openweather/"))
print(download("https://extensions.gnome.org/extension/750/openweather/"))
