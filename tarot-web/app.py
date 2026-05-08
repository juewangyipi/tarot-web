import os
from flask import Flask, render_template, request, jsonify
import random
import json

app = Flask(__name__)
app.secret_key = 'tarot-mystic-2026'

# ==================== 完整数据和逻辑（来自你的原代码） ====================

CARD_DATABASE = {
    "The Fool": {
        "upright": {
            "overall": "New beginnings, freedom, exploration, and open potential. This card suggests entering a new stage with curiosity, but basic awareness is still needed.",
            "situation": "You may be standing at the beginning of a new stage. The situation carries openness, possibility, and uncertainty at the same time. There may not be a fixed path yet, but this also means there is room to explore, try, and discover new directions.",
            "challenge": "The main challenge is that the situation may lack structure or preparation. Curiosity can bring movement, but acting too casually may lead to unnecessary mistakes. The risk is moving forward without checking whether the basic conditions are ready.",
            "advice": "Stay open to new possibilities, but do not rely only on excitement. Before making a choice, check the basic risks, resources, and direction. A flexible attitude is useful, but it should be supported by simple planning."
        },
        "reversed": {
            "overall": "Carelessness, avoidance, poor preparation, or unclear direction. It warns against acting only from impulse without checking the risks.",
            "situation": "You may be facing a situation where the direction is unclear, or where you feel hesitant before starting something new. There may also be impulsive energy, but it is not yet supported by enough preparation or judgment.",
            "challenge": "The main challenge is carelessness, avoidance, or weak planning. You may want to escape pressure by making a quick choice, but the problem is that the choice may not be grounded in clear information.",
            "advice": "Slow down before taking action. Check whether your decision is based on real readiness or temporary impulse. It is better to clarify your direction first than to rush into a path that may become difficult to control later."
        },
        "scores": {
            "opportunity": 5,
            "challenge": 2,
            "emotion": 3,
            "action": 4,
            "stability": 1
        }
    },

    "The Magician": {
        "upright": {
            "overall": "Skill, resources, communication, and initiative. This card suggests that you have what you need, but you must turn ideas into action.",
            "situation": "The current situation may already contain useful resources, skills, or opportunities. You may not need to wait for perfect conditions, because the key issue is whether you can actively organize what you already have.",
            "challenge": "The main challenge is execution. Ideas, abilities, and resources may exist, but they will not produce results unless they are used clearly and purposefully. The risk is staying at the level of imagination without practical movement.",
            "advice": "Clarify your goal and turn your idea into a concrete step. Use communication, planning, and initiative to connect your resources with action. This is a moment to act deliberately rather than wait passively."
        },
        "reversed": {
            "overall": "Wasted potential, unclear communication, or weak execution. It asks you to clarify your goal before making promises or taking action.",
            "situation": "You may have ability or resources, but they are not being used effectively. The situation may involve scattered attention, unclear expression, or a gap between what you say and what you can actually complete.",
            "challenge": "The main challenge is wasted potential. You may be trying to do many things at once, or making plans without enough structure. Miscommunication or overpromising may also weaken trust and efficiency.",
            "advice": "Return to the basic goal before taking further action. Avoid exaggerating what you can deliver. Make your plan smaller, clearer, and easier to execute, then rebuild momentum through practical steps."
        },
        "scores": {
            "opportunity": 5,
            "challenge": 2,
            "emotion": 2,
            "action": 5,
            "stability": 3
        }
    },

    "The High Priestess": {
        "upright": {
            "overall": "Intuition, hidden knowledge, observation, and inner wisdom. The situation may not be fully visible yet, so patience and careful attention are needed.",
            "situation": "The situation may contain hidden information or unclear signals. Not everything is visible on the surface, so direct action may not be the most suitable response yet. Observation and inner judgment are important now.",
            "challenge": "The main challenge is uncertainty. You may not have enough facts, or other people may not be expressing everything clearly. The risk is forcing a conclusion before the deeper situation has become visible.",
            "advice": "Observe more carefully and give yourself time to understand what is not being said directly. Trust intuition, but do not confuse intuition with assumption. Wait for clearer evidence before making a major decision."
        },
        "reversed": {
            "overall": "Blocked intuition, confusion, or unclear information. It warns against relying only on assumptions or ignoring subtle signs.",
            "situation": "You may be missing important signals or ignoring your own inner judgment. The situation may feel confusing because the available information is incomplete or because you are relying too much on assumptions.",
            "challenge": "The main challenge is blocked perception. You may either doubt your intuition too much or trust unclear feelings without checking the facts. Secrecy, confusion, or emotional noise may distort your judgment.",
            "advice": "Ask for more information and review the situation calmly. Do not make decisions based only on fear, guesswork, or other people’s vague signals. Clarify the facts while also paying attention to repeated patterns."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 3,
            "emotion": 4,
            "action": 2,
            "stability": 3
        }
    },

    "The Empress": {
        "upright": {
            "overall": "Growth, nurturing, creativity, and emotional support. This card suggests that something can develop steadily if given time and care.",
            "situation": "The situation may involve growth, emotional support, creativity, or the gradual development of something valuable. It may not produce immediate results, but it has the potential to become stable if it is cared for properly.",
            "challenge": "The main challenge is maintaining balance while giving attention, care, or emotional energy. Growth requires patience, but too much dependence on comfort or external support may slow down practical progress.",
            "advice": "Give the situation enough time to develop. Support what is growing through steady attention and realistic care. At the same time, avoid overgiving or losing your own boundaries in the process."
        },
        "reversed": {
            "overall": "Emotional imbalance, overgiving, dependence, or blocked growth. It asks you to restore boundaries and avoid neglecting yourself.",
            "situation": "The situation may involve emotional imbalance, blocked development, or excessive dependence. Something that should be growing may feel stuck because the support system is unstable or one-sided.",
            "challenge": "The main challenge is overgiving, emotional exhaustion, or neglecting your own needs. You may be trying to care for something or someone, but the process may no longer be healthy or sustainable.",
            "advice": "Restore balance before continuing to invest more energy. Set clearer boundaries and check whether the support you give is actually helping growth. Do not use care as a way to avoid your own needs."
        },
        "scores": {
            "opportunity": 4,
            "challenge": 2,
            "emotion": 5,
            "action": 3,
            "stability": 4
        }
    },

    "The Emperor": {
        "upright": {
            "overall": "Order, responsibility, structure, and leadership. This card suggests the need for planning, discipline, and stable decision-making.",
            "situation": "The current situation may require structure, rules, responsibility, or leadership. Emotional reactions alone may not be enough; what matters now is whether there is a stable framework for action.",
            "challenge": "The main challenge is handling responsibility without becoming too controlling. You may need to make decisions, set boundaries, or organize others, but pressure may increase if the structure is too rigid or unclear.",
            "advice": "Create a clear plan and define responsibilities. Use discipline and structure to stabilize the situation. Lead through consistency rather than force, and make decisions based on long-term order instead of temporary emotion."
        },
        "reversed": {
            "overall": "Rigidity, control issues, unstable structure, or misuse of authority. It asks for boundaries without becoming overly dominant.",
            "situation": "The situation may involve weak boundaries, unstable rules, or excessive control. There may be a lack of order, or the existing order may feel too rigid and difficult to adapt to real needs.",
            "challenge": "The main challenge is imbalance in control. Either there is not enough structure to support progress, or someone is using authority in a way that creates pressure and resistance.",
            "advice": "Rebuild structure, but do not become overly dominant. Set boundaries that are clear and practical. A stable plan is needed, but it should leave enough flexibility for adjustment."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 4,
            "emotion": 2,
            "action": 4,
            "stability": 5
        }
    },

    "The Hierophant": {
        "upright": {
            "overall": "Tradition, systems, learning, and guidance. This card suggests following reliable structures or seeking advice from established sources.",
            "situation": "The situation may be connected to rules, systems, education, institutions, or accepted standards. You may need to understand how an existing structure works before deciding whether to follow or adjust it.",
            "challenge": "The main challenge is dealing with expectations or external standards. You may feel pressure to fit into a system, or you may need to learn from authority before gaining enough independence.",
            "advice": "Use reliable guidance, established knowledge, or formal rules as a reference. This is not necessarily a time to reject structure immediately. Learn the system first, then decide where adjustment is needed."
        },
        "reversed": {
            "overall": "Restriction, value conflict, or unconventional thinking. It encourages questioning old assumptions without rejecting structure blindly.",
            "situation": "You may feel restricted by traditional expectations, group norms, or external rules. The situation may involve a conflict between personal values and what a system expects from you.",
            "challenge": "The main challenge is deciding whether the existing structure still fits the current situation. Blind obedience may limit growth, but rejecting all rules may also create instability.",
            "advice": "Question old assumptions carefully. Keep what is useful and adjust what no longer works. Avoid rebellion for its own sake; the goal is to find a structure that matches your actual values and needs."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 3,
            "emotion": 2,
            "action": 3,
            "stability": 5
        }
    },

    "The Lovers": {
        "upright": {
            "overall": "Connection, choice, attraction, and shared values. This card points to communication, trust, and decisions aligned with what matters.",
            "situation": "The situation may involve an important relationship, value-based choice, or emotional connection. It is not only about attraction or preference, but also about whether different sides can align with shared values.",
            "challenge": "The main challenge is making a choice that is consistent with what truly matters. Misalignment may appear if communication is weak or if the decision is made only from temporary emotion.",
            "advice": "Pay attention to communication, trust, and long-term fit. Choose based on values rather than surface attraction. A good decision should create alignment between feeling, responsibility, and future direction."
        },
        "reversed": {
            "overall": "Disharmony, poor communication, misalignment, or difficult choices. It asks you to clarify your values before committing.",
            "situation": "The situation may involve emotional distance, poor communication, or conflict between desire and value. A relationship, partnership, or decision may look attractive but lack deeper alignment.",
            "challenge": "The main challenge is confusion about commitment or values. You may be trying to choose without knowing what you actually want, or there may be disagreement between people involved.",
            "advice": "Clarify your values before making a commitment. Do not rely only on temporary feelings or external expectations. Honest communication is needed before the situation can move toward harmony."
        },
        "scores": {
            "opportunity": 4,
            "challenge": 3,
            "emotion": 5,
            "action": 3,
            "stability": 3
        }
    },

    "The Chariot": {
        "upright": {
            "overall": "Progress, willpower, control, and determination. This card suggests focused movement toward a clear goal.",
            "situation": "The situation is moving toward action, progress, or competition. You may need strong direction and self-control to keep different forces working toward the same goal.",
            "challenge": "The main challenge is maintaining focus. There may be conflicting pressures, emotions, or choices pulling you in different directions. Without discipline, movement may become scattered.",
            "advice": "Define your target clearly and keep moving with discipline. Control does not mean forcing everything; it means keeping your energy organized. Progress is possible if you stay focused and do not let distraction lead the process."
        },
        "reversed": {
            "overall": "Loss of control, blocked progress, scattered direction, or forced action. It asks you to regain direction before pushing forward.",
            "situation": "Progress may feel blocked, unstable, or difficult to control. You may be trying to move forward, but the direction is unclear or the effort is being applied in a scattered way.",
            "challenge": "The main challenge is loss of direction. If you continue pushing without knowing where you are going, the action may create more pressure rather than real progress.",
            "advice": "Stop forcing movement for a moment and regain direction first. Clarify the goal, remove unnecessary distractions, and rebuild control through smaller, more organized steps."
        },
        "scores": {
            "opportunity": 4,
            "challenge": 3,
            "emotion": 2,
            "action": 5,
            "stability": 3
        }
    },

    "Strength": {
        "upright": {
            "overall": "Courage, patience, resilience, and emotional control. This card suggests quiet strength rather than force.",
            "situation": "The situation may require patience, emotional control, and steady confidence. It may not be solved through pressure or aggression, but through resilience and inner stability.",
            "challenge": "The main challenge is handling pressure without reacting impulsively. You may need to face fear, conflict, or uncertainty while still keeping your emotions under control.",
            "advice": "Use calm courage rather than force. Be patient with the process and with yourself. A steady response will be more effective than a dramatic reaction, especially when emotions are strong."
        },
        "reversed": {
            "overall": "Self-doubt, emotional pressure, insecurity, or weakened confidence. It asks for gradual rebuilding instead of harsh self-criticism.",
            "situation": "You may feel emotionally pressured, insecure, or unsure of your own ability. The situation may be testing your confidence, and you may feel weaker than usual.",
            "challenge": "The main challenge is self-doubt. Harsh self-criticism or fear may make the problem seem larger than it actually is. Emotional instability may also reduce your ability to respond clearly.",
            "advice": "Rebuild confidence gradually. Do not demand immediate perfection from yourself. Focus on small actions that restore control, and avoid judging yourself too harshly during a difficult stage."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 3,
            "emotion": 5,
            "action": 5,
            "stability": 4
        }
    },

    "The Hermit": {
        "upright": {
            "overall": "Solitude, reflection, study, and inner guidance. This card suggests stepping back to understand the situation more deeply.",
            "situation": "The situation may require distance, reflection, or deeper study. Immediate action may not be the most useful response because you first need to understand what is really happening beneath the surface.",
            "challenge": "The main challenge is the possibility of isolation or overthinking. Reflection can bring wisdom, but staying withdrawn for too long may reduce practical contact with reality.",
            "advice": "Take time to think carefully and examine your direction. Use solitude as a tool for clarity, not as an escape. After reflection, reconnect with practical information and real communication."
        },
        "reversed": {
            "overall": "Isolation, avoidance, overthinking, or unclear inner direction. It asks you to balance reflection with practical contact.",
            "situation": "You may be withdrawing too much or avoiding outside input. The situation may feel unclear because you are staying inside your own thoughts without enough practical feedback.",
            "challenge": "The main challenge is excessive isolation. Thinking alone may no longer bring clarity if it becomes avoidance, loneliness, or repeated self-questioning.",
            "advice": "Balance inner reflection with external contact. Ask for useful feedback, reconnect with the situation, and avoid using solitude as a way to delay necessary action."
        },
        "scores": {
            "opportunity": 2,
            "challenge": 4,
            "emotion": 3,
            "action": 2,
            "stability": 4
        }
    },

    "Wheel of Fortune": {
        "upright": {
            "overall": "Change, cycles, timing, and opportunity. This card suggests that circumstances are shifting and adaptation is important.",
            "situation": "The situation may be entering a new cycle. External conditions may be changing, and new opportunities or turning points may appear even if they are not fully under your control.",
            "challenge": "The main challenge is uncertainty. You may not be able to control every factor, and timing may play an important role. Resistance to change may make the transition harder.",
            "advice": "Stay flexible and prepare to adapt. Watch for timing, repeated patterns, and new openings. Instead of trying to control everything, focus on responding wisely when the situation shifts."
        },
        "reversed": {
            "overall": "Delay, repeated patterns, poor timing, or feeling stuck. It asks you to recognize cycles and change your response.",
            "situation": "You may feel stuck in a repeated pattern or delayed by poor timing. The situation may seem unstable because changes are happening slowly or not in the direction you expected.",
            "challenge": "The main challenge is repetition. If the same problem keeps appearing, the issue may not only be external luck but also an unchanged response pattern.",
            "advice": "Identify what keeps repeating and adjust your reaction. Do not wait passively for circumstances to improve. Small changes in response may help break the cycle."
        },
        "scores": {
            "opportunity": 5,
            "challenge": 3,
            "emotion": 3,
            "action": 3,
            "stability": 2
        }
    },

    "Justice": {
        "upright": {
            "overall": "Fairness, responsibility, truth, and balanced judgment. This card asks for decisions based on evidence and accountability.",
            "situation": "The situation may involve fairness, responsibility, facts, or consequences. A decision may need to be made carefully, and the result may depend on whether the judgment is balanced and evidence-based.",
            "challenge": "The main challenge is facing facts honestly. You may need to accept responsibility, review previous choices, or make a decision without letting emotion distort the truth.",
            "advice": "Base your decision on evidence, logic, and accountability. Avoid bias, exaggeration, or emotional reaction. A fair outcome requires clear standards and willingness to face the consequences."
        },
        "reversed": {
            "overall": "Unfairness, bias, avoidance of responsibility, or unclear facts. It asks you to correct imbalance and review the truth carefully.",
            "situation": "The situation may involve imbalance, unfair treatment, unclear facts, or avoidance of responsibility. There may be a gap between what is true and what is being acknowledged.",
            "challenge": "The main challenge is bias or avoidance. Someone may not be taking responsibility, or the available information may be incomplete, making fair judgment difficult.",
            "advice": "Review the facts carefully and correct any imbalance. Do not ignore evidence because it is uncomfortable. A clearer and fairer decision can only come after the truth is examined directly."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 4,
            "emotion": 2,
            "action": 3,
            "stability": 4
        }
    },

    "The Hanged Man": {
        "upright": {
            "overall": "Pause, patience, sacrifice, and new perspective. This card suggests waiting or seeing the situation differently before acting.",
            "situation": "The situation may be temporarily suspended or moving more slowly than expected. This pause may feel uncomfortable, but it can create space for a different perspective.",
            "challenge": "The main challenge is accepting delay without becoming passive or frustrated. You may need to give up an old viewpoint or release something that prevents clearer understanding.",
            "advice": "Pause before forcing action. Try to see the situation from another angle. Waiting is useful only if it leads to insight, so use this time to understand what needs to be released or changed."
        },
        "reversed": {
            "overall": "Resistance, impatience, useless delay, or blocked perspective. It asks you to stop forcing movement and examine what must be released.",
            "situation": "You may feel impatient with slow progress or trapped in a delay that no longer feels meaningful. The situation may be stuck because you are resisting a necessary shift in perspective.",
            "challenge": "The main challenge is resistance. You may want movement, but the way you are pushing may not solve the core issue. Refusing to adjust your viewpoint may keep the problem in place.",
            "advice": "Stop forcing progress in the same way. Examine what belief, habit, or expectation needs to be released. A different perspective may be more useful than more pressure."
        },
        "scores": {
            "opportunity": 2,
            "challenge": 4,
            "emotion": 3,
            "action": 1,
            "stability": 3
        }
    },

    "Death": {
        "upright": {
            "overall": "Ending, transformation, renewal, and transition. This card usually means that an old phase must close for something new to begin.",
            "situation": "The situation may be reaching an ending or transition point. Something old may no longer work in its current form, and the next stage requires release before renewal can happen.",
            "challenge": "The main challenge is accepting change. Endings may feel uncomfortable even when they are necessary. Holding onto the old structure may delay the possibility of renewal.",
            "advice": "Let go of what no longer supports growth. Treat the ending as part of transformation rather than only as loss. Make space for a new phase by closing what has already reached its limit."
        },
        "reversed": {
            "overall": "Resistance to change, delayed transformation, or holding onto the past. It asks you to identify what you are avoiding.",
            "situation": "You may be holding onto an old situation, identity, habit, or expectation even though it no longer fits. The transformation is delayed because release has not fully happened.",
            "challenge": "The main challenge is fear of change. Familiarity may feel safer than transformation, but staying attached to the past may keep the current problem unresolved.",
            "advice": "Identify what you are avoiding and why it feels difficult to release. Change does not need to happen violently, but it does need to happen honestly. Begin with one unnecessary attachment that can be reduced."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 5,
            "emotion": 4,
            "action": 3,
            "stability": 1
        }
    },

    "Temperance": {
        "upright": {
            "overall": "Balance, harmony, patience, and gradual adjustment. This card suggests moderation and steady progress.",
            "situation": "The situation may require coordination between different needs, people, or directions. Progress is possible, but it is more likely to come through balance and gradual adjustment than through extreme action.",
            "challenge": "The main challenge is avoiding extremes. You may need to integrate different parts of the situation without rushing, forcing, or overcorrecting in one direction.",
            "advice": "Choose moderation and steady adjustment. Rebalance priorities, manage timing carefully, and allow progress to happen step by step. A calm rhythm will be more useful than sudden change."
        },
        "reversed": {
            "overall": "Imbalance, impatience, poor timing, or lack of coordination. It asks you to slow down and restore balance.",
            "situation": "The situation may feel unstable because different parts are not working together. There may be impatience, poor timing, or conflict between what you want and what the situation can support.",
            "challenge": "The main challenge is imbalance. Moving too fast, reacting too strongly, or ignoring coordination may create more disorder instead of solving the issue.",
            "advice": "Slow down and restore balance before making major decisions. Adjust your pace, review your priorities, and avoid extreme responses. Stability can return through careful coordination."
        },
        "scores": {
            "opportunity": 3,
            "challenge": 2,
            "emotion": 4,
            "action": 3,
            "stability": 5
        }
    },

    "The Devil": {
        "upright": {
            "overall": "Attachment, temptation, restriction, and unhealthy patterns. This card suggests that something may be limiting your freedom.",
            "situation": "The situation may involve strong attachment, repeated habits, pressure, temptation, or dependence. Something may seem attractive or familiar, but it may also be reducing your freedom or control.",
            "challenge": "The main challenge is recognizing the pattern. The restriction may not come only from outside; it may also come from fear, dependence, avoidance, or a repeated choice that keeps you stuck.",
            "advice": "Identify what is limiting your freedom. Do not only focus on the surface problem; look at the habit or attachment behind it. Take practical steps to reduce dependence and regain control."
        },
        "reversed": {
            "overall": "Awareness, release, and breaking old patterns. It shows the beginning of freedom, but consistent action is still needed.",
            "situation": "You may be starting to recognize a limiting pattern and may already be trying to break away from it. The situation carries the possibility of release, but the process may still require discipline.",
            "challenge": "The main challenge is maintaining change after awareness appears. Recognizing the problem is only the first step; old habits may still pull you back if there is no practical plan.",
            "advice": "Continue removing unhealthy patterns step by step. Replace the old habit with a clearer structure, and avoid returning to what has already shown itself to be restrictive."
        },
        "scores": {
            "opportunity": 1,
            "challenge": 5,
            "emotion": 5,
            "action": 2,
            "stability": 1
        }
    },

    "The Tower": {
        "upright": {
            "overall": "Sudden change, disruption, collapse, and rebuilding. This card reveals unstable structures that can no longer stand.",
            "situation": "The situation may involve disruption, sudden change, or the breakdown of an old structure. What seemed stable may be exposed as fragile, and the change may arrive faster than expected.",
            "challenge": "The main challenge is dealing with instability without denial. The collapse may feel uncomfortable, but it may also reveal problems that were already present beneath the surface.",
            "advice": "Accept that some structures need to be rebuilt. Do not waste energy protecting what has already become unstable. Focus on understanding what failed, then rebuild from a more realistic foundation."
        },
        "reversed": {
            "overall": "Avoided change, delayed crisis, or internal pressure. It asks you to face the issue before the pressure increases.",
            "situation": "You may be avoiding a necessary change or sensing pressure building beneath the surface. The disruption may not have fully appeared yet, but the signs of instability are already present.",
            "challenge": "The main challenge is delay. Avoiding the problem may temporarily reduce fear, but it can also make the eventual disruption stronger or harder to manage.",
            "advice": "Face the issue earlier rather than waiting for pressure to increase. Make small repairs where possible, and be honest about what can no longer continue in its current form."
        },
        "scores": {
            "opportunity": 2,
            "challenge": 5,
            "emotion": 5,
            "action": 3,
            "stability": 1
        }
    },

    "The Star": {
        "upright": {
            "overall": "Hope, healing, inspiration, and long-term vision. This card suggests recovery and renewed confidence after difficulty.",
            "situation": "The situation may be entering a period of recovery, inspiration, or renewed hope. Even if progress is still slow, there may be a clearer long-term direction emerging.",
            "challenge": "The main challenge is keeping hope realistic. Inspiration is valuable, but it needs to be supported by consistent action, especially if the situation is still recovering from difficulty.",
            "advice": "Reconnect with long-term vision and allow recovery to happen gradually. Stay hopeful, but turn hope into small, practical steps that can rebuild confidence and direction."
        },
        "reversed": {
            "overall": "Discouragement, weakened hope, low motivation, or loss of faith. It asks you to rebuild hope through small practical steps.",
            "situation": "You may feel discouraged or disconnected from your long-term hope. The situation may still contain potential, but your confidence or motivation may be weakened.",
            "challenge": "The main challenge is loss of faith in the process. When progress is slow, it may be easy to assume that nothing is improving, even if recovery is still possible.",
            "advice": "Rebuild hope through small and realistic actions. Do not wait for full confidence before moving. A small step can help restore motivation and reconnect you with a larger direction."
        },
        "scores": {
            "opportunity": 5,
            "challenge": 2,
            "emotion": 4,
            "action": 3,
            "stability": 3
        }
    },

    "The Moon": {
        "upright": {
            "overall": "Uncertainty, illusion, fear, and hidden information. This card asks you to separate facts from emotions and assumptions.",
            "situation": "The situation may be unclear, emotionally confusing, or influenced by hidden information. What you see on the surface may not fully represent what is actually happening.",
            "challenge": "The main challenge is distinguishing facts from fear, imagination, or assumption. Emotional reactions may be strong, but they may not provide reliable evidence by themselves.",
            "advice": "Avoid making major decisions while the situation is unclear. Check facts carefully, observe repeated signals, and give the truth time to become more visible before acting."
        },
        "reversed": {
            "overall": "Emerging clarity, partial truth, or unresolved anxiety. It suggests that confusion is lifting, but careful checking is still needed.",
            "situation": "Some confusion may be starting to clear, but the situation is not fully transparent yet. You may have partial information, while emotional anxiety or uncertainty still remains.",
            "challenge": "The main challenge is acting too soon after only partial clarity. You may feel relief because some truth has appeared, but there may still be details that need verification.",
            "advice": "Continue checking the facts and avoid decisions based on fear. Use the emerging clarity carefully, but do not assume that every hidden factor has already been revealed."
        },
        "scores": {
            "opportunity": 2,
            "challenge": 5,
            "emotion": 5,
            "action": 2,
            "stability": 1
        }
    },

    "The Sun": {
        "upright": {
            "overall": "Clarity, success, confidence, and positive growth. This card suggests openness, progress, and visible results.",
            "situation": "The situation may be becoming clearer and more positive. There may be visible progress, stronger confidence, or a sense that things are moving in a healthy direction.",
            "challenge": "The main challenge is staying realistic while the situation feels positive. Confidence is useful, but overconfidence may cause you to ignore details that still require attention.",
            "advice": "Use this clear and positive energy to move forward. Be confident, but also practical. Make use of the current openness to build results that can last beyond the present moment."
        },
        "reversed": {
            "overall": "Delayed success, reduced confidence, or weakened clarity. Positive potential remains, but practical effort is needed.",
            "situation": "The situation may still contain positive potential, but the result may be delayed or less clear than expected. Confidence may be weakened even though progress is still possible.",
            "challenge": "The main challenge is temporary doubt, unrealistic expectation, or disappointment because success has not appeared in the expected form. Positive energy may be present but not fully expressed.",
            "advice": "Focus on practical progress rather than waiting for perfect confidence. Look for partial success, adjust expectations, and continue building toward clearer results."
        },
        "scores": {
            "opportunity": 5,
            "challenge": 1,
            "emotion": 4,
            "action": 4,
            "stability": 4
        }
    },

    "Judgement": {
        "upright": {
            "overall": "Awakening, reflection, evaluation, and important decisions. This card asks you to learn from the past and choose with clearer awareness.",
            "situation": "The situation may require reflection, evaluation, or an important decision. Past choices may now need to be reviewed so that a clearer direction can be chosen.",
            "challenge": "The main challenge is honesty. You may need to face feedback, consequences, or past patterns without avoiding responsibility. This process may be uncomfortable but useful.",
            "advice": "Review the past carefully and learn from it. Use reflection as a basis for better judgment. Make the next decision with clearer self-awareness instead of repeating old patterns automatically."
        },
        "reversed": {
            "overall": "Avoidance of judgment, fear of feedback, or blocked self-reflection. It asks you to face what needs to be reviewed.",
            "situation": "You may be avoiding evaluation, feedback, or self-reflection. The situation may feel blocked because something important has not yet been honestly reviewed.",
            "challenge": "The main challenge is fear of judgment or reluctance to face previous choices. Avoidance may temporarily reduce pressure, but it can also prevent necessary adjustment.",
            "advice": "Do not avoid review. Look at feedback and past choices as information rather than only as criticism. Adjustment becomes possible when you are willing to face what needs to be changed."
        },
        "scores": {
            "opportunity": 4,
            "challenge": 4,
            "emotion": 3,
            "action": 4,
            "stability": 3
        }
    },

    "The World": {
        "upright": {
            "overall": "Completion, achievement, integration, and wholeness. This card suggests reaching a milestone and preparing for the next cycle.",
            "situation": "The situation may be approaching completion or an important milestone. Different parts may be coming together, and the current stage may be ready to close in a more integrated way.",
            "challenge": "The main challenge is completing the cycle properly. Even when achievement is close, there may still be final details, closure, or integration that must be handled before moving forward.",
            "advice": "Recognize what has been completed and organize the final steps carefully. Prepare for the next cycle, but do not skip the process of closure, review, and integration."
        },
        "reversed": {
            "overall": "Incompletion, delay, lack of closure, or unfinished work. It asks you to complete what remains before moving on.",
            "situation": "Something may feel unfinished even though it is close to completion. The situation may involve delay, lack of closure, or difficulty bringing different parts together.",
            "challenge": "The main challenge is leaving things incomplete. Moving on too quickly may create repeated problems because the previous stage has not been fully integrated.",
            "advice": "Review what remains unfinished and complete the necessary final steps. Do not start a new cycle only to avoid closure. Finishing properly will create a more stable foundation for what comes next."
        },
        "scores": {
            "opportunity": 4,
            "challenge": 2,
            "emotion": 3,
            "action": 4,
            "stability": 5
        }
    }
}



