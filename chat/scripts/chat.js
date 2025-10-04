const API_URL = "http://127.0.0.1:8000/talk";

/* ---------- UTILITÁRIOS ---------- */
const $messages = document.getElementById('messages');
const $input = document.getElementById('input');
const $send = document.getElementById('send');
const $clear = document.getElementById('clear');

function scrollToBottom(){ $messages.scrollTop = $messages.scrollHeight; }

function formatTime(date = new Date()){
  return date.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
}

function appendMessage(text, who = 'bot', meta = ''){
  const el = document.createElement('div');
  el.className = 'message ' + (who === 'me' ? 'me' : 'bot');
  el.innerText = text;
  const container = document.createElement('div');
  container.appendChild(el);
  if(meta){
	const m = document.createElement('div');
	m.className = 'meta';
	m.innerText = meta;
	container.appendChild(m);
  }
  $messages.appendChild(container);
  scrollToBottom();
  return el;
}

/* ---------- Conversa (histórico local) ---------- */
const conversation = [];

/* ---------- Envio / Recebimento ---------- */
async function sendMessage(){
  const text = $input.value.trim();
  if(!text) return;

  // adicionar mensagem do usuário ao histórico e UI
  conversation.push({role:'user', content:text});
  appendMessage(text, 'me');
  $input.value = '';
  $input.focus();
  setUIBusy(true);

  try{
	const reply = await getReplyFromAPI(conversation);
	conversation.push({role:'assistant', content:reply});
	appendMessage(reply, 'bot');
  }catch(err){
	console.error(err);
	appendMessage('Erro: não foi possível obter resposta do servidor.', 'bot', formatTime());
  }finally{
	setUIBusy(false);
  }
}

function setUIBusy(isBusy){
  $send.disabled = isBusy;
  $input.disabled = isBusy;
  if(isBusy) $send.innerText = 'Aguardando...'; else $send.innerText = 'Enviar';
}

/* ---------- Função que chama a API (ou mock) ---------- */
async function getReplyFromAPI(history){
  // Se API_URL estiver vazia, usamos uma simulação local (mock)
  if(!API_URL){
	return mockReply(history[history.length-1].content);
  }

  // Exemplo de payload: você pode enviar o histórico como quiser
  //const payload = { messages: history };
  const payload = { message: history[history.length-1].content };

  const res = await fetch(API_URL, {
	method: 'POST',
	headers: { 'Content-Type': 'application/json' },
	body: JSON.stringify(payload)
  });

  if(!res.ok) throw new Error('HTTP ' + res.status);
  const json = await res.json();

  // espera-se { reply: 'texto' } ou ajustar conforme sua API
  if(json.persona_response)
	return json.persona_response;
  throw new Error('Formato de resposta inesperado');
}

// Mock inteligente simples — personalize como quiser
function mockReply(userText){
  // respostas simuladas rápidas
  const lower = userText.toLowerCase();
  if(lower.includes('olá') || lower.includes('oi')) return 'Olá — eu sou um bot de demonstração. Como posso ajudar?';
  if(lower.includes('ajuda')) return 'Diga o que precisa: posso simular respostas, devolver o que você enviou, ou demonstrar integração.';
  // se nada específico, devolve eco com pequenas variações
  return 'Você disse: "' + userText + '" — (resposta simulada)';
}

/* ---------- Eventos UI ---------- */
$send.addEventListener('click', sendMessage);
$clear.addEventListener('click', ()=>{ $messages.innerHTML=''; conversation.length=0; $input.value=''; $input.focus(); });

$input.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter' && !e.shiftKey){
	e.preventDefault();
	sendMessage();
  }
});

/* ---------- Kickstart com mensagem do bot ---------- */
appendMessage('Olá! Eu sou o bot. Pergunte algo ou escreva um prompt para o LLM.', 'bot');

/* ---------- Dicas rápidas para integrar com um LLM real ----------
  - No backend, receba `messages` e envie para o LLM (ex: OpenAI, local Llama/LLM) retornando {reply: "..."}.
  - Adicione autenticação (API keys) e limite de taxa.
  - Para respostas longas, considere streaming (EventSource / SSE / WebSocket).
---------------------------------------------- */