import os
from dataclasses import dataclass


@dataclass
class Config:
    """
    A class providing configuration for this app.
    By default it will try getting the configuration from environment variables. If the environment variable isn't set, it will set defaults.

    :param str article_directory: The directory in which articles are stored. (default ../../articles)
    :param str article_template_file: The name of the article template file. (default "article.j2")
    :param str base_url: The base URL to be used for expanding URLs in the HTML output. (default https://blog.enidisepic.gay)
    """

    article_directory: str = os.getenv("ARTICLE_DIRECTORY") or os.path.join(
        "../..", "articles"
    )
    output_directory: str = os.getenv("OUTPUT_DIRECTORY") or os.path.join(
        "../..", "output"
    )
    article_template_file_name: str = os.getenv("ARTICLE_TEMPLATE_FILE") or "article.j2"
    base_url: str = os.getenv("BASE_URL") or "https://blog.enidisepic.gay"