DECK = list(CARD_DATABASE.keys())

OPPOSING_PAIRS = [
            (("The Tower", "The Star"),
             {"opportunity": 0.75, "challenge": 1.25, "emotion": 1.45, "action": 0.65, "stability": 0.45}),
            (("Death", "The Fool"),
             {"opportunity": 0.75, "challenge": 1.25, "emotion": 1.45, "action": 0.65, "stability": 0.45}),
            (("The Devil", "Strength"),
             {"opportunity": 0.80, "challenge": 1.20, "emotion": 1.35, "action": 0.70, "stability": 0.55}),
            (("The Moon", "The Sun"),
             {"opportunity": 0.80, "challenge": 1.20, "emotion": 1.35, "action": 0.70, "stability": 0.55}),
            (("The Magician", "The High Priestess"),
             {"opportunity": 0.85, "challenge": 1.15, "emotion": 1.25, "action": 0.75, "stability": 0.65}),
            (("The Emperor", "The Empress"),
             {"opportunity": 0.85, "challenge": 1.15, "emotion": 1.25, "action": 0.75, "stability": 0.65}),
            (("The Chariot", "The Hanged Man"),
             {"opportunity": 0.90, "challenge": 1.10, "emotion": 1.15, "action": 0.85, "stability": 0.75}),
            (("The Hierophant", "The Lovers"),
             {"opportunity": 0.90, "challenge": 1.10, "emotion": 1.15, "action": 0.85, "stability": 0.75})
        ]

