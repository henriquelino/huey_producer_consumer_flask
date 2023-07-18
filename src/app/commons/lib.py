from pathlib import Path
from threading import Lock

from fake_useragent import FakeUserAgent
from loguru import logger
from selenium_tkit.chrome import ChromeOptions, CreateChrome

lock = Lock()


def create_chrome():
    base_dir = Path('.').resolve()
    chrome_configs = {
        "driver_path": str(base_dir / 'chromedriver'),
        "port": None,
    }

    chrome_options = {
        "arguments": [
            "log-level=3",
            "no-first-run",
            # "incognito",
            "no-default-browser-check",
            "disable-infobars",
            "disable-blink-features",
            "disable-blink-features=AutomationControlled"
        ],
        "experimental": {
            "prefs": {
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "plugins.always_open_pdf_externally": True,
                "download.default_directory": str(base_dir / "chromedriver" / "downloads"),
            },
            "excludeSwitches": ["enable-automation", "ignore-certificate-errors"],
            "useAutomationExtension": False,
        },
        "extensions": [
            # r"path_to\extensions" # --> a folder will use all .crx of folder
            # r"path_to\extensions\uBlock-Origin.crx", # --> only a single extension
        ],
    }  # yapf: disable

    options = ChromeOptions()

    # --------------------------------------------------
    # add arguments
    for arg in chrome_options["arguments"]:
        options.add_argument(arg)

    # --------------------------------------------------
    # add experimental options
    for k, v in chrome_options["experimental"].items():
        options.add_experimental_option(k, v)

    # --------------------------------------------------
    # if extension isn't a list or a tuple, fixes to a list
    if chrome_options["extensions"] and not isinstance(chrome_options["extensions"], (list, tuple)):
        chrome_options["extensions"] = list(chrome_options["extensions"])

    # add extensions
    all_extensions = list()
    for ext in chrome_options["extensions"]:
        ext = Path(ext)
        if ext.is_dir():
            for e in ext.glob("*.*"):
                all_extensions.append(str(e))
        else:
            all_extensions.append(str(ext))

    for ext in all_extensions:
        options.add_extension(ext)

    # --------------------------------------------------

    with lock:
        # CreateChrome use webdrivermanager
        # each instance try to update/download a new chromedriver
        # so we need to lock so only one thread at time can try to download wdm
        # if we dont mora than one thread can
        # download same file and maybe corrupt .zip
        driver = CreateChrome(**chrome_configs, options=options)

    if not driver.begin():
        logger.critical("Something went wrong creating a chrome instance. Check logs for details.")
        return False

    # --------------------------------------------------

    # driver.rotate_user_agent()

    ua = FakeUserAgent(use_external_data=True).random

    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": ua})

    driver.set_navigator_to_undefined()

    # driver.refresh()

    # corrects the exception: "unknown command: session/xxxxxx/se/file"
    driver._is_remote = False

    return driver


if __name__ == '__main__':
    driver1 = create_chrome()
    driver2 = create_chrome()

    driver1.open_url('https://github.com/henriquelino/selenium_tkit')
    driver2.open_url('https://github.com/henriquelino')

    # input()
