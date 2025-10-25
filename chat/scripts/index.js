window.onload = async function() {
    startLoading();

    try {
        await loadPersonas();
    } catch (err) {
        console.log(err);
        showToast('Não foi possível carregar os personas.');
    } finally {
        endLoading();
    }
};

$personasSelect = document.getElementById('personas');
$startChatButton = document.getElementById('main-persona-button')

async function loadPersonas() {
    const res = await get('persona');

    if (!res) {
        throw new Error('Não foi possível recuperar os personas.');
    }

    $personasSelect.innerHtml = '';
    removeOptions();
    res.forEach(persona => {
        handlePersonaOption(persona.id, persona.name);
    });
}

function handlePersonaOption(id, name) {
    const $option = document.createElement('option');
    $option.value = id;
    $option.textContent = name;
    $option.className = 'persona-option';
    $personasSelect.appendChild($option);
}

$startChatButton.addEventListener('click', () => {
    const personaId = $personasSelect.value;
    if (!personaId) {
        return;
    }

    window.location.href = `./pages/chat.html?id=${personaId}`;
});

function removeOptions() {
   let i, L = $personasSelect.options.length - 1;

   for(i = L; i >= 0; i--) {
      $personasSelect.remove(i);
   }
}