from typing import Dict, Any

import wikipedia


def hello_world(
    event: Dict[str, Any],
    context,
):
    """
    This is the handler function that Lambda calls when the function is invoked.

    https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html

    :param event: Event data
    :param context: Runtime information.
        This object provides methods and properties that provide information
        about the invocation, function, and execution environment.
        https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    :return: JSON serializable data
    """
    wiki_search_term = event.get("searchTerm", "")
    if not wiki_search_term:
        return "Wikipedia search term was not provided"
    else:
        return wikipedia.summary(wiki_search_term)
