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

        await loadPersonaData(personaId);
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
const $personaName = document.getElementById('persona-name');
const $personaImage = document.getElementById('persona-image');

function scrollToBottom() {
    $messages.scrollTop = $messages.scrollHeight;
}

function formatTime(date = new Date()){
    return date.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
}

function appendMessage(text, who = 'bot', meta = '', appendLastMessage = false) {
    if (appendLastMessage) {
        const messages = document.querySelectorAll(`.${who}`);
        const lastMessage = messages[messages.length - 1];

        lastMessage.textContent += text;
        return;
    }

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
        let answerStarted = false;
        const conversationObj = {role: 'assistant', content: ''};
        for await (const chunk of gePersonaAnswer(personaId, conversation)) {
            conversationObj.content += chunk;
            appendMessage(chunk, 'bot', '', answerStarted);
            answerStarted = true;
        }
        
        conversation.push(conversationObj);
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

async function* gePersonaAnswer(personaId, history) {
    if (!API_URL) {
	      yield handleFailToCommunicateWithPersona();
        return;
    }

    const payload = { message: history[history.length-1].content };

    const res = postStream(`talk/${getId()}/${personaId}`, payload);
    for await (const chunk of res) {
        yield chunk;
    }
}

function handleFailToCommunicateWithPersona() {
    return 'Não foi possível comunicar com o Persona. Tente novamente mais tarde.';
}

$send.addEventListener('click', sendMessage);
$clear.addEventListener('click', async () => {
    $messages.innerHTML= '';
    conversation.length= 0;
    $input.value= '';
    $input.focus();

    await remove(`messages/${getId()}/${personaId}`);
});

$input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

async function loadPersonaData(id) {
    const res = await get(`persona/${id}`);

    if (!res) {
        throw new Error('Falha ao recuperar os dados do persona.');
    }

    $personaName.textContent = res.name;
    $personaImage.src = res.image;
}

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
