from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from flask import current_app


def get_remote_webdriver():
    options = get_firefox_options()

    return webdriver.Remote(
        # command_executor='http://192.168.64.2:4444/wd/hub',
        # command_executor='http://localhost:4444/wd/hub',
        command_executor='http://172.17.0.1:4444/wd/hub',
        # command_executor='http://0.0.0.0:4444/wd/hub',
        browser_profile=get_remote_firefox_profile(),
        options=options
    )


def get_remote_firefox_profile():
    path_download = current_app.config['UPLOAD_FOLDER']
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", True)
    mime_types = "application/pdf,application/vnd.adobe.xfdf,application/vnd.fdf,application/vnd.adobe.xdp+xml"
    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", path_download)
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    firefox_profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
    firefox_profile.set_preference("pdfjs.disabled", True)
    firefox_profile.update_preferences()
    return firefox_profile


def get_firefox_options():
    options = Options()
    options.page_load_strategy = 'normal'

    return options
