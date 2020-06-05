import xml.etree.ElementTree as ET
trackXML = ET.parse('info.xml')
trackRoot = trackXML.getroot()

deep = 0
def _branchInit(track: ET.Element):
    global deep
    print("-"*deep,track.find('./name').text)
    branch = track.find('./branch').findall('track')
    deep += 1
    if branch is None:
        deep += -1
        return True
    else:
        for i in branch:
            _branchInit(i)
        deep += -1
        return True
_branchInit(trackRoot)

#     j = i.find("name")
#     if j is not None:
#         print(i.find("name").text)
# import pandas as pd
# import numpy as np
# writer = pd.ExcelWriter("test.xlsx")
# b1 = pd.DataFrame({"A":np.arange(0,5,1),"B":np.arange(0,5,1)})
# b1.to_excel(excel_writer=writer,sheet_name='first')
# writer.save()
# b2 = pd.DataFrame({"jim": np.random.normal(size=10), 'book': np.random.normal(size=10)})
# b2.to_excel(excel_writer=writer,sheet_name='secend')
# writer.save()
# b1["A"][2]="df"
# #b1.to_excel(excel_writer=writer,sheet_name="first")
# writer.save()
# writer.close()
