
import sys

def init():
    sys.path.append("mobius_score/")
    sys.path.append("mobius_score/Mask_RCNN/")
    from mobius_score.main import setupOnce, parseArgs
    return setupOnce('models/mask_rcnn_notes_0122_512_v2.h5')

def scoreMp3(fn='zitah', model=None):
    from mobius_score.main import main
    main('songs/' + fn + '.mp3',
        'models/mask_rcnn_notes_0122_512_v2.h5',
        64,
        'midis/' + fn + '.midi',
        'sheets/' + fn + '.xml',
        model)

if __name__=='__main__':
    init()
    parseArgs()