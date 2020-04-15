# -*- coding: utf-8 -*-
"""Crawler module

This module provides all of the generic and specific crawlers for
various content sources like HTML (others coming soon?).

Examples:
    Sample class hierarchy: ``Crawler --> HtmlCrawler``::

        from crawler.crawler import Crawler
        from crawler.html_crawler import HtmlCrawler

        crawler: Crawler = HtmlCrawler()

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
