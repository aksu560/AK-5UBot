# -*- coding: utf-8 -*-
from discord.ext import commands
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time
import os


class D20PFSRD(object):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True, brief="[Query]")
    async def srd(self, ctx: commands.Context, *, query: str = ""):
        """Searches D20PFSRD"""

        await self.client.send_typing(ctx.message.channel)

        if query == "":
            await self.client.reply("You do need to specify what to look for ya dumb dumb.")
            return

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver')
        adblock = os.path.abspath("Resources/Other/adblock.xpi")

        # Open the main page
        driver.get("https://www.d20pfsrd.com/")
        # Find the search box
        search = driver.find_element_by_css_selector("input.form-control")
        search.click()
        search.clear()
        # Type in search and press enter
        search.send_keys(query)
        search.send_keys(Keys.RETURN)
        # Wait for page to load
        time.sleep(1)
        # Get the first results URL, and reopen selenium with it. This is because the screnshots refused to work
        # properly
        result_link = driver.find_element_by_css_selector("a.gs-title").get_attribute("href")
        driver.quit()
        driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver')
        driver.install_addon(adblock, temporary=True)
        driver.set_window_size(1920, 1080)
        driver.get(result_link)
        # Close the announcements
        try:
            cookieconsent = driver.find_element_by_css_selector("button#cookieconsentok")
            cookieconsent.click()
        except NoSuchElementException:
            pass
        driver.find_element_by_xpath('//button[@id="ognannouncement-ok"]').click()
        driver.get_screenshot_as_file("Resources/Other/srd.png")
        driver.quit()

        path = "Resources/Other/srd.png"
        img = open(path, "rb")
        await self.client.reply(f"<{result_link}>")
        await self.client.send_file(ctx.message.channel, img)
        img.close()

    @srd.error
    async def srd(self, err, ctx: commands.Context):
        await self.client.reply("Something went wrong sorry :c, this command is kinda unstable, because selenium "
                                "||~~sucks ass~~|| is not something Aksu#1010 really knows")


def setup(client: commands.Bot):
    client.add_cog(D20PFSRD(client))
