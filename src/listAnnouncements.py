import boto3
import os
from errorHandler import createErrorResponse
from CustomError import CustomError

def listAnnouncementProperty(event): 
    try:
        #Initialize DB connection
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('AnnouncementTable')
        #Initialize default Limit
        limit = int(os.environ['defaultLimit'])
        #check if there is query string paramter
        if(event['params']['querystring'] == {}):
            #get Announcements by default Limit
            response = table.scan(Limit = limit)
        else:
            #Get announcements by requested Limit
            if ('limit' in event['params']['querystring']):
                numberOfAnnouncements = (event['params']['querystring']['limit'])
                #check if limit is grater than 0 , if not raise exception
                if (numberOfAnnouncements == '0'):
                    raise CustomError('limit must be greater than 0')
                limit = int(numberOfAnnouncements)
            # Get index paginated results
            if ('offset' in event['params']['querystring']):
                offsetIndex = event['params']['querystring']['offset']
                indexId = {}
                indexId['id'] = offsetIndex
                response = table.scan(ExclusiveStartKey = indexId,Limit=limit)
            else:
                response = table.scan(Limit = limit)

        # Check if it is of last results returned
        if ('LastEvaluatedKey' in response):
            lastEvaluatedKey = response['LastEvaluatedKey']
        else:
            lastEvaluatedKey = None
            
        announcements =   response['Items']
        #Construct response Data
        responseData = {}
        responseData['announcements'] = announcements

        #Construct MetaData
        metaData = {}
        metaData['numberOfAnnouncementReturned'] = len(announcements)
        metaData['LastEvaluatedKey'] = lastEvaluatedKey
        
        responseData['meta'] = metaData
        
        return responseData
              
    except CustomError as error:
        statusCode = '400'
        title = 'Business exception'
        errorResponse = createErrorResponse(error,statusCode,title)
        return errorResponse
    except Exception as error:
        statusCode = '500'
        title = 'Exception occured while generating list of announcemenets'
        errorResponse = createErrorResponse(error,statusCode,title)
        return errorResponse
