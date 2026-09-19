from hooks.seo_mutation_guard import authorize
cases=[
 {"resource":"robots_txt","production":True,"scope":1,"reduces_access":True},
 {"resource":"canonical","production":True,"scope":100},
 {"operation":"fake_reviews","production":False},
 {"resource":"title","production":True,"scope":1},
]
for case in cases:
    print(case, "=>", authorize(case))
