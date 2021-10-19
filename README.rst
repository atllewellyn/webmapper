webmapper
=========
.. image:: https://img.shields.io/github/license/atllewellyn/webmapper.svg?style=flat-square
    :alt: License


webmapper is a Python client for creating a recursive url web map from a base url

webmapper is tested against Python versions 3.7, 3.8, 3.9

© atllewellyn 2021 under the `MIT
License <https://github.com/atllewellyn/webmapper/blob/main/LICENSE>`__.

usage
-----

To create a webmap:

.. code:: pycon

    >>> from webmapper import mapper
    >>> m = mapper(base_url='https://www.webscraper.io/test-sites/e-commerce/allinone')
    >>> m.map(max_depth=2)

To print the webmap as a JSON:

.. code:: pycon

    >>> m.printJSON(indentJSON=3)
    {
       "https://www.webscraper.io/test-sites/e-commerce/allinone": [
          {
             "https://forum.webscraper.io/": [
                "https://www.discourse.org"
             ]
          },
          "https://chrome.google.com/webstore/detail/web-scraper/jnhgnonknehpejjnehehllkliplmbmhn?hl=en",
          {
             "https://cloud.webscraper.io/": [
                "https://cloud.webscraper.io/jobs"
             ]
          },
          "https://www.facebook.com/webscraperio/",
          {
             "https://twitter.com/webscraperio": [
                "https://help.twitter.com/using-twitter/twitter-supported-browsers",
                "https://twitter.com/tos",
                "https://twitter.com/privacy",
                "https://support.twitter.com/articles/20170514",
                "https://legal.twitter.com/imprint",
                "https://business.twitter.com/en/help/troubleshooting/how-twitter-ads-work.html?ref=web-twc-ao-gbl-adsinfo&utm_source=twc&utm_medium=web&utm_campaign=ao&utm_content=adsinfo"
             ]
          }
       ]
    }

To save the webmap to a JSON file:

.. code:: pycon

    >>> m.saveJSON(filename="map.json", indentJSON=3)


