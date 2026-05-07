async function drawCards(useRandom = false) {
    const category = document.getElementById('category').value;
    const spread = document.getElementById('spread').value;
    let numbers = document.getElementById('numbers').value.trim();

    if (useRandom) numbers = '';

    const res = await fetch('/api/draw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ category, spread, numbers })
    });

    const data = await res.json();
    renderResult(data);
}

function randomDraw() {
    drawCards(true);
}

function renderResult(data) {
    document.getElementById('result').classList.remove('hidden');

    document.getElementById('main-theme').innerText = data.main_theme.toUpperCase();
    document.getElementById('summary').innerText = data.summary;

    const container = document.getElementById('cards-container');
    container.innerHTML = '';

    data.cards.forEach((card) => {
        const div = document.createElement('div');
        div.className = `card group`;
        
        div.innerHTML = `
            <div class="card-inner relative w-full h-full">
                
                <!-- 卡背 -->
                <div class="card-back absolute inset-0 overflow-hidden rounded-3xl border border-amber-400">
                    <img src="/static/images/cards/card_back.png" 
                         class="w-full h-full object-cover" 
                         alt="Card Back">
                </div>

                <!-- 卡面 -->
                <div class="card-front absolute inset-0 bg-zinc-950 border border-purple-700 flex flex-col rounded-3xl overflow-hidden">
                    
                    <!-- 牌面图片（完全占满） -->
                    <div class="h-full overflow-hidden">
                        <img src="/static/images/cards/${card.image}" 
                             class="w-full h-full object-cover" 
                             alt="${card.name}">
                    </div>
                    
                    <!-- 文字面板（初始隐藏，点击后从底部滑入） -->
                    <div class="text-panel absolute bottom-0 left-0 right-0 
                                bg-gradient-to-t from-black/90 via-black/85 to-transparent 
                                p-4 max-h-[35%] overflow-y-auto transition-all duration-500 ease-out translate-y-full
                                scrollbar-hide">
                        
                        <div class="font-bold text-[16px] mb-1">${card.name}</div>
                        <div class="text-purple-400 text-xs tracking-[2px] mb-2">
                            ${card.orientation.toUpperCase()} · ${card.position.toUpperCase()}
                        </div>
                        
                        <div class="text-xs leading-snug text-zinc-200">
                            ${card.interpretation}
                        </div>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(div);

        const cardInner = div.querySelector('.card-inner');
        const textPanel = div.querySelector('.text-panel');
        let isFlipped = false;
        let textShown = false;

        div.addEventListener('click', () => {
            if (!isFlipped) {
                // 第一次点击 → 翻到正面（图片完全显示）
                cardInner.style.transform = 'rotateY(180deg)';
                isFlipped = true;
            } else {
                // 第二次点击 → 文字滑入/滑出
                if (!textShown) {
                    textPanel.classList.remove('translate-y-full');
                    textPanel.classList.add('translate-y-0');
                    textShown = true;
                } else {
                    textPanel.classList.remove('translate-y-0');
                    textPanel.classList.add('translate-y-full');
                    textShown = false;
                }
            }
        });
    });

    // 分数条
    const scoresDiv = document.getElementById('scores-container');
    scoresDiv.innerHTML = '';
    
    Object.entries(data.scores).forEach(([key, value]) => {
        const percent = Math.round(value * 10);
        const bar = document.createElement('div');
        bar.innerHTML = `
            <div class="flex items-center gap-4">
                <div class="w-24 text-right text-sm font-medium">${key}</div>
                <div class="flex-1 bg-zinc-800 rounded-full h-5 overflow-hidden">
                    <div class="h-5 bg-gradient-to-r from-amber-400 via-purple-500 to-pink-500" 
                         style="width: ${percent}%"></div>
                </div>
                <div class="w-12 text-right font-mono text-lg">${value}</div>
            </div>
        `;
        scoresDiv.appendChild(bar);
    });
}