ORIENTATION_WEIGHTS = {
    "upright": {"opportunity": 1.0, "challenge": 1.0, "emotion": 1.0, "action": 1.0, "stability": 1.0},
    "reversed": {"opportunity": 0.7, "challenge": 1.3, "emotion": 1.2, "action": 0.8, "stability": 0.8}
}

POSITION_WEIGHTS = {
    "overall": {"opportunity": 1.0, "challenge": 1.0, "emotion": 1.0, "action": 1.0, "stability": 1.0},
    "situation": {"opportunity": 1.0, "challenge": 1.0, "emotion": 1.0, "action": 0.8, "stability": 1.0},
    "challenge": {"opportunity": 0.7, "challenge": 1.5, "emotion": 1.2, "action": 0.8, "stability": 0.8},
    "advice": {"opportunity": 1.1, "challenge": 0.8, "emotion": 0.9, "action": 1.5, "stability": 1.0}
}

CATEGORY_WEIGHTS = {
    "career": {"opportunity": 1.3, "challenge": 1.2, "emotion": 0.8, "action": 1.3, "stability": 1.0},
    "love": {"opportunity": 1.0, "challenge": 1.0, "emotion": 1.5, "action": 0.9, "stability": 1.2},
    "study": {"opportunity": 1.1, "challenge": 1.2, "emotion": 0.9, "action": 1.4, "stability": 1.0},
    "general": {"opportunity": 1.0, "challenge": 1.0, "emotion": 1.0, "action": 1.0, "stability": 1.0}
}

