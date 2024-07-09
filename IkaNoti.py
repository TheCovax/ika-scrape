import requests
import datetime
from bs4 import BeautifulSoup

def chunk_string(text, chunk_size):
    # List to hold the chunks
    chunks = []
    # Loop through the text, taking substrings of chunk_size
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

def sendDcNoti():
    global payload

    chunks = chunk_string(payload, 1900)
    for i, chunk in enumerate(chunks):
    
        data = {
            "content": chunk
        }
        print(requests.post(webhook_url, json=data).status_code)

webhook_url = "https://discord.com/api/webhooks/1226806125266210887/Lq3dM6PPIif4NSi3owWhLia8Rm0zUFtEtz06LJBkbwGrPzt4NAD-ttgIkWFt3eMfpxM1"


#html = '<td> <script type="text/javascript">  $(document).ready(function () { getCountdown({ enddate: 1718146915,   currentdate: 1718232682, el: "researchCountDown30"                    }, 3, " ", "", true, true);                });           </script>           <div class="type">                <div class="time" id="researchCountDown30">-</div>            </div>        </td>        <td class="left red">Fleets station</td>        <td class="center">5</td>        <td class="left">            <a class="bold" href="?view=avatarProfile&amp;avatarId=134186"                onclick="ajaxHandlerCall(this.href); return false;">Lalu</a>            <a class="bold" href="?view=island&amp;cityId=71479">(Sorisz )</a>            <a class="allyMailIcon" href="?view=sendIKMessage&amp;receiverId=134186"                onclick="ajaxHandlerCall(this.href);return false;" title="Write message"></a>        </td>        <td class="left">            <a class="bold" href="?view=avatarProfile&amp;avatarId=137473"                onclick="ajaxHandlerCall(this.href); return false;">OogieBoogie</a>            <a class="bold" href="?view=island&amp;cityId=87318">(Drunk )</a>            <a class="allyMailIcon" href="?view=sendIKMessage&amp;receiverId=137473"                onclick="ajaxHandlerCall(this.href);return false;" title="Write message"></a>        </td>'



def getGeneralViewRow(inner_html):
    soup = BeautifulSoup(inner_html, 'html.parser')

    cells = soup.findAll("td")
    rowString = "| "
    for c in cells:
        rowString = rowString + str(c.getText(strip=True)).strip().replace("  ","") + " | "

    print(rowString)
    return rowString

def payloadToTxt():
    f = open("general.txt","w")
    f.write(payload)
    f.close()

def payloadFromTxt():
    f = open("general.txt",'r')
    return f.read()