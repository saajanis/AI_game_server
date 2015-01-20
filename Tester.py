from xml.dom import minidom
from bs4 import BeautifulSoup


print range(80, 86, 1)

handler = open('./xml/2_xml_for_demo.xml').read()
soup = BeautifulSoup(handler);

c_task_list=soup.findAll('c_task')


print c_task_list[0]

#print c_task_list


print "####################"

print c_task_list[0].specifier.contents
print c_task_list[0].post_cond.credits.true
print c_task_list[0].post_cond.variables.contents


# print c_task_list[8].message.contents
# 
# if (len(c_task_list[8].message.contents) == 0):
#     print "detected"
# response = ''
# for individual_response in c_task_list[1].response.findAll('resp'):
#     response += "\"resp_" +  individual_response.attrs['id'] +"\": \"" + individual_response.contents[0] + "\", "
# response = response[:-2]
# 
# print response

# for (individual_response in (c_task_list[1].response.findAll('resp'))):
#         print individual_response.contents[0]

# for c_task in soup.findAll('c_task'):
#     #print c_task.find('image_url').contents[0] #get value in a node
#     #print c_task.attrs['id'] # get value of an id
#     print c_task.image_url.contents[0]

