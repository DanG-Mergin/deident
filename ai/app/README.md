contains all machine learning code which may be split off into a separate server


# launch.json which is actually working
{
   "version":"0.2.0",
   "configurations":[
      {
         "name":"Python: Remote Attach",
         "type":"python",
         "request":"attach",
         "connect":{
            "host":"localhost",
            "port":5678
         },
         "pathMappings":[
            {
               "localRoot":"${workspaceFolder}",
               "remoteRoot":"/code"
            }
         ]
      }
   ]
}