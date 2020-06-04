import xml.etree.ElementTree as ET
trackXML = ET.parse('info_base.xml')
trackRoot = trackXML.getroot()
print(trackRoot.find('./branch').tag)
for i in trackXML.iter():
    j = i.find('path')
    print(j)
d = {"a":1,'b':2}
for key in d:
    print(key)

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
