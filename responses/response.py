


def ResponseData(response_code: str, response_message :str, data: any = None):
    return {
        "ResponseCode": response_code,
        "ResponseMessage": response_message,
        "Data": data   
    }