CATEGORY_CONTEXT = {
    "career": "In a career context, this result relates to work direction, opportunity, pressure, and professional decision-making.",
    "love": "In a relationship context, this result relates to emotional interaction, communication, trust, and personal boundaries.",
    "study": "In a study context, this result relates to learning attitude, academic pressure, planning, and self-discipline.",
    "general": "In a general context, this result relates to personal reflection, decision-making, and current life direction."
}

THEME_EXPLANATIONS = {
    "opportunity": "The overall reading mainly points to potential, new openings, or possible development...",
    "challenge": "The overall reading mainly points to obstacles, pressure, or unresolved problems...",
    "emotion": "The overall reading mainly points to emotional state, relationship patterns, or inner reactions...",
    "action": "The overall reading mainly suggests that practical action, planning, or execution is important...",
    "stability": "The overall reading mainly points to long-term structure, consistency, or the need for stability..."
}

# ==================== 核心函数（完全保留你原来的逻辑） ====================

def draw_unique_cards(numbers, deck):
    selected_cards = []
    for number in numbers:
        card_index = (number - 1) // 2
        card_name = deck[card_index]
        orientation = "upright" if number % 2 == 0 else "reversed"
        selected_cards.append({"number": number, "card": card_name, "orientation": orientation})
    return selected_cards

