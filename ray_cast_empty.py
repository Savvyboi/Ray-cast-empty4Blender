import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader
from mathutils import Vector

def update_empty(scene):
    camera = scene.camera

    camera_location = camera.matrix_world.to_translation()

    direction = camera.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
    ray_origin = camera_location
    ray_target = ray_origin + direction

    result, location, normal, index, object, matrix = scene.ray_cast(bpy.context.view_layer.depsgraph, ray_origin, direction)

    # If ray hits an object, update the empty's location
    if result:
        print("Ray hit object at location:", location)

        empty = bpy.data.objects.get("Empty")

        # If the empty doesn't exist, create it
        if empty is None:
            empty = bpy.data.objects.new("Empty", None)
            scene.collection.objects.link(empty)

        # Set the empty's location to the hit location
        empty.location = location
    else:
        print("Ray did not hit any object")

bpy.app.handlers.frame_change_post.append(update_empty)
