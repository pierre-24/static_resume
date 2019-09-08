import markdown


def proc_base(keyword: str, config: dict) -> dict:
    """Basic processor: just return the keyword-value context

    :param keyword: the keyword
    :param config: config dict
    """
    return {keyword: config}


def proc_md(key: str, config: str) -> dict:
    """Parse the text as markdown
    """

    return {key: markdown.markdown(config)}
