import sys
from utils.blend_packer import BlendPacker

'''
requirements:
+ pyyaml
'''

def main():
    bp = BlendPacker(
        root=sys.argv[1], 
        force='--force' in sys.argv or '--f', 
        tag_with_time='--with_tag' in sys.argv or '--wt' in sys.argv)
    res = bp.packup().upload()
    print(res)

if __name__ == '__main__':
    main()