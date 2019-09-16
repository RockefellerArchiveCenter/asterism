

def prepare_response(data):
    """Transforms a string, Exception or tuple to consistently structured output"""
    data = data.args if isinstance(data, Exception) else data
    if isinstance(data, str):
        detail = data
        objects = []
    else:
        detail = str(data[0])
        objects = data[1] if len(data) > 1 else []
    if objects and not isinstance(objects, list):
        objects = [objects]
    count = len(objects) if objects else 0
    return {"detail": detail, "objects": objects, "count": count}
