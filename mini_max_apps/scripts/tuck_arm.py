#!/usr/bin/env python

"""
  Copyright (c) 2011 Vanadium Labs LLC.  
  All right reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
      * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
      * Neither the name of Vanadium Labs LLC nor the names of its 
        contributors may be used to endorse or promote products derived 
        from this software without specific prior written permission.
  
  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL VANADIUM LABS BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import roslib; roslib.load_manifest('mini_max_apps')
import rospy
import actionlib
import sys

from actionlib_msgs.msg import GoalStatus
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.msg import *

servos = ['arm_wrist_flex_joint', 'arm_shoulder_lift_joint', 'arm_shoulder_pan_joint', 'arm_elbow_flex_joint']
tucked = [1.5084144414208807, -0.71585770101329926, 1.4726215563702156, 1.9634954084936207]
utcked = [1.5135277107138327, 0.015339807878856412, 1.5288675185926892, 1.5544338650574498]

if __name__ == '__main__':
    rospy.init_node('tuck_arm')

    # a publisher for arm movement
    client = actionlib.SimpleActionClient('follow_joint_trajectory', FollowJointTrajectoryAction)
    client.wait_for_server()

    # prepare a joint trajectory
    msg = JointTrajectory()
    msg.joint_names = servos
    msg.points = list()
    
    # tucking or untucking?
    if len(sys.argv) > 1 and sys.argv[1] == "u":
        point = JointTrajectoryPoint()
        point.positions = utcked
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(3.0)
        msg.points.append(point)
    else:
        point = JointTrajectoryPoint()
        point.positions = utcked
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(5.0)
        msg.points.append(point)
        point = JointTrajectoryPoint()
        point.positions = tucked
        point.velocities = [ 0.0 for servo in msg.joint_names ]
        point.time_from_start = rospy.Duration(8.0)
        msg.points.append(point)
    
    # execute
    msg.header.stamp = rospy.Time.now()
    goal = FollowJointTrajectoryGoal()
    goal.trajectory = msg
    client.send_goal(goal)
    client.wait_for_result()

