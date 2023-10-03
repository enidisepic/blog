import os

from article_processor import ArticleProcessor
from config import Config

config = Config()

article_processor = ArticleProcessor(config)
article_processor.run()

if not os.path.isdir(config.output_directory):
    os.mkdir(config.output_directory)

for article in article_processor.run():
    article_path = os.path.join(config.output_directory, f"{article.name}.html")

    with open(article_path, "w") as file:
        file.write(article.content)
        print(f"Successfully wrote {article_path}")
