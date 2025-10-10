const hiddenClass = 'hidden'
const $loading = document.getElementById('loading');
const $spinner = document.createElement('div');
$spinner.classList.add('spinner');
$loading.appendChild($spinner);
endLoading();

function startLoading() {
    $loading.classList.remove(hiddenClass);
}

function endLoading() {
    $loading.classList.add(hiddenClass);
}