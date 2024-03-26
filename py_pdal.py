#!.conda/bin/python
#used laszip to convert laz to las
json = """
[
    "crack.las",
    {
        "type": "filters.crop",
        "bounds":"([-10, 0],[11, 20])"
    },
    {
        "type":"writers.las",
        "filename":"file-cropped.las"
    }
]
"""

import pdal
pipeline = pdal.Pipeline(json)
count = pipeline.execute()
arrays = pipeline.arrays
metadata = pipeline.metadata
log = pipeline.log