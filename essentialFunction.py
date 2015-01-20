from xml.dom import minidom
from bs4 import BeautifulSoup

################################################################
def add_credits (previous_credits, update_string):
    update_list = (update_string.split(","))
    update_list = [item.strip().lower() for item in update_list]
    
    for item in update_list:
        if (item not in previous_credits):
            previous_credits.append(item)
            
    return previous_credits
    

def remove_credits (previous_credits, update_string):
    update_list = (update_string.split(","))
    update_list = [item.strip().lower() for item in update_list]
    
    for item in update_list:
        if (item in previous_credits):
            previous_credits.remove(item)
            
    return previous_credits

def update_variables (previous_variables, update_string):
    print "lalaa"
    print previous_variables
    print update_string
    update_list = (update_string.split(","))
    
    for i in range (len(previous_variables)):
        if (previous_variables[i]==-1):
            previous_variables[i]=int(update_list[i])
            continue
        previous_variables[i] += int(update_list[i])
        if (previous_variables[i]<0):
            previous_variables[i]=0
        if (previous_variables[i]>10):
            previous_variables[i]=10   
            
    return previous_variables

####

def satisfies_credits_precondition (player_credits, pre_cond_credits_string):
    pre_cond_credits_list = (pre_cond_credits_string.split(","))
    pre_cond_credits_list = [item.strip().lower() for item in pre_cond_credits_list]

    for item in pre_cond_credits_list:
        if (item not in player_credits):
            return False
    
    return True    

def satisfies_variables_precondition (player_variables, pre_cond_variables_string):
    pre_cond_variables_list = (pre_cond_variables_string.split(","))
    player_variables = player_variables.split(",")
    
    for i in range (len(player_variables)):      
        if (int (player_variables[i]) < int(pre_cond_variables_list[i])):
            return False
        
        return True
            

def get_ctask_values (ctask):
    
    pre_cond_location = None
    pre_cond_credits_string  = None
    pre_cond_variables_string  = None
    child_nodes_string  = None
    image_url  = None
    header  = None
    message  = None
    post_cond_credits_true_string  = None
    post_cond_credits_false_string  = None  
    player_variables_update_string  = None
    
    if (len(ctask.location.contents) != 0):
        pre_cond_location = str(ctask.location.contents[0])
    if (len(ctask.credits.contents) != 0):
        pre_cond_credits_string = str(ctask.credits.contents[0])
    if (len(ctask.variables.contents) != 0):
        pre_cond_variables_string = str(ctask.variables.contents[0])
    if (len(ctask.next_in_order.contents) != 0):
        child_nodes_string = str(ctask.next_in_order.contents[0])
    if (len(ctask.image_url.contents) != 0):
        image_url = str(ctask.image_url.contents[0])
    if (len(ctask.header.contents) != 0):
        header = str(ctask.header.contents[0])
    if (len(ctask.message.contents) != 0):
        message = str(ctask.message.contents[0])
    if (len(ctask.post_cond.credits.true.contents) != 0):
        post_cond_credits_true_string = str(ctask.post_cond.credits.true.contents[0])
    if (len(ctask.post_cond.credits.false.contents) != 0):
        post_cond_credits_false_string = str(ctask.post_cond.credits.false.contents[0])  
    if (len(ctask.post_cond.variables.contents[0]) != 0):
        player_variables_update_string = str(ctask.post_cond.variables.contents[0])
    
    return (pre_cond_location, pre_cond_credits_string, pre_cond_variables_string, child_nodes_string, image_url, header, message,  post_cond_credits_true_string, post_cond_credits_false_string, player_variables_update_string) 

def get_node_by_id (c_task_list, id):
    
    for c_task in c_task_list:
        if (c_task['id']==str(id)):
            return c_task
    return False

def get_responses_from_children (c_task_list, child_nodes_string, player_credits, player_variables):
    responses = []
    child_nodes_list = (child_nodes_string.strip().split(","))
    child_nodes_list = [int(node) for node in child_nodes_list]
    for node in child_nodes_list:
        print node
        if (get_node_by_id (c_task_list, node) == False):
            continue
        pre_cond_credits_string = get_node_by_id (c_task_list, node).pre_cond.credits.contents[0]
        pre_cond_variables_string = get_node_by_id (c_task_list, node).pre_cond.variables.contents[0]
        
        satisfies_credits = satisfies_credits_precondition(player_credits, pre_cond_credits_string)
        satisfies_variables = satisfies_variables_precondition (player_variables, pre_cond_variables_string)
        
        if (satisfies_credits==True and satisfies_variables ==True):
            responses.append (str(node)+":"+str(get_node_by_id (c_task_list, node).specifier.contents[0].strip()))
    
    return responses
        
def check_trivial_conversation (next_node, convo_count_student, convo_count_professor, convo_count_janitor, threshold_count_student, threshold_count_professor, threshold_count_janitor, sudent_convo_range, professor_convo_range, janitor_convo_range):
  
    print "Output: check_trivial_conversation"
    callContingency = 0
    
    if (int(next_node) in range(int(sudent_convo_range[0]), int(sudent_convo_range[1]))):
        convo_count_student+=1
        print "inrementing Student counter: " +  str(convo_count_student)
    if (int(next_node) in range(int(professor_convo_range[0]), int(professor_convo_range[1]))):
        convo_count_professor+=1
        print "inrementing Professor counter: " +  str(convo_count_professor)
    if (int(next_node) in range(int(janitor_convo_range[0]), int(janitor_convo_range[1]))):
        convo_count_janitor+=1
        print "inrementing Janitor counter: " +  str(convo_count_janitor)
    
    ######CONTINGENCY CHECK
    if (convo_count_student>threshold_count_student or convo_count_professor>threshold_count_professor  or convo_count_janitor>threshold_count_janitor):
        callContingency = 1
        print "call contingency!!"
    ####################### 
    
    return (convo_count_student, convo_count_professor, convo_count_janitor, callContingency)
    ##RETURN updated vals
    
    print "##################################"

   
#def replace_with_contingency_node():   
    

##################################################################


