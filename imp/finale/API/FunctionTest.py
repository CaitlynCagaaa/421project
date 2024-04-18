from APIFunctions import addDrawer, addTool, addEvent, getToolsInfo, getDrawersInfo, updateToolsInfo

#URL for accessing different endpoints
url = 'http://localhost:5000/add_drawer'

#getToolsInfo(url,100)   #getToolsInfo function

#getDrawersInfo(url,1)   #getDrawersInfo function

#updateToolsInfo(url, True,10, 100) #updateToolsInfo function

### addDrawer function test ###

drawerID = 102
drawerNum = 1
drawerBoxNum = 1
drawerStartX = 10
drawerStartY = 20
drawerPixelWidth = 100
drawerPixelHeight = 200
drawerYAML = "example_yaml_data"
drawerPicAllTools = "path_to_all_tools_image"
drawerPicNoTools = "path_to_no_tools_image"
drawerSymbols = [{"ID": 0, "X": 2168, "Y": 514, "W": 72, "H": 66, "picall": "toolbox0/drawer0/drawer_2_symbol0.jpg"}, {"ID": 1, "X": 2251, "Y": 1234, "W": 67, "H": 69, "picall": "toolbox0/drawer0/drawer_2_symbol1.jpg"}, {"ID": 2, "X": 2307, "Y": 1842, "W": 75, "H": 85, "picall": "toolbox0/drawer0/drawer_2_symbol2.jpg"}]
addDrawer(url, drawerNum, drawerBoxNum, drawerStartX, drawerStartY, drawerPixelWidth, drawerPixelHeight, drawerYAML, drawerPicAllTools, drawerPicNoTools, drawerSymbols)

### addTool function test ###

toolID = 12
toolName = "test"
toolType = "test"
toolClassifierType = "test"
toolDrawerID = 100
toolSymbolAvailable = False
toolSymbolPath = "test"
toolCheckedOut = False
toolStartX = 10
toolStartY = 10
toolPixelWidth = 100
toolPixelHeight = 100
toolPictureWithPath = "test"
toolPictureWithoutPath = "test"
toolInfoTakenManually = False
#addTool(url, toolID,toolName,toolType,toolClassifierType,toolDrawerID,
#        toolSymbolAvailable, toolSymbolPath, toolCheckedOut, toolStartX,
#        toolStartY, toolPixelWidth, toolPixelHeight, toolPictureWithPath,
#        toolPictureWithoutPath, toolInfoTakenManually)

### addEvent function test ###

eventID = 1
eventType = 1
eventToolID = 12
eventTimestamp = '2024-03-27 12:00:00'
eventDrawerLocation = 4
eventUserID = 456
eventNotes = 'Tool checked out by user'
#addEvent(url, eventID, eventType, eventToolID, eventTimestamp, eventDrawerLocation, eventUserID, eventNotes)
