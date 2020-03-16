from src.utils import TilemapFileParser
import numpy

def test_tilemap_file_parser():
    parser = TilemapFileParser("assets/maps/test.tm")
    expected = numpy.array(
        [[1,1,1,1,3,7,7,8,8,8],
         [1,1,3,3,2,3,7,7,8,8],
         [1,3,2,2,2,2,3,7,7,7],
         [1,3,2,2,2,2,2,3,3,7],
         [1,1,3,3,2,2,2,2,2,3],
         [4,1,1,1,3,2,2,2,3,3],
         [5,4,1,1,1,3,2,3,3,4],
         [6,5,4,1,1,3,3,3,4,7],
         [2,5,4,4,3,3,3,4,7,7],
         [6,5,7,7,4,4,4,7,7,7],]
    )
    assert numpy.array_equal(parser.parse(), expected) == True
    