import pandas as pd

list1 = ['Phone', 'Bag', 'Laptop', 'Glasses']
list2 = ['21', '15', '150', '200']
list3 = ['Germany', 'USA', 'Japan', 'Canada']

listall = [list1, list2, list3]

frame = pd.DataFrame(listall)
frame = frame.transpose()
print(frame)