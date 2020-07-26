## /api-submit

- **METHOD**: POST
- **Args**:
  - dataSet: the data set to submit, must be shaped like :
    - ["id" : ["1","2", "3", "4"], "feature1" : ["abc", "12fw", "nmd", "wtm", "haode1"]]
  - dropColumns: the columns to be dropped, must have the same length of the columns of data set like :
    - ["id", "feature1"]
  - discreteColumns: the columns with discrete elements value like:
    - ["feature1"]

