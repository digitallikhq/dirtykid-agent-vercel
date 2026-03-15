from dirtykid_agent import run_dirty_kid


def handler(request):
    result = run_dirty_kid()

    return {
        "statusCode": 200,
        "body": result["post"]
    }
