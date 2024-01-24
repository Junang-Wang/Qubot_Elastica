import matplotlib.pyplot as plt
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
    plt.savefig('Load_Angle.jpg')
    plt.show()
    plt.close()