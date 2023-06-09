from mocap_api import *

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

def poll_data():
    mcp_evts = mocap_app.poll_next_event()
    for mcp_evt in mcp_evts:
        if mcp_evt.event_type == MCPEventType.AvatarUpdated:
            avatar = MCPAvatar(mcp_evt.event_data.avatar_handle)
            # print_joint(avatar.get_root_joint())
            # animate_armatures(ctx, avatar)

def axisConnect():
    # global mocap_timer
    settings = MCPSettings()
    mocap_app.set_settings(settings)
    # settings.set_tcp('127.0.0.1', 7001)
    settings.set_udp_server('255.255.255.255', 8903)
    # settings.set_bvh_data(MCPBvhData.Binary)
    if mocap_app.is_opened() :
        mocap_app.close()
    status, msg = mocap_app.open()
    print(status)
    if status:
        print ('Connect Successful CT')
    else:
        print ({'ERROR'}, 'Connect failed: {0}'.format(msg))

def axisDisconnect():
    status, msg = mocap_app.close()
    if not status:
        print ({'ERROR'}, 'Disconnect failed: {0}'.format(msg))
    print ('Disconnect Successful CT')

def axisStartRecord():
    err = MCPCommand(MCPCommands.CommandStartRecored)
    
def axisStopRecord():
    command = MCPCommand(MCPCommands.CommandStopRecored)

def startCapture():
    print("stopping capture")
    command = MCPCommand(MCPCommands.CommandStartCapture)

def stopCapture():
    print("stopping capture")
    command = MCPCommand(MCPCommands.CommandStopCapture)

if __name__ == '__main__':
    init_mocap_api()
    axisConnect()
    startCapture()
    poll_data()
    axisDisconnect()