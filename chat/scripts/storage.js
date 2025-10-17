const SESSION_ID_VAR = 'session-id';

function saveSessionId(id, expiresIn) {
    localStorage.setItem(SESSION_ID_VAR, `${id}:${expiresIn}`);
}

function getSessionId() {
  const sessionId = localStorage.getItem(SESSION_ID_VAR);
  if (!sessionId) {
    return null;
  }

  const sessionIdParts = sessionId.split(':');
  const id = sessionIdParts[0];
  const expiresIn = sessionIdParts[1];

  if (Date.now() > formatExpiresIn(expiresIn)) {
    localStorage.removeItem(SESSION_ID_VAR);
    return undefined;
  }

  return id;
}

function formatExpiresIn(expiresIn) {
  if (!expiresIn) {
    return 0;
  }

  return expiresIn * 1000;
}