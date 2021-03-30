def scaling(u_c, l_c, scale):
    scale = max(min(scale, 100), 1) * 2
    x1, y1 = u_c.split()
    x2, y2 = l_c.split()
    return str(abs(float(x1) - float(x2))/scale) + ',' + str(abs(float(y1) - float(y2))/scale)