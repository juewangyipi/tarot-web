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
                
                <!-- Card Back -->
                <div class="card-back absolute inset-0 overflow-hidden rounded-3xl border border-amber-400">
                    <img src="/static/images/cards/card_back.png" 
                         class="w-full h-full object-cover" 
                         alt="Card Back">
                </div>
                <!-- Card Front -->
                <div class="card-front absolute inset-0 bg-zinc-950 border border-purple-700 flex flex-col rounded-3xl overflow-hidden">
                    
                    <!-- Card Image (Full Size) -->
                    <div class="h-full overflow-hidden">
                        <img src="/static/images/cards/${card.image}" 
                             class="w-full h-full object-cover" 
                             alt="${card.name}">
                    </div>
                    
                    <!-- Text Panel (Slides in from bottom on second click) -->
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
                // First click → Flip to front (show image)
                cardInner.style.transform = 'rotateY(180deg)';
                isFlipped = true;
            } else {
                // Second click → Slide text panel in/out
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
    
    // Remove previous comprehensive interpretation before adding new one
    const oldInterpretationContainer = document.getElementById('interpretation-container');
    if (oldInterpretationContainer) {
        oldInterpretationContainer.remove();
    }
    
    // Add Comprehensive Interpretation Button and Panel
    addComprehensiveInterpretation(data);
    
    // Score Bars
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

function addComprehensiveInterpretation(data) {
    // Create container for button and interpretation panel
    const interpretationContainer = document.createElement('div');
    interpretationContainer.className = 'max-w-3xl mx-auto mb-12';
    interpretationContainer.id = 'interpretation-container';
    
    // Create the button
    const button = document.createElement('button');
    button.className = 'w-full py-4 bg-gradient-to-r from-indigo-700 to-purple-800 hover:from-indigo-600 hover:to-purple-700 rounded-2xl text-xl font-medium transition flex items-center justify-center gap-3';
    button.innerHTML = `
        <span>✨</span>
        <span>Comprehensive Interpretation</span>
        <span>✨</span>
    `;
    
    // Create the interpretation panel (initially hidden)
    const panel = document.createElement('div');
    panel.className = 'bg-zinc-900/80 border border-indigo-800 rounded-3xl p-8 mt-6 hidden';
    panel.id = 'interpretation-panel';
    
    // Generate comprehensive interpretation content
    const interpretationContent = generateComprehensiveInterpretation(data);
    panel.innerHTML = interpretationContent;
    
    // Add toggle functionality to the button
    button.addEventListener('click', () => {
        panel.classList.toggle('hidden');
        if (!panel.classList.contains('hidden')) {
            button.innerHTML = `
                <span>🔮</span>
                <span>Hide Comprehensive Interpretation</span>
                <span>🔮</span>
            `;
        } else {
            button.innerHTML = `
                <span>✨</span>
                <span>Comprehensive Interpretation</span>
                <span>✨</span>
            `;
        }
    });
    
    // Assemble the container
    interpretationContainer.appendChild(button);
    interpretationContainer.appendChild(panel);
    
    // Insert between cards container and scores container
    const cardsContainer = document.getElementById('cards-container');
    cardsContainer.after(interpretationContainer);
}

function generateComprehensiveInterpretation(data) {
    const { category, cards, scores, main_theme } = data;
    const isThreeCardSpread = cards.length === 3;
    
    // Extract card information
    const situationCard = isThreeCardSpread ? cards[0] : cards[0];
    const challengeCard = isThreeCardSpread ? cards[1] : null;
    const adviceCard = isThreeCardSpread ? cards[2] : null;
    
    // Generate theme analysis
    const themeAnalysis = generateThemeAnalysis(main_theme, scores);
    
    // Generate card interaction analysis
    const cardInteraction = generateCardInteraction(cards, isThreeCardSpread);
    
    // Generate overall guidance
    const overallGuidance = generateOverallGuidance(cards, main_theme, category);
    
    // Generate key takeaways
    const keyTakeaways = generateKeyTakeaways(cards, scores, main_theme);
    
    return `
        <h3 class="text-2xl font-bold text-center mb-6 text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-purple-300">
            Complete Reading Synthesis
        </h3>
        
        <div class="space-y-6">
            <!-- Theme Analysis -->
            <div class="rounded-2xl border border-amber-500/30 bg-amber-500/5 p-6">
                <h4 class="text-xl font-semibold mb-3 text-amber-200">Dominant Energy: ${main_theme.charAt(0).toUpperCase() + main_theme.slice(1)}</h4>
                ${themeAnalysis}
            </div>
            
            <!-- Card Interaction -->
            <div class="rounded-2xl border border-purple-500/30 bg-purple-500/5 p-6">
                <h4 class="text-xl font-semibold mb-3 text-purple-200">Card Dynamics & Narrative Flow</h4>
                ${cardInteraction}
            </div>
            
            <!-- Overall Guidance -->
            <div class="rounded-2xl border border-indigo-500/30 bg-indigo-500/5 p-6">
                <h4 class="text-xl font-semibold mb-3 text-indigo-200">Integrated Guidance</h4>
                ${overallGuidance}
            </div>
            
            <!-- Key Takeaways -->
            <div class="rounded-2xl border border-pink-500/30 bg-pink-500/5 p-6">
                <h4 class="text-xl font-semibold mb-3 text-pink-200">Key Takeaways</h4>
                ${keyTakeaways}
            </div>
        </div>
    `;
}

function generateThemeAnalysis(mainTheme, scores) {
    const themeDescriptions = {
        opportunity: "This reading is strongly oriented toward new possibilities and growth. The cards indicate that doors are opening, and you have the potential to make significant progress in your chosen area.",
        challenge: "Obstacles and difficulties are the central focus of this reading. While this may feel uncomfortable, these challenges are presenting you with important lessons and opportunities for growth.",
        emotion: "Emotional dynamics play a crucial role in your current situation. Your feelings, relationships, and inner state are shaping the outcome more than external circumstances.",
        action: "Practical steps and deliberate movement are essential right now. The cards emphasize that progress will come through what you do, not just what you think or feel.",
        stability: "Structure, consistency, and long-term planning are highlighted in this reading. Building a solid foundation will be more important than quick wins or sudden changes."
    };
    
    // Find second highest score
    const sortedScores = Object.entries(scores).sort((a, b) => b[1] - a[1]);
    const secondTheme = sortedScores[1][0];
    const secondScore = sortedScores[1][1];
    
    let analysis = `<p class="leading-relaxed">${themeDescriptions[mainTheme]}</p>`;
    
    if (secondScore >= 6) {
        analysis += `
            <p class="leading-relaxed mt-3">
                <strong>Secondary influence:</strong> ${secondTheme.charAt(0).toUpperCase() + secondTheme.slice(1)} (${secondScore}/10) also plays a significant role, 
                adding a layer of ${secondTheme === 'opportunity' ? 'potential' : 
                                 secondTheme === 'challenge' ? 'difficulty' : 
                                 secondTheme === 'emotion' ? 'feeling' : 
                                 secondTheme === 'action' ? 'movement' : 'structure'} to the overall energy.
            </p>
        `;
    }
    
    // Add balance note
    const lowestScore = sortedScores[sortedScores.length - 1];
    if (lowestScore[1] <= 3) {
        analysis += `
            <p class="leading-relaxed mt-3 text-amber-300">
                <strong>Area needing attention:</strong> ${lowestScore[0].charAt(0).toUpperCase() + lowestScore[0].slice(1)} is relatively low (${lowestScore[1]}/10), 
                suggesting you may need to give this aspect more conscious consideration.
            </p>
        `;
    }
    
    return analysis;
}

function generateCardInteraction(cards, isThreeCardSpread) {
    if (!isThreeCardSpread) {
        return `
            <p class="leading-relaxed">
                The <strong>${cards[0].name} (${cards[0].orientation})</strong> provides a snapshot of your current overall energy. 
                This card represents the primary force at work in your life right now, influencing all areas of your experience.
            </p>
            <p class="leading-relaxed mt-3">
                ${cards[0].orientation === 'upright' 
                    ? 'In its upright position, this card brings its most constructive and positive qualities to your situation.' 
                    : 'In its reversed position, this card suggests you may be experiencing challenges related to its themes, or that its energy is blocked or misdirected.'}
            </p>
        `;
    }
    
    const situation = cards[0];
    const challenge = cards[1];
    const advice = cards[2];
    
    // Analyze the relationship between situation and challenge
    let situationChallengeRelation = '';
    if (situation.orientation === 'upright' && challenge.orientation === 'upright') {
        situationChallengeRelation = "Your current situation contains the seeds of the challenge you're facing.";
    } else if (situation.orientation === 'upright' && challenge.orientation === 'reversed') {
        situationChallengeRelation = "The positive aspects of your current situation are being undermined by the reversed energy of the challenge card.";
    } else if (situation.orientation === 'reversed' && challenge.orientation === 'upright') {
        situationChallengeRelation = "The difficulties in your current situation are creating the conditions for the challenge you're facing.";
    } else {
        situationChallengeRelation = "Both your current situation and the challenge you're facing are marked by blocked or misdirected energy.";
    }
    
    // Analyze how advice addresses the challenge
    let adviceChallengeRelation = '';
    if (advice.orientation === 'upright') {
        adviceChallengeRelation = "The advice card offers a constructive, forward-moving approach to addressing your challenge.";
    } else {
        adviceChallengeRelation = "The advice card suggests that you first need to address the reversed aspects of this energy before you can effectively move forward.";
    }
    
    return `
        <div class="space-y-4">
            <div>
                <h5 class="font-semibold text-purple-300 mb-2">Situation → Challenge</h5>
                <p class="leading-relaxed">
                    ${situationChallengeRelation} 
                    <strong>${situation.name} (${situation.orientation})</strong> describes the landscape you're currently navigating, 
                    while <strong>${challenge.name} (${challenge.orientation})</strong> reveals the specific obstacle or tension that requires your attention.
                </p>
            </div>
            
            <div>
                <h5 class="font-semibold text-purple-300 mb-2">Challenge → Advice</h5>
                <p class="leading-relaxed">
                    ${adviceChallengeRelation} 
                    <strong>${advice.name} (${advice.orientation})</strong> provides the key insight or action that will help you navigate through 
                    the challenges presented by <strong>${challenge.name}</strong>.
                </p>
            </div>
            
            <div>
                <h5 class="font-semibold text-purple-300 mb-2">Overall Narrative</h5>
                <p class="leading-relaxed">
                    The reading tells a story of moving from <strong>${situation.name.toLowerCase()}</strong> 
                    through <strong>${challenge.name.toLowerCase()}</strong> 
                    toward <strong>${advice.name.toLowerCase()}</strong>. 
                    This progression suggests that by embracing the wisdom of the advice card, 
                    you can transform the challenges of your current situation into growth and progress.
                </p>
            </div>
        </div>
    `;
}

function generateOverallGuidance(cards, mainTheme, category) {
    const isThreeCardSpread = cards.length === 3;
    const adviceCard = isThreeCardSpread ? cards[2] : cards[0];
    
    let guidance = `
        <p class="leading-relaxed">
            Based on the combined energy of all cards, the reading suggests that your primary focus should be on 
            <strong>${mainTheme}</strong> within the context of ${category} matters.
        </p>
    `;
    
    if (isThreeCardSpread) {
        guidance += `
            <p class="leading-relaxed mt-3">
                The path forward involves acknowledging the reality of your current situation (${cards[0].name}), 
                facing the challenge directly (${cards[1].name}), 
                and then applying the specific guidance offered by ${cards[2].name}.
            </p>
        `;
    }
    
    // Add orientation-specific guidance
    const uprightCount = cards.filter(c => c.orientation === 'upright').length;
    const reversedCount = cards.length - uprightCount;
    
    if (uprightCount > reversedCount) {
        guidance += `
            <p class="leading-relaxed mt-3">
                With ${uprightCount} out of ${cards.length} cards in the upright position, 
                the overall energy of the reading is constructive and forward-moving. 
                You have the resources and potential to create positive change in your situation.
            </p>
        `;
    } else if (reversedCount > uprightCount) {
        guidance += `
            <p class="leading-relaxed mt-3">
                With ${reversedCount} out of ${cards.length} cards in the reversed position, 
                the reading suggests that some aspects of your situation may be blocked, unclear, or in need of adjustment. 
                This is a time for reflection and careful consideration before taking major action.
            </p>
        `;
    } else {
        guidance += `
            <p class="leading-relaxed mt-3">
                With an equal number of upright and reversed cards, 
                the reading indicates a balance of opportunities and challenges. 
                Success will come from working with both the constructive and difficult aspects of your situation.
            </p>
        `;
    }
    
    return guidance;
}

function generateKeyTakeaways(cards, scores, mainTheme) {
    const takeaways = [];
    
    // Add main theme takeaway
    takeaways.push(`Focus on ${mainTheme} as your guiding principle in the coming days.`);
    
    // Add card-specific takeaways
    cards.forEach((card, index) => {
        const position = card.position.charAt(0).toUpperCase() + card.position.slice(1);
        if (card.orientation === 'upright') {
            takeaways.push(`${position}: Embrace the positive qualities of ${card.name} - ${card.scores.opportunity >= 4 ? 'it brings significant opportunities' : 'it offers valuable insights'}.`);
        } else {
            takeaways.push(`${position}: Be mindful of the challenges associated with ${card.name} reversed - ${card.scores.challenge >= 4 ? 'it indicates areas needing attention' : 'it suggests a need for adjustment'}.`);
        }
    });
    
    // Add score-based takeaway
    const highestScore = Math.max(...Object.values(scores));
    const lowestScore = Math.min(...Object.values(scores));
    
    if (highestScore >= 8) {
        takeaways.push(`Your strength in ${Object.keys(scores).find(k => scores[k] === highestScore)} is particularly strong - leverage this to your advantage.`);
    }
    
    if (lowestScore <= 3) {
        takeaways.push(`Give extra attention to ${Object.keys(scores).find(k => scores[k] === lowestScore)} - this area may need more conscious effort.`);
    }
    
    // Format as list
    return `
        <ul class="space-y-2">
            ${takeaways.map(takeaway => `<li class="flex items-start gap-2">
                <span class="text-pink-400 mt-1">•</span>
                <span class="leading-relaxed">${takeaway}</span>
            </li>`).join('')}
        </ul>
    `;
}