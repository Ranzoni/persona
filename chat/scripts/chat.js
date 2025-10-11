const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const personaId = urlParams.get('id'); 
const conversation = [];

window.onload = async function() {
    if (!personaId) {
        window.location.href = '../index.html';
        return;
    }

    startLoading();

    try {
        if (!getId()) {
            await generateId();
        }

        await loadPreviousMessages();
    } catch (err) {
        console.log(err);
    } finally {
        endLoading();
    }
};

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

    const res = await post(`talk/${getId()}/${personaId}`, payload);
  
    if (res) {
        return res;
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

async function loadPreviousMessages() {
    const res = await get(`messages/${getId()}/${personaId}`);

    if (!res) {
        throw new Error('Formato de resposta inesperado');
    }

    res.forEach(message => appendMessage(message.content, message.who));
}

async function generateId() {
    const res = await post('generate-id');
    
    if (!res) {
        throw new Error('ID gerado não é válido');
    }

    saveId(res);
}
