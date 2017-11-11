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
