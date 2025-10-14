const API_URL = 'http://127.0.0.1:8000';

async function post(path, payload) {
    const res = await request(path, 'POST', { 'Content-Type': 'application/json' }, JSON.stringify(payload));
    return res;
}

async function get(path) {
    const res = await request(path, 'GET');
    return res;
}

async function remove(path) {
    const res = await request(path, 'DELETE');
    return res;
}

async function request(path, method, headers = undefined, payload = undefined) {
    const res = await fetch(`${API_URL}/${path}`, {
        method: method,
        headers: headers,
        body: payload
    });

    if (!res.ok) {
        throw new Error('HTTP ' + res.status);
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (!res.ok) {
        throw new Error('HTTP ' + res.status);
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