const API_URL = 'http://127.0.0.1:8000';
const sessionIdHeader = 'X-Session-ID';

function buildHeaders(value, sendSession) {
    let headers = value;
    if (sendSession) {
        if (!headers) {
            headers = { };
        }
        headers[sessionIdHeader] = getSessionId();
    }

    return headers;
}

async function post(path, payload, sendSession = false) {
    const headers = buildHeaders({ 'Content-Type': 'application/json' }, sendSession);
    const res = await request(path, 'POST', headers, JSON.stringify(payload));
    return res;
}

async function get(path, sendSession = false) {
    const headers = buildHeaders(undefined, sendSession);
    const res = await request(path, 'GET', headers);
    return res;
}

async function remove(path) {
    const headers = buildHeaders(undefined, sendSession);
    const ers = await request(path, 'DELETE', headers);
    return res;
}

async function request(path, method, headers, payload = undefined) {
    const res = await fetch(`${API_URL}/${path}`, {
        method: method,
        headers: headers,
        body: payload
    });

    const successRequest = await handleFailRequest(res, path, method, headers, payload);
    if (!successRequest) {
        return;
    }

    const json = await res.json()

    if (!json.success) {
        throw new Error(json.source);
    }
  
    return json.source;
}

async function* postStream(path, payload) {
    const res = await fetch(`${API_URL}/${path}`, {
        method: 'POST',
        headers: buildHeaders({ 'Content-Type': 'application/json'}, true),
        body: JSON.stringify(payload)
    });

    const successRequest = await handleFailRequest(res, path, 'POST', buildHeaders({ 'Content-Type': 'application/json'}, true), payload);
    if (!successRequest) {
        return;
    }
    
    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
        const { done, value } = await reader.read();

        if (done) {
            console.log("Stream finished.");
            break;
        }

        const chunkText = decoder.decode(value, { stream: true });
        yield chunkText;
    }
}

async function handleFailRequest(res, path, method, headers, payload = undefined) {
    if (!res.ok) {
        if (res.status === 401) {
            await generateId();
            await request(path, method, headers, payload);
            return false;
        }

        throw new Error('HTTP ' + res.status);
    }

    return true;
}

async function generateId() {
    const res = await post('generate-id');
    
    if (!res) {
        throw new Error('ID gerado não é válido');
    }

    saveSessionId(res.id, res.expiresIn);
}