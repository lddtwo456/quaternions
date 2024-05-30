from ObjectsHandler import ObjectsHandler


class Renderer:
  cam = None
  ctx = None

  def setCam(cam):
    Renderer.cam = cam

  def setContext(ctx):
    Renderer.ctx = ctx

  def renderScene(IMGbuf):
    # get transform matrices from local coords to projected points
    ObjectsHandler.getTransforms(Renderer.cam)

    for key in ObjectsHandler.objects.keys():
      obj = ObjectsHandler.objects[key]
      VBO = obj.VBO
      IBO = obj.IBO