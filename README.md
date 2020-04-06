# Flask_Microservice
A simple flask based microservice app to fetch volume statistics. Runs by default on http://localhost:5000

Endpoint: `/getVolumeStat`

Input argument: vol=`<valid path of a volume>`

Example: `http://localhost:5000/getVolumeStat?vol=/home`

Sample output:
```
{
  "1_df_output_details": {
    "/home": {
      "available_size": "252G", 
      "filesystem": "/dev/sda4", 
      "total_size": "265G", 
      "used_percent": "1%", 
      "used_size": "290M"
    }
  }, 
  "2_inode": 2, 
  "3_time_details": {
    "access_time": "Sun Apr  5 13:44:50 2020", 
    "metadata_change_time": "Sun Aug 18 18:21:05 2019", 
    "modification_time": "Sun Aug 18 18:21:05 2019"
  }, 
  "4_size_details": {
    "available_size_in_mb": 257066.328125, 
    "total_size_in_mb": 271200.06640625
  }, 
  "5_raw_stat_output": {
    "st_atime": 1586074490.77016, 
    "st_atime_ns": 1586074490770159892, 
    "st_blksize": 4096, 
    "st_blocks": 8, 
    "st_ctime": 1566132665.564, 
    "st_ctime_ns": 1566132665564000000, 
    "st_dev": 2052, 
    "st_gid": 0, 
    "st_ino": 2, 
    "st_mode": 16877, 
    "st_mtime": 1566132665.564, 
    "st_mtime_ns": 1566132665564000000, 
    "st_nlink": 4, 
    "st_rdev": 0, 
    "st_size": 4096, 
    "st_uid": 0
  }, 
  "6_raw_statvfs_output": {
    "f_bavail": 65808980, 
    "f_bfree": 69353108, 
    "f_blocks": 69427217, 
    "f_bsize": 4096, 
    "f_favail": 17699637, 
    "f_ffree": 17699637, 
    "f_files": 17702912, 
    "f_flag": 4096, 
    "f_frsize": 4096, 
    "f_namemax": 255
  }
}
```
