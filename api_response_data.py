def api_response_data(result, reply=None):
    data = {"result_code": result}
    if reply:
        data["reply"] = reply
    return data