def calculate_card_score(card_name, orientation, position, category):
    base_scores = CARD_DATABASE[card_name]["scores"]
    final_scores = {}
    for dimension in base_scores:
        final_scores[dimension] = round(
            base_scores[dimension]
            * ORIENTATION_WEIGHTS[orientation][dimension]
            * POSITION_WEIGHTS[position][dimension]
            * CATEGORY_WEIGHTS[category][dimension], 2
        )
    return final_scores

def calculate_total_scores(selected_cards, positions, category):
    total_scores = {"opportunity": 0, "challenge": 0, "emotion": 0, "action": 0, "stability": 0}
    card_scores = []
    card_names = [c["card"] for c in selected_cards]

    for index, card_info in enumerate(selected_cards):
        card_name = card_info["card"]
        orientation = card_info["orientation"]
        position = positions[index]
        card_score = calculate_card_score(card_name, orientation, position, category)
        card_scores.append(card_score)
    # 对立牌加成
    if len(card_scores) == 3:
        opposing_coeffs = None
        opposing_indices = []
        for pair, coeffs in OPPOSING_PAIRS:
            if pair[0] in card_names and pair[1] in card_names:
                opposing_coeffs = coeffs
                opposing_indices = [card_names.index(pair[0]), card_names.index(pair[1])]
                break
        if opposing_coeffs:
            for idx in opposing_indices:
                for dim in opposing_coeffs:
                    card_scores[idx][dim] *= opposing_coeffs[dim]
            neutral_idx = 3 - opposing_indices[0] - opposing_indices[1]
            for dim in card_scores[neutral_idx]:
                card_scores[neutral_idx][dim] *= 1.2

    for score in card_scores:
        for dimension in total_scores:
            total_scores[dimension] += score[dimension]

    MAX_THEORETICAL_SCORE = 20 if len(card_scores) == 3 else 7
    for dimension in total_scores:
        total_scores[dimension] = round(min(total_scores[dimension] / MAX_THEORETICAL_SCORE * 10, 10), 1)
    return total_scores

