#!/usr/bin/python3

import json
import subprocess

try:  # open the enact/suggest file
    with open('enact/suggested.json') as data_file:    
        suggested_data = json.load(data_file)
    
    rate = suggested_data['rate']
    temp = suggested_data['temp']

except:
    print ("error loading enact/suggested.json")

try:  # parse the enact/suggested file and see if there is a duration in there
    duration = suggested_data['duration']
    
    try:  # write a temp file that will be used to enact a new temp basal
        with open('enact/temp.json', 'w') as file:
            temp_json = ({"duration":duration,"rate":rate,"temp":temp})
            file.write = json.dump(temp_json,file,indent=2,separators=(',', ':'),sort_keys=True)
            
    except:
        print ("error writing out enact/temp.json file")
        
    try:  # attempt to send the set_temp_basal using the enact/temp.json file just created
        output = subprocess.Popen(["openaps", "use", "pump","set_temp_basal","enact/temp.json"], stdout=subprocess.PIPE).communicate()[0]

        output = output.decode("utf-8")    # convert from byte object to unicode text string
        output = output.replace('\n','')   # remove newlines
        output = " ".join(output.split())  # replace double-spaces with single spaces
        returned_data = json.loads(output) # returned_data now contains a dict of the returned object data
        
        # merge returned_data dictionary with enact/suggested.json dictionary
        enacted_data = suggested_data.copy()
        enacted_data.update(returned_data)
        
        print(enacted_data)
        
        # write out merged dictionary
        with open('enact/enacted.json', 'w') as file:
            file.write = json.dump(enacted_data,file,indent=2,separators=(',', ':'),sort_keys=True)    
    
    except:  # failure in the setting of a temp basal somewhere
        print ("error calling set_temp_basal, dissecting function output, or merging dictionaries")

except:  # there wasn't a duration in enact/suggested, meaning no temp is necessary    
    
    try:  # check for a temp basal currently set
        with open('monitor/temp_basal.json') as data_file:    
            temp_basal_data = json.load(data_file)
        
        duration = temp_basal_data['duration']       
        
        if duration is not 0:  # there is currently a temp basal underway that needs cancelled
            with open('enact/temp.json', 'w') as file:
                    temp_json = ({"duration":0,"rate":rate,"temp":"absolute"})
                    file.write = json.dump(temp_json,file,indent=2,separators=(',', ':'),sort_keys=True)

            output = subprocess.Popen(["openaps", "use", "pump","set_temp_basal","enact/temp.json"], stdout=subprocess.PIPE).communicate()[0] 
    except:
        print ("error reading monitor/temp_basal, writing out enact/temp.json, or issuing command to cancel temp basal")       
    
    try:      
        output = output.decode("utf-8")    # convert from byte object to unicode text string
        output = output.replace('\n','')   # remove newlines
        output = " ".join(output.split())  # replace double-spaces with single spaces
        returned_data = json.loads(output) # returned_data now contains a dict of the returned object data
        
        # merge returned_data dictionary with enact/suggested.json dictionary
        enacted_data = suggested_data.copy()
        enacted_data.update(returned_data)
        
        print(enacted_data)
    
        # write out merged dictionary
        with open('enact/enacted.json', 'w') as file:
            file.write = json.dump(enacted_data,file,indent=2,separators=(',', ':'),sort_keys=True)   
    except:
        print ("error writing out enact/enacted.json")
