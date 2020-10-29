import json
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
    body_str = event.get("body", "{}")
    body_str = body_str if body_str else "{}"
    body_obj = json.loads(body_str)
    wiki_search_term = body_obj.get("searchTerm", "")
    if not body_obj or not wiki_search_term:
        # https://docs.aws.amazon.com/apigateway/latest/developerguide/handle-errors-in-lambda-integration.html
        response = {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Wikipedia search term was not provided"}),
        }
    else:
        summary = wikipedia.summary(wiki_search_term)
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(summary),
        }
    # https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format
    return response