def find_main_theme(total_scores):
    return max(total_scores, key=total_scores.get)

def get_card_interpretation(card_name, orientation, position, category):
    card_text = CARD_DATABASE[card_name][orientation][position]
    category_text = CATEGORY_CONTEXT[category]
    return f"{card_text} {category_text}"

def generate_reading(selected_cards, positions, category, total_scores):
    main_theme = find_main_theme(total_scores)
    result = {
        "category": category,
        "cards": [],
        "scores": total_scores,
        "main_theme": main_theme,
        "summary": THEME_EXPLANATIONS[main_theme]
    }
    for index, card_info in enumerate(selected_cards):
        card_name = card_info["card"]
        orientation = card_info["orientation"]
        position = positions[index]
        image_filename = card_name.lower().replace(" ", "_") + ".png"
        result["cards"].append({
            "name": card_name,
            "orientation": orientation,
            "position": position,
            "interpretation": get_card_interpretation(card_name, orientation, position, category),
            "image": image_filename,
            "scores": CARD_DATABASE[card_name]["scores"]
        })
    return result

# ==================== Flask 路由 ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/draw', methods=['POST'])
def api_draw():
    data = request.json
    category = data.get('category', 'general')
    spread = data.get('spread', '3')
    numbers_str = data.get('numbers', '')

    positions = ["overall"] if spread == '1' else ["situation", "challenge", "advice"]
    required_count = len(positions)

    # 如果用户没输入数字，就随机生成
    if not numbers_str.strip():
        numbers = [random.randint(1, 44) for _ in range(required_count)]
    else:
        numbers = [int(x) for x in numbers_str.split() if x.strip().isdigit()][:required_count]

    # 保证不重复

    while len(set([(n - 1) // 2 for n in numbers])) < len(numbers):
        numbers = [random.randint(1, 44) for _ in range(required_count)]

    random.shuffle(DECK)
    selected_cards = draw_unique_cards(numbers, DECK)
    total_scores = calculate_total_scores(selected_cards, positions, category)
    result = generate_reading(selected_cards, positions, category, total_scores)

    return jsonify(result)



def get_card_image_filename(card_name):
    return card_name.lower().replace(" ", "_") + ".png"

@app.route('/meanings')
def meanings_page():
    return render_template('card_meanings.html')

@app.route('/api/cards', methods=['GET'])
def api_cards():
    cards = []
    for index, card_name in enumerate(DECK, start=1):
        cards.append({
            "id": index,
            "name": card_name,
            "image": get_card_image_filename(card_name),
            "upright": CARD_DATABASE[card_name]["upright"]["overall"],
            "reversed": CARD_DATABASE[card_name]["reversed"]["overall"]
        })
    return jsonify(cards)

@app.route('/api/cards/<int:card_id>', methods=['GET'])
def api_card_detail(card_id):
    if card_id < 1 or card_id > len(DECK):
        return jsonify({"error": "Card not found"}), 404

    card_name = DECK[card_id - 1]
    card_info = CARD_DATABASE[card_name]

    return jsonify({
        "id": card_id,
        "name": card_name,
        "image": get_card_image_filename(card_name),
        "upright": card_info["upright"]["overall"],
        "reversed": card_info["reversed"]["overall"]
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
