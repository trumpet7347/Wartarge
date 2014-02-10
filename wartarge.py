from ghost import Ghost
import math
import time

eveApiUrl = "http://api.eveonline.com/eve/CharacterID.xml.aspx?names="
eveApiUrlAlliances = "https://api.eveonline.com/eve/AllianceList.xml.aspx?version=1"
eveWhoUrl = "http://evewho.com/api.php"

browser = Ghost(cache_dir='cache', download_images=False)

#Get Corporation ID from Eve API
def getCorpId(corpName):
  import xml.etree.ElementTree as ET
  url = eveApiUrl + corpName
  page, resources = browser.open(url)
  root = ET.fromstring(page.content)
  corpID = root.find("./result/rowset/row[@characterID]").attrib["characterID"]
  return corpID

def getAllianceId(allianceName):
  import xml.etree.ElementTree as ET
  name = allianceName
  page, resource = browser.open(eveApiUrlAlliances)
  root = ET.fromstring(page.content)
  allianceID = root.find("./result/rowset/row[@name='%s']" %(name)).attrib["allianceID"]
  return allianceID

#Get list of members from Eve Who API
def getMemberList(form, ID):
  import json
  url = eveWhoUrl + "?type=" + form + "&id=" + ID
  page, resources = browser.open(url)
  print url
  eveWhoList = json.loads(page.content)
  members = {}
  membersCount = int(eveWhoList['info']['memberCount'])

  if membersCount <= 200:
    index = 1
    for characters in eveWhoList['characters']:
      members[index] = str(characters['name'])
      index += 1

  else:
    count = int(math.ceil(201/200.0))

    index = 1
    for characters in eveWhoList['characters']:
      members[index] = str(characters['name'])
      index += 1

    for x in range(1, count+2):
      time.sleep(1)
      newUrl = url + '&page=' + str(x)
      page, resource = browser.open(newUrl)
      eveWhoList = json.loads(page.content)

      for characters in eveWhoList['characters']:
        members[index] = str(characters['name'])
        index += 1

  return members

def loginEveGate(username, password):
  page, resources = browser.open('http://gate.eveonline.com/')
  browser.click('.ccploginwidget-login a', expect_loading=True)
  browser.fill("form", {"UserName" : username, "Password" : password})
  page, resources = browser.fire_on("form", "submit", expect_loading=True)

  if browser.exists('.validation-summary-errors'):
    raise Exception('Login Failure')

def addContact(characterName):
  try:
    page, resources = browser.open("http://gate.eveonline.com/Profile/%s" %(characterName))
    browser.evaluate("document.getElementById('addContactPopUp').setAttribute('style', '')")
    browser.click('#divStanding0 img')
    browser.click('#addToWatchlist')
    browser.click('#addContactButton img', expect_loading=True)
  except:
    print "Couldn't add user, it may not exist, or is already a contact"



def createNewLable(labelName):
  page, resources = browser.open("https://gate.eveonline.com/Contacts")
  browser.evaluate("document.getElementById('toggleContainerContentLabels').setAttribute('style', 'display: block; left: 163px; top: 48px;')")
  browser.evaluate("document.getElementById('labelFilterField').value = '%s'" %(labelName))
  browser.click('#labelCreateNew', expect_loading=True)

  #lets find the label id
  lblID, resources = browser.evaluate("var LabelID = 0; $('.labelListContainer').each( function(){ var id = $(this).attr('id'); var text = $(this).find('a > span').text();  if(text.split(' (')[0] == '" + labelName + "') LabelID = id;  } ) ; LabelID.replace(/[a-z]+/, '');")
  return lblID


  #browser.capture_to('test.png')

def moveToLabel(contactName, labelID):


  try:
    page, resources = browser.open("https://gate.eveonline.com/Contacts/Index/Neutral")
    browser.click('#checkBoxCheckAll')
    browser.evaluate("document.getElementById('toggleContainerContentLabels').setAttribute('style', 'display: block; left: 163px; top: 48px;')")

    browser.evaluate("document.getElementById('chkLabel" + labelID + "').setAttribute('checked', 'checked')")
    browser.click('input[id=chkLabel' + labelID + ']')
    browser.evaluate("document.getElementById('labelApply').setAttribute('style', 'display: inline;')")
    #browser.capture_to('test-apply.png')
    
    
    #browser.capture_to('test-after.png')    
    browser.click('#labelApply', expect_loading=True)

    #return
  except:
    print "There was an issue appplying labels..."
    #return # we should return, but something funky is going on, so set standing to red!

  #update the standing to red!!
  page, resources = browser.open("https://gate.eveonline.com/Contacts/Index/Neutral")
  browser.click('#checkBoxCheckAll')

  browser.click('#editMultipleContactsButtonTop')
  browser.click('#divStandingM10')
  browser.click('#editContactButton', expect_loading=True)