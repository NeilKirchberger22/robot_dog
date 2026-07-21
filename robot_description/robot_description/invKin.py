import numpy as np
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import numpy as np

#angles from cartesian points
leg_chain = Chain(
    name= 'dog_leg',
    links = [
        OriginLink(),
        URDFLink(
            name= 'hip_joint',
            origin_translation =[0, 0, 0],
            origin_orientation = [0,0,0],
            bounds = [-np.pi/5, np.pi/5],
            rotation=[0, 1, 0]
        ),
        URDFLink(
            name= 'shoulder_joint',
            origin_translation=[2.5, 1.5, 0],
            origin_orientation = [0,0,0],
            rotation=[1,0 , 0]
        ),
        URDFLink(
            name= 'elbow_joint',
            origin_translation=[0, 0, -16],
            origin_orientation = [0,0,0],
            rotation=[1, 0, 0]
        ),
        URDFLink(
            name= 'foot',
            origin_translation=[0, 17.25, -1],
            origin_orientation = [0,0,0],
            rotation= None,
            joint_type="fixed"
        ),
    ],
    active_links_mask=[False, True, True, True, False]
)


