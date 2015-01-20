import math

from xml.etree.ElementTree import Element, SubElement, tostring
import web
import xml.etree.ElementTree

from xml.dom import minidom
from bs4 import BeautifulSoup

import urlparse
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


###########################
def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    return arc*3791000




###########################
urls = (
    '/topics/(.*)', 'game_response',
    '/location/(.*)', 'location_handler',
    '/tweets/(.*)', 'get_tweets',
    '/update/(.*)/(.*)/(.*)/(.*)', 'updateUserInfo'
)

app = web.application(urls, globals())

class game_response:        
    def GET(self, user):
        user = user.split("/")
        print "User: " + str(user)
        user_response = str(user[0])
        current_c_task_id = int (user[1])
        next_c_task_id = int (current_c_task_id+1)
        print next_c_task_id
        handler = open('./xml/xml_for_demo.xml').read()
        soup = BeautifulSoup(handler);
        
        c_task_list=soup.findAll('c_task')
        
        
        output = '';
          # pass userid to sasjan function providing topicid
          # make calls to saajan function
          # organise to 3 essential info below   
          # assume data organised as seen below
#         uid = "uid"
#         tid_input = ["tid1","tid2","tid3","tid4","tid5"];
#         topic_input = ["topic1","topic2","topic3","topic4","topic5"];
#         root = convert_to_xml_topic(uid,tid_input,topic_input) 
#         for child in root:
#             print 'child', child.tag, child.attrib
#             output += str(child.attrib) + ','
#         output += ']';

        img_url=''
        response=''
        text = ''
        location = ''
        
        message=''
        if (len(c_task_list[next_c_task_id].image_url.contents) != 0):
            img_url = str(c_task_list[next_c_task_id].image_url.contents[0])
       
        if (len(c_task_list[next_c_task_id].response.contents) != 0):
            for individual_response in c_task_list[next_c_task_id].response.findAll('resp'):
                response += "\"resp_" +  individual_response.attrs['id'] +"\": \"" + individual_response.contents[0] + "\", "
            response = response[:-2]
        
        if (len(c_task_list[8].message.contents) != 0):
            message = str(c_task_list[next_c_task_id].find('message').contents[0])
        
        output =  '{"current_c_task_id": "' + str(next_c_task_id) + '", "message": "'+message+'","img_url": "' + img_url + '","response":{'+response+'}}'
        print output
        
        return output


class location_handler:        
    def GET(self, user):
        GPS = user.split("/")
        print "GPS: " + str(GPS)
        destination = str( GPS[2] )
        latitude = float( GPS[0] )
        longitude = float( GPS[1] )

        storedLocations = {'klaus': [33.789897229357294, -84.40235430767432]}
        
        distanceDifference = distance_on_unit_sphere ( latitude, longitude, storedLocations[destination][0], storedLocations[destination][1])

        print "Distance: " + str(distanceDifference)

        #return "{\"web-app\": { }}"
        return str(distanceDifference)

class updateUserInfo:        
    def GET(self, notification,userID,key,secret):
        return notification + userID + key + secret
        
          

class get_tweets:
    def GET(self, topic_id):
        output = 'tweets:[';            
        # make calls to sajann function providing topicid
        # organise messages to 3 essential info below
        # assume data organised as seen below
        tid = "topicID1"
        topic_input = "topic1"
        mid_input = ["mid1","mid2","mid3","mid4","mid5"];
        root = convert_to_xml_tweet(tid,mid_input,topic_input)
        for child in root:
            print 'child', child.tag, child.attrib
            output += str(child.attrib) + ','
        output += ']';
        return output


#Example Specific to Topic
#<Topics uid="userID">
#    <topic id="topicID1" name="Rocky" />
#    <topic id="topicID2" name="Steve" />
#    <topic id="topicID3" name="Melinda" />
#</Topics>


def convert_to_xml_topic(uid,tid_input,topic_input):
    top = Element('Topics',{'uid':uid})
    i=0
    for topic in topic_input:
        child = SubElement(top, 'topic',{'id':tid_input[i] ,'name':topic })
        i=i+1
    return top
  
#Example: Specific Tweets Topic 
#<Tweets tid="topicID1" name="Rocky">
#    <message id="messageID1"/>
#    <message id="messageID2"/>
#    <message id="messageID3"/>
#    <message id="messageID1"/>
#    <message id="messageID2"/>
#    <message id="messageID3"/>
#</Tweets>

def convert_to_xml_tweet(tid,mid_input,topic_input):
    top = Element('Tweets',{'tid':tid,'name':topic_input })
    i=0
    for mid in mid_input:
        child = SubElement(top, 'message',{'id':mid})
        i=i+1
    return top

#print tostring(tweet_xml)



if __name__ == "__main__":
    app.run()
    
    
    
    
# Reference Beautiful Soup XML Usage

# handler = open('./xml/xml_for_demo.xml').read()
# soup = BeautifulSoup(handler);
# 
# 
# x=soup.findAll('c_task')
# print x[0]

# for c_task in soup.findAll('c_task'):
#     #print c_task.find('image_url').contents[0] #get value in a node
#     #print c_task.attrs['id'] # get value of an id
#     print c_task.image_url.contents[0]

