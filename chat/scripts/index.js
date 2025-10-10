window.onload = async function() {
    startLoading();

    try {
        await loadPersonas();
    } catch (err) {
        console.log(err);
    } finally {
        endLoading();
    }
};

$personasSelect = document.getElementById('personas');

async function loadPersonas() {
    const res = await get('personas');
    const json = await res.json();

    if (!json.personas) {
        throw new Error('Não foi possível recuperar os personas.');
    }

    json.personas.forEach(persona => {
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