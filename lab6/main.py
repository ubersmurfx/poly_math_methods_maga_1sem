import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def transition_model(bel, action):
    new_bel = np.zeros_like(bel)
    n = len(bel)

    for i in range(n):
        if action == 'forward':
            if i == n - 1:
                new_bel[i] += bel[i]
            elif i == n - 2:
                new_bel[i] += bel[i] * 0.25
                new_bel[i+1] += bel[i] * 0.75
            else:
                new_bel[i] += bel[i] * 0.25
                new_bel[i+1] += bel[i] * 0.5
                new_bel[i+2] += bel[i] * 0.25
        elif action == 'backward':
            if i == 0:
                new_bel[i] += bel[i]
            elif i == 1:
                new_bel[i] += bel[i] * 0.25
                new_bel[i-1] += bel[i] * 0.75
            else:
                new_bel[i] += bel[i] * 0.25
                new_bel[i-1] += bel[i] * 0.5
                new_bel[i-2] += bel[i] * 0.25
    return new_bel

bel = np.hstack((np.zeros(9), 1, np.zeros(10)))

actions = ['forward'] * 9 + ['backward'] * 3

belief_history = [bel]
for action in actions:
    bel = transition_model(bel, action)
    belief_history.append(bel)

fig, ax = plt.subplots()
lines, = ax.plot([], [], 'b-', lw=2)
ax.set_xlim(0, len(bel) - 1)
ax.set_ylim(0, 1)
ax.set_xlabel('Номер ячейки')
ax.set_ylabel('Вероятность')
ax.set_title('Дискретный Байесовский Фильтр (Анимация)')
ax.grid(True)

print(belief_history)

def animate(i):
    lines.set_data(np.arange(len(belief_history[i])), belief_history[i])
    action_label = actions[i - 1] if i > 0 else ["Старт"]
    action_string = ' '.join(map(str, action_label)) if i > 0 else "Старт"
    ax.set_title(f"Шаг {i+1}, {action_string}", fontsize=12)
    fig.canvas.draw() 
    return lines,

ani = animation.FuncAnimation(fig, animate, frames=len(belief_history), interval=500, blit=True)

plt.show()

print(f"Сумма вероятностей после всех действий: {np.sum(belief_history[-1]):.4f}")
