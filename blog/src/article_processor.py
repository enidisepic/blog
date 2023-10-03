import os
import re
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Self

import jinja2
import markdown
from bs4 import BeautifulSoup
from config import Config


@dataclass
class PreprocessedArticle:
    """
    Return type for preprocess_article

    :param str html_head: The HTML head to be inserted used later
    :param str article: The article's contents as Markdown
    """

    content: str = ""
    html_head: str = ""


@dataclass
class ProcessedArticle:
    """
    Return type for run

    :param str name: The article's output HTML as a string
    :param str content: The article's name
    """

    name: str = ""
    content: str = ""


class ArticleProcessor:
    def __init__(self: Self, config: Config):
        """
        Initializes the class.

        :param Config config: The application-wide configuration opject.
        """

        self.__config = config
        self.__jinja_environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader("templates")
        )
        self.__article_template = self.__jinja_environment.get_template(
            self.__config.article_template_file_name
        )

    def run(self) -> list[ProcessedArticle]:
        """
        Run the article processor, first preprocessing the article to acquire other data and then creating the output HTML.

        :return: A list containing the fully rendered articles as strings containing HTML
        :rtype: str
        """

        output: list[ProcessedArticle] = []

        for article_file_name in os.listdir(self.__config.article_directory):
            article_file_handle = open(
                f"{self.__config.article_directory}/{article_file_name}"
            )

            preprocessed_article = self.__preprocess(article_file_handle)

            article_html = markdown.markdown(preprocessed_article.content)

            rendered_article = self.__article_template.render(
                head=preprocessed_article.html_head, body=article_html
            )

            soup = BeautifulSoup(rendered_article, features="html.parser")
            prettified_soup = soup.prettify()

            prettified_html = ""
            # Indent HTML
            for line in prettified_soup.splitlines():
                spaces = re.search("^ +", line)

                if spaces is None:
                    prettified_html += line + "\n"
                    continue

                prettified_html += (
                    re.sub(
                        "^ +",
                        " " * (4 * len(spaces.group())),
                        line,
                    )
                    + "\n"
                )

            output.append(
                ProcessedArticle(
                    ".".join(article_file_name.split(".")[:-1]), prettified_html
                )
            )

        return output

    def __preprocess(
        self: Self, article_file_handle: TextIOWrapper
    ) -> PreprocessedArticle:
        """
        A function to preprocess article files.

        :param TextIOWrapper article_file_handle: The raw article, as a file handle in read-only mode
        :return: An object of type PreprocessedArticle, which includes the information this function extracts as well as the remaining content of the article
        :rtype: PreprocessedArticle
        """

        # Default HTML <head> content
        html_head = f"""
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta property="og:url" content="{self.__config.base_url}/articles/{article_file_handle.name.split("/")[-1][:-3]}.html" />
        """
        article = ""

        in_meta_block = False

        for line in article_file_handle.readlines():
            # Check whether we are entering or leaving a meta tag block
            if line.startswith("META_START"):
                in_meta_block = True
                continue
            elif line.startswith("META_END"):
                in_meta_block = False
                continue

            if not in_meta_block:
                article += line + "\n"
                continue

            if line.isspace():
                continue

            # Format: "<name/og:property> content"
            meta_split = line.split(" ")
            meta_name = meta_split[0]
            meta_content = " ".join(meta_split[1:]).strip()

            if meta_name.startswith("og"):
                html_head += (
                    f'\n<meta property="{meta_name}" content="{meta_content}" />'
                )
            elif meta_name == "web_title":
                html_head += f"<title>{meta_content}</title>"
            else:
                html_head += f'\n<meta name="{meta_name}" content="{meta_content}" />'

        return PreprocessedArticle(article, html_head)
