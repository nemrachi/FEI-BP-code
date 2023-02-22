# from mathutils import Vector, Matrix, Quaternion, Euler
import time
from .mocap_api import *
import math

mocap_app = None

mocap_timer = None

# {key:object_name, value:{key:bone_name, value:[(time_delta, location, rotation_quaternion, scale)]}}
record_data = None

def init_mocap_api():
    global mocap_app
    mocap_app = MCPApplication()
    mocap_app.enable_event_cache()
    render_settings = MCPRenderSettings()
    render_settings.set_up_vector(MCPUpVector.ZAxis, 1)
    render_settings.set_coord_system(MCPCoordSystem.RightHanded)
    render_settings.set_front_vector(MCPFrontVector.ParityEven, -1)
    render_settings.set_rotating_direction(MCPRotatingDirection.CounterClockwise)
    render_settings.set_unit(MCPUnit.Meter)
    mocap_app.set_render_settings(render_settings)

def uninit_mocap_api():
    global mocap_app
    if mocap_app.is_opened():
        mocap_app.close()
    mocap_app = None

def poll_data(ctx):
    mcp_evts = mocap_app.poll_next_event()
    for mcp_evt in mcp_evts:
        if mcp_evt.event_type == MCPEventType.AvatarUpdated:
            avatar = MCPAvatar(mcp_evt.event_data.avatar_handle)
            # animate_armatures(ctx, avatar)

def axisConnect():
    global mocap_timer
    settings = MCPSettings()
    
    settings.set_udp(7004)
    # settings.set_udp_server(ctx.scene.nml_ip, ctx.scene.nml_port)
    settings.set_bvh_data(MCPBvhData.Binary)
    
    mocap_app.set_settings(settings)
    if mocap_app.is_opened() :
        mocap_app.close()
    status, msg = mocap_app.open()
    if status:
        return ('Connect Successful CT')
    else:
        return ({'ERROR'}, 'Connect failed: {0}'.format(msg))

    # def modal(self, ctx, evt):
    #     if evt.type == 'TIMER':
    #         poll_data(ctx)
    #     if not ctx.scene.nml_living:
    #         return {'FINISHED'}
    #     return {'PASS_THROUGH'}

def axisDisconnect():
    global mocap_timer
    status, msg = mocap_app.close()
    if not status:
        return ({'ERROR'}, 'Disconnect failed: {0}'.format(msg))
    return ('Disconnect Successful CT')

def axisStartRecord():
    command = MCPCommand()

def axisStopRecord():
    command = MCPCommand()

if __name__ == '__main__':
    def print_joint(joint):
        print(joint.get_name())
        print(joint.get_local_rotation())
        print(joint.get_local_rotation_by_euler())
        print(joint.get_local_position())
        
        children = joint.get_children()
        for child in children:
            print_joint(child)

    app = MCPApplication()
    settings = MCPSettings()
    settings.set_udp(7004)
    app.set_settings(settings)
    app.open()
    while True:
        evts = app.poll_next_event()
        for evt in evts:
            if evt.event_type == MCPEventType.AvatarUpdated:
                avatar = MCPAvatar(evt.event_data.avatar_handle)
                print(avatar.get_index())
                print(avatar.get_name())
                print_joint(avatar.get_root_joint())
            elif evt.event_type == MCPEventType.RigidBodyUpdated:
                print('rigid body updated')
            else:
                print('unknow event')

        time.sleep(0.001)