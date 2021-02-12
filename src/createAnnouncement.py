import json
import boto3
import sys
import uuid
from time import gmtime, strftime
from datetime import datetime
currentDateTime = datetime.now()
from errorHandler import createErrorResponse

def postAnnouncement(event):
    try:
        #Initialize DB connection
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('AnnouncementTable')
        
        #Retreive create announcement property from body
        announcementId = uuid.uuid4().hex
        announcementData = event['body-json']['announcement']
        announcementTitle = announcementData['title']
        announcementDescription = announcementData['description']
        announcementDate = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
        
        #Check if date is provided in request , if not have current date
        if "date" in announcementData:
            announcementDate = announcementData['date']
        #else:
        #    announcementDate = currentDateTime.strftime("%d/%m/%Y %H:%M:%S")
        #insert into Table
        response = table.put_item(
        Item={
            'id': announcementId,
            'announcementTitle':announcementTitle,
            'announcementDescription':announcementDescription, 
            'announcementDate':announcementDate
            })
        # create return object with newly created ID
        createdAnnouncement = {"id": announcementId, "title": announcementTitle,"description": announcementDescription,"date":announcementDate}    

        #Construct return object
        reponseData = {}
        reponseData['announcement'] = createdAnnouncement

        #Create metaData
        metaData = {}
        metaData['created'] = 'Announcement created'
        metaData['lastModified'] = announcementDate

        reponseData['meta'] = metaData
        
        return reponseData
    
    except Exception as error:
        statusCode = '500'
        title = 'Exception occured while creating announcement'
        errorResponse = createErrorResponse(error,statusCode,title)
        return errorResponse
        
