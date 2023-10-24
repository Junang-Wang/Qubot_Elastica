import matplotlib.pyplot as plt
from matplotlib.patches import Arrow
import matplotlib.animation as animation
import numpy as np
'''
this function plot 2D video, and end of the rod curve, the end of plot_params should be at the last order
'''
def plot_video_2D(normal:np.array, x_lim, y_lim, *plot_params:dict, video_name = "video.mp4", fps = 15, PLOT_VELOCITY = True, VELOCITY_SCALE = 0.1):
    position = []
    lines = []
    velocity = []
    for plot_param in plot_params:
        t = np.array(plot_param['time'])
        position.append(np.array(plot_param["position"]))
        velocity.append(VELOCITY_SCALE*np.array(plot_param["velocity"]))
    total_time = int(np.around(t[...,-1],1))
    total_frame = total_time * fps
    step = round(len(t)/ total_frame)
    zeros_index = np.where(normal==0)[0]

    print("Creating 2D video -- this can take a few minutes--------------------")
    FFMpegWriter = animation.writers["ffmpeg"]
    metadata = dict(title ="Movie Test", artist="Matplotlib", comment= "Movie support")
    writer = FFMpegWriter(fps=fps, metadata=metadata)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    # plt.axis("equal") # other options "tight", "scale", "auto"
    for i in range(len(position)):
        rod_lines_2d = ax.plot(
           position[i][0][zeros_index[0]], position[i][0][zeros_index[1]], linewidth = 3
        )[0]
        lines.append(rod_lines_2d)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    plt.xlabel('Position x (mm)')
    plt.ylabel('Position y (mm)')
    # -------bonus---------
    l = plt.plot([],[],"k--")[0] # end of rod curve
    l_x = []
    l_y = []

    # v = Arrow(position[-1][0][zeros_index[0]][-1], position[-1][0][zeros_index[1]][-1], position[-1][0][zeros_index[0]][-1]+ velocity[-1][0][zeros_index[0]][-1], position[-1][0][zeros_index[1]][-1]+velocity[-1][0][zeros_index[1]][-1])
    v = Arrow(position[-1][0][zeros_index[0]][-1], position[-1][0][zeros_index[1]][-1], velocity[-1][0][zeros_index[0]][-1], velocity[-1][0][zeros_index[1]][-1])

    a = ax.add_patch(v)
    plt.draw()
    
    
    with writer.saving(fig, video_name, dpi=100):
        with plt.style.context("seaborn-v0_8-whitegrid"):
            for time in range(1, len(t), step):
                for i in range(len(lines)):
                    # rod_lines_2d.set_xdata(position[time][zeros_index[0]])
                    # rod_lines_2d.set_ydata(position[time][zeros_index[1]])
                    lines[i].set_data(position[i][time][zeros_index[0]],position[i][time][zeros_index[1]])
                    
                    if i == len(lines)-1:
                        l_x.append(position[i][time][zeros_index[0]][-1]) # the x position of end of line i at time t
                        l_y.append(position[i][time][zeros_index[1]][-1])
                        l.set_data(l_x,l_y)
                        if PLOT_VELOCITY:
                            a.remove()
                            v = Arrow(position[i][time][zeros_index[0]][-1], position[i][time][zeros_index[1]][-1], velocity[i][time][zeros_index[0]][-1], velocity[i][time][zeros_index[1]][-1])
                            a = ax.add_patch(v)
                        

                writer.grab_frame()
    plt.close(fig)
