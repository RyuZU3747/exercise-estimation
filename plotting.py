def plot(plt, ax, results):
    face = [[] for _ in range(3)]
    lefteye = [[] for _ in range(3)]
    righteye = [[] for _ in range(3)]
    mouse = [[] for _ in range(3)]
    leftarm = [[] for _ in range(3)]
    rightarm = [[] for _ in range(3)]
    lefttmb = [[] for _ in range(3)]
    righttmb = [[] for _ in range(3)]
    leftleg = [[] for _ in range(3)]
    rightleg = [[] for _ in range(3)]
    body1 = [[] for _ in range(3)]
    body2 = [[] for _ in range(3)]
    
    for i, landmark in enumerate(results.pose_world_landmarks.landmark):
        if i in [0, 7, 8]:
            face[0].append(landmark.x)
            face[1].append(-landmark.y)
            face[2].append(landmark.z)
        if i in [1, 2, 3]:
            righteye[0].append(landmark.x)
            righteye[1].append(-landmark.y)
            righteye[2].append(landmark.z)
        if i in [4, 5, 6]:
            lefteye[0].append(landmark.x)
            lefteye[1].append(-landmark.y)
            lefteye[2].append(landmark.z)
        if i in [9, 10]:
            mouse[0].append(landmark.x)
            mouse[1].append(-landmark.y)
            mouse[2].append(landmark.z)
        if i in [11, 13, 15, 17, 19]:
            leftarm[0].append(landmark.x)
            leftarm[1].append(-landmark.y)
            leftarm[2].append(landmark.z)
        if i in [12, 14, 16, 18, 20]:
            rightarm[0].append(landmark.x)
            rightarm[1].append(-landmark.y)
            rightarm[2].append(landmark.z)
        if i in [15, 21]:
            lefttmb[0].append(landmark.x)
            lefttmb[1].append(-landmark.y)
            lefttmb[2].append(landmark.z)
        if i in [16, 22]:
            righttmb[0].append(landmark.x)
            righttmb[1].append(-landmark.y)
            righttmb[2].append(landmark.z)
        if i in [11, 23, 25, 27, 29, 31]:
            leftleg[0].append(landmark.x)
            leftleg[1].append(-landmark.y)
            leftleg[2].append(landmark.z)
        if i in [12, 24, 26, 28, 30, 32]:
            rightleg[0].append(landmark.x)
            rightleg[1].append(-landmark.y)
            rightleg[2].append(landmark.z)
        if i in [11, 12]:
            body1[0].append(landmark.x)
            body1[1].append(-landmark.y)
            body1[2].append(landmark.z)
        if i in [23, 24]:
            body2[0].append(landmark.x)
            body2[1].append(-landmark.y)
            body2[2].append(landmark.z)
    
    ax.set_xlim3d(-1, 1)
    ax.set_ylim3d(-1, 1)
    ax.set_zlim3d(-1, 1)
    
    ax.scatter(face[0], face[2], face[1])
    ax.plot(mouse[0], mouse[2], mouse[1])
    ax.plot(lefteye[0], lefteye[2], lefteye[1])
    ax.plot(righteye[0], righteye[2], righteye[1])
    ax.plot(leftarm[0], leftarm[2], leftarm[1])
    ax.plot(rightarm[0], rightarm[2], rightarm[1])
    ax.plot(lefttmb[0], lefttmb[2], lefttmb[1])
    ax.plot(righttmb[0], righttmb[2], righttmb[1])
    ax.plot(leftleg[0], leftleg[2], leftleg[1])
    ax.plot(rightleg[0], rightleg[2], rightleg[1])
    ax.plot(body1[0], body1[2], body1[1])
    ax.plot(body2[0], body2[2], body2[1])
    
    plt.draw()
    plt.pause(0.001)
    ax.clear()
    return