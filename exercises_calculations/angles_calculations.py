import math

def _angle_between(A, B, C):
    """
    Returns the angle at point B formed by the segments BA and BC, in degrees.
    A, B, C are (x, y) tuples.
    """
    # build vectors BA and BC
    BA = (A[0] - B[0], A[1] - B[1])
    BC = (C[0] - B[0], C[1] - B[1])
    # dot product and magnitudes
    dot = BA[0]*BC[0] + BA[1]*BC[1]
    mag_BA = math.hypot(*BA)
    mag_BC = math.hypot(*BC)
    # protect against rounding errors
    cos_angle = max(-1.0, min(1.0, dot / (mag_BA * mag_BC)))
    # return in degrees
    return math.degrees(math.acos(cos_angle))

def _angle_with_horizontal(P, Q):
    """
    Returns the angle (in degrees) between the line P→Q and the horizontal axis.
    Positive is counter‑clockwise from the +x direction.
    """
    dx = Q[0] - P[0]
    dy = Q[1] - P[1]
    return math.degrees(math.atan2(dy, dx))