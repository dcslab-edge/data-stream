from pyspark import SparkContext
from pyspark.streaming import StreamingContext
sc = SparkContext(appName="SparkGPUDataReceivePython")
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
lines= ssc.socketTextStream("localhost",8888)
# Split each line into words
data_RDD = lines.flatMap(lambda line: line.encode("ascii", "ignore").split(" ")).map(lambda cell: cell.split(":"))
#data_RDD.pprint()
strings=data_RDD.filter(lambda x: x[0][:6]=="string")
strings_pair=strings.map(lambda x: ("string",x[1]))
#strings=data_RDD.filter(lambda dat: dat[0].startswith("s"))
longs = data_RDD.filter(lambda x: x[0][:4]=="long")
longs_pair=longs.map(lambda x: ("long",long(x[1])))
#longs = data_RDD.filter(lambda dat: dat[0].startswith("l"))
ints = data_RDD.filter(lambda x: x[0][:3]=="int")
ints_pair=ints.map(lambda x: ("int",int(x[1])))
#ints = data_RDD.filter(lambda dat: dat[0].startswith("i"))

strings_filtered = strings.filter(lambda x: 'X' not in x[1] and 'Y' not in x[1] and 'Z' not in x[1])
longs_filtered = longs.filter(lambda x: long(x[1])<880000)
ints_filtered = ints.filter(lambda x: int(x[1])>=50 and int(x[1])<=80)
strings_filtered.pprint()
longs_filtered.pprint()
ints_filtered.pprint()




strings_reduce = strings_pair.reduceByKey(lambda x,y: x if 'a' not in x+y else '')
ints_reduce = ints_pair.reduceByKey(lambda x,y: x*x + y*y + x*y + x*y)
longs_reduce = longs_pair.reduceByKey(lambda x,y: x-y if x>y else y-x)

#strings_result = strings_reduce.map(lambda x:("string_result", True if len(x.second)>20 else False))
#ints_result = ints_reduce.map(lambda x: ("int_result",True if x.second>200000 else False))


strings_reduce.pprint()
longs_reduce.pprint()
ints_reduce.pprint()
#strings_result.pprint()
#ints_result.pprint()

#strings.countByValue().pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
