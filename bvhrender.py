import argparse
import matplotlib.animation as animation
import matplotlib.pyplot as pyplot
import numpy as np
import re
import socket
from transforms3d.euler import euler2mat

# EXAMPLE HOW TO RUN SCRIPT
# py render.py --bvh=./resources/zdvihnutie_p_ruky_chr01.bvh

##JOINT#CLASS###################################################################
class Joint:
    def __init__(self, index, name, parent):
        self.index = index # BFS hierarchy structure position
        self.name = name
        self.parent = parent
        self.children = []
        self.offset = np.zeros(3)
        self.channels = []
        self.motion = [] # motion of each frame
##JOINT#CLASS###################################################################

##SKELETON#CLASS################################################################
class Skeleton:
    def __init__(self):
        self.root = None # root joint, first in hierarchy
        self.joints = [] # all joints including root joint
        self.bones = [] # pairs of adjacent joint indexes defining bone
        self.frame_matrix = [] # numpy array of motion frames
        self.frame_time = 0 # frame per milisecond
        self.frame_num = 0 # number of frames

    # parse lines from bvh file
    def parse(self, lines):
        lines = [line.strip() for line in lines] # remove leading/trailing spaces
        i = lines.index('MOTION') # get index of MOTION block
        self.parse_hierarchy(lines[:i])
        self.parse_motion(lines[i+1:])
        
    def parse_hierarchy(self, lines):
        joint_stack = []
        count = 0
        for line in lines:
            words = re.split(r'\s+', line) # split by whitespace characters
            match words[0]:
                case 'ROOT':
                    joint = Joint(count, words[1], None)
                    self.root = joint
                    self.joints.append(joint)
                    joint_stack.append(joint)
                    count += 1
                case 'OFFSET':
                    for i in range(1, len(words)): # save offsets for last joint
                        joint_stack[-1].offset[i-1] = float(words[i])
                case 'CHANNELS':
                    for i in range(2, len(words)): # save channels for last joint
                        joint_stack[-1].channels.append(words[i])
                case 'JOINT' | 'End':
                    parent = joint_stack[-1]
                    name = words[1] if words[0] == 'JOINT' else 'End' 
                    joint = Joint(count, name, parent)
                    self.joints.append(joint)
                    joint_stack.append(joint)
                    parent.children.append(joint)        
                    # define bone between parent and child joints           
                    self.bones.append(tuple((parent.index, joint.index)))
                    count += 1
                case '}':
                    joint_stack.pop()

    def parse_motion(self, lines):
        for line in lines:
            if line == '':
                continue
            words = re.split(r'\s+', line)
            if line.startswith('Frames'):
                self.frame_num = int(words[1])
            elif line.startswith('Frame Time'):
                self.frame_time = float(words[2])
            else: # get save motions to matrix rows
                frame = [float(word) for word in words]
                self.frame_matrix.append(frame)
        self.frame_matrix = np.array(self.frame_matrix)

    # calculate the position of each joint for each frame
    def get_all_positions(self, frame_num=None):
        global motion_index
        frame_num = frame_num or self.frame_num
        for i in range(frame_num):
            motion_index = 0
            self.get_joint_positions(i, self.root, np.eye(3), np.zeros(3))
            # eye = 2-D array with ones on the diagonal and zeros elsewhere

    # recursively calculate position of given joint in given frame(index)
    # resource: https://research.cs.wisc.edu/graphics/Courses/cs-838-1999/Jeff/BVH.html
    def get_joint_positions(self, frame_index, joint, parent_matrix, parent_position):
        global motion_index
        # find value corresponding to given joint of given frame in frame_matrix
        offset = np.zeros(3)
        matrix = np.eye(3)
        for ch in joint.channels:
            match ch:
                case 'Xrotation':
                    rotation = self.frame_matrix[frame_index, motion_index]
                    rotation = np.deg2rad(rotation)
                    euler_rotation = np.array([rotation, 0., 0.]) # floats
                    # rotation matrix from Euler angles and axis sequences
                    M = euler2mat(*euler_rotation)
                    matrix = matrix.dot(M) # dot product of arrays
                case 'Yrotation':
                    rotation = self.frame_matrix[frame_index, motion_index]
                    rotation = np.deg2rad(rotation)
                    euler_rotation = np.array([0., rotation, 0.])
                    M = euler2mat(*euler_rotation)
                    matrix = matrix.dot(M)
                case 'Zrotation':
                    rotation = self.frame_matrix[frame_index, motion_index]
                    rotation = np.deg2rad(rotation)
                    euler_rotation = np.array([0., 0., rotation])
                    M = euler2mat(*euler_rotation)
                    matrix = matrix.dot(M)
                case 'Xposition':
                    offset[0] = self.frame_matrix[frame_index, motion_index]
                case 'Yposition':
                    offset[1] = self.frame_matrix[frame_index, motion_index]
                case 'Zposition':
                    offset[2] = self.frame_matrix[frame_index, motion_index]
            motion_index += 1
        # based on parent node, calculate position of current node
        new_position = parent_position + parent_matrix.dot(joint.offset) + offset
        new_matrix = parent_matrix.dot(matrix)
        joint.motion.append(new_position)
        # calculate position of child nodes
        for c in joint.children:
            self.get_joint_positions(frame_index, c, new_matrix, new_position)

    def get_bone_data(self):
        bone_data = []
        for bone in self.bones:
            joint_a = bone[0]
            joint_b = bone[1]
            position_a = skeleton.joints[joint_a].motion
            position_b = skeleton.joints[joint_b].motion
            bone_data.append([position_a, position_b])
        bone_data = np.array(bone_data)
        return bone_data
