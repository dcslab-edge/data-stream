from pyspark import SparkContext
from pyspark.streaming import StreamingContext
sc = SparkContext(appName="SparkGPUDataReceivePython")
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines= ssc.socketTextStream("localhost",8888)
# Split each line into words
data_RDD = lines.flatMap(lambda line: line.encode("ascii", "ignore").split(" ")).map(lambda cell: cell.split(":"))
longs = data_RDD.filter(lambda x: x[0][:4]=="long")
longs_value = longs.map(lambda x: long(x[1]))
ints = data_RDD.filter(lambda x: x[0][:3]=="int")
ints_value = ints.map(lambda x: int(x[1]))

longs_value_filtered = longs_value.map(lambda x: 0 if x>10000 else 1)
ints_value_filtered = ints_value.map(lambda x: 0 if x >= 50 and x<80 else 1)

ints_reduce = ints_value_filtered.reduceByKey(lambda x,y: x+y)
longs_reduce = longs_value_filtered.reduceByKey(lambda x,y: x+y)

longs_reduce.pprint()
ints_reduce.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
