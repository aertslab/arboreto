# error messages

```
distributed.worker - INFO - Can't find dependencies for key infer_data-e613bb78d805c6895285531ee785bb0f    
distributed.worker - INFO - Can't find dependencies for key infer_data-a174ef22d844b96c0b16398131fba613    
distributed.worker - INFO - Can't find dependencies for key infer_data-c8cc0618ceb72b2a7dea62009edc8f44
```

```
distributed.core - WARNING - Event loop was unresponsive for 1.24s.  This is often caused by long-running GIL-holding functions or moving large chunks of data. This can cause timeouts and instability.              
distributed.core - WARNING - Event loop was unresponsive for 1.49s.  This is often caused by long-running GIL-holding functions or moving large chunks of data. This can cause timeouts and instability.              
distributed.core - WARNING - Event loop was unresponsive for 1.17s.  This is often caused by long-running GIL-holding functions or moving large chunks of data. This can cause timeouts and instability.
```

```
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/concurrent.py", line 238, in result                                                                                    
    raise_exc_info(self._exc_info)                                                                         
  File "<string>", line 4, in raise_exc_info                                                               
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/gen.py", line 1063, in run                                                                                             
    yielded = self.gen.throw(*exc_info)                                                                    
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/distributed/core.py", line 504, in send_recv_from_rpc                                                                          
    comm = yield self.pool.connect(self.addr)                                                              
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/gen.py", line 1055, in run                                                                                             
    value = future.result()                                                                                
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/concurrent.py", line 238, in result                                                                                    
    raise_exc_info(self._exc_info)                                                                         
  File "<string>", line 4, in raise_exc_info                                                               
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/gen.py", line 1063, in run                                                                                             
    yielded = self.gen.throw(*exc_info)                                                                    
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/distributed/core.py", line 609, in connect                                                                                     
    connection_args=self.connection_args)                                                                  
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/gen.py", line 1055, in run                                                                                             
    value = future.result()                                                                                
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/concurrent.py", line 238, in result                                                                                    
    raise_exc_info(self._exc_info)                                                                         
  File "<string>", line 4, in raise_exc_info                                                               
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/tornado/gen.py", line 1063, in run                                                                                             
    yielded = self.gen.throw(*exc_info)                                                                    
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/distributed/comm/core.py", line 194, in connect                                                                                
    _raise(error)                                                                                          
  File "/data/leuven/software/biomed/Anaconda/5-Python-3.6/lib/python3.6/site-packages/distributed/comm/core.py", line 177, in _raise                                                                                 
    raise IOError(msg)                                                                                     
OSError: Timed out trying to connect to 'tcp://10.118.224.141:35656' after 3.0 s: in <distributed.comm.tcp.TCPConnector object at 0x2b8aa76581d0>: ConnectionRefusedError: [Errno 111] Connection refused 
```


Mapping a function of variable execution time over a large collection.

I have a large collection of entries E and a function f: E --> pd.DataFrame.
The execution time of function f can vary drastically for different inputs.
Finally all DataFrames are aggregated into a single DataFrame.

The situation I'd like to avoid is a partitioning (using 2 partitions for the 
sake of the example) where accidentally all fast function executions happen 
on partition 1 and all slow executions on partition 2, thus not optimally 
using the workers.

```
partition 1:
[==][==][==]

partition 2:
[============][=============][===============]
```

My current solution is to iterate over the collection of entries and create 
a graph using `delayed`, aggregating the delayed partial DataFrame results in
a final result DataFrame with `dd.from_delayed`.

```python
delayed_dfs = []  
    
for e in collection:
    delayed_partial_df = delayed(f)(arg1, arg2, ...)
    
    delayed_dfs.append(delayed_partial_df)

result_df = from_delayed(delayed_dfs, meta=make_meta({..}))
```

I reasoned that the Dask scheduler would take care of optimally assigning work
to the available workers. Is this a reasonable approach?
