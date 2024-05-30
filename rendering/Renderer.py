from ObjectsHandler import ObjectsHandler


class Renderer:
  cam = None

  def setCam(cam):
    Renderer.cam = cam

  def renderScene(IMGbuf):
    ObjectsHandler.getTransforms(Renderer.cam)

    for key in ObjectsHandler.objects.keys():
      obj = ObjectsHandler.objects[key]
      VBO = obj.VBO
      IBO = obj.IBO



