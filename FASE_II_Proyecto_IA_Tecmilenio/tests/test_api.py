from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    r=client.get('/health'); assert r.status_code==200 and r.json()['status']=='ok'

def test_frontend():
    r=client.get('/'); assert r.status_code==200 and 'Asistente' in r.text

def test_faq():
    d=client.post('/api/chat',json={'question':'¿Dónde consulto mi estado de cuenta?'}).json()
    assert d['source']=='FAQ-004' and d['escalate'] is False

def test_unknown_escalates():
    d=client.post('/api/chat',json={'question':'¿Me autorizan un crédito?'}).json()
    assert d['escalate'] is True

def test_empty_rejected():
    assert client.post('/api/chat',json={'question':'   '}).status_code==422

def test_long_rejected():
    assert client.post('/api/chat',json={'question':'x'*501}).status_code==422

def test_sensitive_escalates():
    d=client.post('/api/chat',json={'question':'Mi CVV: 123'}).json()
    assert d['escalate'] is True and d['source']=='SEG-001'
