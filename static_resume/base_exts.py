
def default_ext(keyword: str, config: dict) -> dict:
    """Basic extension: just return the keyword-value context

    :param keyword: the keyword
    :param config: config dict
    """
    return {keyword: config}
