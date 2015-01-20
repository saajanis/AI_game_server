from essentialFunction import *
import math
import random

from xml.etree.ElementTree import Element, SubElement, tostring
import web
import xml.etree.ElementTree

from xml.dom import minidom
from bs4 import BeautifulSoup

import urlparse
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer



##### GLOBAL VARS
convo_count_student = 0
convo_count_professor = 0
convo_count_janitor = 0

threshold_count_student = 10
threshold_count_professor = 5
threshold_count_janitor = 5

sudent_convo_range = [80, 104]
professor_convo_range = [31, 37]
janitor_convo_range = [38, 45]
        
        ####


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
        
        handler = open('./xml/Sanjana_xml_3.xml').read()
        soup = BeautifulSoup(handler);
        c_task_list=soup.findAll('c_task')
        
        user = user.split("/")
        print "User: " + str(user)
        user_response = str(user[0])
        print user_response
        next_node = int( user_response.split(":")[0] )
        
        if (user[1] == ''):
            current_c_task_id = ""
        else:
            current_c_task_id = int (user[1])
        
        if (user[2] == "null"):
            credits_string = ""
        else:
            credits_string = str(user[2])
        
        if (user[3] == ""):
            variables_string = ""
        else:    
            variables_string = str(user[3])
        if (user[4] == ""):
            story_so_far = ""
        else:    
            story_so_far = str(user[4])
        player_credits = add_credits ([], credits_string)
        player_variables = update_variables ([-1, -1, -1], variables_string)
                                                #^^ before, it was default [-1, -1, -1]
        print "wopp: " + str(player_variables)
        
        ####GLOBAL INIT
        global convo_count_student
        global convo_count_professor 
        global convo_count_janitor
        
        global threshold_count_student
        global threshold_count_professor
        global threshold_count_janitor 
        if (next_node == 0):
            convo_count_student = 0
            convo_count_professor = 0
            convo_count_janitor = 0
        
        global sudent_convo_range 
        global professor_convo_range
        global janitor_convo_range
        
        #############TRIVIAL CONVERSATION CHECK
        (convo_count_student, convo_count_professor, convo_count_janitor, callContingency) = check_trivial_conversation (next_node, convo_count_student, convo_count_professor, convo_count_janitor, threshold_count_student, threshold_count_professor, threshold_count_janitor, sudent_convo_range, professor_convo_range, janitor_convo_range)
        
        if (callContingency==1):
            convo_count_student = 0
            convo_count_professor = 0
            convo_count_janitor = 0
            next_node = 1000
        #######################################
        ##############
        
        (pre_cond_location, pre_cond_credits_string, pre_cond_variables_string, child_nodes_string, image_url, header, message,  post_cond_credits_true_string, post_cond_credits_false_string, player_variables_update_string) = get_ctask_values( get_node_by_id(c_task_list, next_node) )
        ## ctype node values return
        
        ##GENERATE RESPONSES
        
        if (post_cond_credits_true_string is not None):
            player_credits = add_credits (player_credits, post_cond_credits_true_string)
        if (post_cond_credits_false_string is not None):    
            player_credits = remove_credits (player_credits, post_cond_credits_false_string)
        player_variables = update_variables (player_variables, player_variables_update_string)
        
        player_credits = str(player_credits).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        player_variables = str(player_variables).replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
        pre_cond_location = pre_cond_location.strip().lower()
        
        
        responses = get_responses_from_children (c_task_list, child_nodes_string, player_credits, player_variables)
        
        
        print pre_cond_location
        print image_url
        print header
        print message
        print responses
        print player_credits
        print player_variables
        
        
        #####TOMMY ISSUE
        header = header.replace("\"", "")
        message = message.replace("\"", "")
        #responses = responses
        
        i=0
        response_json = ""
        for response in responses:
            i+=1
            response_json += '"'+str(i)+'": '+'"'+str(response).replace("\"", "").replace("\'", "")+'", ' 
        response_json = response_json.strip(", ")
        
        
        
        
        
        
        json_response = '{"pre_cond_location": "'+str(pre_cond_location)+'", "current_c_task_id": "'+str(next_node)+'", "img_url": "'+ str(image_url)+'", "header": "'+str(header)+'", "message": "'+str(message)+'", "response":{' +str(response_json)+'}' +' , "player_credits": "'+str(player_credits)+'", "player_variables": "'+str(player_variables)+'", "story_so_far": "'+str(story_so_far) + '"}'
        print json_response
        ## CHECK LOCATION PRE_COND LATER 

        
        return json_response


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

