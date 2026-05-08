let allCards = [];
let activeCardId = null;

async function loadCardList() {
    const res = await fetch('/api/cards');
    allCards = await res.json();

    const list = document.getElementById('card-list');
    list.innerHTML = '';

    allCards.forEach((card) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'w-full text-left px-4 py-3 rounded-2xl border border-purple-700 bg-zinc-800/80 hover:bg-purple-900/60 transition';
        button.innerHTML = `
            <div class="flex items-center justify-between gap-3">
                <span class="font-medium">${card.id}. ${card.name}</span>
                <span class="text-purple-300">›</span>
            </div>
        `;
        button.addEventListener('click', () => showCardDetail(card.id));
        list.appendChild(button);
    });
}

async function showCardDetail(cardId) {
    activeCardId = cardId;

    const res = await fetch(`/api/cards/${cardId}`);
    const card = await res.json();

    document.getElementById('empty-state').classList.add('hidden');
    document.getElementById('card-detail').classList.remove('hidden');

    const image = document.getElementById('detail-image');
    image.src = `/static/images/cards/${card.image}`;
    image.alt = card.name;

    document.getElementById('detail-name').innerText = card.name;
    document.getElementById('detail-upright').innerText = card.upright;
    document.getElementById('detail-reversed').innerText = card.reversed;

    updateActiveButton();
}

function updateActiveButton() {
    const buttons = document.querySelectorAll('#card-list button');
    buttons.forEach((button, index) => {
        const isActive = allCards[index].id === activeCardId;
        button.classList.toggle('border-amber-400', isActive);
        button.classList.toggle('bg-purple-900/80', isActive);
    });
}

document.addEventListener('DOMContentLoaded', loadCardList);
