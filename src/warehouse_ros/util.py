# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Bhaskara Marthi

# Utilities

import roslib
import rospy
import pymongo as pm

def load_message_class(pkg, msg):
    """
    Given a ROS package and message name, returns the corresponding Python
    class object.
    """
    roslib.load_manifest(pkg)
    m = __import__(pkg+'.msg')
    mod = getattr(m, 'msg')
    return getattr(mod, msg)


def drop_database(db, db_host=None, db_port=None):
    """
    @param db: Name of database
    @param db_hosts: The host where the db server is listening.
    @param db_port: The port on which the db server is listening.

    Drops the db.
    The database host and port are set to the provided values if given.
    If not, the ROS parameters warehouse_host and warehouse_port are used,
    and these in turn default to localhost and 27017.
    """

    # Connect to mongo
    host = db_host or rospy.get_param('warehouse_host', 'localhost')
    port = db_port or rospy.get_param('warehouse_port', 27017)
    conn = None
    while not rospy.is_shutdown():
        try:
            conn = pm.Connection(host, port)
            break
        except:
            rospy.loginfo( "Attempting to connect to mongodb @ {0}:{1}".\
                    format(host, port))
            rospy.sleep(2.0)

    if conn:
        conn.drop_database(db)

