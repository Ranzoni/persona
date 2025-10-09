let personaId;

window.onload = function() {
  startLoading();

  handleIp(async (ip) => {
    try {
      personaId = 1;
      saveIp(ip);
      await load_previous_messages();
    } catch (err) {
      console.log(err);
    } finally {
      endLoading();
    }
  });
};

const API_URL = 'http://127.0.0.1:8000';

const $messages = document.getElementById('messages');
const $input = document.getElementById('input');
const $send = document.getElementById('send');
const $clear = document.getElementById('clear');

function scrollToBottom() {
  $messages.scrollTop = $messages.scrollHeight;
}

function formatTime(date = new Date()){
  return date.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
}

function appendMessage(text, who = 'bot', meta = '') {
  const el = document.createElement('div');
  el.className = 'message ' + (who === 'me' ? 'me' : 'bot');
  el.innerText = text;
  const container = document.createElement('div');
  container.appendChild(el);
  
  if (meta) {
    const m = document.createElement('div');
    m.className = 'meta';
    m.innerText = meta;
    container.appendChild(m);
  }

  $messages.appendChild(container);
  scrollToBottom();
  return el;
}

const conversation = [];

async function sendMessage(){
  const text = $input.value.trim();
  if (!text) {
    return;
  }

  conversation.push({role:'user', content:text});
  appendMessage(text, 'me');
  $input.value = '';
  $input.focus();
  setUIBusy(true);

  try {
    const reply = await gePersonaAnswer(personaId, conversation);
    conversation.push({role:'assistant', content:reply});
    appendMessage(reply, 'bot');
  } catch(err) {
    console.error(err);
    appendMessage('Erro: não foi possível obter resposta do servidor.', 'bot', formatTime());
  } finally {
    setUIBusy(false);
  }
}

function setUIBusy(isBusy){
  $send.disabled = isBusy;
  $input.disabled = isBusy;

  if (isBusy) {
    $send.innerText = 'Aguardando...'; 
  } else {
    $send.innerText = 'Enviar';
  }
}

async function gePersonaAnswer(personaId, history) {
  if (!API_URL) {
	  return handleFailToCommunicateWithPersona();
  }

  const payload = { message: history[history.length-1].content };

  const res = await fetch(`${API_URL}/talk/${getIp()}/${personaId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  if (!res.ok) {
    throw new Error('HTTP ' + res.status);
  }

  const json = await res.json();
  
  if (json.persona_response) {
    return json.persona_response;
  }

  throw new Error('Formato de resposta inesperado');
}

function handleFailToCommunicateWithPersona() {
  return 'Não foi possível comunicar com o Persona. Tente novamente mais tarde.';
}

$send.addEventListener('click', sendMessage);
$clear.addEventListener('click', () => {
  $messages.innerHTML='';
  conversation.length=0;
  $input.value='';
  $input.focus();
});

$input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

async function load_previous_messages() {
  const res = await fetch(`${API_URL}/messages/${getIp()}/${personaId}`, {
    method: 'GET'
  });

  debugger;
  if (!res.ok) {
    throw new Error('HTTP ' + res.status);
  }

  const json = await res.json();

  if (!json.history_messages) {
    throw new Error('Formato de resposta inesperado');
  }

  json.history_messages.forEach(message => appendMessage(message.content, message.who));
}

