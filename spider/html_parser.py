from bs4 import BeautifulSoup
import re

class htmlParser(object):

    def _get_tx_new_data(self, page_url, soup, platform, video_category, **kwargs):
        res_data = []

        links = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > a')
        images = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > a > img')
        names = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_title_score > strong > a')
        descs = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_desc')
        play_nums = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_count > span')
        update_status_links = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > a')
        scroes = soup.select('body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li > div.figure_title_score > div')
        statuss = []
        for update_link in update_status_links:
            if update_link.find('div') is not None:
                statuss.append(update_link.find('span').get_text())
            else:
                statuss.append('')
        for image, name, desc, num, status, link, scroe in zip(images, names, descs, play_nums, statuss, links, scroes):
            data = {
                'name' : name.get_text(),
                'image' : 'http:' + image.get('r-lazyload'),
                'desc' : ' '.join(desc.get_text().strip().split()),
                'play_num' : num.get_text(),
                'update_num' : status,
                'link' : link.get('href'),
                'score' : ''.join(scroe.get_text().strip().split()),
                'platform' : platform,
                'video_category' : video_category,
                'series_region' : kwargs.get('series_region') or '',
                'movie_region' : kwargs.get('movie_region') or '',
                'veriety_region' : kwargs.get('veriety_region') or ''
            }
            res_data.append(data)
        return res_data

    def _get_aiqiyi_new_data(self, page_url, soup, platform, video_category, **kwargs):
        res_data = []

        links = soup.select(
            'body > div.page-list > div > div > div.wrapper-cols > div > ul > li > div.site-piclist_pic > a')
        images = soup.select(
            'body > div.page-list > div > div > div.wrapper-cols > div > ul > li > div.site-piclist_pic > a > img')
        names = soup.select(
            'body > div.page-list > div > div > div.wrapper-cols > div > ul > li > div.site-piclist_info > div.mod-listTitle_left > p > a')
        descs = soup.select(
            'body > div.page-list > div > div > div.wrapper-cols > div > ul > li > div.site-piclist_info')
        update_statuss = soup.select(
            'body > div.page-list > div > div > div.wrapper-cols > div > ul > li > div.site-piclist_pic > a > div > div > p > span')

        descss = []
        for desc in descs:
            if desc.find('div', class_='role_info') is not None:
                descss.append(' '.join(desc.find('div', class_='role_info').get_text().strip().split()))
            else:
                descss.append('')

        for image, name, desc, status, link in zip(images, names, descss, update_statuss, links):
            data = {
                'name': name.get_text(),
                'image': 'http:' + image.get('src'),
                'desc': desc,
                'update_num': ''.join(status.get_text().strip().split()),
                'link': link.get('href'),
                'platform': platform,
                'video_category': video_category,
                'series_region': kwargs.get('series_region') or '',
                'movie_region': kwargs.get('movie_region') or '',
                'veriety_region': kwargs.get('veriety_region') or ''
            }
            res_data.append(data)
        return res_data

    def parse_tx_video_data(self, page_url, html_cont, platform, video_category, **kwargs):
        if page_url is None or html_cont is None or platform is None or video_category is None:
            return None
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_tx_new_data(page_url=page_url, soup=soup, platform=platform, video_category=video_category, **kwargs)
        return new_data

    def parse_aiqiyi_video_data(self, page_url, html_cont, platform, video_category, **kwargs):
        if page_url is None or html_cont is None or platform is None or video_category is None:
            return None
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_data = self._get_aiqiyi_new_data(page_url=page_url, soup=soup, platform=platform, video_category=video_category,
                                         **kwargs)
        return new_data
"""
tx
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > a > img
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_title_score > strong > a
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_desc
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_count > span
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > a > div > span
body > div.site_container.container_main > div > div > div.mod_figures_wrapper > div.mod_bd > div > ul > li:nth-child(1) > div.figure_title_score > div

aiqiyi
body > div.page-list > div > div > div.wrapper-cols > div > ul > li:nth-child(1) > div.site-piclist_pic > a
body > div.page-list > div > div > div.wrapper-cols > div > ul > li:nth-child(1) > div.site-piclist_pic > a > img
body > div.page-list > div > div > div.wrapper-cols > div > ul > li:nth-child(1) > div.site-piclist_info > div.mod-listTitle_left > p > a
body > div.page-list > div > div > div.wrapper-cols > div > ul > li:nth-child(2) > div.site-piclist_info
body > div.page-list > div > div > div.wrapper-cols > div > ul > li:nth-child(1) > div.site-piclist_pic > a > div > div > p > span
"""