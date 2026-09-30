def test_register_login_logout(client):
    r=client.post("/register",data={"username":"testuser","email":"test@example.com","password":"password123"},follow_redirects=False)
    assert r.status_code==303
    r=client.post("/login",data={"username":"testuser","password":"password123"},follow_redirects=False)
    assert r.status_code==303
    assert "pocketsmart_token" in r.headers.get("set-cookie","")
    r=client.get("/dashboard")
    assert r.status_code==200 and "testuser" in r.text
    assert client.get("/logout",follow_redirects=False).status_code==303

def test_invalid_login(client):
    client.post("/register",data={"username":"testuser","email":"test@example.com","password":"password123"})
    r=client.post("/login",data={"username":"testuser","password":"wrong-password"},follow_redirects=False)
    assert r.status_code==303 and "error=Invalid" in r.headers["location"]
