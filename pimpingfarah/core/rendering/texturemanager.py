import tcod
import imageio as iio

class TextureManager:
    def __init__(self, sdlRenderer) -> None:
        self.imgDictionary = {}
        self.texDictionary = {}
        self.sdlRenderer = sdlRenderer

    def loadTexture(self, filename, texName) -> None:
        self.imgDictionary[texName]=iio.imread(filename,pilmode="RGB")
        h, w, c = self.imgDictionary[texName].shape
        assert c==3
        self.texDictionary[texName]=tcod.lib.SDL_CreateTexture(self.sdlRenderer, tcod.lib.SDL_PIXELFORMAT_RGB24, tcod.lib.SDL_TEXTUREACCESS_TARGET, w,h)
        tcod.lib.SDL_UpdateTexture(self.texDictionary[texName], tcod.ffi.NULL, tcod.ffi.cast("void*", self.imgDictionary[texName].ctypes.data), self.imgDictionary[texName].strides[0])

