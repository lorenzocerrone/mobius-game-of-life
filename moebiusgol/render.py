import matplotlib.pyplot as plt
import matplotlib.animation as animation
from moebiusgol.utils import add_pattern_from_macro, add_pattern_from_file
from moebiusgol.gol_step import update_grid2d
import numpy as np
from PIL import Image
import os
from skimage.transform import rescale
import tqdm
import subprocess
import math

render_method = {'Basic2png', 'BasicAnimation'}


class BaseRender:
    def __init__(self, config):
        global_config = config['global_param']
        self.canvas_size = global_config['canvas_size']
        self.render_method = global_config['render']
        self.max_iterations = global_config['max_iterations']
        self.export_path = global_config['export_path']
        self.export_size = global_config['export_size']
        self.do_rescale = global_config['rescale']
        self.do_crop_center = global_config['crop_center']

        self.fps = global_config['fps']
        self.name = global_config['name']

        self.timeline = config['timeline']
        self.timeline_keys = self.timeline.keys()

        self.gol_state = np.zeros(self.canvas_size)
        self.iteration = 0
        self.fig, self.im, self.ani = None, None, None

    def step(self):
        if self.iteration in self.timeline.keys():
            for value in self.timeline[self.iteration]:
                if value['type'] == 'macro':
                    self.gol_state = add_pattern_from_macro(self.gol_state,
                                                            **value['kwargs'])
                elif value['type'] == 'file':
                    self.gol_state = add_pattern_from_file(self.gol_state,
                                                           **value['kwargs'])

        self.gol_state = update_grid2d(self.gol_state)
        self.iteration += 1

    def render_next(self, _):
        self.step()
        self.im.set_array(self.gol_state)
        return self.im

    def rescale(self, im):
        min_scale = min(self.export_size[0]/self.canvas_size[0], self.export_size[1]/self.canvas_size[1])
        im = rescale(im, scale=min_scale, order=0)
        diff_x, diff_y = self.export_size[0] - im.shape[0], self.export_size[1] - im.shape[1]
        im = np.pad(im, ((math.floor(diff_x/2), math.ceil(diff_x/2)),
                         (math.floor(diff_y/2), math.ceil(diff_y/2))))
        return im

    def crop(self, im):
        im = im[self.canvas_size[0]//2 - self.export_size[0]//2:self.canvas_size[0]//2 + self.export_size[0]//2,
                self.canvas_size[1]//2 - self.export_size[1]//2:self.canvas_size[1]//2 + self.export_size[1]//2]
        return im

    def save_png(self):
        export_frames_path = os.path.join(self.export_path, 'frames')
        os.makedirs(export_frames_path, exist_ok=True)
        for _ in tqdm.tqdm(range(self.max_iterations)):
            self.step()
            if self.do_rescale:
                im = self.rescale(self.gol_state)

            elif self.do_crop_center:
                im = self.crop(self.gol_state)

            else:
                raise NotImplemented

            im = im[::-1]

            im = Image.fromarray(255 * im)
            im = im.convert("L")
            file_name = os.path.join(export_frames_path, f"frame_{self.iteration:06d}.png")
            im.save(file_name)

        frame_naming_rule = os.path.join(export_frames_path, f"frame_%06d.png")
        out_movie = os.path.join(self.export_path, f"{self.name}.mp4")

        subprocess.run(['ffmpeg',
                        '-r', f'{self.fps}',
                        '-f', 'image2',
                        '-i', frame_naming_rule,
                        '-vcodec', 'libx264',
                        '-crf', '25',
                        '-pix_fmt', 'yuv420p',
                        '-y', out_movie])

    def animate(self):
        self.fig = plt.figure(figsize=(10, 10))
        self.im = plt.imshow(self.gol_state, animated=True,
                             vmax=1,
                             vmin=0,
                             interpolation='nearest',
                             cmap='gray',
                             origin='lower')

        self.ani = animation.FuncAnimation(self.fig,
                                           self.render_next,
                                           init_func=self.init_gol,
                                           interval=0, frames=10, blit=False)
        plt.tight_layout()
        plt.show()

    def init_gol(self):
        return self.gol_state





