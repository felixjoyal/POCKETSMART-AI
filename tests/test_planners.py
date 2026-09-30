def login(client):
    client.post("/register",data={"username":"planner","email":"planner@example.com","password":"password123"})
    client.post("/login",data={"username":"planner","password":"password123"})

def test_home_planner(client):
    login(client)
    r=client.post("/api/generate-home",json={"budget":50000,"rooms":["Living Room"],"lights":2,"fans":1,"furniture_items":2,"style":"Modern","notes":""})
    assert r.status_code==200
    d=r.json()
    assert d["planner_type"]=="home" and d["remaining_budget"]>=0 and d["sections"]

def test_party_planner(client):
    login(client)
    r=client.post("/api/generate-party",json={"budget":60000,"guests":50,"event_type":"Birthday","venue_type":"Indoor","catering":True,"decoration":True,"entertainment":True,"notes":""})
    assert r.status_code==200 and r.json()["planner_type"]=="party"

def test_jewelry_planner(client):
    login(client)
    r=client.post("/api/generate-jewelry",data={"budget":15000,"occasion":"Wedding","style":"Elegant","preferences":"Lightweight"})
    assert r.status_code==200 and r.json()["planner_type"]=="jewelry"

def test_history(client):
    login(client)
    client.post("/api/generate-home",json={"budget":30000,"rooms":["Bedroom"],"lights":1,"fans":1,"furniture_items":1,"style":"Minimal","notes":""})
    r=client.get("/api/history")
    assert r.status_code==200 and len(r.json())==1
