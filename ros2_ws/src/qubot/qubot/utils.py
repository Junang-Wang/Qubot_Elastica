#! /home/qubot/.pyenv/shims/python3
import serial
import struct
import time
import threading
class PCB():
    def __init__(
            self,        
            port="/dev/ttyUSB0",
            baudrate = 115200):

        self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.magnetic_field_spherical = [0.,0.,0.]
        if not self.ser.is_open:
            self.ser.open()
        print(str(self.ser.is_open))

    def PCB_read(self, node_pub, msg):
        # count = 0
        # time0 = time.time()
        while True:
            if self.ser.in_waiting >0:
                value = self.ser.read(60)
                # time1 = time.time()
                # print('time:',time1-time0)
                if value[2] == 1:
                    # magnetic field
                    self.magnetic_field_spherical[0] = struct.unpack('f',value[8:12])[0]
                    self.magnetic_field_spherical[1] = struct.unpack('f',value[12:16])[0]/180 *np.pi
                    self.magnetic_field_spherical[2] = struct.unpack('f',value[16:20])[0]/180*np.pi
                    msg.magnetic_field_spherical = self.magnetic_field_spherical
                    node_pub.publish(msg)
            
                # count += 1
                # print(count)
                # print(self.magnetic_amp,self.magnetic_theta,self.magnetic_phi)

#----------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
def plotFigure(forces, analyticalBendingAngle, bendingAngle):
    fig = plt.figure(figsize=(5,4))
    ax = fig.add_subplot(111)
    ax.plot(
        forces*1e-6,
        bendingAngle[0],
        'ro',
        label = 'soft rod'
    )
    ax.plot(
        forces*1e-6,
        analyticalBendingAngle[0],
        'k-',
        label = 'analytical soft rod'
    )
    ax.plot(
        forces*1e-6,
        bendingAngle[1],
        'bo',
        label = 'stiff rod',
    )
    ax.plot(
        forces*1e-6,
        analyticalBendingAngle[1],
        'k--',
        label = 'analytical stiff rod'
    )
    ax.legend(prop={'size':12},loc='lower right')
    ax.set_ylabel('Bending Angle', fontsize=12)
    ax.set_xlabel('End Force(N)', fontsize=12)
    ax.set_title('Load and Angles')
    plt.ticklabel_format(style='sci',axis='x',scilimits=(-1,2))
    plt.savefig('./SOFA_playground/Figures/Load_Angle.jpg')
    plt.show()
    plt.close()

def plotMagneticFigure(magnetic_field_amplitudes,
                        magnet_magnetization, 
                        youngModulus, 
                        r_size, 
                        tangentAngles, 
                        length_diameter_ratio, 
                        small_scope_size,
                        delta_div_L,
                        poissonRatio=0.5):
    fig = plt.figure(figsize=(8,14))
    ax = fig.add_subplot(211)
    plt.title("Deformation Angles Under Uniform Magnetic Field")
    plt.xlabel("MB/G")
    plt.ylabel("Tangent Angles(deg)")
    shearModulus = youngModulus/(2*(1+poissonRatio))
    x = magnetic_field_amplitudes*magnet_magnetization/(shearModulus)
    for i in range(r_size):
        ax.plot(
            x,tangentAngles[i],
            'o-',
            label = f"L/D = {length_diameter_ratio[i]:.0f}"
        )
    ax.set_ylim(0,90)
    ax.set_xlim(0,25e-3)
    ax.ticklabel_format(style="sci",scilimits=(-3,-3),axis="x")
    ax.legend(prop ={"size":18}, loc = "lower right")

    ax2 = fig.add_subplot(212)
    plt.title("Deflection Under Uniform Magnetic Field")
    plt.xlabel("MB/G")
    plt.ylabel("$\delta$ / L")
    for i in range(r_size):
        ax2.plot(
            x[:small_scope_size], delta_div_L[i,:small_scope_size],
            'o',
            label = f"L/D = {length_diameter_ratio[i]:.0f}",
        )
        ax2.plot(
            x[:small_scope_size], 16/9*x[:small_scope_size]*length_diameter_ratio[i]**2
        )
    ax2.set_xlim(0,3e-4)
    ax2.ticklabel_format(style="sci",scilimits=(-3,-3),axis="x")
    ax2.ticklabel_format(style="sci",scilimits=(-2,-2),axis="y")
    ax2.legend(prop ={"size":18}, loc = "upper left")
    plt.savefig('./SOFA_playground/Figures/Magnetization_Angle.jpg')
    plt.show()
    plt.close()


def plotMagneticFigurePKU(magnetic_field_amplitudes,
                        magnet_magnetization, 
                        youngModulus, 
                        p_size, 
                        bendingAngles, 
                        experimentBendingAngles,
                        pAngles,
                        small_scope_size,
                        delta_div_L,
                        poissonRatio=0.5):
    fig = plt.figure(figsize=(10,14))
    ax = fig.add_subplot(111)
    plt.title("Deformation Angles Under Uniform Magnetic Field")
    plt.xlabel("MB/G")
    plt.ylabel("Bending Angles(deg)")
    shearModulus = youngModulus/(2*(1+poissonRatio))
    x = magnetic_field_amplitudes*magnet_magnetization/(shearModulus)
    color = ['r','b','g','c','m','y']
    for i in range(p_size):
        ax.plot(
            x[i],bendingAngles[i],
            color[i]+'-',
            label = f" $\\theta$ = {pAngles[i]/np.pi*180:.0f}"
        )
        ax.plot(
            x[i], experimentBendingAngles[i],
            color[i]+'o'           
        )
    ax.set_ylim(0,120)
    ax.set_xlim(0,3e-3)
    ax.ticklabel_format(style="sci",scilimits=(-3,-3),axis="x")
    ax.legend(prop ={"size":18}, loc = "lower right")

    # ax2 = fig.add_subplot(212)
    # plt.title("Deflection Under Uniform Magnetic Field")
    # plt.xlabel("MB/G")
    # plt.ylabel("$\delta$ / L")
    # for i in range(r_size):
    #     ax2.plot(
    #         x[:small_scope_size], delta_div_L[i,:small_scope_size],
    #         'o',
    #         label = f"L/D = {length_diameter_ratio[i]:.0f}",
    #     )
    #     ax2.plot(
    #         x[:small_scope_size], 16/9*x[:small_scope_size]*length_diameter_ratio[i]**2
    #     )
    # ax2.set_xlim(0,3e-4)
    # ax2.ticklabel_format(style="sci",scilimits=(-3,-3),axis="x")
    # ax2.ticklabel_format(style="sci",scilimits=(-2,-2),axis="y")
    # ax2.legend(prop ={"size":18}, loc = "upper left")
    plt.savefig('./SOFA_playground/Figures/MagnetizationPKU_Angle.jpg')
    plt.show()
    plt.close()