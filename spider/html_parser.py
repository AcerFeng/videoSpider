from bs4 import BeautifulSoup
import re

class htmlParser(object):

    def _get_new_data(self, page_url, soup):
        res_data = []

        links = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > a')
        images = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > a > img')
        names = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_title_score > strong > a')
        descs = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_desc')
        play_nums = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_count > span')
        update_status_links = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > a')
        statuss = []
        for update_link in update_status_links:
            if update_link.find('div') is not None:
                statuss.append(update_link.find('span').get_text())
            else:
                statuss.append(' ')
        for image, name, desc, num, status, link in zip(images, names, descs, play_nums, statuss, links):
            data = {
                'name' : name.get_text(),
                'image' : 'http:' + image.get('r-lazyload'),
                'desc' : ' '.join(desc.get_text().strip().split()),
                'play_number' : num.get_text(),
                'update_status' : status,
                'link' : link.get('href')
            }
            res_data.append(data)
        return res_data

    def parser_tx_tv(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return None
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_new_data(page_url, soup)
        return new_data

"""
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > a > img
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_title_score > strong > a
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_desc
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_count > span
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > a > div > span
"""