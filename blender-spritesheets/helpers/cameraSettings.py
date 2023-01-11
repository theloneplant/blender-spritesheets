from math import sin, cos, radians

class CameraSettingsFactory():
    anim_suffix = ['_S', '_SW', '_W', '_NW', '_N', '_NE', '_E', '_SE']

    def __init__(self, height, radius, rx):
        self.height = height
        self.radius = radius
        self.rx = rx


    def getCameraSettingsList(self):
        return [self.getCameraSettings(angle_num, angle_num * 45.) for angle_num in range(8)]

    def getCameraSettings(self, num, rz):
        return CameraSettings(self.rx, 0, rz, self.radius * sin(radians(rz)), -self.radius * cos(radians(rz)), self.height, self.anim_suffix[num])


class CameraSettings():
    def __init__(self, rx, ry, rz, tx, ty, tz, suffix):
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.tx = tx
        self.ty = ty
        self.tz = tz

        self.suffix = suffix

    def setRenderSettings(self, scene):
        scene.camera.rotation_mode = 'XYZ'
        scene.camera.rotation_euler[0] = radians(self.rx)
        scene.camera.rotation_euler[1] = radians(self.ry)
        scene.camera.rotation_euler[2] = radians(self.rz)

        scene.camera.location.x = self.tx
        scene.camera.location.y = self.ty
        scene.camera.location.z = self.tz
