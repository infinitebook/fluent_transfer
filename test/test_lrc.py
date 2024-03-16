from openlrc.openlrc import LRCer
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

if __name__ == '__main__':
    lrcer = LRCer()

 # Single file
    lrcer.run("D:\CloudMusic\电台节目\阿坑是个坑 - 四六级长难句精听磨耳朵 19.mp3" , bilingual_sub= True
              )  # Generate translated ./data/test.lrc with default translate prompt.