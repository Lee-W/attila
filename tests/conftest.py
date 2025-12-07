from __future__ import annotations

import os
from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import pytest
from bs4 import BeautifulSoup
from pelican.contents import Article
from pelican.generators import ArticlesGenerator, PagesGenerator
from pelican.readers import Author, Page, RstReader
from pelican.settings import read_settings
from pelican.writers import Writer

if TYPE_CHECKING:
    from pelican.settings import Settings

CUR_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(CUR_DIR, "content")
OUTPUT_DIR = os.path.join(CUR_DIR, "output")


@pytest.fixture
def default_settings() -> Settings:
    default_conf_path = Path(__file__).parent / "default_conf.py"
    settings = read_settings(str(default_conf_path))
    settings["THEME"] = "../"
    settings["filenames"] = {}
    return settings


@pytest.fixture
def default_reader(default_settings: Settings) -> RstReader:
    return RstReader(default_settings)


@pytest.fixture
def default_writer(default_settings: Settings) -> Writer:
    return Writer("output", default_settings)


@pytest.fixture(autouse=True)
def chdir_base_to_tests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir("tests")


def _gen_article_and_html_from_rst(
    rst_path: str,
    reader: RstReader,
    writer: Writer,
    settings: Settings,
) -> tuple[Article, BeautifulSoup]:
    content, metadata = reader.read(rst_path)
    article = Article(content=content, metadata=metadata)
    context = settings.copy()
    context["generated_content"] = {}
    context["static_links"] = set()
    context["static_content"] = {}
    context["localsiteurl"] = settings["SITEURL"]

    generator = ArticlesGenerator(
        context=context,
        settings=settings,
        path=CONTENT_DIR,
        theme=settings["THEME"],
        output_path=OUTPUT_DIR,
    )
    generator.generate_context()

    def _has_the_same_slug(other: Article) -> bool:
        return other.slug == article.slug

    result = list(filter(_has_the_same_slug, generator.context["articles"]))[0]
    writer.write_file(
        result.save_as,
        generator.get_template("article"),
        generator.context,
        article=result,
    )
    soup = BeautifulSoup(
        open(f"./{writer.output_path}/{result.save_as}"),
        "html.parser",
    )
    return (result, soup)


@pytest.fixture
def gen_article_and_html_from_rst(
    default_reader: RstReader,
    default_writer: Writer,
    default_settings: Settings,
) -> Callable:
    return partial(
        _gen_article_and_html_from_rst,
        reader=default_reader,
        writer=default_writer,
        settings=default_settings,
    )


def _gen_author_and_html_from_name(
    name: str,
    writer: Writer,
    settings: Settings,
) -> tuple[Author | None, BeautifulSoup]:
    context = settings.copy()
    context["generated_content"] = {}
    context["static_links"] = set()
    context["static_content"] = {}
    context["localsiteurl"] = settings["SITEURL"]

    generator = ArticlesGenerator(
        context=context,
        settings=settings,
        path=CONTENT_DIR,
        theme=settings["THEME"],
        output_path=OUTPUT_DIR,
    )
    generator.generate_context()
    generator.generate_authors(writer.write_file)

    if not (
        selected_author := next(
            (author for author, _ in generator.authors if author.name == name), None
        )
    ):
        raise ValueError("Author should not be None")

    soup = BeautifulSoup(
        open(f"./{writer.output_path}/{selected_author.save_as}"),
        "html.parser",
    )
    return (selected_author, soup)


@pytest.fixture
def gen_author_and_html_from_name(
    default_writer: Writer, default_settings: Settings
) -> Callable:
    return partial(
        _gen_author_and_html_from_name,
        writer=default_writer,
        settings=default_settings,
    )


def _gen_page_and_html_from_rst(
    rst_path: str,
    reader: RstReader,
    writer: Writer,
    settings: Settings,
):
    content, metadata = reader.read(rst_path)
    page = Page(content=content or "", metadata=metadata)
    context = settings.copy()
    context["generated_content"] = {}
    context["static_links"] = set()
    context["static_content"] = {}
    context["localsiteurl"] = settings["SITEURL"]
    generator = PagesGenerator(
        context=context,
        settings=settings,
        path=CONTENT_DIR,
        theme=settings["THEME"],
        output_path=OUTPUT_DIR,
    )
    generator.generate_context()

    def _has_the_same_slug(other: Page) -> bool:
        return other.slug == page.slug

    result = list(filter(_has_the_same_slug, generator.context["pages"]))[0]
    writer.write_file(
        result.save_as, generator.get_template("page"), generator.context, page=result
    )
    soup = BeautifulSoup(
        open(f"./{writer.output_path}/{result.save_as}"), "html.parser"
    )
    return (result, soup)


@pytest.fixture
def gen_page_and_html_from_rst(
    default_reader: RstReader,
    default_writer: Writer,
    default_settings: Settings,
):
    return partial(
        _gen_page_and_html_from_rst,
        reader=default_reader,
        writer=default_writer,
        settings=default_settings,
    )


def _gen_tag_and_html_from_name(
    tag_name: str,
    writer: Writer,
    settings: Settings,
):
    context = settings.copy()
    context["generated_content"] = {}
    context["static_links"] = set()
    context["static_content"] = {}
    context["localsiteurl"] = settings["SITEURL"]

    generator = ArticlesGenerator(
        context=context,
        settings=settings,
        path=CONTENT_DIR,
        theme=settings["THEME"],
        output_path=OUTPUT_DIR,
    )
    generator.generate_context()
    generator.generate_tags(writer.write_file)

    selected_tag = None
    for tag, articles in generator.tags.items():
        if tag.name == tag_name:
            selected_tag = tag
            break

    if selected_tag is None:
        raise ValueError(f"Tag '{tag_name}' not found in generated tags")

    soup = BeautifulSoup(
        open(f"./{writer.output_path}/{selected_tag.save_as}"), "html.parser"
    )
    return selected_tag, soup


@pytest.fixture
def gen_tag_and_html_from_name(default_writer: Writer, default_settings: Settings):
    return partial(
        _gen_tag_and_html_from_name,
        writer=default_writer,
        settings=default_settings,
    )


def _gen_category_and_html_from_name(name: str, writer: Writer, settings: Settings):
    context = settings.copy()
    context["generated_content"] = {}
    context["static_links"] = set()
    context["static_content"] = {}
    context["localsiteurl"] = settings["SITEURL"]

    generator = ArticlesGenerator(
        context=context,
        settings=settings,
        path=CONTENT_DIR,
        theme=settings["THEME"],
        output_path=OUTPUT_DIR,
    )
    generator.generate_context()
    generator.generate_categories(writer.write_file)

    selected_category = None
    for category, articles in generator.categories:
        if category.name == name:
            selected_category = category
            break

    if selected_category is None:
        raise ValueError(f"Category '{name}' not found")

    soup = BeautifulSoup(
        open(f"./{writer.output_path}/{selected_category.save_as}"), "html.parser"
    )
    return selected_category, soup


@pytest.fixture
def gen_category_and_html_from_name(default_writer: Writer, default_settings: Settings):
    return partial(
        _gen_category_and_html_from_name,
        writer=default_writer,
        settings=default_settings,
    )