##SKELETON#CLASS################################################################

##ANIMATION#FUNCTIONS###########################################################
# update animation from bvh file
def update(num, lines, bone_data):
    for line, data in zip(lines,bone_data):
        line.set_data([data[:, num, 0], data[:, num, 2]]) # first dimension = 2 - refers to the 2 vertices of each edge
        line.set_3d_properties(data[:, num, 1])
    return lines

# update animation from bvh broadcasting
def update_live_data(num):
    global ax        
    skeleton.frame_matrix = skeleton.frame_matrix + get_live_motion_frame()
    skeleton.get_all_positions(1)
    bone_data = skeleton.get_bone_data()
    # in bvh file, Y and Z axes are reversed, so exchange (XYZ)
    lines = [ax.plot([bone[0,0,0], bone[1,0,0]], 
                [bone[0,0,2],bone[1,0,2]],
                [bone[0,0,1],bone[1,0,1]])[0] for bone in bone_data]
    for line, data in zip(lines, bone_data):
        line.set_data([data[:, num, 0], data[:, num, 2]]) # first dimension is 2: refers to the two vertices of each edge
        line.set_3d_properties(data[:, num, 1])
    return lines

# parse motion frame from socket data
def get_live_motion_frame():
    global bvh_socket
    # remove metadata from motion frame
    motion_frame = bvh_socket.recv(3000).decode("utf-8")[15:-3]
    motion_frame = np.fromstring(motion_frame, dtype=float, sep=' ')
    without_meta = []
    n = 3 # slice frame to lists of 3 numbers 
    motion_frame = [motion_frame[i:i + n] for i in range(0, len(motion_frame), n)]
    # fisrt six numbers and then every second number trio are actual data
    for i, trio in enumerate(motion_frame):
        if i in (0,1) or i % 2:
            without_meta.extend(trio)
    return np.array([without_meta])
##ANIMATION#FUNCTIONS###########################################################

##GLOBAL########################################################################
UDP_IP = '127.0.0.1'
UDP_PORT_EDIT = 7001
UDP_PORT_CAPTURE = 7002

parser = argparse.ArgumentParser()
parser.add_argument('--bvh', type=str, required=False, help='path to bvh file to render', default='./basic_hierarchy.bvh')
##GLOBAL########################################################################

if __name__ == '__main__':
    # check and read bvh file
    file_path = parser.parse_args().bvh
    if (not file_path.endswith('.bvh')):
        raise ValueError('File extension must be \'.bvh\'.')
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # parse bvh file to Skeleton structure
    skeleton = Skeleton()
    skeleton.parse(lines)

    # animate
    fig = pyplot.figure()
    global ax
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-1, 199)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    pyplot.axis('off')

    if skeleton.frame_num > 1: # bvh file
        skeleton.get_all_positions()
        bone_data = skeleton.get_bone_data()
        # in bvh file, Y and Z axes are reversed, so exchange (XYZ)
        lines = [ax.plot([bone[0,0,0], bone[1,0,0]], 
                        [bone[0,0,2],bone[1,0,2]],
                        [bone[0,0,1],bone[1,0,1]])[0] for bone in bone_data]
        anim = animation.FuncAnimation(fig, update, skeleton.frame_num, 
                interval=skeleton.frame_time, blit=True, fargs=(lines, bone_data))
        pyplot.show()

    else: # real-time bvh data
        global bvh_socket
        bvh_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bvh_socket.bind((UDP_IP, UDP_PORT_EDIT))
        
        anim = animation.FuncAnimation(fig, update_live_data, frames=1,
                interval=skeleton.frame_time, blit=True)
        # anim.save('motion.mp4')
        pyplot.show()
