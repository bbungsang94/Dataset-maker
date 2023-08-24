import os
from labeler.torchbase import Base


class SkinPatcher(Base):
    def __call__(self, output_path,
                 index, input_image, input_shape, skin, skin_shape) -> str:
        save_dict = {
            "index": index,
            "image": input_image,
            "input_shape": input_shape,
            "skin_shape": skin_shape,
            "skin": skin
        }
        save_path = os.path.join(output_path, "%06d.pth" % index)
        super(SkinPatcher, self).save(save_dict, save_path)
        desc = "index: %06d" % index
        return desc
