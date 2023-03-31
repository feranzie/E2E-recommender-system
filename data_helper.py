import pandas as pd
from prefect import flow, task, get_run_logger

#IMPORTING DATA FROM CSV FILES INTO A DATAFRAME FOR ANALYSIS 
post = pd.read_csv("data/posts.csv")
user = pd.read_csv("data/users.csv")
view = pd.read_csv("data/views.csv")
post["category"] = post["category"].fillna("random")
cat = {}
for i in post["category"]:
    cat.update({i:[]})
    for j in i.split("|"):
        cat[i].append(j)
updated_data =  []
for i in cat:
    dummy = post[post['category']==i]
    id = dummy['_id'].values[0]
    title = dummy['title'].values[0]
    post_type = dummy[' post_type'].values[0]
    for j in cat[i]: 
        dict1 = {}
        dict1.update({'_id':id})
        dict1.update({'title':title})
        dict1.update({'category':j})
        dict1.update({' post_type':post_type})
        updated_data.append(dict1)
post1 = pd.DataFrame(updated_data)
post1.rename(columns={"_id":'post_id'}, inplace = True)
user.rename(columns={"user_id":'post_id'},  inplace = True)
main = pd.merge(view,post1)
users = list(main["user_id"].unique())
categories = list(main["category"].unique())

#MATRIX WILL BE OF 88,235
user_mat = [[] for i in range(len(users))]
for i in range(len(users)):
    for j in range(len(categories)):
        value = len(main[(main["user_id"]==users[i]) & (main["category"]==categories[j])])
        user_mat[i].append(value)
from scipy.sparse import csr_matrix 
user_mat = csr_matrix(user_mat)