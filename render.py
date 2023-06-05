import argparse
import matplotlib.animation as animation
import matplotlib.pyplot as pyplot
import numpy as np
import re

from transforms3d.euler import euler2mat, mat2euler

# py render.py --bvhFile=./resources/zdvihnutie_p_ruky_chr01.bvh


class Joint:
    def __init__(self, name, parent, index):
        self.name = name
        self.parent = parent
        self.children = []
        self.offset = np.zeros(3)
        self.channels = []
        self.motion = [] # position of each frame
        self.index = index # index in array (from hierarchy structure position)


class Skeleton:
    def __init__(self):
        self.root = None
        self.joints = []
        self.bones = [] # joint indexes of bone
        self.frame_matrix = [] # numpy array of motion lines
        self.frame_time = 0
        self.frame_num = 0

    # parse lines from bvh file  
    def parse(self, lines):
        lines = [line.strip() for line in lines] # remove leadinf and trailing space
        li = lines.index("MOTION") # get first index of MOTION block
        # TODO when ValueError: 'MOTION' is not in list, expect live data
        self.parse_hierarchy(lines[:li])
        self.parse_motion(lines[li+1:])
        
    def parse_hierarchy(self, lines):
        joint_stack = []
        count = 0
        for line in lines:
            if line == '':
                continue
            words = re.split(r'\s+', line) # split by whitespace characters
            match words[0]:
                case "ROOT":
                    joint = Joint(words[1], None, count)
                    self.root = joint
                    self.joints.append(joint)
                    joint_stack.append(joint)
                    count += 1
                case "OFFSET":
                    for i in range(1, len(words)):
                        joint_stack[-1].offset[i-1] = float(words[i])
                case "CHANNELS":
                    for i in range(2, len(words)):
                        joint_stack[-1].channels.append(words[i])
                case "JOINT" | "End":
                    name = words[1] if words[0] == "JOINT" else "End" 
                    parent = joint_stack[-1]
                    joint = Joint(name, parent, count)
                    parent.children.append(joint) # add child to parent
                    self.joints.append(joint) # add joint to global skeleton joints
                    self.bones.append(list([parent.index, joint.index])) # define bone between parend and child joint
                    joint_stack.append(joint)
                    count += 1
                case "}":
                    joint_stack.pop()

    def parse_motion(self, lines):
        for line in lines:
            if line == '':
                continue
            words = re.split(r'\s+', line)
            if line.startswith("Frame Time"):
                self.frame_time = float(words[2])
            elif line.startswith("Frames"):
                self.frame_num = int(words[1])
            else: # get action matrix
                curr_frame = []
                for word in words:
                    curr_frame.append(float(word))
                self.frame_matrix.append(curr_frame)
        self.frame_matrix = np.array(self.frame_matrix) # turn into numpy array

    # calculate the position of each joint for each frame
    def get_all_positions(self):
        global motion_index
        for i in range(self.frame_num):
            motion_index = 0
            self.get_joint_positions(i, self.root, np.eye(3), np.zeros(3))
            # eye = 2-D array with ones on the diagonal and zeros elsewhere

    # recursively calculate position of given joint in given frame(index)
    def get_joint_positions(self, frame_index, joint, parent_matrix, parent_position):
        global motion_index
        # find value corresponding to given joint of given frame in frame_matrix
        offset = np.zeros(3)
        current_matrix = np.eye(3)
        for ch in joint.channels:
            match ch:
                case "Xrotation":
                    rotation = self.frame_matrix[frame_index, motion_index]
                    rotation = np.deg2rad(rotation)
                    euler_rotation = np.array([rotation, 0., 0.]) # floats
                    M = euler2mat(*euler_rotation) # rotation matrix from Euler angles and axis sequence
                    current_matrix = current_matrix.dot(M) # dot product of arrays
                case "Yrotation":
                    rotation = self.frame_matrix[frame_index, motion_index]
                    rotation = np.deg2rad(rotation)
                    euler_rotation = np.array([0., rotation, 0.])
                    M = euler2mat(*euler_rotation)
                    current_matrix = current_matrix.dot(M)
                case "Zrotation":
                    rotation = self.frame_matrix[frame_index, motion_index]
                    rotation = np.deg2rad(rotation)
                    euler_rotation = np.array([0., 0., rotation])
                    M = euler2mat(*euler_rotation)
                    current_matrix = current_matrix.dot(M)
                case "Xposition":
                    offset[0] = self.frame_matrix[frame_index, motion_index]
                case "Yposition":
                    offset[1] = self.frame_matrix[frame_index, motion_index]
                case "Zposition":
                    offset[2] = self.frame_matrix[frame_index, motion_index]
            motion_index += 1
        # based on parent node, calculate position of the current node
        new_position = parent_position + parent_matrix.dot(joint.offset) + offset
        new_matrix = parent_matrix.dot(current_matrix)
        joint.motion.append(new_position)
        # calculate position of the child node
        for c in joint.children:
            self.get_joint_positions(frame_index, c, new_matrix, new_position)
        return

# update animation
def update(num, lines, boneDatas):
    for line,data in zip(lines,boneDatas):
        line.set_data([data[:, num, 0], data[:, num, 2]]) # first dimension is 2: refers to the two vertices of each edge
        line.set_3d_properties(data[:, num, 1])
    return lines

parser = argparse.ArgumentParser()
parser.add_argument('--bvhFile', type=str, required=False, help='bvh file to render') # can set default

if __name__ == '__main__':
    file_path = parser.parse_args().bvhFile if parser.parse_args().bvhFile else "./basic_hierarchy.txt"
    with open(file_path, 'r') as file:
        lines = file.readlines() # read lines from file entered in script arguments
    
    skeleton = Skeleton()
    skeleton.parse(lines)
    skeleton.get_all_positions()

    bone_data = []
    for bone in skeleton.bones:
        joint_a = bone[0]
        joint_b = bone[1]
        position_a = skeleton.joints[joint_a].motion
        position_b = skeleton.joints[joint_b].motion
        bone_data.append([position_a, position_b])
    bone_data = np.array(bone_data)

    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-1, 199)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    pyplot.axis('off')

    # in bvh file, Y and Z axes are reversed, so exchange
    lines=[ax.plot([boneData[0,0,0],boneData[1,0,0]],[boneData[0,0,2],boneData[1,0,2]],[boneData[0,0,1],boneData[1,0,1]])[0] for boneData in bone_data]

    ani = animation.FuncAnimation(fig, update,
             skeleton.frame_num, interval=skeleton.frame_time, blit=True, fargs=(lines, bone_data))

    pyplot.show()

    # ani.save('motion.mp4')
