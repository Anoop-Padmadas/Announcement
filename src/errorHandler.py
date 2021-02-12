def createErrorResponse(error,statusCode,title):
    errorData = {}
    errorData['status'] = statusCode
    errorData['title'] = title
    errorData['detail'] = str(error)

    errorResponse = {}
    errorResponse['errors'] = errorData
    return errorResponse
