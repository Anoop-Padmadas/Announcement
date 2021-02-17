from listAnnouncements import listAnnouncementProperty
from createAnnouncement import postAnnouncement
from errorHandler import createErrorResponse

def lambda_handler(event, context):
    try:
        #get method type based on methodType
        methodType = event['context']['http-method']      
        if methodType == 'GET':
            #Call list Announcements Function
            results = listAnnouncementProperty(event);
            return results
        else:
            #Call create Announcement function
            results = postAnnouncement(event);
            return results
              
    except Exception as error:
        statusCode = '500'
        title = 'exception occured while porocessing client request'
        errorResponse = createErrorResponse(error,statusCode,title)
        return errorResponse
