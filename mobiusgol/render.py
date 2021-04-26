import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mobiusgol.utils import add_pattern_from_macro, add_pattern_from_file
from mobiusgol.gol_step import update_grid2d
import numpy as np

render_method = {'Basic2png', 'BasicAnimation'}


class BaseRender:
    def __init__(self, config):
        global_config = config['global_param']
        self.canvas_size = global_config['canvas_size']
        self.render_method = global_config['render']
        self.timeline = config['timeline']
        self.timeline_keys = self.timeline.keys()

        self.gol_state = np.zeros(self.canvas_size)
        self.iteration = 0

        self.fig = plt.figure(figsize=(10, 10))
        self.im = plt.imshow(self.gol_state, animated=True,
                             vmax=1,
                             vmin=0,
                             interpolation='nearest',
                             cmap='gray',
                             origin='lower')

    def animate(self):
        self.ani = animation.FuncAnimation(self.fig,
                                           self.render_next,
                                           init_func=self.init_gol,
                                           interval=0, frames=1000, blit=False)
        plt.tight_layout()
        plt.show()

    def init_gol(self):
        return self.gol_state

    def render_next(self, _):
        if self.iteration in self.timeline.keys():
            for value in self.timeline[self.iteration]:
                if value['type'] == 'macro':
                    self.gol_state = add_pattern_from_macro(self.gol_state,
                                                            **value['kwargs'])

        self.gol_state = update_grid2d(self.gol_state)
        self.im.set_array(self.gol_state)
        self.iteration += 1
        return self.im






