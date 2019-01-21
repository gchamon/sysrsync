# sysrsync
Python module that wraps system calls to rsync

## Usage

* Basic file sync

```
import sysrsync

sysrsync.run(source='/home/user/foo.txt',
             destination='/home/server/bar')
# runs 'rsync /home/users/foo.txt /home/server/files'
```

* ssh with options

```
import sysrsync

sysrsync.run(source='/home/user/files',
             destination='/home/server/files',
             destination_ssh='myserver',
             options=['-a'])
# runs 'rsync -a /home/users/files/ myserver:/home/server/files'
```

* exclusions

```
import sysrsync

sysrsync.run(source='/home/user/files',
             destination='/home/server/files',
             destination_ssh='myserver',
             options=['-a'],
             exclusions=['file_to_exclude', 'unwanted_file'])
# runs 'rsync -a /home/users/files/ myserver:/home/server/files --exclude file_to_exclude --exclude unwanted_file'
```

## API

`sysrsync.run`

| argument  | type | default | description |
| --------- | ---- | ------- | ----------- |
| cwd  | str  | `os.getcwd()` | working directory in which subprocess will run the rsync command |
| strict  | bool | `True` | raises `RsyncError` when rsync return code is different than 0  |
| verbose | bool | `False` | verbose mode: currently prints rsync command before executing |
| **kwargs | dict | Not Applicable | arguments that will be forwarded to call to `sysrsync.get_rsync_command` |

`sysrsync.get_rsync_command`

| argument  | type | default | description |
| --------- | ---- | ------- | ----------- |



## 
